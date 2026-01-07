"use client";

import React from "react";

type Props = {
    dict: any;
};

export default function FaqSection({ dict }: Props) {
    return (
        <section className="w-full max-w-3xl mx-auto py-12 px-6">
            <h2 className="text-3xl font-bold text-center mb-10 text-white">{dict.faq.title}</h2>

            <div className="space-y-4">
                {dict.faq.items.map((item: any, index: number) => (
                    <div
                        key={index}
                        className="group p-6 rounded-2xl border border-white/5 bg-white/5 hover:bg-white/[0.07] transition-colors"
                    >
                        <h3 className="text-lg font-bold text-gray-200 mb-2 group-hover:text-white transition-colors">
                            {item.q}
                        </h3>
                        <p className="text-gray-400 text-sm leading-relaxed" dangerouslySetInnerHTML={{ __html: item.a }}>
                        </p>
                    </div>
                ))}
            </div>
        </section>
    );
}
