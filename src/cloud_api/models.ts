// AS1 Clone - Data Models
// TypeScript interfaces for the asphalt plant control system

// ============================================
// CORE DATA MODELS
// ============================================

export interface Plant {
  id: string;
  name: string;
  location: string;
  capacity_tph: number;
  installedDate: string;
  status: PlantStatus;
  createdAt: string;
}

export type PlantStatus = 'active' | 'maintenance' | 'decommissioned' | 'running' | 'stopped' | 'alarm';

export interface Recipe {
  id: string;
  plantId: string;
  name: string;
  version: number;
  mixTempC: number;
  mixingTimeSec: number;
  components: RecipeComponent[];
  additives: Additive[];
  active: boolean;
  createdAt: string;
}

export interface RecipeComponent {
  componentId: string;
  name: string;
  percentage: number;
  tolerancePct: number;
  minTempC?: number;
}

export interface Additive {
  name: string;
  percentage: number;
  unit: string; // weight_percent_bitumen
}

export interface Batch {
  id: string;
  plantId: string;
  recipeId: string;
  batchNumber: string;
  startTime: string;
  endTime?: string;
  targetQuantityKg: number;
  actualQuantityKg: number;
  components: BatchComponent[];
  temperatures: TemperatureRecord;
  qualityPassed: boolean;
  operatorId: string;
  status: BatchStatus;
}

export type BatchStatus = 'in_progress' | 'completed' | 'aborted';

export interface BatchComponent {
  name: string;
  targetKg: number;
  actualKg: number;
  tolerancePct: number;
}

export interface TemperatureRecord {
  mixerOutlet: number;
  target: number;
  tolerance: number;
}

export interface SensorReading {
  id: string;
  plantId: string;
  sensorName: string;
  sensorType: SensorType;
  value: number;
  unit: string;
  timestamp: string;
}

export type SensorType = 'temperature' | 'level' | 'weight' | 'pressure' | 'flow' | 'status' | 'alarm';

export interface PlantStatus {
  plantId: string;
  timestamp: string;
  overall: OverallStatus;
  production: ProductionData;
  sensors: SensorData;
  alarms: Alarm[];
}

export type OverallStatus = 'stopped' | 'running' | 'alarm' | 'maintenance';

export interface ProductionData {
  currentBatch?: string;
  batchesToday: number;
  tonsToday: number;
  rateTph: number;
}

export interface SensorData {
  temperatures: Record<string, number>;
  levels: Record<string, number>;
}

export interface Alarm {
  id: string;
  code: string;
  message: string;
  severity: AlarmSeverity;
  acknowledged: boolean;
  acknowledgedBy?: string;
  acknowledgedAt?: string;
  timestamp: string;
}

export type AlarmSeverity = 'info' | 'warning' | 'critical';

export interface Order {
  id: string;
  plantId: string;
  customerId: string;
  projectName: string;
  recipeId: string;
  quantityTons: number;
  deliveryAddress: string;
  deliveryDate: string;
  status: OrderStatus;
  notes?: string;
  createdAt: string;
}

export type OrderStatus = 'pending' | 'confirmed' | 'producing' | 'delivered';

// ============================================
// API RESPONSE TYPES
// ============================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

// ============================================
// WEBSOCKET EVENT TYPES
// ============================================

export interface WsEvent {
  event: WsEventType;
  data: any;
  timestamp: string;
}

export type WsEventType = 
  | 'plant_status'
  | 'sensor_update'
  | 'batch_started'
  | 'batch_completed'
  | 'alarm'
  | 'order_update';

// ============================================
// DASHBOARD WIDGET TYPES
// ============================================

export interface DashboardWidget {
  id: string;
  type: WidgetType;
  title: string;
  config: WidgetConfig;
}

export type WidgetType = 
  | 'temperature_gauge'
  | 'level_bar'
  | 'production_chart'
  | 'batch_list'
  | 'alarm_feed'
  | 'kpi_card';

export interface WidgetConfig {
  sensors?: string[];
  plantId?: string;
  timeRange?: string;
  refreshInterval?: number;
}

// ============================================
// REGISTER MAP (for PLC communication)
// ============================================

export interface RegisterMap {
  [key: string]: {
    address: number;
    type: SensorType;
    scale: number;
    unit: string;
    description: string;
  };
}

export const REGISTER_MAP: RegisterMap = {
  // Temperatures (40001-40099)
  dryer_outlet_temp: { address: 0, type: 'temperature', scale: 0.1, unit: '°C', description: 'Dryer outlet temperature' },
  burner_temp: { address: 1, type: 'temperature', scale: 0.1, unit: '°C', description: 'Burner flame temperature' },
  mixer_temp: { address: 2, type: 'temperature', scale: 0.1, unit: '°C', description: 'Mixer temperature' },
  bitumen_temp: { address: 3, type: 'temperature', scale: 0.1, unit: '°C', description: 'Bitumen temperature' },
  aggregate_temp: { address: 4, type: 'temperature', scale: 0.1, unit: '°C', description: 'Aggregate temperature' },
  
  // Levels (40101-40199)
  cold_feed_bin_1: { address: 100, type: 'level', scale: 0.1, unit: '%', description: 'Cold feed bin 1 level' },
  cold_feed_bin_2: { address: 101, type: 'level', scale: 0.1, unit: '%', description: 'Cold feed bin 2 level' },
  cold_feed_bin_3: { address: 102, type: 'level', scale: 0.1, unit: '%', description: 'Cold feed bin 3 level' },
  cold_feed_bin_4: { address: 103, type: 'level', scale: 0.1, unit: '%', description: 'Cold feed bin 4 level' },
  bitumen_tank_level: { address: 104, type: 'level', scale: 0.1, unit: '%', description: 'Bitumen tank level' },
  filler_silo_level: { address: 105, type: 'level', scale: 0.1, unit: '%', description: 'Filler silo level' },
  
  // Weights (40201-40299)
  total_aggregate_weight: { address: 200, type: 'weight', scale: 0.01, unit: 'tons', description: 'Total aggregate weight' },
  bitumen_weight: { address: 201, type: 'weight', scale: 0.01, unit: 'tons', description: 'Bitumen weight' },
  filler_weight: { address: 202, type: 'weight', scale: 0.01, unit: 'tons', description: 'Filler weight' },
  total_mix_weight: { address: 203, type: 'weight', scale: 0.01, unit: 'tons', description: 'Total mix weight' },
  
  // Production (40301-40399)
  current_batch_number: { address: 300, type: 'status', scale: 1, unit: '', description: 'Current batch number' },
  active_recipe_id: { address: 301, type: 'status', scale: 1, unit: '', description: 'Active recipe ID' },
  production_rate: { address: 302, type: 'flow', scale: 0.1, unit: 't/h', description: 'Production rate' },
  energy_consumption: { address: 303, type: 'weight', scale: 1, unit: 'kWh', description: 'Energy consumption' },
  
  // Status (40501-40599)
  plant_status: { address: 500, type: 'status', scale: 1, unit: '', description: 'Overall plant status' },
  burner_status: { address: 501, type: 'status', scale: 1, unit: '', description: 'Burner status' },
  mixer_status: { address: 502, type: 'status', scale: 1, unit: '', description: 'Mixer status' },
  alarm_word_1: { address: 503, type: 'alarm', scale: 1, unit: '', description: 'Alarm word 1' },
  alarm_word_2: { address: 504, type: 'alarm', scale: 1, unit: '', description: 'Alarm word 2' },
};
