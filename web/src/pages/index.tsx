import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import Layout from '@theme/Layout';
import Book from '../components/Book/Book';
import FloatingChat from '../components/FloatingChat';
import CoverPage from '../components/CoverPage'; // Import CoverPage

const bookFiles = [
    '/docs/module-1-ros2/intro.md',
    '/docs/module-2-gazebo/sim.md',
    '/docs/module-3-isaac/brain.md',
    '/docs/module-3-isaac/hardware.md',
    '/docs/module-4-vla/capstone.md'
];

export default function Home() {
    const [pages, setPages] = useState([]);
    const [showCover, setShowCover] = useState(true);
    const history = useHistory(); // Initialize useHistory

    useEffect(() => {
        const fetchPages = async () => {
            const fetchedPages = await Promise.all(
                bookFiles.map(file => fetch(file).then(res => res.text()))
            );
            setPages(fetchedPages);
        };

        fetchPages();
    }, []);

    const handleStartReading = () => {
        setShowCover(false);
        history.push('/AI-Humanoid-Robotics/docs/module-1-ros2/intro'); // Navigate to the first module
    };

    return (
        <Layout> {/* Removed title and description props from Layout */}
            {showCover ? (
                <CoverPage onStartReading={handleStartReading} />
            ) : (
                <main>
                    <Book pages={pages} />
                </main>
            )}
            <FloatingChat />
        </Layout>
    );
}
