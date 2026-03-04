# AS1 Clone - Hardware Recommendations

## Recommended PLC Systems

### Tier 1: Enterprise (Large Plants)

#### Siemens S7-1500 + TIA Portal
- **CPU**: CPU 1516-3 PN/DP (416 KB work memory)
- **Communication**: PROFINET, Modbus TCP, OPC UA
- **Price**: ~$3,000-5,000
- **Pros**: Industry standard, excellent support, wide compatibility
- **Cons**: Proprietary software (TIA Portal) costs extra

#### Allen Bradley ControlLogix 1756
- **CPU**: 1756-L73S (2MB memory)
- **Communication**: EtherNet/IP, OPC UA
- **Price**: ~$4,000-6,000
- **Pros**: Robust, great integration with US systems
- **Cons**: Expensive licensing

### Tier 2: Mid-Range (Medium Plants)

#### Siemens S7-1200
- **CPU**: CPU 1215C DC/DC/DC (150 KB work memory)
- **Communication**: PROFINET, Modbus TCP
- **Price**: ~$800-1,200
- **Pros**: Compact, good features, affordable
- **Cons**: Limited scalability

#### Schneider Modicon M241
- **CPU**: TM241CEC (128 KB)
- **Communication**: EtherNet/IP, Modbus TCP, OPC UA
- **Price**: ~$600-900
- **Pros**: Good connectivity, competitive price
- **Cons**: Smaller ecosystem

#### Omron NX1P2
- **CPU**: NX1P2-9024DT (160 KB)
- **Communication**: EtherNet/IP, OPC UA
- **Price**: ~$700-1,000
- **Pros**: Fast, compact, good for small plants

### Tier 3: Budget/Small Plants

#### Siemens Logo! 8
- **CPU**: LOGO! 8.3
- **Communication**: Modbus TCP
- **Price**: ~$300-500
- **Pros**: Very affordable, easy to program
- **Cons**: Limited I/O, basic functionality

#### Mitsubishi FX5U
- **CPU**: FX5U-32MT/ES
- **Communication**: Modbus TCP, Ethernet
- **Price**: ~$400-600
- **Pros**: Good value, compact

#### AutomationDirect Productivity
- **CPU**: P1000
- **Communication**: Modbus TCP
- **Price**: ~$300-500
- **Pros**: Low cost, open source programming

---

## Recommended Plant Gateway Hardware

### Industrial PC (On-Premise)

| Model | Specs | Price | Use Case |
|-------|-------|-------|-----------|
| **Dell Edge Gateway 3003** | Intel Atom, 4GB RAM, 128GB SSD | ~$600 | Small plants |
| **Siemens SIMATIC IPC127E** | Intel Celeron, 8GB RAM | ~$800 | Medium plants |
| **Beckhoff CX9020** | Intel Atom, Linux-ready | ~$1,200 | Enterprise |
| **Advantech UNO-260** | Intel Atom, wide temp | ~$900 | Harsh environments |

### Single-Board Computer (DIY/Small)

| Model | Specs | Price | Use Case |
|-------|-------|-------|-----------|
| **Raspberry Pi 5** | 8GB RAM, NVMe slot | ~$80-120 | Prototyping |
| **Rock 5B** | RK3588, 16GB RAM | ~$150 | Prototyping |
| **Atomic Pi** | Intel Atom, 4GB RAM | ~$100 | Budget deployment |

---

## Recommended Network Equipment

### Industrial Ethernet Switch

| Model | Ports | Features | Price |
|-------|-------|----------|-------|
| **Moxa EDS-205A** | 5x RJ45 | Industrial, DIN-rail | ~$80 |
| **Siemens SCALANCE XB005** | 5x RJ45 | PROFINET compatible | ~$120 |
| **Cisco IE-4000** | 8x GE | Enterprise grade | ~$1,500 |

### Firewall/VPN

| Model | Features | Price |
|-------|----------|-------|
| **OpnSense** (PC Engines) | Full firewall, VPN | ~$200 |
| **Siemens SCALANCE S615** | Industrial VPN | ~$800 |
| **Cisco ISR 1100** | Enterprise router | ~$1,000 |

---

## Recommended Sensors

### Temperature

| Model | Range | Accuracy | Protocol | Price |
|-------|-------|----------|----------|-------|
| **PT100 RTD** | -200 to 850°C | ±0.1°C | 4-20mA | ~$50 |
| **Thermocouple K** | 0-1100°C | ±0.5°C | 4-20mA | ~$30 |
| **Infrared IR-ETH** | -20 to 500°C | ±1°C | Modbus TCP | ~$200 |

### Level/Silo

| Model | Range | Accuracy | Protocol | Price |
|-------|-------|----------|----------|-------|
| **Ultrasonic LUF200** | 0-20m | ±0.5% | 4-20mA | ~$150 |
| **Radar VEGAPULS 61** | 0-35m | ±2mm | 4-20mA/HART | ~$600 |
| **Load Cells** | Per application | ±0.1% | Modbus | ~$500/set |

### Flow

| Model | Range | Accuracy | Protocol | Price |
|-------|-------|----------|----------|-------|
| **Coriolis MASSFLOW** | 0-1000 kg/h | ±0.1% | Modbus | ~$2,000 |
| **Vortex FTV** | 0-50 m/s | ±1% | 4-20mA | ~$400 |

---

## Complete Small Plant Bill of Materials

| Category | Item | Qty | Unit Price | Total |
|----------|------|-----|------------|-------|
| **PLC** | Siemens S7-1200 CPU 1215C | 1 | $800 | $800 |
| **PLC** | Digital I/O Module 16DI/16DO | 2 | $250 | $500 |
| **PLC** | Analog I/O Module 4AI/2AO | 2 | $300 | $600 |
| **Gateway** | Raspberry Pi 5 8GB | 1 | $100 | $100 |
| **Gateway** | NVMe SSD 256GB | 1 | $40 | $40 |
| **Network** | Industrial Switch 8-port | 1 | $150 | $150 |
| **Sensors** | PT100 Temperature Probes | 6 | $50 | $300 |
| **Sensors** | Ultrasonic Level Sensors | 4 | $150 | $600 |
| **Sensors** | Load Cells (silo) | 4 | $150 | $600 |
| **Enclosure** | DIN-rail Cabinet 600x400x200 | 1 | $200 | $200 |
| **Power** | 24V DC Power Supply 10A | 1 | $100 | $100 |
| **Cabling** | Cat6, Connectors, Wire | Lot | $150 | $150 |
| **Software** | Node-RED (free) | - | $0 | $0 |
| **Software** | InfluxDB (free) | - | $0 | $0 |
| **Software** | Python (free) | - | $0 | $0 |
| | | | **TOTAL** | **$4,140** |

---

## Enterprise Plant Bill of Materials

| Category | Item | Qty | Unit Price | Total |
|----------|------|-----|------------|-------|
| **PLC** | Siemens S7-1500 CPU 1516-3 | 1 | $4,000 | $4,000 |
| **PLC** | Digital I/O (various) | 10 | $300 | $3,000 |
| **PLC** | Analog I/O (various) | 6 | $400 | $2,400 |
| **Gateway** | Dell Edge Gateway 3003 | 1 | $600 | $600 |
| **Network** | Industrial Switch 24-port | 2 | $400 | $800 |
| **Firewall** | Siemens SCALANCE S615 | 1 | $800 | $800 |
| **Sensors** | Radar Level VEGAPULS 61 | 8 | $600 | $4,800 |
| **Sensors** | Flow Meters (Coriolis) | 4 | $2,000 | $8,000 |
| **Sensors** | Temp Probes (PT100) | 12 | $50 | $600 |
| **Sensors** | Load Cells | 12 | $200 | $2,400 |
| **Software** | TIA Portal Basic | 1 | $500 | $500 |
| **Software** | InfluxDB Enterprise | 1 | $1,500/yr | $1,500 |
| **Cloud** | AWS IoT (est.) | 1 | $200/mo | $2,400/yr |
| | | | **TOTAL** | **~$32,000** |

---

## Wiring Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────┐
│                    PLANT NETWORK (192.168.1.0/24)           │
│                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │   S7-1200   │────►│  Gateway    │────►│   Cloud     │  │
│  │    PLC      │     │   (Pi 5)    │     │  (AWS)      │  │
│  └──────┬──────┘     └──────┬──────┘     └─────────────┘  │
│         │                   │                                 │
│  ┌──────┴──────┐     ┌──────┴──────┐                        │
│  │   I/O       │     │   MQTT      │                        │
│  │  Modules    │     │   Broker    │                        │
│  └──────┬──────┘     └─────────────┘                        │
│         │                                                   │
│  ┌──────┴──────────────────────────────────────────────┐   │
│  │                   SENSORS                            │   │
│  │  Temps  │  Levels  │  Weights  │  Flow  │  Status  │   │
│  │   PT100 │  Radar   │ LoadCells │Coriolis│  Switch  │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Software Stack Summary

| Layer | Technology | License |
|-------|-----------|---------|
| Gateway OS | Ubuntu Server 22.04 LTS | Free |
| PLC Protocol | Python + pymodbus | Free |
| OPC UA | Python + opcua-asyncio | Free |
| Time-Series DB | InfluxDB | Free/Paid |
| Message Broker | Mosquitto MQTT | Free |
| API Server | Node.js + FastAPI | Free |
| Dashboard | Grafana | Free |
| Cloud | AWS/Azure | Pay per use |
