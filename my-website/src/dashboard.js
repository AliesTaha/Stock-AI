import React, { useEffect, useState } from "react";
import "./dashboard.css";

const Dashboard = () => { 
    const handleLogout = () => {
		localStorage.removeItem("token");
		window.location.reload();
    window.location.href = "/";
	};
    return (
    <div className = "App">
        <div className = "gradient__bg">
            hi
        </div>
        <button className="logout" onClick={handleLogout}>
          Logout
        </button>
        <button className="buy" onClick={handleLogout}> 
        {/* need to implement buy */}
          Buy
        </button>
        <button className="sell" onClick={handleLogout}>
        {/* need to implement buy */}
          Sell
        </button>
    </div>
    )
}
  
export default Dashboard