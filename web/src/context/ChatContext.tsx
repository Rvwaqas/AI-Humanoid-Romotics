import React, { createContext, useState, useContext } from 'react';

const ChatContext = createContext({
  isChatOpen: false,
  toggleChat: () => {},
});

export const useChat = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  return (
    <ChatContext.Provider value={{ isChatOpen, toggleChat }}>
      {children}
    </ChatContext.Provider>
  );
};
