import React, { useEffect, useState } from "react";
import { getModelStatus, predictPrice, triggerTraining } from "./api/api";
import HouseForm from "./components/HouseForm";
import type { ModelStatus, HouseFeatures } from "./types";
import "./index.css";

function App() {
  const [status, setStatus] = useState<ModelStatus | null>(null);
  const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
  const [loadingStatus, setLoadingStatus] = useState<boolean>(false);
  const [training, setTraining] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const refreshStatus = async () => {
    setLoadingStatus(true);
    try {
      const data = await getModelStatus();
      setStatus(data);
    } catch (e) {
      console.error(e);
      setError("Failed to load model status");
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    refreshStatus();
  }, []);

  const handlePredict = async (payload: HouseFeatures) => {
    setError("");
    setPredictedPrice(null);
    try {
      const data = await predictPrice(payload);
      setPredictedPrice(data.predicted_price);
    } catch (e) {
      console.error(e);
      setError("Prediction failed");
    }
  };

  const handleTrain = async () => {
    setTraining(true);
    setError("");
    try {
      await triggerTraining();
      await refreshStatus();
    } catch (e) {
      console.error(e);
      setError("Failed to trigger training");
    } finally {
      setTraining(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Smart House Price Predictor</h1>
        <p className="subtitle">
          Self-updating ML model with scheduled retraining
        </p>
      </header>

      <main className="layout">
        <section className="card main-card">
          <h2>Estimate a price</h2>
          <HouseForm onSubmit={handlePredict} />
          {predictedPrice !== null && (
            <div className="result">
              <span>Estimated price:</span>
              <strong>${predictedPrice.toLocaleString()}</strong>
            </div>
          )}
          {error && <div className="error">{error}</div>}
        </section>

        <section className="card side-card">
          <h2>Model status</h2>
          {loadingStatus && <p>Loading status...</p>}
          {status && status.trained && (
            <ul className="status-list">
              <li>
                <span>Last trained:</span>
                <strong>
                  {status.last_trained_at
                    ? new Date(status.last_trained_at).toLocaleString()
                    : "N/A"}
                </strong>
              </li>
              <li>
                <span>Rows:</span>
                <strong>{status.rows ?? "N/A"}</strong>
              </li>
              <li>
                <span>R² score:</span>
                <strong>{status.r2?.toFixed(3) ?? "N/A"}</strong>
              </li>
              <li>
                <span>MAE:</span>
                <strong>{status.mae?.toFixed(0) ?? "N/A"}</strong>
              </li>
            </ul>
          )}
          {status && !status.trained && (
            <p>No training has been run yet. Start a training job below.</p>
          )}

          <button
            className="primary-button"
            onClick={handleTrain}
            disabled={training}
          >
            {training ? "Starting training..." : "Trigger retraining"}
          </button>
          <p className="hint">
            Background scheduler (Celery Beat) also retrains daily at 02:00.
          </p>
        </section>
      </main>
    </div>
  );
}

export default App;

