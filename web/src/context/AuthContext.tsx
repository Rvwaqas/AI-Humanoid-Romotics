import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext({
  isLoginModalOpen: false,
  isSignupModalOpen: false,
  isLoggedIn: false,
  token: null,
  openLoginModal: () => {},
  closeLoginModal: () => {},
  openSignupModal: () => {},
  closeSignupModal: () => {},
  login: (token) => {},
  logout: () => {},
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const [isSignupModalOpen, setIsSignupModalOpen] = useState(false);
  const [token, setToken] = useState(null);

  const openLoginModal = () => setIsLoginModalOpen(true);
  const closeLoginModal = () => setIsLoginModalOpen(false);
  const openSignupModal = () => setIsSignupModalOpen(true);
  const closeSignupModal = () => setIsSignupModalOpen(false);

  const login = (token) => {
    setToken(token);
  };

  const logout = () => {
    setToken(null);
  };

  const isLoggedIn = !!token;

  return (
    <AuthContext.Provider
      value={{
        isLoginModalOpen,
        isSignupModalOpen,
        isLoggedIn,
        token,
        openLoginModal,
        closeLoginModal,
        openSignupModal,
        closeSignupModal,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
