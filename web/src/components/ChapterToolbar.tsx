import React from 'react';

const ChapterToolbar = () => {
    const handlePersonalize = () => {
        // Handle personalize logic
    };

    const handleTranslate = () => {
        // Handle translate logic
    };

    return (
        <div>
            <button onClick={handlePersonalize}>Personalize</button>
            <button onClick={handleTranslate}>Translate to Urdu</button>
        </div>
    );
};

export default ChapterToolbar;
