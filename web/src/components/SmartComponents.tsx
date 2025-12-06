import React, { useState } from 'react';
import styles from './SmartComponents.module.css';

interface SmartComponentsProps {
  chapterContent: string;
  userEmail: string; // Assuming user email is available for API calls
  onPersonalize: (personalizedText: string) => void;
  onTranslate: (translatedText: string) => void;
}

const SmartComponents: React.FC<SmartComponentsProps> = ({
  chapterContent,
  userEmail,
  onPersonalize,
  onTranslate,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePersonalize = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/features/personalize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: chapterContent, user_email: userEmail }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      onPersonalize(data.personalized_text);
    } catch (e: any) {
      setError(`Personalization failed: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleTranslate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/features/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: chapterContent, user_email: userEmail }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      onTranslate(data.translated_text);
    } catch (e: any) {
      setError(`Translation failed: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.toolbar}>
      <button onClick={handlePersonalize} disabled={loading}>
        {loading ? 'Personalizing...' : 'Personalize for [User Role]'}
      </button>
      <button onClick={handleTranslate} disabled={loading}>
        {loading ? 'Translating...' : 'Translate to Urdu'}
      </button>
      {error && <p className={styles.error}>{error}</p>}
    </div>
  );
};

export default SmartComponents;
