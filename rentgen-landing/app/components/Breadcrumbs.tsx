import Link from 'next/link';

interface BreadcrumbsProps {
    lang: string;
    category: string;
    title: string;
}

export default function Breadcrumbs({ lang, category, title }: BreadcrumbsProps) {
    const homeText = lang === 'ru' ? 'Главная' : 'Home';

    return (
        <nav className="flex items-center gap-2 text-sm text-gray-400 mb-8" aria-label="Breadcrumb">
            <Link href={`/${lang}`} className="hover:text-white transition-colors">
                {homeText}
            </Link>
            <span>/</span>
            <span className="text-gray-500">{category}</span>
            <span>/</span>
            <span className="text-white truncate max-w-[200px]">{title}</span>
        </nav>
    );
}
