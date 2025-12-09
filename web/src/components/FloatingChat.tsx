import React, { useState } from 'react';
import ChatWidget from './ChatWidget'; // Import the actual ChatWidget
import styles from './FloatingChat.module.css'; // Assuming a separate CSS module for FloatingChat

const FloatingChat = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className={styles.floatingChatContainer}>
            <button className={styles.chatToggleButton} onClick={toggleChat}>
                {isOpen ? 'Close Chat' : 'Open Chat'}
            </button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <ChatWidget /> {/* Render the actual ChatWidget here */}
                </div>
            )}
        </div>
    );
};

export default FloatingChat;