import React from 'react';
import { useAuth } from '../../context/AuthContext';

export default function AuthNavbarItem() {
  const { isLoggedIn, openLoginModal, openSignupModal, logout } = useAuth();

  return (
    <>
      {isLoggedIn ? (
        <button className="navbar__item navbar__link" onClick={logout}>
          Logout
        </button>
      ) : (
        <>
          <button className="navbar__item navbar__link" onClick={openLoginModal}>
            Login
          </button>
          <button className="navbar__item navbar__link" onClick={openSignupModal}>
            Sign Up
          </button>
        </>
      )}
    </>
  );
}
