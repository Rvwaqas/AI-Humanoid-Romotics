import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css';

interface ChatMessage {
  type: 'user' | 'bot';
  text: string;
  sources?: { file_path: string; section_title: string; score: number }[];
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage: ChatMessage = { type: 'user', text: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setQuery('');
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/chat/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const botMessage: ChatMessage = {
        type: 'bot',
        text: data.answer,
        sources: data.source_sections,
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (e: any) {
      setError(`Chat failed: ${e.message}`);
      const errorMessage: ChatMessage = { type: 'bot', text: `Error: ${e.message}` };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={clsx(styles.chatWidget, { [styles.open]: isOpen })}>
      <button className={styles.toggleButton} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? '-' : 'Chat'}
      </button>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div key={index} className={clsx(styles.message, styles[msg.type])}>
                <p>{msg.text}</p>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((src, srcIndex) => (
                        <li key={srcIndex}>
                          {src.section_title} (Score: {src.score.toFixed(2)}) in {src.file_path}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
            {loading && <div className={styles.loading}>Bot is typing...</div>}
            {error && <div className={styles.error}>Error: {error}</div>}
            <div ref={messagesEndRef} />
          </div>
          <form onSubmit={handleSendMessage} className={styles.inputContainer}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about the book..."
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
