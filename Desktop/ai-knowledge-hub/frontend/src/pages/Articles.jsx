import React, { useEffect, useState } from "react";
import api from "../utils/api";
import ArticleCard from "../components/ArticleCard";
import Loader from "../components/Loader";

const Articles = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const res = await api.get("/articles/");
        setArticles(res.data);
      } catch {
        setArticles([]);
      } finally {
        setLoading(false);
      }
    };
    fetchArticles();
  }, []);

  if (loading) return <Loader />;

  return (
    <div className="page articles">
      <h2>Articles</h2>
      <div className="articles__list">
        {articles.length > 0 ? (
          articles.map((article) => (
            <ArticleCard
              key={article.id}
              title={article.title}
              summary={article.summary}
              author={article.author}
            />
          ))
        ) : (
          <p>No articles available.</p>
        )}
      </div>
    </div>
  );
};

export default Articles;
