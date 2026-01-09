import React from "react";
import LanguageSwitcher from "../../components/LanguageSwitcher";
import StickyCTA from "../../components/StickyCTA";
import TelegramLoginButton from "@/app/components/TelegramLoginButton";
import ROICalculator from "@/app/components/dome/ROICalculator";

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
            <section className="relative pt-32 pb-20 px-6 min-h-[90vh] flex flex-col justify-center items-center text-center overflow-hidden">
                {/* Background Image with Overlay */}
                <div className="absolute inset-0 z-0">
                    <img src="/images/dome/hero.png" alt="Dome Luxe Bali" className="w-full h-full object-cover opacity-100" />
                    <div className="absolute inset-0 bg-gradient-to-b from-white/90 via-white/40 to-white/90"></div>
                </div>

                <div className="relative z-10 max-w-4xl space-y-8 mt-20">
                    <p className="text-sm font-mono uppercase tracking-[0.3em] text-black bg-white/50 backdrop-blur-sm px-4 py-1 rounded-full inline-block">{t.subtitle}</p>
                    <h1 className="text-6xl md:text-8xl font-black leading-[0.9] tracking-tighter drop-shadow-sm">
                        {t.hero.h1.split(" ").map((word, i) => (
                            <span key={i} className="block">{word}</span>
                        ))}
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-900 max-w-2xl mx-auto font-light leading-relaxed bg-white/70 backdrop-blur-md p-4 rounded-xl">
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
            <section className="w-full border-y border-black/10 bg-white relative z-10">
                <div className="max-w-6xl mx-auto grid grid-cols-3 divide-x divide-black/10">
                    {t.stats.map((stat, i) => (
                        <div key={i} className="py-12 px-6 text-center">
                            <div className="text-4xl md:text-5xl font-black mb-2">{stat.val}</div>
                            <div className="text-xs uppercase tracking-widest text-gray-400">{stat.label}</div>
                        </div>
                    ))}
                </div>
            </section>

            {/* NEW: INTERIOR VISUAL */}
            <section className="py-0">
                <div className="w-full h-[80vh] relative">
                    <img src="/images/dome/interior.png" alt="Dome Interior" className="w-full h-full object-cover" />
                    <div className="absolute bottom-10 left-6 md:left-20 bg-white/90 p-8 max-w-lg backdrop-blur-md">
                        <h3 className="text-2xl font-bold mb-2">Zen Living</h3>
                        <p className="text-gray-600">The oculus skylight brings natural rhythm to your life. No sharp corners, only seamless flow.</p>
                    </div>
                </div>
            </section>

            {/* TECHNOLOGY DEEP DIVE */}
            <section className="py-24 px-6 bg-white text-black">
                <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">

                    <div className="space-y-16">
                        <div className="text-left space-y-4">
                            <h2 className="text-3xl md:text-5xl font-black uppercase tracking-tighter">Why Airform?</h2>
                            <p className="text-gray-500 font-mono tracking-widest text-xs uppercase">The Physics of Efficiency</p>
                        </div>

                        <div className="space-y-12">
                            <div className="space-y-4">
                                <h3 className="text-xl font-bold border-b border-black pb-2">01. Physics</h3>
                                <p className="text-gray-600 leading-relaxed font-light">
                                    A sphere is the strongest shape in nature. Wind simply flows around it, making it hurricane-proof.
                                </p>
                            </div>
                            <div className="space-y-4">
                                <h3 className="text-xl font-bold border-b border-black pb-2">02. Speed</h3>
                                <p className="text-gray-600 leading-relaxed font-light">
                                    We inflate the form in 4 hours. Spray concrete in 7 days. Move in in 30 days.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* TECH IMAGE */}
                    <div className="relative h-[600px] rounded-3xl overflow-hidden shadow-2xl">
                        <img src="/images/dome/tech.png" alt="Airform Construction" className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-black/10"></div>
                    </div>

                </div>
            </section>

            {/* INVESTMENT ROI */}
            <section className="py-24 px-6 bg-black text-white">
                <div className="max-w-4xl mx-auto">
                    <h2 className="text-3xl md:text-5xl font-black uppercase tracking-tighter mb-12 text-center text-white">The Math</h2>

                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse font-mono text-sm">
                            <thead>
                                <tr className="border-b border-white/20 text-gray-500 uppercase tracking-widest">
                                    <th className="py-4">Parameter</th>
                                    <th className="py-4">Dome 3 (Airform)</th>
                                    <th className="py-4">Traditional Villa</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/10">
                                <tr className="hover:bg-white/5 transition-colors">
                                    <td className="py-4 font-bold">Build Cost (Shell)</td>
                                    <td className="py-4 text-[#00FF00]">$25,000</td>
                                    <td className="py-4 text-red-500">$85,000+</td>
                                </tr>
                                <tr className="hover:bg-white/5 transition-colors">
                                    <td className="py-4 font-bold">Construction Time</td>
                                    <td className="py-4 text-[#00FF00]">30 Days</td>
                                    <td className="py-4 text-red-500">8-12 Months</td>
                                </tr>
                                <tr className="hover:bg-white/5 transition-colors">
                                    <td className="py-4 font-bold">Maintenance/Yr</td>
                                    <td className="py-4 text-[#00FF00]">$200 (Paint only)</td>
                                    <td className="py-4 text-red-500">$2,500+ (Plaster, Roof)</td>
                                </tr>
                                <tr className="hover:bg-white/5 transition-colors">
                                    <td className="py-4 font-bold">Lifespan</td>
                                    <td className="py-4 text-[#00FF00]">500+ Years (Stone)</td>
                                    <td className="py-4 text-red-500">50-70 Years</td>
                                </tr>
                                <tr className="bg-white/10">
                                    <td className="py-4 font-bold pl-2">Rental ROI (Bali)</td>
                                    <td className="py-4 font-bold text-[#00FF00]">~28% / Year</td>
                                    <td className="py-4 text-gray-400">~12% / Year</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div className="mt-12 text-center">
                        <p className="text-gray-400 max-w-lg mx-auto mb-8 font-light">
                            Stop investing in decaying drywall. Start investing in eternal geometry.
                            Calculate your project implementation plan now.
                        </p>
                        <TelegramLoginButton
                            dict={{
                                login: {
                                    button: "Calculate My ROI",
                                    sub: "Launch AI Constructor"
                                }
                            }}
                            botName="DogovorCheckBot"
                            startParam="alex_sales"
                        />
                    </div>
                </div>
            </section>

            {/* GLOBAL FOOTPRINT */}
            <section className="py-24 px-6 bg-[#F0F0F0]">
                <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 text-center md:text-left">
                    <div>
                        <h4 className="font-bold uppercase tracking-widest mb-4">Locations</h4>
                        <ul className="space-y-2 text-gray-500 font-light text-sm">
                            <li>Bali, Indonesia (HQ)</li>
                            <li>Phuket, Thailand</li>
                            <li>Siargao, Philippines</li>
                            <li>Goa, India (Coming Soon)</li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="font-bold uppercase tracking-widest mb-4">Services</h4>
                        <ul className="space-y-2 text-gray-500 font-light text-sm">
                            <li>Land Acquisition</li>
                            <li>Architectural Planning</li>
                            <li>Permit Management</li>
                            <li>Turnkey Construction</li>
                        </ul>
                    </div>
                    <div>
                        <h4 className="font-bold uppercase tracking-widest mb-4">Contact</h4>
                        <ul className="space-y-2 text-gray-500 font-light text-sm">
                            <li>dome@chatedem.com</li>
                            <li>Telegram Support: @Alex_Dome</li>
                        </ul>
                    </div>
                </div>
            </section>

            {/* MODELS CATALOG */}
            <section className="py-24 px-6 bg-[#F8F8F8] text-black">
                <div className="max-w-6xl mx-auto text-center space-y-16">
                    <h2 className="text-3xl md:text-5xl font-black uppercase tracking-tighter">Choose Your Geometry</h2>

                    <div className="grid md:grid-cols-3 gap-8">

                        {/* Model 1: Eco Pod */}
                        <div className="bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all group">
                            <div className="h-64 overflow-hidden">
                                <img src="/images/dome/model_pod.png" alt="Eco Pod" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                            </div>
                            <div className="p-8 text-left space-y-4">
                                <div>
                                    <h4 className="text-2xl font-bold">The Eco Pod</h4>
                                    <p className="text-sm font-mono text-gray-400">35m² • Studio • 1 Bath</p>
                                </div>
                                <p className="text-gray-600 font-light text-sm line-clamp-3">
                                    Perfect for glamping resorts or guest houses. High ROI rental unit.
                                    Minimalist design with panoramic oculus.
                                </p>
                                <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
                                    <span className="font-bold text-xl">$25,000</span>
                                    <TelegramLoginButton
                                        dict={{ login: { button: "Order", sub: "View Plan" } }}
                                        botName="DogovorCheckBot" startParam="order_pod"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Model 2: Family Hive */}
                        <div className="bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all group relative border-2 border-black/5">
                            <div className="absolute top-4 right-4 bg-black text-white text-xs px-3 py-1 rounded-full uppercase tracking-widest font-bold">Bestseller</div>
                            <div className="h-64 overflow-hidden">
                                <img src="/images/dome/model_hive.png" alt="Family Hive" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                            </div>
                            <div className="p-8 text-left space-y-4">
                                <div>
                                    <h4 className="text-2xl font-bold">Family Hive</h4>
                                    <p className="text-sm font-mono text-gray-400">90m² • 2 Bed • 2 Bath</p>
                                </div>
                                <p className="text-gray-600 font-light text-sm line-clamp-3">
                                    Double-dome structure connecting living and sleeping zones.
                                    Ideal for small families or premium long-term rentals.
                                </p>
                                <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
                                    <span className="font-bold text-xl">$65,000</span>
                                    <TelegramLoginButton
                                        dict={{ login: { button: "Order", sub: "View Plan" } }}
                                        botName="DogovorCheckBot" startParam="order_hive"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Model 3: Luxe Estate */}
                        <div className="bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all group">
                            <div className="h-64 overflow-hidden">
                                <img src="/images/dome/model_estate.png" alt="Luxe Estate" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                            </div>
                            <div className="p-8 text-left space-y-4">
                                <div>
                                    <h4 className="text-2xl font-bold">Luxe Estate</h4>
                                    <p className="text-sm font-mono text-gray-400">250m² • 4 Bed • Pool</p>
                                </div>
                                <p className="text-gray-600 font-light text-sm line-clamp-3">
                                    The ultimate architectural statement. Infinity pool integration,
                                    panoramic glass walls, smart home ecosystem.
                                </p>
                                <div className="pt-4 border-t border-gray-100 flex justify-between items-center">
                                    <span className="font-bold text-xl">$180,000</span>
                                    <TelegramLoginButton
                                        dict={{ login: { button: "Order", sub: "View Plan" } }}
                                        botName="DogovorCheckBot" startParam="order_estate"
                                    />
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </section>


            <ROICalculator />

            <footer className="py-12 text-center text-xs font-mono uppercase text-gray-400">
                Dome Luxe Global © 2026. Designed by Antigravity.
            </footer>

        </main>
    );
}
