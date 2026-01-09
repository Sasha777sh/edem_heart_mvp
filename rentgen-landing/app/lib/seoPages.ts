import { CONTRACT_TYPES_RU, DREAMS_RU, SYMPTOMS_RU, RED_FLAGS_RU, PSYCHO_RU } from './seoData';

export type SeoPage = {
    slug: string;
    title: string;
    h1: string;
    desc: string;
    category: string;
    startParam?: string; // "dream", "med", "red_flag", "paper"
}

// MANUAL HIGH-QUALITY PAGES (Core Landing)
const MANUAL_PAGES: SeoPage[] = [
    {
        slug: "proverit-dogovor",
        title: "Проверить договор онлайн | RENTGEN",
        h1: "Проверка договоров за 5 секунд (AI)",
        desc: "Загрузите файл. Искусственный интеллект найдет риски, штрафы и скрытые условия.",
        category: "Главная",
        startParam: "paper"
    },
];

// GENERATOR ENGINE
function generatePages(): SeoPage[] {
    const pages: SeoPage[] = [...MANUAL_PAGES];

    // 1. CONTRACTS (General Safety)
    CONTRACT_TYPES_RU.forEach(type => {
        pages.push({
            slug: `proverit-dogovor-${type.slug}`,
            title: `Проверить договор ${type.name} онлайн | RENTGEN`,
            h1: `Аудит договора: ${type.name}`,
            desc: `Как найти риски (${type.risk}) в договоре? Загрузите фото/PDF. Проверка юристом (AI) онлайн.`,
            category: "Юрист",
            startParam: "paper"
        });
    });

    // 2. DREAMS (Interpretation)
    DREAMS_RU.forEach(dream => {
        pages.push({
            slug: `k-chemu-snitsya-${dream.slug}`,
            title: `К чему снится ${dream.name}? Толкование сна | RENTGEN`,
            h1: `Сонник: ${dream.name}. Значение Фрейда и Юнга`,
            desc: `Приснилась ${dream.name}? Это знак: ${dream.meaning}. Узнайте точную расшифровку вашего сна от ИИ-психоаналитика.`,
            category: "Сонник",
            startParam: "dream"
        });

        pages.push({
            slug: `son-${dream.slug}-znachenie`,
            title: `Сон ${dream.name} - что значит? | RENTGEN`,
            h1: `Расшифровка сна: ${dream.name}`,
            desc: `Психологический разбор сна про ${dream.name}. Предупреждение о: ${dream.meaning}.`,
            category: "Сонник",
            startParam: "dream"
        });
    });

    // 3. MED (Symptoms)
    SYMPTOMS_RU.forEach(sym => {
        pages.push({
            slug: `simptom-${sym.slug}-chto-delat`,
            title: `${sym.name}: причины и расшифровка | RENTGEN`,
            h1: `${sym.name}: О чем кричит организм?`,
            desc: `${sym.name} может указывать на ${sym.check}. Загрузите анализы или опишите состояние для AI-диагностики.`,
            category: "Здоровье",
            startParam: "med"
        });
    });

    // 4. RED FLAGS (Psychology)
    RED_FLAGS_RU.forEach(flag => {
        pages.push({
            slug: `priznaki-${flag.slug}-v-otnosheniyah`,
            title: `${flag.name} в отношениях: как распознать | RENTGEN`,
            h1: `${flag.name}: 🚩 Красный флаг`,
            desc: `${flag.desc}. Как понять, что вами манипулируют? Загрузите переписку в бот для анализа.`,
            category: "Психология",
            startParam: "red_flag"
        });
    });

    // 5. PSYCHOSOMATICS (The Profit Step)
    PSYCHO_RU.forEach(p => {
        pages.push({
            slug: `psihosomatika-${p.slug}`,
            title: `Психосоматика: ${p.name}. Эмоциональные причины | RENTGEN`,
            h1: `Почему ${p.name.toLowerCase()}? Психосоматический разбор`,
            desc: `Узнайте, какая эмоция вызывает симптом "${p.name}". Вероятная причина: ${p.cause}. Полная расшифровка связи тела и психики.`,
            category: "Психосоматика",
            startParam: "psycho"
        });
    });

    return pages;
}

// HELPER: Simple Translit for Cities & Slugs
function translit(word: string): string {
    const map: Record<string, string> = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'yo', 'Ж': 'zh',
        'З': 'z', 'И': 'i', 'Й': 'y', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n', 'О': 'o',
        'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'f', 'Х': 'kh', 'Ц': 'ts',
        'Ч': 'ch', 'Ш': 'sh', 'Щ': 'sch', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e', 'Ю': 'yu', 'Я': 'ya'
    };
    return word.split('').map(c => map[c] || c).join('').toLowerCase().replace(/[^a-z0-9-]/g, '');
}

export const seoPages = generatePages();
