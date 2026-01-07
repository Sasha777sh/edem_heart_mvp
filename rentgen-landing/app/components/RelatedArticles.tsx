import Link from 'next/link';

interface RelatedArticle {
    title: string;
    slug: string;
    category: string;
}

interface RelatedArticlesProps {
    currentSlug: string;
    currentCategory: string;
    lang: string;
    allPages: any[];
}

export default function RelatedArticles({ currentSlug, currentCategory, lang, allPages }: RelatedArticlesProps) {
    // Find related pages (same category, different slug)
    const related = allPages
        .filter(page => page.category === currentCategory && page.slug !== currentSlug)
        .slice(0, 5); // Max 5 related

    if (related.length === 0) return null;

    return (
        <section className="w-full mt-16 pt-8 border-t border-white/10">
            <h3 className="text-2xl font-bold mb-6 text-white">
                {lang === 'ru' ? '📚 Похожие материалы' : '📚 Related Articles'}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {related.map((article) => (
                    <Link
                        key={article.slug}
                        href={`/${lang}/${article.slug}`}
                        className="group block p-4 rounded-lg border border-white/10 bg-white/5 backdrop-blur-md hover:bg-white/10 hover:border-white/20 transition-all duration-300"
                    >
                        <div className="text-xs text-gray-500 mb-2">{article.category}</div>
                        <h4 className="text-white font-medium group-hover:text-blue-400 transition-colors line-clamp-2">
                            {article.title}
                        </h4>
                        <p className="text-sm text-gray-400 mt-2 line-clamp-2">
                            {article.desc}
                        </p>
                    </Link>
                ))}
            </div>
        </section>
    );
}
