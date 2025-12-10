import React from 'react';
import Root from '@theme-original/Root';
import { ChatProvider, useChat } from '../context/ChatContext';
import { AuthProvider, useAuth } from '../context/AuthContext';
import ChatWidget from '../components/ChatWidget';
import LoginModal from '../components/LoginModal';
import SignupModal from '../components/SignupModal';
import FloatingChat from '../components/FloatingChat';
import styles from '../components/FloatingChat.module.css';

function App({children}) {
  const { isChatOpen } = useChat();
  const { isLoginModalOpen, closeLoginModal, login, isSignupModalOpen, closeSignupModal } = useAuth();
  return (
    <>
      <Root>{children}</Root>
      <FloatingChat />
      {isLoginModalOpen && <LoginModal onClose={closeLoginModal} onLoginSuccess={login} />}
      {isSignupModalOpen && <SignupModal onClose={closeSignupModal} />}
    </>
  );
}

export default function RootWrapper({children}) {
  return (
    <AuthProvider>
      <ChatProvider>
        <App>{children}</App>
      </ChatProvider>
    </AuthProvider>
  );
}
