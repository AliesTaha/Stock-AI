import React, { useRef, useEffect } from 'react';
import "./header.css";
import { Link } from "react-router-dom";
import stockimg from "../../assets/Stocks.png";

const user = localStorage.getItem("token");
const Header = () => {
  return (
    <div className="gpt3__header section__padding" id="home">
      <div className="gpt3__header-content">
        <h1 className="gradient__text">StockAI</h1>
        <p>Unlock the wisdom of GPT-4 Turbo for your stock decisions!</p>

        <div className="gpt3__header-content__input">
        {user ? (
        <button type="button">
          <Link to="/login">Get Started</Link>
        </button>
        ):
        (
          <button type="button">
            <Link to="/dashboard">Get Started</Link>
          </button>)}
        </div>
      </div>
      <div className="gpt3__header-image">
        <img src={stockimg} alt = ""/>
      </div>
    </div>
  );
};


export default 
Header


