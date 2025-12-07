import React, { useState } from 'react';
import styles from './ChatWidget.module.css';

const FloatingChat = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!newMessage.trim()) return;

        const userMessage = { text: newMessage, sender: 'user' };
        setMessages(prevMessages => [...prevMessages, userMessage]);
        setNewMessage('');

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: newMessage, context: '' }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            const botMessage = { text: data.answer, sender: 'bot' };
            setMessages(prevMessages => [...prevMessages, botMessage]);
        } catch (error) {
            console.error('Error fetching chat response:', error);
            const errorMessage = { text: 'Sorry, I am having trouble connecting to the server.', sender: 'bot' };
            setMessages(prevMessages => [...prevMessages, errorMessage]);
        }
    };

    return (
        <div className={styles.chatContainer}>
            <button className={styles.chatButton} onClick={() => setIsOpen(!isOpen)}>Chat</button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.messages}>
                        {messages.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                {msg.text}
                            </div>
                        ))}
                    </div>
                    <form onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            value={newMessage}
                            onChange={e => setNewMessage(e.target.value)}
                            placeholder="Type a message..."
                        />
                        <button type="submit">Send</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default FloatingChat;

