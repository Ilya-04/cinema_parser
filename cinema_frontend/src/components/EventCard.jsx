import { useEffect, useState } from 'react';
import axios from 'axios';
import SessionList from './SessionList';

function EventCard({ event }) {
  const [sessions, setSessions] = useState([]);
  const [venue, setVenue] = useState(null); // Для хранения информации о месте проведения

  useEffect(() => {
    // Загружаем сеансы
    axios.get(`http://localhost:8000/sessions?event_id=${event.id}`)
      .then(response => {
        setSessions(response.data);
        // Если у сеанса есть venue_id, запрашиваем информацию о месте проведения
        if (response.data.length > 0 && response.data[0].venue_id) {
          const venueId = response.data[0].venue_id;
          axios.get(`http://localhost:8000/venues/${venueId}`)
            .then(response => setVenue(response.data))
            .catch(error => console.error('Ошибка загрузки места проведения:', error));
        }
      })
      .catch(error => console.error('Ошибка загрузки сеансов:', error));
  }, [event.id]);

  return (
    <div 
      style={{
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '1rem',
        margin: '1rem 0',
        display: 'flex',
        flexDirection: 'column',
        width: '1000px',  // Фиксированная ширина карточки
        boxSizing: 'border-box', // Учитываем padding и border в расчете ширины
      }}
    >
      <h2 style={{ marginBottom: '1rem' }}>{event.title}</h2>
      <div style={{ display: 'flex' }}>
        {/* Постер слева */}
        <img
          src={event.poster_url}
          alt={event.title}
          style={{
            width: '200px',     // фиксированная ширина постера
            height: 'auto',     // сохраняем пропорции
            marginRight: '1rem',
            borderRadius: '4px',
            objectFit: 'contain',  // если нужно — подгонка внутри блока
          }}
        />

        {/* Информация справа */}
        <div style={{ flex: 1 }}>
          <p><strong>Тип:</strong> {event.type_event}</p>
          <p><strong>Жанр:</strong> {event.genre}</p>
          <p><strong>Возраст:</strong> {event.age_rating}</p>
          <p>{event.description}</p>

          {venue && (
            <p><strong>Место проведения:</strong> {venue.address}</p>
          )}

          <h4>Сеансы:</h4>
          <SessionList sessions={sessions} />

          <a href={event.url} target="_blank" rel="noopener noreferrer" style={{ display: 'inline-block', marginTop: '0.5rem' }}>
            Подробнее
          </a>
        </div>
      </div>
    </div>
  );
}

export default EventCard;
