import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="page home">
      <h1>Welcome to AI Knowledge Hub</h1>
      <p>Your one-stop platform for AI-powered insights and curated articles.</p>
      <div className="home__actions">
        <Link to="/articles" className="btn">Browse Articles</Link>
        <Link to="/chat" className="btn btn-primary">Chat with AI</Link>
      </div>
    </div>
  );
};

export default Home;
