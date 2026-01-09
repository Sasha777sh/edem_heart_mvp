"use client";

import React from "react";

type Props = {
    dict: any;
    botName?: string;
    startParam?: string;
    customText?: string;
    customSub?: string;
};

export default function TelegramLoginButton({ dict, botName = "DogovorCheckBot", startParam = "website_login", customText, customSub }: Props) {
    return (
        <a
            href={`https://t.me/${botName}?start=${startParam}`}
            target="_blank"
            rel="noopener noreferrer"
            className="group relative inline-flex items-center gap-3 px-8 py-4 bg-[#2AABEE] text-white font-bold rounded-full overflow-hidden transition-all hover:scale-105 hover:shadow-[0_0_30px_rgba(42,171,238,0.5)] active:scale-95"
        >
            <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>

            {/* Telegram SVG Icon */}
            <svg className="w-6 h-6 fill-current relative z-10" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 11.944 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.638z" />
            </svg>

            <div className="flex flex-col items-start leading-none relative z-10">
                <span className="text-sm">{customText || dict.login.button}</span>
                <span className="text-[10px] opacity-80 font-normal mt-0.5">{customSub || dict.login.sub}</span>
            </div>
        </a>
    );
}
