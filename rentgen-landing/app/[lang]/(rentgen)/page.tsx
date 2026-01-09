import React from "react";
import ComparisonCalculator from "../../components/ComparisonCalculator";
import TelegramLoginButton from "../../components/TelegramLoginButton";
import FaqSection from "../../components/FaqSection";
import StickyCTA from "../../components/StickyCTA";
import LanguageSwitcher from "../../components/LanguageSwitcher";


export default async function Home({ params }: { params: Promise<{ lang: "en" | "ru" | "es" | "pt" }> }) {
  const dictionaries = {
    en: () => import("../../dictionaries/en.json").then((module) => module.default),
    ru: () => import("../../dictionaries/ru.json").then((module) => module.default),
    es: () => import("../../dictionaries/es.json").then((module) => module.default),
    pt: () => import("../../dictionaries/pt.json").then((module) => module.default),
  };
  const { lang } = await params;
  const dict = await dictionaries[lang]();

  return (
    <main className="min-h-screen bg-black text-white relative overflow-hidden selection:bg-white selection:text-black">

      {/* GLOBAL UI ELEMENTS */}
      <LanguageSwitcher />
      <StickyCTA text={dict.sticky_cta} />

      {/* Background Gradients (Aurora) */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[20%] w-[500px] h-[500px] bg-blue-900/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
        <div className="absolute bottom-[-10%] right-[20%] w-[600px] h-[600px] bg-purple-900/10 rounded-full blur-[120px] mix-blend-screen"></div>
      </div>

      <div className="relative z-10 max-w-5xl mx-auto px-6 py-20 flex flex-col items-center gap-24">

        {/* 1. HERO */}
        <section className="text-center space-y-8 animate-fade-in-up">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-md text-xs font-medium text-gray-400 tracking-wider uppercase">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            {dict.hero.badge}
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-gray-400 leading-[1.1]" dangerouslySetInnerHTML={{ __html: dict.hero.title }}>
          </h1>

          <p className="max-w-2xl mx-auto text-xl text-gray-400 leading-relaxed font-light" dangerouslySetInnerHTML={{ __html: dict.hero.subtitle }}>
          </p>

          <div className="flex flex-col md:flex-row gap-4 justify-center pt-8">
            <TelegramLoginButton dict={dict} />
          </div>
        </section>

        {/* 2. DEMO BLOCK */}
        <section className="w-full max-w-3xl animate-fade-in-up delay-100">
          <div className="relative rounded-3xl border border-white/10 bg-[#0A0A0A] overflow-hidden shadow-2xl">
            {/* Fake Window Header */}
            <div className="h-10 border-b border-white/5 bg-white/5 flex items-center px-4 gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
              <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
              <div className="ml-4 text-xs text-gray-600 font-mono">{dict.demo.header}</div>
            </div>

            {/* Demo Content */}
            <div className="p-8 font-mono text-sm md:text-base space-y-6">
              <div className="flex gap-4 opacity-50">
                <div className="text-gray-500">{dict.demo.user_label}</div>
                <div className="p-3 rounded-xl bg-white/5 border border-white/5 text-gray-300 max-w-md" dangerouslySetInnerHTML={{ __html: dict.demo.user_text }}></div>
              </div>

              <div className="flex gap-4">
                <div className="text-blue-400">{dict.demo.ai_label}</div>
                <div className="space-y-4 w-full">
                  <div className="text-white font-bold">{dict.demo.ai_header}</div>

                  <div className="grid gap-3">
                    <div className="flex items-center gap-3 p-3 rounded-lg border border-red-900/30 bg-red-900/10">
                      <span className="text-red-500">{dict.demo.risk_high}</span>
                      <span className="text-gray-300">{dict.demo.risk_text}</span>
                    </div>

                    <div className="flex items-center gap-3 p-3 rounded-lg border border-yellow-900/30 bg-yellow-900/10">
                      <span className="text-yellow-500">{dict.demo.asymmetry_label}</span>
                      <span className="text-gray-300">{dict.demo.asymmetry_text}</span>
                    </div>

                    <div className="p-3">
                      <span className="text-gray-500">{dict.demo.calculating}</span>
                      <span className="ml-2 animate-pulse text-blue-400">{dict.demo.unlock}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Demo Overlay CTA */}
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-80 pointer-events-none"></div>
            <div className="absolute bottom-6 w-full text-center">
              <p className="text-gray-400 text-xs uppercase tracking-widest mb-2">{dict.demo.caption}</p>
            </div>
          </div>
        </section>

        {/* 3. FEATURES */}
        <section className="w-full grid md:grid-cols-2 gap-8">
          <h2 className="text-3xl font-bold md:col-span-2 text-center mb-4">{dict.features.title}</h2>

          <div className="p-8 rounded-3xl border border-white/10 bg-neutral-900/30 hover:bg-neutral-900/50 transition-colors">
            <div className="text-2xl mb-4">{dict.features.contracts.title}</div>
            <p className="text-gray-400">
              <span className="text-white block mb-2 font-medium">{dict.features.contracts.highlight}</span>
              {dict.features.contracts.desc}
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/10 bg-neutral-900/30 hover:bg-neutral-900/50 transition-colors">
            <div className="text-2xl mb-4">{dict.features.purchases.title}</div>
            <p className="text-gray-400">
              <span className="text-white block mb-2 font-medium">{dict.features.purchases.highlight}</span>
              {dict.features.purchases.desc}
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/10 bg-neutral-900/30 hover:bg-neutral-900/50 transition-colors">
            <div className="text-2xl mb-4">{dict.features.jobs.title}</div>
            <p className="text-gray-400">
              <span className="text-white block mb-2 font-medium">{dict.features.jobs.highlight}</span>
              {dict.features.jobs.desc}
            </p>
          </div>

          <div className="p-8 rounded-3xl border border-white/10 bg-neutral-900/30 hover:bg-neutral-900/50 transition-colors">
            <div className="text-2xl mb-4">{dict.features.decisions.title}</div>
            <p className="text-gray-400">
              <span className="text-white block mb-2 font-medium">{dict.features.decisions.highlight}</span>
              {dict.features.decisions.desc}
            </p>
          </div>
        </section>

        {/* 3.1 CALCULATOR */}
        <ComparisonCalculator dict={dict} />

        {/* 4. PAYWALL */}
        <section className="w-full p-1 rounded-3xl bg-gradient-to-b from-white/10 to-transparent">
          <div className="bg-black rounded-[22px] p-10 text-center">
            <h2 className="text-3xl font-bold mb-6">{dict.paywall.title}</h2>
            <div className="grid md:grid-cols-3 gap-6 max-w-3xl mx-auto mb-10">
              <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                <div className="text-2xl font-bold text-green-400 mb-1">{dict.paywall.money.value}</div>
                <div className="text-sm text-gray-400">{dict.paywall.money.desc}</div>
              </div>
              <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                <div className="text-2xl font-bold text-red-400 mb-1">{dict.paywall.time.value}</div>
                <div className="text-sm text-gray-400">{dict.paywall.time.desc}</div>
              </div>
              <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                <div className="text-2xl font-bold text-blue-400 mb-1">{dict.paywall.exit.value}</div>
                <div className="text-sm text-gray-400">{dict.paywall.exit.desc}</div>
              </div>
            </div>
            <a
              href="https://t.me/DogovorCheckBot?start=website_paywall"
              className="inline-flex items-center gap-2 text-white border-b border-white pb-1 hover:text-gray-300 transition-colors"
            >
              {dict.paywall.link}
            </a>
          </div>
        </section>

        {/* 5. FAQ */}
        <FaqSection dict={dict} />



        <footer className="w-full text-center text-gray-600 text-sm py-10">
          <p>{dict.footer}</p>
        </footer>

      </div>
    </main>
  );
}
