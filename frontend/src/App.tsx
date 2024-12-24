import './App.css';
import { useState } from 'react';
import CarEntryForm from './components/CarEntryForm';
import NoteForm from './components/Notes';
import CarServiceList from './components/ServiceList';
import LoginComponent from './components/LoginComponent'
interface ServiceNote {
  id: number;
  service: string;
  date: string;
  description: string;
}

function App() {
  const [isCarFormVisible, setIsCarFormVisible] = useState(false);
  const [isServiceFormVisible, setIsServiceFormVisible] = useState(false);
  const [services, setServices] = useState<ServiceNote[]>([]);

  const toggleCarForm = () => setIsCarFormVisible(!isCarFormVisible);
  const toggleServiceForm = () => setIsServiceFormVisible(!isServiceFormVisible);

  const addServiceNote = (serviceNote: ServiceNote) => {
    setServices((prevServices) => [...prevServices, serviceNote]);
  };

  return (
    <div className="app-container">
      <h1 className="app-title">Digital Servicebok</h1>
      
      {/* Button Group */}
      <div className="button-group">
        <button className="toggle-button" onClick={toggleCarForm}>
          {isCarFormVisible ? 'Stäng' : 'Lägg till bil'}
        </button>
        <button className="toggle-button" onClick={toggleServiceForm}>
          {isServiceFormVisible ? 'Stäng' : 'Lägg till service'}
        </button>
      </div>

      {/* Conditional Forms */}
      {isCarFormVisible && <CarEntryForm />}
      {isServiceFormVisible && <NoteForm onAddService={addServiceNote} />}

      {/* Display Service Notes */}
      <CarServiceList services={services} />
      <LoginComponent></LoginComponent>
    </div>
  );
}

export default App;
