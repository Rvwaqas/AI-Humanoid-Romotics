import React, { useState, useRef, useEffect } from 'react';

export default function PhysicalAIChatbot() {
  const [question, setQuestion] = useState('');
  const [context, setContext] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // Text selection → auto-fill context
  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText && selectedText.length > 10) {
      setContext(selectedText);
      textareaRef.current?.focus();
    }
  };

  // Send to backend (Hackathon RAG endpoint)
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

  // Enter to send
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
    <div className="physical-ai-chatbot" style={{
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      width: '420px',
      height: '600px',
      background: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
      borderRadius: '20px',
      boxShadow: '0 25px 50px rgba(0,0,0,0.25)',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 10000,
      fontFamily: 'system-ui, -apple-system, sans-serif',
      overflow: 'hidden'
    }}>
      {/* Header */}
      <div style={{
        padding: '20px',
        background: 'linear-gradient(135deg, #1e40af 0%, #3b82f6 100%)',
        color: 'white',
        textAlign: 'center',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
      }}>
        <div style={{ fontSize: '24px', fontWeight: 'bold' }}>🤖 Physical AI Bot</div>
        <div style={{ fontSize: '14px', opacity: 0.9 }}>ROS2 • Gazebo • Isaac Sim • VLA</div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        padding: '20px',
        overflowY: 'auto',
        background: 'rgba(255,255,255,0.95)',
        backdropFilter: 'blur(10px)'
      }}>
        {messages.length === 0 ? (
          <div style={{
            textAlign: 'center',
            color: '#64748b',
            padding: '40px 20px',
            fontSize: '16px'
          }}>
            💡 <strong>Select text</strong> on any page or <br/>
            ask about Physical AI, ROS2, Gazebo, Isaac Sim<br/><br/>
            <small>Powered by OpenAI Agents + Qdrant RAG</small>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} style={{
              marginBottom: '16px',
              padding: '16px 20px',
              borderRadius: '18px',
              maxWidth: '85%',
              boxShadow: msg.role === 'user' 
                ? '0 4px 12px rgba(59,130,246,0.3)' 
                : '0 4px 12px rgba(0,0,0,0.1)',
              background: msg.role === 'user' 
                ? 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)' 
                : '#f8fafc',
              color: msg.role === 'user' ? 'white' : '#1e293b',
              marginLeft: msg.role === 'ai' ? '15%' : 'auto',
              alignSelf: msg.role === 'ai' ? 'flex-start' : 'flex-end'
            }}>
              <div style={{ fontWeight: '600', marginBottom: '4px' }}>
                {msg.role === 'user' ? 'You' : 'Physical AI Bot'}
              </div>
              <div style={{ lineHeight: '1.5', whiteSpace: 'pre-wrap' }}>
                {msg.content}
              </div>
              {msg.sources && msg.sources.length > 0 && (
                <div style={{
                  marginTop: '8px',
                  padding: '8px',
                  background: 'rgba(59,130,246,0.1)',
                  borderRadius: '12px',
                  fontSize: '12px'
                }}>
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

      {/* Input */}
      <div style={{
        padding: '20px',
        borderTop: '1px solid rgba(255,255,255,0.2)',
        background: 'rgba(255,255,255,0.95)',
        display: 'flex',
        flexDirection: 'column',
        gap: '12px'
      }}>
        <textarea
          ref={textareaRef}
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="📖 Select text from book (auto-fills) or paste here..."
          rows={2}
          style={{
            width: '100%',
            padding: '12px 16px',
            border: '2px solid #e2e8f0',
            borderRadius: '12px',
            resize: 'none',
            fontSize: '14px',
            fontFamily: 'inherit',
            background: 'white'
          }}
          onKeyPress={handleKeyPress}
        />
        <div style={{ display: 'flex', gap: '12px' }}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask about ROS2, Gazebo, Isaac Sim..."
            onKeyPress={handleKeyPress}
            style={{
              flex: 1,
              padding: '14px 18px',
              border: '2px solid #e2e8f0',
              borderRadius: '12px',
              fontSize: '14px',
              fontFamily: 'inherit'
            }}
          />
          <button
            onClick={sendMessage}
            disabled={loading || (!question.trim() && !context.trim())}
            style={{
              padding: '14px 24px',
              background: loading 
                ? '#94a3b8' 
                : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              minWidth: '80px'
            }}
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
