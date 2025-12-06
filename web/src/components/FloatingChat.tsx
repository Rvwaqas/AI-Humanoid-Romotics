import React, { useState } from 'react';
import styles from './ChatWidget.module.css';

const FloatingChat = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    const handleSendMessage = (e) => {
        e.preventDefault();
        // Handle send message logic
        setNewMessage('');
    };

    return (
        <div className={styles.chatContainer}>
            <button className={styles.chatButton} onClick={() => setIsOpen(!isOpen)}>Chat</button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.messages}>
                        {messages.map((msg, index) => (
                            <div key={index} className={styles.message}>{msg}</div>
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
