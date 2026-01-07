import type { Metadata } from "next";
import "../globals.css";
import React from 'react';

// Dictionaries loader
const dictionaries = {
  en: () => import("../dictionaries/en.json").then((module) => module.default),
  ru: () => import("../dictionaries/ru.json").then((module) => module.default),
};

type Props = {
  params: Promise<{ lang: "en" | "ru" }>;
};

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { lang } = await params;
  const dict = await dictionaries[lang]();
  return {
    title: dict.seo.title,
    description: dict.seo.description,
    keywords: dict.seo.keywords,
    openGraph: {
      title: dict.seo.title,
      description: dict.seo.description,
      type: "website",
    },
    verification: {
      google: "nWw0Us4PfjP1KNSpdCidJPyZwlxdGm5sq6D7LObyQB4",
      yandex: "2683d26821666265",
    },
  };
}

export async function generateStaticParams() {
  return [{ lang: "en" }, { lang: "ru" }];
}

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  return (
    <html lang={lang}>
      <body className="bg-black text-white">{children}</body>
    </html>
  );
}
