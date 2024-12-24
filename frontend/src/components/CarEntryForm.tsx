import React, { useState } from 'react';
import CarInput from './CarInput';
import CarTable from '../components/CarTable';
import { fetchCarData } from "../functions/fetchCarData";
import '../styles/CarEntryForm.css';

interface Car {
  data: {
    data: Record<string, string | number>;
  };
}

const CarEntryForm = () => {
  const [carDetails, setCarDetails] = useState({
    model: '',
    engine_type: '',
    registration_number: '',
  });
  const [cars, setCars] = useState<Car[]>([]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(carDetails);
  };

  const fetchData = async (registration_number: string, engine_type: string, model: string) => {
    const fetched_car = await fetchCarData(registration_number, engine_type, model);

    const fetchedCars: Car[] = [{ data: fetched_car }];
    console.log(fetchedCars);
    setCars(fetchedCars);
  };

  return (
    <div className="car-entry-form">
      <h2>Skriv in uppgifter om din bil</h2>
      <form onSubmit={handleSubmit}>
        <CarInput
          label="Märke på bil"
          type="text"
          value={carDetails.model}
          onChange={(e) => setCarDetails({ ...carDetails, model: e.target.value })}
        />
        <CarInput
          label="Motortyp(ex D4, T8)"
          type="text"
          value={carDetails.engine_type}
          onChange={(e) => setCarDetails({ ...carDetails, engine_type: e.target.value })}
        />
        <CarInput
          label="Registreringsnummer"
          type="text"
          value={carDetails.registration_number}
          onChange={(e) => setCarDetails({ ...carDetails, registration_number: e.target.value })}
        />
        <button onClick={() => fetchData(carDetails.registration_number, carDetails.engine_type, carDetails.model)} type="submit" className="submit-button">
          Hämta
        </button>
        <CarTable cars={cars} />
      </form>
      <button className="add-car-button">Lägg till bil</button> {/* New Button */}
    </div>
  );
};

export default CarEntryForm;
