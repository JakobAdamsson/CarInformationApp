import { useState } from 'react';

interface CarServiceFormProps {
  onAddService: (serviceNote: { id: number; service: string; date: string; description: string }) => void;
}

function NoteForm({ onAddService }: CarServiceFormProps) {
  const [service, setService] = useState('');
  const [date, setDate] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!service || !date || !description) return;

    onAddService({
      id: Date.now(),
      service,
      date,
      description,
    });

    setService('');
    setDate('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="service-form">
      <h2>Lägg till Service</h2>

      <div className="form-group">
        <label htmlFor="service">Service</label>
        <input
          type="text"
          id="service"
          value={service}
          onChange={(e) => setService(e.target.value)}
          placeholder="Ex: Oljeservice"
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="date">Datum</label>
        <input
          type="date"
          id="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Beskrivning</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Kort beskrivning av service"
          required
        ></textarea>
      </div>

      <button type="submit" className="submit-button">Spara Service</button>
    </form>
  );
}

export default NoteForm;
