function SessionList({ sessions }) {
    if (sessions.length === 0) return <p>Сеансы не найдены</p>;
  
    return (
      <ul>
        {sessions.map((session) => (
          <li key={session.id}>
            📅 {session.date} 🕒 {session.time} — 💸 {session.price} ₸
          </li>
        ))}
      </ul>
    );
  }
  
  export default SessionList;
  