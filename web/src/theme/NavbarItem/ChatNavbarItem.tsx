import React from 'react';
import { useChat } from '../../context/ChatContext';
import clsx from 'clsx';
// Assuming a styles file for custom navbar items, you might need to create this
// import styles from './styles.module.css';

export default function ChatNavbarItem() {
  const { isChatOpen, toggleChat } = useChat();

  return (
    <button
      className={clsx(
        'navbar__item',
        'navbar__link',
        // styles.chatNavbarItem, // Apply custom styles if they exist
        // isChatOpen && styles.chatNavbarItemActive, // Apply active state styles
      )}
      onClick={toggleChat}>
      Chat
    </button>
  );
}
