import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',  // Центрируем по горизонтали
          alignItems: 'flex-start',  // Выравниваем сверху
          minHeight: '100vh',         // Высота на всю высоту экрана
          padding: '0 20px',          // Добавляем отступы слева и справа
          boxSizing: 'border-box',    // Учитываем отступы в размере
        }}
      >
        <div
          style={{
            maxWidth: '1200px', // Максимальная ширина
            width: '100%',      // Растягиваем на всю доступную ширину
          }}
        >
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;




// .\venv\Scripts\Activate
// cd cinema_frontend
// npm run dev