import type { ModelStatus, PredictionResponse, TrainingResponse, HouseFeatures } from '../types';

const BASE = "/api";

export async function getModelStatus(): Promise<ModelStatus> {
  const res = await fetch(`${BASE}/status/`);
  if (!res.ok) throw new Error("Status error");
  return res.json();
}

export async function predictPrice(payload: HouseFeatures): Promise<PredictionResponse> {
  const res = await fetch(`${BASE}/predict/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Predict error");
  return res.json();
}

export async function triggerTraining(): Promise<TrainingResponse> {
  const res = await fetch(`${BASE}/train/`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Train error");
  return res.json();
}

