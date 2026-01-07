"use client";

import React from "react";

type Props = {
    dict: any;
};

export default function ComparisonCalculator({ dict }: Props) {
    return (
        <div className="w-full max-w-4xl mx-auto p-6 animate-fade-in-up">
            <h2 className="text-3xl font-bold text-center mb-12 text-white">{dict.calculator.title}</h2>

            <div className="grid md:grid-cols-2 gap-8 items-center">

                {/* LAWYER CARD (Left) */}
                <div className="relative group p-8 rounded-3xl border border-white/5 bg-white/5 backdrop-blur-sm grayscale opacity-70 hover:opacity-100 hover:grayscale-0 transition-all duration-500">
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 text-4xl bg-[#0A0A0A] p-2 rounded-full border border-white/10">
                        {dict.calculator.lawyer.icon}
                    </div>
                    <div className="text-center mt-12 space-y-4">
                        <h3 className="text-xl font-bold text-gray-400 tracking-widest">{dict.calculator.lawyer.title}</h3>

                        <div className="py-2 border-b border-white/5">
                            <p className="text-xs text-gray-500 uppercase">Time</p>
                            <div className="text-2xl font-mono text-gray-300">{dict.calculator.lawyer.time}</div>
                        </div>

                        <div className="py-2 border-b border-white/5">
                            <p className="text-xs text-gray-500 uppercase">Cost</p>
                            <div className="text-2xl font-mono text-gray-300">{dict.calculator.lawyer.cost}</div>
                        </div>

                        <div className="py-2">
                            <p className="text-xs text-gray-500 uppercase">Output</p>
                            <div className="text-2xl font-mono text-gray-300">{dict.calculator.lawyer.result}</div>
                        </div>
                    </div>
                </div>

                {/* RENTGEN CARD (Right - Winner) */}
                <div className="relative p-8 rounded-3xl border border-green-500/30 bg-gradient-to-br from-green-900/10 to-blue-900/10 shadow-[0_0_50px_-10px_rgba(34,197,94,0.2)] transform hover:scale-105 transition-all duration-300">
                    <div className="absolute -inset-[1px] bg-gradient-to-r from-green-500 via-blue-500 to-green-500 rounded-3xl opacity-30 blur-sm animate-pulse-slow"></div>

                    <div className="relative z-10">
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 text-4xl bg-[#0A0A0A] p-2 rounded-full border border-green-500/50 shadow-[0_0_20px_rgba(34,197,94,0.5)]">
                            {dict.calculator.rentgen.icon}
                        </div>

                        <div className="text-center mt-12 space-y-4">
                            <h3 className="text-xl font-bold text-white tracking-widest bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-400">
                                {dict.calculator.rentgen.title}
                            </h3>

                            <div className="py-2 border-b border-white/10">
                                <p className="text-xs text-green-400/70 uppercase">Time</p>
                                <div className="text-3xl font-bold font-mono text-white">{dict.calculator.rentgen.time}</div>
                            </div>

                            <div className="py-2 border-b border-white/10">
                                <p className="text-xs text-green-400/70 uppercase">Cost</p>
                                <div className="text-3xl font-bold font-mono text-green-400">{dict.calculator.rentgen.cost}</div>
                            </div>

                            <div className="py-2">
                                <p className="text-xs text-green-400/70 uppercase">Output</p>
                                <div className="text-2xl font-bold font-mono text-white">{dict.calculator.rentgen.result}</div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}
