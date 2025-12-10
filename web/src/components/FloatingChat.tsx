import React, { useState } from 'react';
import ChatWidget from './ChatWidget';
import styles from './FloatingChat.module.css';
import { useAuth } from '../context/AuthContext';

const FloatingChat = () => {
    const [isOpen, setIsOpen] = useState(false);
    const { isLoggedIn, openLoginModal, openSignupModal, logout } = useAuth();

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className={styles.floatingChatContainer}>
            {!isLoggedIn ? (
                <>
                    <button className={styles.authButton} onClick={openLoginModal}>
                        Login
                    </button>
                    <button className={styles.authButton} onClick={openSignupModal}>
                        Sign Up
                    </button>
                </>
            ) : (
                <button className={styles.authButton} onClick={logout}>
                    Logout
                </button>
            )}
            <button className={styles.chatToggleButton} onClick={toggleChat}>
                {isOpen ? 'Close Chat' : 'Open Chat'}
            </button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <ChatWidget />
                </div>
            )}
        </div>
    );
};

export default FloatingChat;