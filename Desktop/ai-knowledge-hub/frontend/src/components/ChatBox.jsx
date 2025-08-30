import React, { useState } from "react";
import Loader from "./Loader";
import api from "../utils/api";

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", content: query };
    setMessages([...messages, userMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await api.post("/ai/query/", { query });
      const aiMessage = { role: "assistant", content: res.data.answer };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "⚠️ Error fetching AI response" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbox">
      <div className="chatbox__messages">
        {messages.map((msg, i) => (
          <div key={i} className={`chatbox__message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && <Loader />}
      </div>
      <div className="chatbox__input">
        <input
          type="text"
          placeholder="Ask AI..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
