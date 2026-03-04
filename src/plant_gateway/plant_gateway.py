#!/usr/bin/env python3
"""
AS1 Clone - Plant Gateway Service
Connects to PLCs via Modbus TCP / OPC UA and collects sensor data
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# PLC Communication
try:
    from pymodbus.client import ModbusTcpClient
    from pymodbus.exceptions import ModbusException
    MODBUS_AVAILABLE = True
except ImportError:
    MODBUS_AVAILABLE = False
    print("pymodbus not installed: pip install pymodbus")

try:
    from opcua import Client, ua
    OPCUA_AVAILABLE = True
except ImportError:
    OPCUA_AVAILABLE = False
    print("opcua not installed: pip install opcua")

# Database
try:
    from influxdb import InfluxDBClient
    from influxdb.client import InfluxDBClient as InfluxClient
    INFLUX_AVAILABLE = True
except ImportError:
    INFLUX_AVAILABLE = False

import time
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlantStatus(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    ALARM = "alarm"
    MAINTENANCE = "maintenance"


@dataclass
class SensorReading:
    plant_id: str
    sensor_name: str
    value: float
    unit: str
    timestamp: datetime
    sensor_type: str  # temperature, level, weight, pressure, status


@dataclass
class BatchRecord:
    batch_id: str
    plant_id: str
    recipe_id: str
    start_time: datetime
    end_time: Optional[datetime]
    target_quantity_kg: float
    actual_quantity_kg: float
    components: List[Dict]
    temperatures: Dict
    quality_passed: bool
    status: str  # in_progress, completed, aborted


class ModbusPLC:
    """Connect to PLC via Modbus TCP"""
    
    def __init__(self, host: str, port: int = 502, unit_id: int = 1):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.client: Optional[ModbusTcpClient] = None
        self.connected = False
        
    def connect(self) -> bool:
        """Establish connection to PLC"""
        try:
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=5
            )
            self.connected = self.client.connect()
            logger.info(f"Modbus connected to {self.host}:{self.port}")
            return self.connected
        except Exception as e:
            logger.error(f"Modbus connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.client:
            self.client.close()
            self.connected = False
    
    def read_holding_registers(self, start: int, count: int) -> Optional[List[int]]:
        """Read holding registers (function code 0x03)"""
        if not self.connected:
            return None
        try:
            result = self.client.read_holding_registers(
                start, count, slave=self.unit_id
            )
            if not result.isError():
                return result.registers
            return None
        except ModbusException as e:
            logger.error(f"Modbus read error: {e}")
            return None
    
    def read_input_registers(self, start: int, count: int) -> Optional[List[int]]:
        """Read input registers (function code 0x04)"""
        if not self.connected:
            return None
        try:
            result = self.client.read_input_registers(
                start, count, slave=self.unit_id
            )
            if not result.isError():
                return result.registers
            return None
        except ModbusException as e:
            logger.error(f"Modbus read error: {e}")
            return None
    
    def write_register(self, address: int, value: int) -> bool:
        """Write single register (function code 0x06)"""
        if not self.connected:
            return False
        try:
            result = self.client.write_register(
                address, value, slave=self.unit_id
            )
            return not result.isError()
        except ModbusException as e:
            logger.error(f"Modbus write error: {e}")
            return False


class OPCUAClient:
    """Connect to PLC via OPC UA"""
    
    def __init__(self, url: str):
        self.url = url
        self.client: Optional[Client] = None
        self.connected = False
        self.nodes = {}
        
    def connect(self) -> bool:
        """Establish connection to OPC UA server"""
        try:
            self.client = Client(self.url)
            self.client.connect()
            self.connected = True
            logger.info(f"OPC UA connected to {self.url}")
            return True
        except Exception as e:
            logger.error(f"OPC UA connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close connection"""
        if self.client:
            self.client.disconnect()
            self.connected = False
    
    def get_node(self, node_id: str):
        """Get node by ID"""
        try:
            return self.client.get_node(node_id)
        except Exception as e:
            logger.error(f"OPC UA get_node error: {e}")
            return None
    
    def read_value(self, node_id: str) -> Optional[float]:
        """Read value from node"""
        try:
            node = self.get_node(node_id)
            if node:
                return node.get_value()
            return None
        except Exception as e:
            logger.error(f"OPC UA read error: {e}")
            return None
    
    def write_value(self, node_id: str, value) -> bool:
        """Write value to node"""
        try:
            node = self.get_node(node_id)
            if node:
                node.set_value(ua.Variant(value, ua.VariantType.Double))
                return True
            return False
        except Exception as e:
            logger.error(f"OPC UA write error: {e}")
            return False


# Register mapping for typical asphalt plant (Modbus TCP)
# Based on common PLC addressing conventions
REGISTER_MAP = {
    # Temperatures (40001-40099)
    "dryer_outlet_temp": {"address": 0, "type": "temp", "scale": 0.1, "unit": "°C"},
    "burner_temp": {"address": 1, "type": "temp", "scale": 0.1, "unit": "°C"},
    "mixer_temp": {"address": 2, "type": "temp", "scale": 0.1, "unit": "°C"},
    "bitumen_temp": {"address": 3, "type": "temp", "scale": 0.1, "unit": "°C"},
    "aggregate_temp": {"address": 4, "type": "temp", "scale": 0.1, "unit": "°C"},
    
    # Levels (40101-40199)
    "cold_feed_bin_1": {"address": 100, "type": "level", "scale": 0.1, "unit": "%"},
    "cold_feed_bin_2": {"address": 101, "type": "level", "scale": 0.1, "unit": "%"},
    "cold_feed_bin_3": {"address": 102, "type": "level", "scale": 0.1, "unit": "%"},
    "cold_feed_bin_4": {"address": 103, "type": "level", "scale": 0.1, "unit": "%"},
    "bitumen_tank_level": {"address": 104, "type": "level", "scale": 0.1, "unit": "%"},
    "filler_silo_level": {"address": 105, "type": "level", "scale": 0.1, "unit": "%"},
    
    # Weights (40201-40299)
    "total_aggregate_weight": {"address": 200, "type": "weight", "scale": 0.01, "unit": "tons"},
    "bitumen_weight": {"address": 201, "type": "weight", "scale": 0.01, "unit": "tons"},
    "filler_weight": {"address": 202, "type": "weight", "scale": 0.01, "unit": "tons"},
    "total_mix_weight": {"address": 203, "type": "weight", "scale": 0.01, "unit": "tons"},
    
    # Production data (40301-40399)
    "current_batch_number": {"address": 300, "type": "counter", "scale": 1, "unit": ""},
    "active_recipe_id": {"address": 301, "type": "counter",1, "unit": ""},
    "production_rate": {"address": 302, "type": "rate", "scale":  "scale": 0.1, "unit": "t/h"},
    "energy_consumption": {"address": 303, "type": "energy", "scale": 1, "unit": "kWh"},
    
    # Status (40501-40599)
    "plant_status": {"address": 500, "type": "status", "scale": 1, "unit": ""},
    "burner_status": {"address": 501, "type": "status", "scale": 1, "unit": ""},
    "mixer_status": {"address": 502, "type": "status", "scale": 1, "unit": ""},
    "alarm_word_1": {"address": 503, "type": "alarm", "scale": 1, "unit": ""},
    "alarm_word_2": {"address": 504, "type": "alarm", "scale": 1, "unit": ""},
}


class PlantGateway:
    """Main plant gateway service"""
    
    def __init__(self, plant_id: str, config: Dict):
        self.plant_id = plant_id
        self.config = config
        self.plc: Optional[ModbusPLC] = None
        self.opcua: Optional[OPCUAClient] = None
        self.influx_client = None
        self.running = False
        self.poll_interval = config.get("poll_interval_ms", 1000) / 1000.0
        
    def initialize(self):
        """Initialize connections"""
        # Setup Modbus
        if self.config.get("modbus"):
            self.plc = ModbusPLC(
                host=self.config["modbus"]["host"],
                port=self.config["modbus"].get("port", 502),
                unit_id=self.config["modbus"].get("unit_id", 1)
            )
            self.plc.connect()
        
        # Setup OPC UA
        if self.config.get("opcua"):
            self.opcua = OPCUAClient(self.config["opcua"]["url"])
            self.opcua.connect()
        
        # Setup InfluxDB
        if INFLUX_AVAILABLE and self.config.get("influxdb"):
            try:
                self.influx_client = InfluxDBClient(
                    host=self.config["influxdb"]["host"],
                    port=self.config["influxdb"].get("port", 8086),
                    database=self.config["influxdb"].get("database", "as1_clone")
                )
                # Create database if not exists
                self.influx_client.create_database("as1_clone")
                logger.info("InfluxDB connected")
            except Exception as e:
                logger.error(f"InfluxDB connection failed: {e}")
    
    def read_all_sensors(self) -> Dict[str, SensorReading]:
        """Read all configured sensors"""
        readings = {}
        timestamp = datetime.utcnow()
        
        # Read from Modbus
        if self.plc and self.plc.connected:
            for sensor_name, config in REGISTER_MAP.items():
                if config["type"] in ["temp", "level", "weight", "rate", "status", "alarm"]:
                    try:
                        registers = self.plc.read_input_registers(
                            config["address"], 1
                        )
                        if registers:
                            raw_value = registers[0]
                            scaled_value = raw_value * config["scale"]
                            readings[sensor_name] = SensorReading(
                                plant_id=self.plant_id,
                                sensor_name=sensor_name,
                                value=scaled_value,
                                unit=config["unit"],
                                timestamp=timestamp,
                                sensor_type=config["type"]
                            )
                    except Exception as e:
                        logger.error(f"Error reading {sensor_name}: {e}")
        
        # Read from OPC UA
        if self.opcua and self.opcua.connected:
            for node_id, mapping in self.config.get("opcua_nodes", {}).items():
                try:
                    value = self.opcua.read_value(node_id)
                    if value is not None:
                        sensor_name = mapping["name"]
                        readings[sensor_name] = SensorReading(
                            plant_id=self.plant_id,
                            sensor_name=sensor_name,
                            value=value * mapping.get("scale", 1),
                            unit=mapping.get("unit", ""),
                            timestamp=timestamp,
                            sensor_type=mapping.get("type", "unknown")
                        )
                except Exception as e:
                    logger.error(f"Error reading OPC UA {node_id}: {e}")
        
        return readings
    
    def write_to_influx(self, readings: Dict[str, SensorReading]):
        """Write readings to InfluxDB"""
        if not self.influx_client:
            return
        
        points = []
        for sensor_name, reading in readings.items():
            points.append({
                "measurement": "sensor_readings",
                "tags": {
                    "plant_id": reading.plant_id,
                    "sensor_name": reading.sensor_name,
                    "sensor_type": reading.sensor_type
                },
                "fields": {
                    "value": reading.value
                },
                "time": reading.timestamp.isoformat()
            })
        
        try:
            self.influx_client.write_points(points)
        except Exception as e:
            logger.error(f"InfluxDB write error: {e}")
    
    def get_plant_status(self) -> Dict:
        """Get current plant status"""
        readings = self.read_all_sensors()
        
        status = {
            "plant_id": self.plant_id,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "unknown",
            "temperatures": {},
            "levels": {},
            "production": {},
            "alarms": []
        }
        
        for name, reading in readings.items():
            if reading.sensor_type == "temp":
                status["temperatures"][name] = reading.value
            elif reading.sensor_type == "level":
                status["levels"][name] = reading.value
            elif reading.sensor_type == "status":
                if name == "plant_status":
                    status["status"] = ["stopped", "running", "alarm", "maintenance"][int(reading.value)] if reading.value < 4 else "unknown"
                elif name == "burner_status":
                    status["production"]["burner"] = ["off", "ignition", "running"][int(reading.value)] if reading.value < 3 else "unknown"
                elif name == "mixer_status":
                    status["production"]["mixer"] = ["stopped", "loading", "mixing", "discharging"][int(reading.value)] if reading.value < 4 else "unknown"
            elif reading.sensor_type == "alarm" and reading.value > 0:
                status["alarms"].append({
                    "code": name,
                    "value": reading.value
                })
        
        return status
    
    def start_polling(self):
        """Start continuous polling"""
        self.running = True
        logger.info(f"Starting plant gateway for {self.plant_id}")
        
        while self.running:
            try:
                readings = self.read_all_sensors()
                self.write_to_influx(re readings)
                
                # Log status changes
                status = self.get_plant_status()
                if status["alarms"]:
                    logger.warning(f"Alarms detected: {status['alarms']}")
                    
            except Exception as e:
                logger.error(f"Polling error: {e}")
            
            time.sleep(self.poll_interval)
    
    def stop(self):
        """Stop polling and cleanup"""
        self.running = False
        if self.plc:
            self.plc.disconnect()
        if self.opcua:
            self.opcua.disconnect()
        logger.info("Plant gateway stopped")


# Example configuration
EXAMPLE_CONFIG = {
    "plant_id": "PLANT-001",
    "poll_interval_ms": 1000,
    "modbus": {
        "host": "192.168.1.100",  # PLC IP address
        "port": 502,
        "unit_id": 1
    },
    "opcua": {
        "url": "opc.tcp://192.168.1.101:4840/freeopcua/server/"
    },
    "influxdb": {
        "host": "localhost",
        "port": 8086,
        "database": "as1_clone"
    }
}


if __name__ == "__main__":
    # Example usage
    config = EXAMPLE_CONFIG
    gateway = PlantGateway("PLANT-001", config)
    gateway.initialize()
    
    # Read once
    status = gateway.get_plant_status()
    print(json.dumps(status, indent=2))
    
    # Or start continuous polling
    # gateway.start_polling()
