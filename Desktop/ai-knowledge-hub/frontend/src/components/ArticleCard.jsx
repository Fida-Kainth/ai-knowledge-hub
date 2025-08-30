import React from "react";

const ArticleCard = ({ title, summary, author, onClick }) => {
  return (
    <div className="article-card" onClick={onClick}>
      <h3>{title}</h3>
      <p>{summary}</p>
      <small>By {author}</small>
    </div>
  );
};

export default ArticleCard;
