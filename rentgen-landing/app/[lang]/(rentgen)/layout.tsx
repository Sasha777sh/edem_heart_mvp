import React from 'react';

export default function RentgenLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="bg-black text-white min-h-screen">
            {children}
        </div>
    );
}
