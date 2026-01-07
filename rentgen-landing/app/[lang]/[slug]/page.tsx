import React from "react";
import { notFound } from "next/navigation";
import { seoPages } from "../../lib/seoPages";
import ComparisonCalculator from "../../components/ComparisonCalculator";
import TelegramLoginButton from "../../components/TelegramLoginButton";
import FaqSection from "../../components/FaqSection";
import StickyCTA from "../../components/StickyCTA";
import LanguageSwitcher from "../../components/LanguageSwitcher";
import { generatePageContent } from "../../lib/geminiContentGenerator";

// Force static generation for these 50 pages if possible, or use dynamic
export async function generateStaticParams() {
    return seoPages.flatMap((page) => [
        { lang: "ru", slug: page.slug },
        { lang: "en", slug: page.slug }
    ]);
}

const dictionaries = {
    en: () => import("../../dictionaries/en.json").then((module) => module.default),
    ru: () => import("../../dictionaries/ru.json").then((module) => module.default),
    es: () => import("../../dictionaries/es.json").then((module) => module.default),
    pt: () => import("../../dictionaries/pt.json").then((module) => module.default),
};

export async function generateMetadata({ params }: { params: Promise<{ lang: "en" | "ru", slug: string }> }) {
    const { lang, slug } = await params;
    const pageData = seoPages.find((p) => p.slug === slug);
    if (!pageData) return {};

    return {
        title: pageData.title,
        description: pageData.desc,
        alternates: {
            canonical: `https://rentgen.chatedem.com/${lang}/${slug}`,
        }
    };
}

// Enable ISR with 24-hour revalidation
export const revalidate = 86400; // 24 hours

export default async function SeoPage({ params }: { params: Promise<{ lang: "en" | "ru" | "es" | "pt", slug: string }> }) {
    const { lang, slug } = await params;
    const dict = await dictionaries[lang]();
    const pageData = seoPages.find((p) => p.slug === slug);

    if (!pageData) {
        notFound();
    }

    // Generate AI content (cached for 24h via revalidate)
    let aiContent = '';
    try {
        aiContent = await generatePageContent(slug, pageData);
    } catch (error) {
        console.error('AI content generation failed:', error);
        // Fallback to description if AI fails
        aiContent = pageData.desc;
    }

    // BOT SELECTION LOGIC
    // 1. RENTGEN (Contracts) -> @DogovorCheckBot (External)
    // 2. EVERYTHING ELSE (Red Flag, Dreams, Med, Paper) -> @RedFlagScannerBot (Our Universal Bot)

    // Explicitly define Rentgen Categories (Legal/Financial focus)
    const rentgenCategories = [
        "Contracts", "Work", "E-com", "Rent", "Services", // New Clusters
        "Аренда", "Сделки", "Риски", "Финансы", "Бизнес", "Работа", "IP", "Оферты", "Подряд", "Услуги", "EdTech", "IT", // Legacy
        "Expat Dubai", "Expat Bali", "Expat Thai", "Expat Cyprus", "Expat Turkey", "Expat Georgia", "Expat Serbia", "Expat LatAm", "Expat General", "Теория", "Психология", "Решения", "Карьера" // Legacy High-Level
    ];

    const isRentgen = rentgenCategories.includes(pageData.category);

    let botName = "DogovorCheckBot";
    let startParam = "website_login";

    if (!isRentgen) {
        // IT IS A NEW NICHE (Universal Bot)
        // Ensure you updated the Universal Bot Username below (e.g. RedFlagScannerBot)
        botName = "RedFlagScannerBot"; // User MUST replace this with actual username if different

        if (pageData.category === "Red Flag") startParam = "red_flag";
        else if (pageData.category === "Dreams") startParam = "dream";
        else if (pageData.category === "Health") startParam = "med";
        else if (pageData.category === "Paper") startParam = "paper";
        else startParam = "red_flag"; // Default
    } else {
        // RENTGEN SPECIFIC
        botName = "DogovorCheckBot";
        startParam = "website_login";
    }

    return (
        <main className="min-h-screen bg-black text-white relative overflow-hidden selection:bg-white selection:text-black">

            {/* GLOBAL UI ELEMENTS */}
            <LanguageSwitcher />
            <StickyCTA text={dict.sticky_cta} />

            {/* Background Gradients */}
            <div className="fixed inset-0 z-0 pointer-events-none">
                <div className="absolute top-[-10%] left-[20%] w-[500px] h-[500px] bg-blue-900/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
                <div className="absolute bottom-[-10%] right-[20%] w-[600px] h-[600px] bg-purple-900/10 rounded-full blur-[120px] mix-blend-screen"></div>
            </div>

            <div className="relative z-10 max-w-4xl mx-auto px-6 py-20 flex flex-col items-center gap-16">

                {/* 1. HERO CONTENT FOR SEO */}
                <section className="text-center space-y-8 animate-fade-in-up">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-md text-xs font-medium text-gray-400 tracking-wider uppercase mb-4">
                        <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                        {pageData.category || "Risk Audit"}
                    </div>

                    <h1 className="text-4xl md:text-6xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-gray-400 leading-[1.1]">
                        {pageData.h1}
                    </h1>

                    <p className="max-w-2xl mx-auto text-xl text-gray-400 leading-relaxed font-light">
                        {pageData.desc}
                        <br /><br />
                        <span className="text-white">Не подписывайте, пока не проверите.</span> Загрузите текст в Rentgen и найдите скрытые условия за 5 секунд.
                    </p>

                    <div className="flex flex-col md:flex-row gap-4 justify-center pt-8">
                        <TelegramLoginButton dict={dict} botName={botName} startParam={startParam} />
                    </div>
                </section>

                {/* 2. DEMO REUSE */}
                <div className="w-full scale-90 md:scale-100">
                    <ComparisonCalculator dict={dict} />
                </div>

                {/* 3. AI-GENERATED UNIQUE CONTENT */}
                <section className="prose prose-invert prose-lg text-gray-400 max-w-none w-full whitespace-pre-line">
                    {aiContent}
                </section>

                {/* 4. FAQ */}
                <FaqSection dict={dict} />

                <footer className="w-full text-center text-gray-600 text-sm py-10">
                    <p>{dict.footer}</p>
                </footer>

            </div>
        </main>
    );
}
