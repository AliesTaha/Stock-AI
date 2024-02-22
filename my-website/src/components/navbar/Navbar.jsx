import React, {useState} from 'react'
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import "./navbar.css"
import logo from '../../assets/Stocks.png';
import { Link } from "react-router-dom";
import { jwtDecode } from 'jwt-decode';

const Menu = () => (
  <>
  <p><a href="#home">Home</a></p>
  <p><a href="#introduction">Introduction</a></p>
  <p><a href="#features">Features</a></p>
  <p><a href="#blog">Library</a></p>
  </>
)

const user = localStorage.getItem("token");
const decodedToken = jwtDecode(user);
const username = decodedToken.exp;
console.log(decodedToken);
const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);
  return (
    <div className = "gpt3__navbar">
      <div className = "gpt3__navbar-links">
        <div className = "gpt3__navbar-links_logo">
          <img src = {logo} alt = "logo" />
        </div>
        <div className="gpt3__navbar-links_container">
          <Menu />
        </div>
      </div>
      <div className = "gpt3__navbar-sign">
        {user ? (
        <button className="sign-in">
          <Link>
            {username}
          </Link>
        </button>
        ):
        (
          <div>
          <button className = "sign-in">
            <Link to="/login">
              Sign in
            </Link>
          </button>
          <button className="register">
            <Link to="/signup">
              Register
            </Link>
          </button>
          </div>)}
      </div>
      <div className = "gpt3__navbar-menu">
        {toggleMenu
          ? <RiCloseLine color="#fff" size={27} onClick={() => setToggleMenu(false)} />
          : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />}
        {toggleMenu && (
        <div className="gpt3__navbar-menu_container scale-up-center">
          <div className="gpt3__navbar-menu_container-links">
            <Menu />
          </div>
          <div className="gpt3__navbar-menu_container-links-sign">
          <button className = "sign-in">Sign in</button>
            <button className="register">Register</button>
          </div>
        </div>)} 
      </div>
    </div>
  )
}

export default 
Navbar