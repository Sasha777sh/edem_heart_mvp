'use client';
import React, { useState, useRef, useEffect } from 'react';

export default function ComparisonSlider() {
    const [sliderPosition, setSliderPosition] = useState(50);
    const [isDragging, setIsDragging] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const handleMove = (event: React.MouseEvent<HTMLDivElement> | React.TouchEvent<HTMLDivElement>) => {
        if (!containerRef.current) return;

        let clientX;
        if ('touches' in event) {
            clientX = event.touches[0].clientX;
        } else {
            clientX = event.clientX;
        }

        const rect = containerRef.current.getBoundingClientRect();
        const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
        const percentage = (x / rect.width) * 100;

        setSliderPosition(percentage);
    };

    const handleMouseDown = () => setIsDragging(true);
    const handleMouseUp = () => setIsDragging(false);

    useEffect(() => {
        const handleGlobalMouseUp = () => setIsDragging(false);
        window.addEventListener('mouseup', handleGlobalMouseUp);
        return () => window.removeEventListener('mouseup', handleGlobalMouseUp);
    }, []);

    return (
        <div className="w-full max-w-6xl mx-auto py-24 px-6">
            <div className="text-center mb-12">
                <h2 className="text-3xl md:text-5xl font-black uppercase tracking-tighter mb-4">Past vs Future</h2>
                <p className="text-gray-500 font-mono tracking-widest text-xs uppercase">Why we don't use bricks</p>
            </div>

            <div
                ref={containerRef}
                className="relative w-full aspect-[16/9] md:aspect-[21/9] rounded-3xl overflow-hidden cursor-ew-resize select-none shadow-2xl"
                onMouseMove={handleMove}
                onTouchMove={handleMove}
                onClick={handleMove}
            >
                {/* IMAGE 1: DIRTY (Traditional) - The "Background" */}
                <img
                    src="/images/dome/construction_dirty.png"
                    alt="Traditional Construction"
                    className="absolute inset-0 w-full h-full object-cover"
                />
                <div className="absolute top-8 left-8 bg-black/80 text-white px-4 py-2 rounded-lg font-bold uppercase tracking-widest text-sm backdrop-blur-md">
                    The Old Way (12 Months)
                </div>

                {/* IMAGE 2: CLEAN (Dome) - Clipped Overlay */}
                <div
                    className="absolute inset-0 overflow-hidden"
                    style={{ clipPath: `polygon(${sliderPosition}% 0, 100% 0, 100% 100%, ${sliderPosition}% 100%)` }}
                >
                    <img
                        src="/images/dome/tech.png"
                        alt="Airform Technology"
                        className="absolute inset-0 w-full h-full object-cover"
                    />
                    <div className="absolute top-8 right-8 bg-white/80 text-black px-4 py-2 rounded-lg font-bold uppercase tracking-widest text-sm backdrop-blur-md">
                        The Future (30 Days)
                    </div>
                </div>

                {/* SLIDER HANDLE */}
                <div
                    className="absolute inset-y-0 w-1 bg-white cursor-ew-resize z-20 shadow-[0_0_20px_rgba(0,0,0,0.5)]"
                    style={{ left: `${sliderPosition}%` }}
                >
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-xl">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6 text-black">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" transform="rotate(-90 12 12)" />
                        </svg>
                    </div>
                </div>

            </div>

            <div className="flex justify-between mt-4 text-xs font-mono uppercase text-gray-400">
                <span>Mud, Waste, Delays</span>
                <span>Speed, Precision, Ecology</span>
            </div>
        </div>
    );
}
