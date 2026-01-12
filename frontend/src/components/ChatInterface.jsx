import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./ChatInterface.css";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
console.log("API_BASE_URL =", API_BASE_URL);
export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [totalTokens, setTotalTokens] = useState(0);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { role: "user", content: text };
    const conversation_history = messages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE_URL}/dialogue`, {
        user_input: text,
        conversation_history,
      });

      const data = res.data;
      const assistantMsg = {
        role: "assistant",
        content: data.socratic_response,
        meta: {
          processed_input: data.processed_input,
          tokens_used: data.tokens_used,
        },
      };

      setMessages((prev) => [...prev, assistantMsg]);
      setTotalTokens((prev) => prev + (data.tokens_used || 0));
    } catch (err) {
      console.error(err);
      const detail =
        err.response?.data?.detail ||
        "Something went wrong talking to the AI. Please try again.";
      setError(detail);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setTotalTokens(0);
    setError("");
  };

  

  return (
    <div className="chat-root">
      <header className="chat-header">
        <div>
          <h1 className="chat-title">Socratic Tutor</h1>
          <p className="chat-subtitle">Guided Q&A powered by GPT.</p>
        </div>
        <button className="reset-btn" onClick={handleReset} disabled={loading}>
          Reset
        </button>
      </header>

      <main className="chat-main">
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <p>Ask me something to begin:</p>
            <ul>
              <li>“Why are plants green?”</li>
              <li>“How does gradient descent work?”</li>
              <li>“What is overfitting in ML?”</li>
            </ul>
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            className={`chat-message ${m.role === "user" ? "user" : "assistant"}`}
          >
            <div className="bubble">
              <p>{m.content}</p>
              {m.meta && (
                <span className="meta">
                  {m.meta.processed_input} · {m.meta.tokens_used} tokens
                </span>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message assistant">
            <div className="bubble typing">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {error && <div className="chat-error">{error}</div>}

        <div ref={bottomRef} />
      </main>

      <footer className="chat-footer">
        <form className="chat-input-row" onSubmit={handleSend}>
          <input
            className="chat-input"
            type="text"
            placeholder="Ask a thoughtful question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button
            className="chat-send-btn"
            type="submit"
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </form>
        <div className="chat-status">
          <span>Backend: {loading ? "Thinking..." : "Ready"}</span>
          <span> · Tokens used: {totalTokens}</span>
        </div>
      </footer>
    </div>
  );
}
