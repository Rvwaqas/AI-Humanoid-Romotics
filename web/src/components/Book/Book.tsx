import React, { useState } from 'react';
import styles from './styles.module.css';
import Page from './Page';
import ChapterToolbar from '../ChapterToolbar';

const Book = ({ pages }) => {
    const [currentPage, setCurrentPage] = useState(0);

    const handleNextPage = () => {
        if (currentPage < pages.length - 2) {
            setCurrentPage(currentPage + 2);
        }
    };

    const handlePrevPage = () => {
        if (currentPage > 0) {
            setCurrentPage(currentPage - 2);
        }
    };

    return (
        <div className={styles.book}>
            <ChapterToolbar />
            <div className={styles.pages}>
                <div className={styles.leftPage}>
                    {currentPage > 0 && <Page content={pages[currentPage - 1]} />}
                </div>
                <div className={styles.rightPage}>
                    {currentPage < pages.length && <Page content={pages[currentPage]} />}
                </div>
            </div>
            <div className={styles.navigation}>
                <button onClick={handlePrevPage} disabled={currentPage === 0}>Previous</button>
                <button onClick={handleNextPage} disabled={currentPage >= pages.length - 2}>Next</button>
            </div>
        </div>
    );
};

export default Book;
