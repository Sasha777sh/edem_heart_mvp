"use client";

import React, { useEffect, useState } from "react";

type Props = {
    text: string;
};

export default function StickyCTA({ text }: Props) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            // Show button after scrolling down 100px
            if (window.scrollY > 100) {
                setIsVisible(true);
            } else {
                setIsVisible(false);
            }
        };

        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <div
            className={`fixed bottom-6 left-6 right-6 z-50 transition-all duration-500 transform md:hidden ${isVisible ? "translate-y-0 opacity-100" : "translate-y-20 opacity-0"
                }`}
        >
            <a
                href="https://t.me/DogovorCheckBot?start=website_sticky"
                className="block w-full py-4 bg-[#2AABEE] text-white text-center font-bold text-lg rounded-2xl shadow-[0_10px_30px_rgba(42,171,238,0.4)] overflow-hidden relative"
            >
                <div className="absolute inset-0 bg-white/20 translate-y-full animate-[shimmer_3s_infinite]"></div>
                <span className="relative z-10">{text}</span>
            </a>
        </div>
    );
}
