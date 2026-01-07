"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

export default function LanguageSwitcher() {
    const pathname = usePathname();
    const isRu = pathname.startsWith("/ru");

    return (
        <div className="fixed top-6 right-6 z-50 flex items-center gap-2 px-3 py-1.5 rounded-full bg-black/50 backdrop-blur-md border border-white/10 text-xs font-medium tracking-widest">
            <Link
                href="/ru"
                className={`transition-colors ${isRu ? "text-white" : "text-gray-500 hover:text-gray-300"}`}
            >
                RU
            </Link>
            <span className="text-gray-700">|</span>
            <Link
                href="/en"
                className={`transition-colors ${!isRu ? "text-white" : "text-gray-500 hover:text-gray-300"}`}
            >
                EN
            </Link>
        </div>
    );
}
