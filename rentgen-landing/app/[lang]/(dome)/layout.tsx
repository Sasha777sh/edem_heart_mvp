import React from 'react';

export default function DomeLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="bg-white text-black min-h-screen">
            {children}
        </div>
    );
}
