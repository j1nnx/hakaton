import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css'
import { MainPage } from './pages/main';
import { AuthPage } from './pages/auth';
import { AdminPage } from './pages/admin';
 
function App() {
  const [count, setCount] = useState(true);

  
  return (
    <div className='app'>
      <Router>
        <Routes>
          <Route path="/" element={<MainPage/>} />
          <Route path="/auth" element={<AuthPage/>} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
