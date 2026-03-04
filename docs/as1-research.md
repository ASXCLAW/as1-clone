# AS1 System Software by Ammann - Deep Technical Research

## Project Goal
Clone/replicate AS1 functionality for asphalt plant control

---

## 1. SYSTEM OVERVIEW

### Company: Ammann
- Swiss construction equipment manufacturer
- Leading supplier of mixing plants and machines
- Year founded: 1869 (need to verify)
- Headquarters: Switzerland

### Product Hierarchy
```
Ammann
├── as1 (Core Control System)
│   ├── as1 PIP (Plant Information Point) - Mobile/remote
│   └── as1 SMM (System Message Management) - Alerts
├── Q Plant (Cloud Platform)
│   ├── Essential (Entry-level)
│   ├── Professional (Integrated)
│   └── Business Intelligence (Analytics)
│   └── Add-Ons
├── Q Machines (Paving/Compaction)
│   ├── Q Pave (Temperature monitoring)
│   └── Q Compaction
└── Connected Worksite (Full Ecosystem)
```

---

## 2. as1 CONTROL SYSTEM

### Core Functions
- Plant operating system for asphalt mixing
- Batch management
- Production control
- Recipe management
- Quality control
- Real-time monitoring

### Data Points Managed
- Dryer operation
- Burner control
- Screen operation
- Aggregate feeding
- Bitumen heating
- Mixing process
- Loadout

---

## 3. as1 PIP (Plant Information Point)

### Type: Mobile Data Solution

### Features
| Feature | Description |
|---------|-------------|
| Plant KPIs | Key performance indicators |
| Current Production | Real-time production info |
| Operating Data | Live operational metrics |
| Plant Status | Running/Stopped/Alarm |
| Daily Trends | Historical daily data |
| Production Logs | PDF batch protocols |
| Document Archive | Historical documents |
| Fill Levels | Bin/silo levels |
| Temperatures | Heater/mixer temps |

### User Interface
- Mobile-friendly web portal
- Real-time data refresh
- Historical data access

---

## 4. as1 SMM (System Message Management)

### Features
- Error message notifications
- Email alerts
- Real-time problem notification
- Multi-language support

---

## 5. Q PLANT (Cloud Platform)

### Overview
- Cloud-based web application
- Digital hub for mixing plant
- Multi-plant support
- Integrates: control systems, weighing, lab, CRM, orders

### Editions

#### Essential (Entry-Level)
- Digital ordering and delivery
- Production sequence optimization
- Basic plant data

#### Professional (Integrated)
- Full IT integration
- ERP/CRM interfaces
- Delivery monitor (dynamic cycle plan)
- Seamless digital process
- Minimal manual intervention

#### Business Intelligence
- Multi-plant analytics
- Cross-plant comparison
- Operational data analysis

### Add-Ons

**Dashboards**
- Operations dashboards
- Production dashboards
- Multi-plant KPI comparison
- Efficiency metrics
- Energy indicators

**Batch Reports & Archive**
- Recipe changes log
- Batch duration
- Batch sizes
- Target-actual comparisons
- Quantity deviations
- Tolerance analysis

**Dynamic Production Planning**
- Order-based optimization
- Individual loading batches
- Recipe change visibility
- Manual adjustment option
- Order combine/split/reschedule

### Interfaces

| Interface | Purpose |
|-----------|---------|
| Master Data (ERP) | Customer, project, article sync |
| Weighing System | Real-time weight data |
| Plant Control (as1) | Production scheduling, operational data |
| Laboratory Systems | Quality assurance data |
| Transport/Trucking | Delivery coordination |

---

## 6. Q MACHINES (Paving/Compaction)

### Type: Intelligent Compaction System

### Components

#### Q Pave
- Asphalt temperature monitoring
- Multi-position temperature sensing
- Quality assurance
- Temperature range alerts

#### Q Compaction
- Stiffness measurement
- Surface temperature
- Crossing count tracking
- Compaction progress visualization

### Features
- Position-accurate control
- Machine-to-machine sync
- Temperature logging
- Weather data overlay
- CO2 reduction (fewer passes)
- Analysis software
- Client reporting
- Multi-manufacturer support (any brand roller)

---

## 7. CONNECTED WORKSITE ECOSYSTEM

### Data Flow Architecture
```
[Construction Company]
        ↓ Orders
[Q Plant] ←→ [as1 Control System] ←→ [Plant Hardware]
        ↓                                    ↓
   [Weighing System]              [Q Machines]
        ↓                                    ↓
[Truck Drivers (TruckBuddy)]      [Paving/Compaction]
        ↓
[Construction Site]
```

### Digital Value Chain
1. **Planning**: Orders from construction companies
2. **Production**: Q Plant → as1 → Plant
3. **Delivery**: Weighing → Truck → Site
4. **Paving**: Q Machines monitoring
5. **Documentation**: Full audit trail

---

## 8. TECHNICAL SPECIFICATIONS (INFERRED)

### Plant Control Interfaces
- **Protocols**: Likely Modbus, OPC-UA, or proprietary
- **PLC**: Industrial programmable logic controllers
- **Sensors**: Temperature, level, flow, pressure, weight

### Cloud Architecture
- **Platform**: Cloud-based (Q Point)
- **Access**: Web browser, mobile apps
- **APIs**: RESTful for integrations
- **Database**: Time-series for production data

### Data Models (Probable)
- Plants (ID, location, capacity)
- Recipes (formulas, tolerances)
- Batches (timestamp, recipe, quantities)
- Orders (customer, project, delivery)
- Trucks (ID, location, status)
- Users (roles, permissions)

---

## 9. COMPETITIVE LANDSCAPE

### Known Competitors
- LINNEX (Linhoff)
- Telsmith
- Custom/Proprietary systems

### Differentiation Factors
- Cloud integration depth
- Multi-plant management
- Mobile accessibility
- Paving/compaction integration
- Real-time alerting

---

## 10. CLONING REQUIREMENTS

### MVP Features

**1. Plant Interface Layer**
```
Requirements:
- PLC communication (Modbus TCP/RTU)
- OPC-UA support
- Sensor ingestion (temps, levels, weights)
- Actuator control signals
- Real-time data streaming

Tech Stack:
- Python (industrial protocols)
- Node-RED (flow-based)
- Apache NiFi (data pipeline)
```

**2. Core Control System**
```
Features:
- Batch management
- Recipe storage & execution
- Production scheduling
- Quality checks
- Alarm handling

Tech Stack:
- PostgreSQL (relational data)
- Redis (real-time cache)
- Python/Node.js backend
```

**3. Dashboard/UI**
```
Features:
- Real-time plant status
- KPI visualization
- Production logs
- Recipe management
- Reporting

Tech Stack:
- React/Vue frontend
- Grafana/Power BI
- PDF generation
```

**4. Cloud/Mobile (Advanced)**
```
Features:
- Multi-plant access
- Mobile apps
- Order management
- Delivery tracking

Tech Stack:
- Cloud hosting (AWS/Azure)
- REST APIs
- Mobile frameworks

Tech Stack:
- Cloud hosting (AWS/Azure)
- REST APIs
- Mobile frameworks
```

### Data Architecture
```
┌─────────────────────────────────────────┐
│           Cloud Platform                │
│  ┌──────────┐  ┌──────────────────┐   │
│  │ Q Plant  │  │   Analytics       │   │
│  │ (Orders) │  │   (BI)            │   │
│  └────┬─────┘  └──────────────────┘   │
│       │                                  │
│  ┌────▼────────────────────────────────┐│
│  │         API Gateway                 ││
│  └────┬────────────────────────────────┘│
└───────┼──────────────────────────────────┘
        │ (HTTPS/MQTT)
┌───────▼──────────────────────────────────┐
│          Local Plant Network            │
│  ┌────────────┐    ┌────────────────┐   │
│  │ as1 Clone │◄───│   PLC/Sensors   │   │
│  │ (Control) │    └────────────────┘   │
│  └────────────┘                        │
└─────────────────────────────────────────┘
```

### Key Development Phases

**Phase 1: Basic Control**
- Read plant sensors
- Basic batch execution
- Local dashboard

**Phase 2: Cloud Add**
- Q Plant-like features
- Order management
- Multi-plant support

**Phase 3: Mobile**
- PIP-like mobile access
- Alerts/notifications

**Phase 4: Ecosystem**
- Q Machines-like features
- Paving integration
- Full documentation

---

## 11. SOURCE LINKS

1. https://www.ammann.com/en-US/news/ammann-as1-pip-plant-information-anytime-anywhere/
2. https://www.ammann.com/en-US/connected-worksite/
3. https://www.ammann.com/en-US/plants/asphalt-plants/
4. https://www.ammann.com/en-US/plants/asphalt-plants/core-components/
5. https://q-point.com/en/product/q-plant-2
6. https://q-point.com/en/product/q-plant-professional
7. https://q-point.com/en/product/q-plant-add-ons
8. https://q-point.com/en/product/q-machines-2
9. https://q-point.com/en/product/q-compaction-2

---

## 12. NEXT STEPS

### Research
- [ ] Find PLC protocol specifications
- [ ] Get actual API documentation (if available)
- [ ] Interview plant operators
- [ ] Source sample data formats

### Development Prep
- [ ] Define data models
- [ ] Choose tech stack
- [ ] Prototype plant interface
- [ ] Build MVP roadmap

---
*Research started: 2026-03-05*
*Last updated: 2026-03-05*
