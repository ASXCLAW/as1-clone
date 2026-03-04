# AS1 Clone - Technical Specification
## Asphalt Plant Control System

---

## 1. INDUSTRIAL PROTOCOLS

### 1.1 PLC Communication Protocols

| Protocol | Type | Use Case | Support |
|----------|------|----------|---------|
| **Modbus RTU** | Serial (RS-485) | Legacy PLCs, sensors | Wide |
| **Modbus TCP** | Ethernet | Modern PLCs | Wide |
| **OPC UA** | Ethernet | Industry 4.0, secure | Growing |
| **EtherNet/IP** | Ethernet | Allen Bradley PLCs | Common |
| **Profinet** | Ethernet | Siemens PLCs | Europe |
| **S7 Communication** | Ethernet | Siemens S7 | Common |

### 1.2 Recommended for AS1 Clone

**Primary:** Modbus TCP + OPC UA
- Modbus TCP for basic sensors/actuators
- OPC UA for advanced PLC integration and security

### 1.3 Protocol Details

#### Modbus TCP
```
Port: 502
Frame Format:
[Transaction ID (2)][Protocol ID (2)][Length (2)][Unit ID (1)][Function Code][Data]

Common Function Codes:
- 0x03: Read Holding Registers
- 0x04: Read Input Registers
- 0x06: Write Single Register
- 0x10: Write Multiple Registers
```

#### OPC UA
```
Transport: HTTPS (10000) / Binary (4840)
Security: TLS + X.509 certificates
Data Access: Read/Write/Subscribe
```

---

## 2. DATA FORMATS

### 2.1 Sensor Data Types

| Data Type | Register Range | Description |
|-----------|---------------|-------------|
| **Temperature** | 40001-40100 | 0.1°C resolution (int16) |
| **Level/Silo** | 40101-40200 | 0.1% (int16) |
| **Weight** | 40201-40300 | 0.01 tons (int32) |
| **Flow Rate** | 40301-40400 | 0.1 m³/h (int16) |
| **Pressure** | 40401-40500 | 0.1 bar (int16) |
| **Status** | 40501-40600 | Boolean flags |
| **Counter** | 40601-40700 | 32-bit integers |

### 2.2 Register Map Example

```
40001: Dryer Outlet Temp (°C × 10)
40002: Burner Flame Temp (°C × 10)
40003: Mixer Temp (°C × 10)
40004: Bitumen Temp (°C × 10)
40005: Aggregate Temp (°C × 10)

40101: Cold Feed Bin 1 Level (%)
40102: Cold Feed Bin 2 Level (%)
40103: Cold Feed Bin 3 Level (%)
40104: Cold Feed Bin 4 Level (%)
40105: Bitumen Tank Level (%)
40106: Filler Silo Level (%)

40201: Total Aggregate Weight (kg × 10)
40202: Bitumen Weight (kg × 10)
40203: Filler Weight (kg × 10)
40204: Total Mix Weight (kg × 10)

40301: Current Batch Number
40302: Recipe ID Active
40303: Production Rate (t/h)
40304: Energy Consumption (kWh)

40501: Plant Status (0=Stop, 1=Run, 2=Alarm)
40502: Burner Status (0=Off, 1=Ignition, 2=Running)
40503: Mixer Status (0=Stop, 1=Loading, 2=Mixing, 3=Discharging)
40504: Alarm Word 1 (bit field)
40505: Alarm Word 2 (bit field)
```

### 2.3 Batch Record Format (JSON)

```json
{
  "batch_id": "BATCH-2026-00001",
  "timestamp_start": "2026-03-05T10:30:00Z",
  "timestamp_end": "2026-03-05T10:35:00Z",
  "recipe_id": "REC-ASPHALT-EM-50",
  "recipe_name": "Asphalt EM 50/70",
  "target_quantity_tons": 200,
  "actual_quantity_tons": 198.5,
  "components": [
    {
      "name": "Aggregate 0/4",
      "target_kg": 48000,
      "actual_kg": 48120,
      "tolerance_pct": 2.0
    },
    {
      "name": "Aggregate 4/8", 
      "target_kg": 28000,
      "actual_kg": 28150,
      "tolerance_pct": 2.0
    },
    {
      "name": "Bitumen 50/70",
      "target_kg": 9600,
      "actual_kg": 9580,
      "tolerance_pct": 1.0
    }
  ],
  "temperatures": {
    "mixer_outlet": 165,
    "target": 160,
    "tolerance": 10
  },
  "quality": {
    "passed": true,
    "deviations": []
  },
  "operator_id": "OP-001",
  "plant_id": "PLANT-001"
}
```

### 2.4 Recipe Format (JSON)

```json
{
  "recipe_id": "REC-ASPHALT-WM-70",
  "name": "Asphalt Warm Mix 70/100",
  "version": 3,
  "active": true,
  "mixing_temp_c": 140,
  "mixing_time_sec": 35,
  "components": [
    {
      "component_id": "AGG-0-4",
      "name": "Aggregate 0/4",
      "percentage": 48.0,
      "tolerance_pct": 2.0,
      "min_temp_c": 140
    },
    {
      "component_id": "AGG-4-8",
      "name": "Aggregate 4/8", 
      "percentage": 28.0,
      "tolerance_pct": 2.0,
      "min_temp_c": 140
    },
    {
      "component_id": "AGG-8-11",
      "name": "Aggregate 8/11",
      "percentage": 14.0,
      "tolerance_pct": 2.0,
      "min_temp_c": 140
    },
    {
      "component_id": "BIT-WM",
      "name": "Bitumen 70/100",
      "percentage": 5.5,
      "tolerance_pct": 1.0,
      "target_temp_c": 150
    },
    {
      "component_id": "FILLER",
      "name": "Mineral Filler",
      "percentage": 4.5,
      "tolerance_pct": 1.5
    }
  ],
  "additives": [
    {
      "name": "Warm Mix Additive",
      "percentage": 0.3,
      "unit": "weight_percent_bitumen"
    }
  ]
}
```

### 2.5 Plant Status Format

```json
{
  "plant_id": "PLANT-001",
  "timestamp": "2026-03-05T10:30:00Z",
  "status": {
    "overall": "running", // stopped, running, alarm, maintenance
    "dryer": "running",
    "burner": "ignition",
    "mixer": "mixing",
    "elevator": "running"
  },
  "production": {
    "current_batch": "BATCH-2026-00001",
    "batches_today": 12,
    "tons_today": 2380,
    "rate_tph": 185
  },
  "sensors": {
    "temperatures": {
      "dryer_outlet": 165,
      "mixer": 162,
      "bitumen": 155
    },
    "levels": {
      "bin_1": 75,
      "bin_2": 60,
      "bin_3": 45,
      "bitumen_tank": 80
    }
  },
  "alarms": [
    {
      "code": "A001",
      "message": "High temperature alarm",
      "severity": "warning",
      "timestamp": "2026-03-05T10:25:00Z"
    }
  ]
}
```

---

## 3. SYSTEM ARCHITECTURE

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLOUD LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Q Plant    │  │  Analytics   │  │    Mobile    │        │
│  │   (Orders)   │  │     (BI)      │  │     API      │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                   │                   │                │
│  ┌──────▼──────────────────▼──────────────────▼───────┐       │
│  │                  API GATEWAY                          │       │
│  │            (Authentication, Rate Limiting)            │       │
│  └──────────────────────┬───────────────────────────────┘       │
└─────────────────────────┼───────────────────────────────────────┘
                          │ TLS/HTTPS
┌─────────────────────────▼───────────────────────────────────────┐
│                   EDGE/GATEWAY LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Plant Gateway (Local Server)                 │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │  Modbus  │  │   OPC    │  │   MQTT   │              │   │
│  │  │  Client  │  │   UA     │  │  Broker  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘              │   │
│  │        │              │              │                   │   │
│  │  ┌─────▼──────────────▼──────────────▼─────┐           │   │
│  │  │         Data Collection Service          │           │   │
│  │  │    (Poll intervals, buffering, sync)     │           │   │
│  │  └─────────────────┬────────────────────────┘           │   │
│  └────────────────────┼────────────────────────────────────┘   │
└───────────────────────┼────────────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────────────┐
│                  PLANT CONTROL LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PLC Network                            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│  │  │  Dryer  │  │ Burner  │  │ Mixer  │  │  Feed   │    │  │
│  │  │   PLC   │  │   PLC   │  │   PLC  │  │   PLC   │    │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │  │
│  │       │            │            │            │          │  │
│  │       └────────────┴────────────┴────────────┘          │  │
│  │                    │                                       │  │
│  └────────────────────┼───────────────────────────────────────┘  │
│                       │                                           │
│  ┌────────────────────▼───────────────────────────────────────┐ │
│  │              Sensors & Actuators                             │ │
│  │  Temp │ Level │ Weight │ Flow │ Pressure │ Motors │ Valves │ │
│  └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Details

#### Plant Gateway Server
```
Hardware: Industrial PC (x86_64)
- CPU: Intel Core i5/i7 or AMD Ryzen 5
- RAM: 8-16 GB
- Storage: 128-256 GB SSD
- Network: Dual Ethernet (isolated plant network)

OS: Linux (Ubuntu Server 22.04 LTS)
- Docker for containerization
- Kernel hardening for security

Software:
- Modbus TCP client (python-pymodbus)
- OPC UA client (python-opcua)
- MQTT broker (Mosquitto)
- Time-series database (InfluxDB)
- Redis cache
- API server (Node.js/Python)
```

#### PLC Configuration (Example)
```
Siemens S7-1500:
- IP: 192.168.1.100
- Rack: 0
- Slot: 1
- DB100: Plant Status
- DB101: Batch Data
- DB102: Recipe Parameters

Allen Bradley CompactLogix:
- IP: 192.168.1.101
- Path: 1,0
- Tags: Plant_Status, Batch_Data, Recipe
```

### 3.3 Data Flow

```
[PLC Sensors]
    │ (100ms polling)
    ▼
[Modbus TCP / OPC UA]
    │ (Convert to internal format)
    ▼
[Data Collection Service]
    │ (Validate, buffer)
    ▼
[Local Time-Series DB (InfluxDB)]
    │ (Batch records, aggregates)
    ▼
[API Server]
    │ (REST/WebSocket)
    ▼
[Cloud Sync] ──────► [Q Plant Cloud]
    │ (MQTT, hourly sync)
    ▼
[Real-time Dashboard]
```

---

## 4. DATABASE SCHEMA

### 4.1 Core Tables

```sql
-- Plants
CREATE TABLE plants (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(200),
    capacity_tph DECIMAL(10,2),
    installed_date DATE,
    status VARCHAR(20), -- active, maintenance, decommissioned
    created_at TIMESTAMP DEFAULT NOW()
);

-- Recipes
CREATE TABLE recipes (
    id UUID PRIMARY KEY,
    plant_id UUID REFERENCES plants(id),
    name VARCHAR(100),
    version INTEGER,
    mix_temp_c DECIMAL(5,1),
    mixing_time_sec INTEGER,
    components JSONB, -- Array of components
    additives JSONB,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Batches
CREATE TABLE batches (
    id UUID PRIMARY KEY,
    plant_id UUID REFERENCES plants(id),
    recipe_id UUID REFERENCES recipes(id),
    batch_number VARCHAR(50),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    target_quantity_kg DECIMAL(12,2),
    actual_quantity_kg DECIMAL(12,2),
    components JSONB, -- Actual weights
    temperatures JSONB,
    quality_passed BOOLEAN,
    operator_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sensor Readings (Time-series)
CREATE TABLE sensor_readings (
    id BIGSERIAL PRIMARY KEY,
    plant_id UUID REFERENCES plants(id),
    sensor_type VARCHAR(50), -- temperature, level, weight, pressure
    sensor_name VARCHAR(100),
    value DECIMAL(12,4),
    unit VARCHAR(20),
    timestamp TIMESTAMP
);

-- Alarms
CREATE TABLE alarms (
    id UUID PRIMARY KEY,
    plant_id UUID REFERENCES plants(id),
    code VARCHAR(20),
    message TEXT,
    severity VARCHAR(20), -- info, warning, critical
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by VARCHAR(50),
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Orders
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    plant_id UUID REFERENCES plants(id),
    customer_id VARCHAR(100),
    project_name VARCHAR(200),
    recipe_id UUID REFERENCES recipes(id),
    quantity_tons DECIMAL(10,2),
    delivery_address TEXT,
    delivery_date DATE,
    status VARCHAR(20), -- pending, confirmed, producing, delivered
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    role VARCHAR(20), -- admin, operator, viewer
    plant_ids UUID[], -- Array of plant IDs
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.2 Time-Series Indexes

```sql
-- Sensor readings partitions by plant and time
CREATE INDEX idx_sensor_readings_plant_time 
ON sensor_readings (plant_id, timestamp DESC);

CREATE INDEX idx_sensor_readings_type_time 
ON sensor_readings (sensor_type, timestamp DESC);
```

---

## 5. API SPECIFICATION

### 5.1 REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/plants | List all plants |
| GET | /api/v1/plants/:id | Plant details |
| GET | /api/v1/plants/:id/status | Current status |
| GET | /api/v1/plants/:id/sensors | Sensor readings |
| GET | /api/v1/plants/:id/batches | Batch history |
| GET | /api/v1/plants/:id/batches/:bid | Batch details |
| POST | /api/v1/plants/:id/batches | Start new batch |
| GET | /api/v1/recipes | List recipes |
| POST | /api/v1/recipes | Create recipe |
| GET | /api/v1/orders | List orders |
| POST | /api/v1/orders | Create order |
| GET | /api/v1/alarms | List alarms |
| POST | /api/v1/alarms/:id/ack | Acknowledge alarm |

### 5.2 WebSocket Events

```javascript
// Server → Client events
{
  "event": "plant_status",
  "data": { /* status object */ }
}
{
  "event": "sensor_update", 
  "data": {
    "plant_id": "xxx",
    "sensor": "temperature_mixer",
    "value": 162,
    "timestamp": "2026-03-05T10:30:00Z"
  }
}
": "batch_complete",
  "data{
  "event": { /* batch record */ }
}
{
  "event": "alarm",
  "data": { /* alarm object */ }
}
```

---

## 6. SECURITY

### 6.1 Network Isolation

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Corporate │     │   Cloud     │     │   Plant     │
│   Network   │────►│   Platform  │────►│   Network   │
│  (Office)   │     │  (AWS/Azure)│     │ (Industrial)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   │
   User Access        API Access         PLC Access
   (VPN optional)   (TLS required)    (Isolated VLAN)
```

### 6.2 Authentication

- **Cloud API**: JWT tokens, OAuth2
- **Plant Gateway**: X.509 certificates + API keys
- **PLC Access**: Network isolation only (no auth at PLC level)

### 6.3 Data Security

- **In Transit**: TLS 1.3
- **At Rest**: AES-256 encryption
- **Backups**: Encrypted, off-site

---

## 7. STACK RECOMMENDATION

### 7.1 Cloud Platform

| Component | Technology |
|-----------|------------|
| API Server | Node.js + Express / Python FastAPI |
| Database | PostgreSQL + TimescaleDB |
| Cache | Redis |
| Message Queue | RabbitMQ |
| File Storage | S3/MinIO |
| Container | Docker + Kubernetes |
| Cloud | AWS / Azure / GCP |

### 7.2 Plant Gateway

| Component | Technology |
|-----------|------------|
| OS | Ubuntu Server 22.04 LTS |
| Runtime | Python 3.11 + Node.js 18 |
| Modbus | pymodbus |
| OPC UA | opcua-asyncio |
| MQTT | Mosquitto |
| Time-series | InfluxDB |
| Local API | FastAPI |
| Sync | Custom MQTT bridge |

### 7.3 Frontend

| Component | Technology |
|-----------|------------|
| Dashboard | React + TypeScript |
| Charts | Grafana / Recharts |
| Mobile | React Native |
| Auth | Auth0 / Cognito |

---

## 8. DEVELOPMENT ROADMAP

### Phase 1: Foundation (Weeks 1-4)
- [ ] Plant gateway setup
- [ ] Modbus TCP client
- [ ] Basic sensor polling
- [ ] Local database (InfluxDB)
- [ ] Simple dashboard

### Phase 2: Control (Weeks 5-8)
- [ ] Recipe management
- [ ] Batch execution logic
- [ ] PLC write operations
- [ ] Alarm handling

### Phase 3: Cloud (Weeks 9-12)
- [ ] Cloud API development
- [ ] Multi-plant support
- [ ] Order management
- [ ] User authentication

### Phase 4: Features (Weeks 13-16)
- [ ] Analytics/BI
- [ ] Mobile apps
- [ ] Q Machine integration
- [ ] Advanced reporting

---

## 9. OPEN SOURCE ALTERNATIVES

| Component | Open Source Option |
|-----------|-------------------|
| SCADA | openSCADA, Prosys OPC |
| PLC Runtime | OpenPLC, Beremiz |
| Time-series | InfluxDB, TimescaleDB |
| MQTT | Mosquitto, EMQX |
| Industrial IoT | Node-RED, Apache NiFi |
| OPC UA | Open62541 |

---

*Document Version: 1.0*
*Created: 2026-03-05*
