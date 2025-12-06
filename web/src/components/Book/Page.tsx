import React from 'react';
import ReactMarkdown from 'react-markdown';

const Page = ({ content }) => {
    return (
        <div>
            <ReactMarkdown>{content}</ReactMarkdown>
        </div>
    );
};

export default Page;
