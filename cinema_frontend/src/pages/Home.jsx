import { useEffect, useState } from 'react';
import axios from 'axios';
import EventCard from '../components/EventCard';
import Filters from '../components/Filters';

function Home() {
  const [events, setEvents] = useState([]);

  const fetchEvents = async (params = {}) => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/events', { params });
      setEvents(res.data);
    } catch (error) {
      console.error('Ошибка при получении событий:', error);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',  // Центрируем по горизонтали
        flexWrap: 'wrap',          // Элементы могут переноситься на новую строку
        width: '100%',             // Растягиваем на всю ширину
        padding: '0 20px',         // Отступы по бокам
        boxSizing: 'border-box',   // Учитываем отступы
      }}
    >
      <div style={{ 
        width: '100%', 
        maxWidth: '1200px',         // Ограничение ширины контейнера
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center',       // Центрируем все содержимое внутри контейнера
      }}>
        <Filters onFilter={fetchEvents} />
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          justifyContent: 'center', // Центрируем карточки
          gap: '1rem',              // Отступы между карточками
        }}>
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      </div>
    </div>
  );
  
}

export default Home;
