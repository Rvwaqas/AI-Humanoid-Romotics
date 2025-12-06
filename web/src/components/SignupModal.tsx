import React, { useState } from 'react';
import styles from './SignupModal.module.css';

const SignupModal = ({ onClose }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [hardwareSpecs, setHardwareSpecs] = useState('');
    const [codingBackground, setCodingBackground] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        // Handle signup logic here
        onClose();
    };

    return (
        <div className={styles.modalBackdrop}>
            <div className={styles.modalContent}>
                <h2>Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
                    <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
                    <textarea placeholder="Hardware Specs" value={hardwareSpecs} onChange={e => setHardwareSpecs(e.target.value)} />
                    <textarea placeholder="Coding Background" value={codingBackground} onChange={e => setCodingBackground(e.target.value)} />
                    <button type="submit">Sign Up</button>
                </form>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
};

export default SignupModal;