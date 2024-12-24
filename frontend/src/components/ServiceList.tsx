interface ServiceNote {
    id: number;
    service: string;
    date: string;
    description: string;
  }
  
  interface CarServiceListProps {
    services: ServiceNote[];
  }
  
  function CarServiceList({ services }: CarServiceListProps) {
    return (
      <div className="service-list">
        <h2>Service Historik</h2>
        {services.length === 0 ? (
          <p>Inga serviceanteckningar ännu.</p>
        ) : (
          services.map((note) => (
            <div key={note.id} className="service-item">
              <h3>{note.service}</h3>
              <p><strong>Datum:</strong> {note.date}</p>
              <p><strong>Beskrivning:</strong> {note.description}</p>
            </div>
          ))
        )}
      </div>
    );
  }
  
  export default CarServiceList;
  