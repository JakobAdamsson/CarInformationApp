import React, { useState } from 'react';
import '../styles/CarTable.css';

interface Car {
  data: {
    data: Record<string, string | number>;
  };
}

const CarTable: React.FC<{ cars?: Car[] }> = ({ cars = [] }) => {
  const [isVisible, setIsVisible] = useState<boolean>(false);  // State to track dropdown visibility
  const keysToDisplay = [
    "Drivlina:",
    "Chassi:",
    "Ventiler:",
    "Bränslesystem:",
    "Bränsle:",
    "Cylindrar:",
    "Motorvolym L:",
    "Chassinummer (VIN):",
    "Däck, fram:",
    "Däck, bak:",
    "Motorkod:",
    "Oljevolym",
    "Registreringsnummer",
    "Motortyp",
    "Bilmodell"
  ];

  // Toggle the visibility of the car information
  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  return (
    <div className="car-table-container">
      <h1>
        <button onClick={toggleVisibility} className="dropdown-button">
          Mer information om bilen
        </button>
      </h1>
      {isVisible && (
        <table className="car-table">
          <thead>
            <tr>
              <th>Typ</th>
              <th>Värde</th>
            </tr>
          </thead>
          <tbody>
            {cars.map((car: Car, index: number) => (
              <React.Fragment key={index}>
                {keysToDisplay.map((key) =>
                  car.data.data[key] !== undefined ? (
                    <tr key={key}>
                      <td>{key}</td>
                      <td>{JSON.stringify(car.data.data[key])}</td>
                    </tr>
                  ) : null
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default CarTable;
