import React, { useState, type FormEvent } from "react";
import type { HouseFeatures } from "../types";

interface HouseFormProps {
  onSubmit: (features: HouseFeatures) => void;
}

function HouseForm({ onSubmit }: HouseFormProps) {
  const [size, setSize] = useState<number>(1800);
  const [bedrooms, setBedrooms] = useState<number>(3);
  const [age, setAge] = useState<number>(10);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit({ size, bedrooms, age });
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <div className="field">
        <label>Size (sqft)</label>
        <input
          type="range"
          min="500"
          max="5000"
          step="50"
          value={size}
          onChange={(e) => setSize(Number(e.target.value))}
        />
        <span className="value">{size} sqft</span>
      </div>

      <div className="field">
        <label>Bedrooms</label>
        <input
          type="range"
          min="1"
          max="6"
          step="1"
          value={bedrooms}
          onChange={(e) => setBedrooms(Number(e.target.value))}
        />
        <span className="value">{bedrooms} beds</span>
      </div>

      <div className="field">
        <label>Age (years)</label>
        <input
          type="range"
          min="0"
          max="60"
          step="1"
          value={age}
          onChange={(e) => setAge(Number(e.target.value))}
        />
        <span className="value">{age} years</span>
      </div>

      <button className="primary-button" type="submit">
        Predict price
      </button>
    </form>
  );
}

export default HouseForm;

