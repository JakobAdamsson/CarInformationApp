import React from 'react';
import '../styles/Input.css';

const CarInput = ({ label, type, value, onChange }: { label: string, type: string, value: string, onChange: (e: React.ChangeEvent<HTMLInputElement>) => void }) => {
  return (
    <div className="input-container">
      <label>{label}</label>
      <input type={type} value={value} onChange={onChange} className="input-field" />
    </div>
  );
};

export default CarInput;
