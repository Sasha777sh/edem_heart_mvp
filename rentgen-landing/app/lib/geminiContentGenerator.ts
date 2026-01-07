import { GoogleGenerativeAI } from '@google/generative-ai';

// Initialize Gemini
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

export async function generateSEOContent(params: {
    city?: string;
    contractType?: string;
    dream?: string;
    symptom?: string;
    redFlag?: string;
    taroCard?: string;
    zodiac?: string;
    career?: string;
    lang?: string;
}): Promise<string> {
    const { city, contractType, dream, symptom, redFlag, taroCard, zodiac, career, lang = 'ru' } = params;

    let prompt = '';

    // Generate prompt based on page type
    if (contractType && city) {
        prompt = `Напиши уникальную SEO-статью на 500-700 слов:

Тема: Проверка договора "${contractType}" в городе ${city}

Структура:
1. Введение (50 слов): Почему важно проверять договоры
2. Основные риски (200 слов): Какие ошибки встречаются в договорах "${contractType}"
3. Как проверить (150 слов): Практические шаги
4. Когда обратиться к юристу (100 слов)
5. Заключение + CTA (50 слов): Предложить бесплатную проверку через AI-бота

Стиль: практический, без воды, с конкретными примерами
Город: упомяни ${city} как минимум 3 раза естественно
Формат: plain text с параграфами (используй \\n\\n для разделения)
Без заголовков типа "## Введение", просто текст.`;
    } else if (dream) {
        prompt = `Напиши уникальную статью-толкование сна на 400-600 слов:

Тема: К чему снится "${dream}"

Структура:
1. Базовое значение (100 слов): Общее толкование
2. Психологическая интерпретация (150 слов): По Фрейду и Юнгу
3. Контекст имеет значение (100 слов): Детали сна меняют смысл
4. Что делать (100 слов): Практические рекомендации
5. CTA: Получить персональный разбор от AI

Стиль: мистический но практичный, без страшилок
Формат: plain text, параграфы через \\n\\n`;
    } else if (symptom) {
        prompt = `Напиши информационную статью на 500 слов:

Тема: Симптом "${symptom}" - что проверить

ВАЖНО: Это НЕ медицинский совет, а информация о том, какие анализы обычно назначают врачи.

Структура:
1. Описание (100 слов): Что такое этот симптом
2. Возможные причины (200 слов): Список распространенных причин
3. Какие анализы назначают (150 слов): Стандартные обследования
4. Disclaimer (50 слов): "Это не диагноз, обратитесь к врачу"
5. CTA: AI поможет расшифровать ваши анализы

Стиль: нейтральный, медицински корректный
Тон: информативный, без запугивания
Формат: plain text`;
    } else if (redFlag) {
        prompt = `Напиши статью о токсичном поведении на 400-500 слов:

Тема: "${redFlag}" в отношениях

Структура:
1. Что это (100 слов): Определение
2. Как проявляется (150 слов): Конкретные примеры фраз и действий
3. Почему опасно (100 слов): Психологические последствия
4. Что делать (100 слов): Первые шаги
5. CTA: Проверить свою переписку через AI

Стиль: поддерживающий, без драмы
Формат: plain text`;
    } else {
        // Default generic content
        prompt = `Напиши короткую SEO-статью на 300 слов о проверке документов и отношений с помощью AI. Стиль: практический.`;
    }

    try {
        const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash-exp' });
        const result = await model.generateContent(prompt);
        const response = result.response;
        const text = response.text();

        return text;
    } catch (error) {
        console.error('Gemini API Error:', error);
        // Fallback to template if API fails
        return generateFallbackContent(params);
    }
}

function generateFallbackContent(params: any): string {
    const { city, contractType, dream, symptom } = params;

    if (contractType && city) {
        return `Проверка договора ${contractType} в городе ${city} — это важный шаг для защиты ваших интересов. Наш AI-бот поможет вам найти скрытые риски и штрафы в документах за несколько секунд. Загрузите фото или PDF договора, и получите детальный анализ.`;
    } else if (dream) {
        return `Сон про "${dream}" может иметь множество значений в зависимости от контекста. Наш AI-психоаналитик поможет вам расшифровать ваш личный сон, учитывая все детали и вашу жизненную ситуацию.`;
    } else if (symptom) {
        return `Симптом "${symptom}" требует внимания. Загрузите ваши анализы в бот, и AI поможет понять, какие показатели выходят за норму и что это может означать. Помните: это не замена консультации врача.`;
    }

    return `Используйте наш AI-бот для анализа документов, снов и здоровья. Быстро, точно, конфиденциально.`;
}

export async function generatePageContent(slug: string, pageData: any): Promise<string> {
    // Extract parameters from slug and pageData
    const params: any = { lang: 'ru' };

    // Parse slug to determine content type
    if (slug.includes('proverit-dogovor')) {
        params.contractType = pageData.title || 'договор';
        params.city = slug.split('-').pop() || 'Москва';
    } else if (slug.includes('k-chemu-snitsya') || slug.includes('son-')) {
        params.dream = pageData.h1 || 'неизвестный сон';
    } else if (slug.includes('simptom-')) {
        params.symptom = pageData.title || 'симптом';
    } else if (slug.includes('priznaki-')) {
        params.redFlag = pageData.title || 'red flag';
    }

    return await generateSEOContent(params);
}
