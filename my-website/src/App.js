import React, { useEffect } from 'react'
import { Header } from "./containers";
import { Navbar } from "./components";
import "./App.css";
import { useLocation } from 'react-router-dom';

const App = () => {
  useEffect(() => {
    document.title = "StockAI"
  }, []);

  const location = useLocation();
  useEffect(() => {
    if (location.pathname === '/home') {
      window.scrollTo(0, 0); // Scroll to the top of the page
    }
  }, [location]);
  return (
    <div className = "App">
        <div className = "gradient__bg">
          <Navbar />
          <Header />
        </div>
    </div>
  )
}

export default App