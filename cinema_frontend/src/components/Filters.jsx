import { useState } from 'react';

function Filters({ onFilter }) {
  const [type, setType] = useState('');
  const [date, setDate] = useState('');
  const [genre, setGenre] = useState('');
  const [age, setAge] = useState('');
  const [time, setTime] = useState('');
  const [price, setPrice] = useState('');

  // Функция для получения сегодняшней даты в формате YYYY-MM-DD
  const getTodayDate = () => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  // Функция для получения завтрашней даты в формате YYYY-MM-DD
  const getTomorrowDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const year = tomorrow.getFullYear();
    const month = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const day = String(tomorrow.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };

  const applyFilters = () => {
    const params = {};
    if (type) params.type = type;
    if (date) params.date = date;
    if (genre) params.genre = genre;
    if (age) params.age_rating = age;
    if (time) params.time = time;
    if (price) params.price = price;

    onFilter(params);
  };

  const resetFilters = () => {
    setType('');
    setDate('');
    setGenre('');
    setAge('');
    setTime('');
    setPrice('');
    onFilter({});
  };

  const setToday = () => setDate(getTodayDate());
  const setTomorrow = () => setDate(getTomorrowDate());

  const inputStyle = {
    padding: '6px 10px',
    borderRadius: '6px',
    border: '1px solid #ccc',
    fontSize: '14px',
  };

  const buttonStyle = {
    padding: '6px 10px',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    fontSize: '14px',
  };

  const resetButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#6c757d',
  };

  return (
    <div
      style={{
        marginBottom: '1rem',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '0.5rem',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid #ccc', // Обводка для всего контейнера
        borderRadius: '6px',
        padding: '10px',
      }}
    >
      <select style={inputStyle} value={type} onChange={(e) => setType(e.target.value)}>
        <option value="">Тип</option>
        <option value="Кино">Кино</option>
        <option value="Концерт">Концерт</option>
        <option value="Спектакль">Спектакль</option>
      </select>

      {/* Контейнер с обводкой для выбора даты и кнопок "Сегодня" и "Завтра" */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          border: '1px solid #ccc',
          borderRadius: '6px',
          padding: '6px 10px',
        }}
      >
        <input
          style={{
            padding: '6px 10px',
            border: 'none',
            fontSize: '14px',
            outline: 'none',
            backgroundColor: 'transparent',
          }}
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
        <button style={buttonStyle} onClick={setToday}>Сегодня</button>
        <button style={buttonStyle} onClick={setTomorrow}>Завтра</button>
      </div>

      <select style={inputStyle} value={time} onChange={(e) => setTime(e.target.value)}>
        <option value="">Время</option>
        <option value="утром">Утром</option>
        <option value="днём">Днём</option>
        <option value="вечером">Вечером</option>
      </select>

      {/* Меню со списками */}
      <select style={inputStyle} value={genre} onChange={(e) => setGenre(e.target.value)}>
        <option value="">Жанр</option>
        <option value="комедия">Комедия</option>
        <option value="фэнтези">Фэнтези</option>
        <option value="драма">Драма</option>
        <option value="шоу">Шоу</option>
        <option value="standup">Standup</option>
        <option value="сказка">Сказка</option>
      </select>

      <select style={inputStyle} value={age} onChange={(e) => setAge(e.target.value)}>
        <option value="">Возраст</option>
        <option value="18+">18+</option>
        <option value="16+">16+</option>
        <option value="14+">14+</option>
        <option value="12+">12+</option>
        <option value="7+">7+</option>
        <option value="6+">6+</option>
        <option value="5+">5+</option>
        <option value="3+">3+</option>
        <option value="1+">1+</option>
      </select>

      <select style={inputStyle} value={price} onChange={(e) => setPrice(e.target.value)}>
        <option value="">Цена</option>
        <option value="asc">По возрастанию</option>
        <option value="desc">По убыванию</option>
      </select>

      {/* Контейнер с обводкой для кнопок "Применить" и "Сбросить" */}
      <div
        style={{
          display: 'flex',
          gap: '0.5rem',
          border: '1px solid #ccc',
          borderRadius: '6px',
          padding: '6px 10px',
        }}
      >
        <button style={buttonStyle} onClick={applyFilters}>Применить</button>
        <button style={resetButtonStyle} onClick={resetFilters}>Сбросить</button>
      </div>
    </div>
  );
}

export default Filters;
