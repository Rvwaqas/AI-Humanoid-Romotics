import React from 'react';
import styles from './CoverPage.module.css';

interface CoverPageProps {
  onStartReading: () => void;
}

const CoverPage: React.FC<CoverPageProps> = ({ onStartReading }) => {
  return (
    <div className={styles.coverPageContainer}>
      <h1 className={styles.title}>AI-Humanoid-Robotics: The Interactive Guide</h1>
      <p className={styles.subtitle}>Explore the future of robotics and artificial intelligence</p>
      <button className={styles.startButton} onClick={onStartReading}>Start Reading</button>
    </div>
  );
};

export default CoverPage;
