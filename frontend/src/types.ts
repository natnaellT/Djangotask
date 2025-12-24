// Type definitions for API responses and component props

export interface ModelStatus {
  trained: boolean;
  last_trained_at?: string;
  rows?: number;
  r2?: number;
  mae?: number;
}

export interface PredictionResponse {
  predicted_price: number;
}

export interface TrainingResponse {
  detail: string;
}

export interface HouseFeatures {
  size: number;
  bedrooms: number;
  age: number;
}