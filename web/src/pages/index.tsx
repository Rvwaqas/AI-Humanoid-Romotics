import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import Book from '../components/Book/Book';
import FloatingChat from '../components/FloatingChat';

const bookFiles = [
    '/docs/module-1-ros2/intro.md',
    '/docs/module-2-gazebo/sim.md',
    '/docs/module-3-isaac/brain.md',
    '/docs/module-3-isaac/hardware.md',
    '/docs/module-4-vla/capstone.md'
];

export default function Home() {
    const [pages, setPages] = useState([]);

    useEffect(() => {
        const fetchPages = async () => {
            const fetchedPages = await Promise.all(
                bookFiles.map(file => fetch(file).then(res => res.text()))
            );
            setPages(fetchedPages);
        };

        fetchPages();
    }, []);

    return (
        <Layout>
            <main>
                <Book pages={pages} />
                <FloatingChat />
            </main>
        </Layout>
    );
}
