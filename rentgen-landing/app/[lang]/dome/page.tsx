import React from "react";
import LanguageSwitcher from "../../components/LanguageSwitcher";
import StickyCTA from "../../components/StickyCTA";
import TelegramLoginButton from "../../components/TelegramLoginButton";

export default async function DomePage({ params }: { params: Promise<{ lang: "en" | "ru" | "es" | "pt" }> }) {
    const { lang } = await params;

    // Hardcoded Content for MVP (Replace with Locale later)
    const content = {
        ru: {
            title: "DOME LUXE GLOBAL",
            subtitle: "Архитектура Будущего. Технология Airform.",
            hero: {
                h1: "Дом по цене автомобиля.",
                p: "Монолитный купол за 30 дней. Вечный, сейсмостойкий, энергоэффективный.",
                btn: "Получить Инвест-План"
            },
            stats: [
                { val: "30 дней", label: "Срок стройки" },
                { val: "$25,000", label: "Стоимость (Shell)" },
                { val: "20%", label: "ROI (Аренда)" }
            ],
            tech: {
                title: "Технология Airform",
                desc: "Мы не строим опалубку из дерева. Мы надуваем форму воздухом, напыляем 10см пенобетона и получаем идеальную сферу без швов."
            }
        },
        en: {
            title: "DOME LUXE GLOBAL",
            subtitle: "Future Architecture. Airform Technology.",
            hero: {
                h1: "A House for the Price of a Car.",
                p: "Monolithic dome in 30 days. Eternal, seismic-proof, energy-efficient.",
                btn: "Get Investment Plan"
            },
            stats: [
                { val: "30 Days", label: "Build Time" },
                { val: "$25,000", label: "Cost (Shell)" },
                { val: "20%", label: "ROI (Rental)" }
            ],
            tech: {
                title: "Airform Technology",
                desc: "We don't build wooden forms. We inflate the shape with air, spray 10cm of aircrete, and get a perfect seamless sphere."
            }
        }
    };

    const t = content[lang] || content.en;

    return (
        <main className="min-h-screen bg-[#F0F0F0] text-black font-sans selection:bg-black selection:text-white">

            {/* HEADER */}
            <nav className="fixed top-0 w-full z-50 px-6 py-4 flex justify-between items-center bg-[#F0F0F0]/80 backdrop-blur-md">
                <div className="text-xl font-bold tracking-widest uppercase border-2 border-black px-2">{t.title}</div>
                <LanguageSwitcher />
            </nav>

            {/* HERO */}
            <section className="relative pt-32 pb-20 px-6 min-h-[80vh] flex flex-col justify-center items-center text-center">
                {/* Abstract Circle Background */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border-[1px] border-black/10 rounded-full z-0"></div>
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border-[1px] border-black/20 rounded-full z-0"></div>

                <div className="relative z-10 max-w-4xl space-y-8">
                    <p className="text-sm font-mono uppercase tracking-[0.3em] text-gray-500">{t.subtitle}</p>
                    <h1 className="text-6xl md:text-8xl font-black leading-[0.9] tracking-tighter">
                        {t.hero.h1.split(" ").map((word, i) => (
                            <span key={i} className="block">{word}</span>
                        ))}
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-600 max-w-2xl mx-auto font-light leading-relaxed">
                        {t.hero.p}
                    </p>

                    <div className="pt-8">
                        <TelegramLoginButton
                            dict={{
                                login: {
                                    button: t.hero.btn,
                                    sub: lang === 'ru' ? "Запустить в Telegram" : "Launch in Telegram"
                                }
                            }}
                            botName="DogovorCheckBot"
                            startParam="alex_sales"
                        />
                    </div>
                </div>
            </section>

            {/* STATS (Ticker Style) */}
            <section className="w-full border-y border-black/10 bg-white">
                <div className="max-w-6xl mx-auto grid grid-cols-3 divide-x divide-black/10">
                    {t.stats.map((stat, i) => (
                        <div key={i} className="py-12 px-6 text-center">
                            <div className="text-4xl md:text-5xl font-black mb-2">{stat.val}</div>
                            <div className="text-xs uppercase tracking-widest text-gray-400">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* TECHNOLOGY (Grid) */}
            <section className="py-24 px-6 bg-[#E5E5E5]">
                <div className="max-w-5xl mx-auto grid md:grid-cols-2 gap-16 items-center">
                    <div className="space-y-6">
                        <h2 className="text-4xl font-bold">{t.tech.title}</h2>
                        <p className="text-lg text-gray-600 leading-relaxed">
                            {t.tech.desc}
                        </p>
                        <ul className="space-y-4 pt-4 font-mono text-sm">
                            <li className="flex items-center gap-3">
                                <span className="w-3 h-3 bg-black"></span>
                                Seismic Resistant (9.0)
                            </li>
                            <li className="flex items-center gap-3">
                                <span className="w-3 h-3 bg-black"></span>
                                Category 5 Hurricane Proof
                            </li>
                            <li className="flex items-center gap-3">
                                <span className="w-3 h-3 bg-black"></span>
                                Mold & Fire Proof
                            </li>
                        </ul>
                    </div>

                    {/* Visual Placeholder (Concrete Sphere) */}
                    <div className="aspect-square bg-gray-300 rounded-full shadow-2xl flex items-center justify-center relative overflow-hidden">
                        <div className="absolute inset-0 bg-gradient-to-br from-white/50 to-black/20"></div>
                        <span className="font-mono text-xs text-black/50 tracking-widest">AIRFORM VISUAL</span>
                    </div>
                </div>
            </section>

            <footer className="py-12 text-center text-xs font-mono uppercase text-gray-400">
                Dome Luxe Global © 2026. Designed by Antigravity.
            </footer>

        </main>
    );
}
