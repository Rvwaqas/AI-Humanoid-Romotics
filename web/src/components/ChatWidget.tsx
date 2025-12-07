// web/src/components/BookChatbot.jsx - Copy to your Docusaurus
import React, { useState, useRef, useEffect } from 'react';

export default function BookChatbot() {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);

  const sendToBackend = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    const userMsg = { role: 'user', content: question, context };
    
    setMessages(prev => [...prev, userMsg]);
    
    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, context })
      });
      
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', content: data.answer, sources: data.sources }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'ai', content: '❌ Backend error. Run: cd backend && uv run uvicorn main:app --reload' }]);
    }
    
    setQuestion('');
    setContext('');
    setLoading(false);
  };

  const handleSelection = () => {
    const text = window.getSelection().toString();
    if (text) {
      setContext(text);
      textareaRef.current.focus();
    }
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  return (
    <div style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '400px',
      height: '500px',
      background: 'white',
      borderRadius: '15px',
      boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 1000,
      fontFamily: 'system-ui'
    }}>
      {/* Header */}
      <div style={{
        padding: '20px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        borderRadius: '15px 15px 0 0',
        textAlign: 'center'
      }}>
        <h3>🤖 Book AI Assistant</h3>
        <small>Physical AI & RAG</small>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        padding: '15px',
        overflowY: 'auto',
        background: '#f8f9fa'
      }}>
        {messages.length === 0 ? (
          <div style={{textAlign: 'center', color: '#666', fontSize: '14px'}}>
            💡 Select text on page or ask about book content<br/>
            <small>Qdrant → Gemini → Answer</small>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} style={{
              marginBottom: '15px',
              padding: '12px',
              borderRadius: '12px',
              background: msg.role === 'user' ? '#007bff' : '#e9ecef',
              color: msg.role === 'user' ? 'white' : 'black'
            }}>
              <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong> {msg.content}
              {msg.sources && msg.sources.length > 0 && (
                <div style={{fontSize: '12px', marginTop: '5px'}}>
                  📚 Sources: {msg.sources.join(', ')}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Input */}
      <div style={{ padding: '15px', borderTop: '1px solid #eee' }}>
        <textarea
          ref={textareaRef}
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="📖 Selected text appears here (optional)"
          rows={2}
          style={{
            width: '100%',
            padding: '8px',
            border: '1px solid #ddd',
            borderRadius: '8px',
            marginBottom: '8px',
            resize: 'none',
            fontSize: '14px'
          }}
        />
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about book..."
            onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendToBackend())}
            style={{
              flex: 1,
              padding: '10px',
              border: '1px solid #ddd',
              borderRadius: '8px',
              fontSize: '14px'
            }}
          />
          <button
            onClick={sendToBackend}
            disabled={loading || !question.trim()}
            style={{
              padding: '10px 20px',
              background: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? '🤔' : '🚀'}
          </button>
        </div>
      </div>
    </div>
  );
}
