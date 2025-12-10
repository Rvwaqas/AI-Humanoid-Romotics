import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css';

export default function PhysicalAIChatbot({ onClose }) {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText && selectedText.length > 10) {
      setContext(selectedText);
      textareaRef.current?.focus();
    }
  };

  const sendMessage = async () => {
    if (!question.trim() && !context.trim()) return;

    const userMessage = { 
      role: 'user', 
      content: question || 'Explain this selected text:', 
      context 
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question: question || 'Explain this Physical AI concept:', 
          context 
        })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: data.answer || 'AI thinking...', 
        sources: data.sources || []
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: '❌ Backend not running? Start: cd backend && uvicorn main:app --reload',
        error: true 
      }]);
    }

    setQuestion('');
    setLoading(false);
    scrollToBottom();
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    return () => document.removeEventListener('mouseup', handleTextSelection);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className={styles.chatbot}>
      <div className={styles.header}>
        <div>
            <div className={styles.headerTitle}>🤖 Physical AI Bot</div>
            <div className={styles.headerSubtitle}>ROS2 • Gazebo • Isaac Sim • VLA</div>
        </div>
        <button onClick={onClose} className={styles.closeButton}>×</button>
      </div>

      <div className={styles.messages}>
        {messages.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#64748b', padding: '40px 20px', fontSize: '16px' }}>
            💡 <strong>Select text</strong> on any page or <br/>
            ask about Physical AI, ROS2, Gazebo, Isaac Sim<br/><br/>
            <small>Powered by OpenAI Agents + Qdrant RAG</small>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.aiMessage}`}>
              <div className={styles.messageHeader}>
                {msg.role === 'user' ? 'You' : 'Physical AI Bot'}
              </div>
              <div className={styles.messageContent}>
                {msg.content}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div style={{ marginTop: '8px', padding: '8px', background: 'rgba(59,130,246,0.1)', borderRadius: '12px', fontSize: '12px' }}>
                  📚 {msg.sources.join(' • ')}
                </div>
              )}
              {msg.error && (
                <div style={{ fontSize: '12px', color: '#ef4444', marginTop: '4px' }}>
                  🔧 Check backend server
                </div>
              )}
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputArea}>
        <textarea
          ref={textareaRef}
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="📖 Select text from book (auto-fills) or paste here..."
          rows={2}
          className={styles.contextTextarea}
          onKeyPress={handleKeyPress}
        />
        <div className={styles.inputWrapper}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about ROS2, Gazebo, Isaac Sim..."
            onKeyPress={handleKeyPress}
            className={styles.questionInput}
          />
          <button
            onClick={sendMessage}
            disabled={loading || (!question.trim() && !context.trim())}
            className={styles.sendButton}
          >
            {loading ? '🤔' : '🚀'}
          </button>
        </div>
        <div style={{ fontSize: '12px', color: '#64748b', textAlign: 'center' }}>
          💡 Select book text → Auto context → AI explains (Hackathon Demo!)
        </div>
      </div>
    </div>
  );
}
