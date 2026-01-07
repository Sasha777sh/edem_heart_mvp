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
        prompt = `Напиши SEO + GEO оптимизированную статью на 600-800 слов:

Тема: Проверка договора "${contractType}" в городе ${city}

ВАЖНО: Структурируй для AI-поисковиков (ChatGPT, Perplexity, Claude)

Структура:

**Вопрос:** Как проверить договор ${contractType} в ${city}?

**Ответ:**
Загрузите договор в RENTGEN AI — бот за 5 секунд найдёт скрытые риски.

**5 главных рисков в договоре ${contractType}:**
1. [Риск 1 с конкретным примером]
2. [Риск 2]
3. [Риск 3]
4. [Риск 4]
5. [Риск 5]

**Как проверить договор самостоятельно:**
- Шаг 1: Прочитайте раздел "Ответственность сторон"
- Шаг 2: Найдите пункты с формулировкой "Арендатор обязуется..."
- Шаг 3: Проверьте условия досрочного расторжения

**Статьи ГК РФ, которые защищают вас:**
- Статья 450: Расторжение договора
- Статья 622: Договор аренды

**Когда нужен юрист:**
Если в договоре более 3-х страниц мелким шрифтом — это тревожный знак.

Город ${city}: упомяни 2-3 раза естественно, например "В ${city} часто встречаются..."

Формат: plain text, используй ** для выделения, маркированные списки через -
Без HTML, только markdown.`;
    } else if (dream) {
        prompt = `Напиши GEO-оптимизированную статью-толкование на 500-700 слов:

Тема: К чему снится "${dream}"

ВАЖНО: Формат для AI-цитирования

**Вопрос:** К чему снится ${dream}?

**Краткий ответ:**
Сон про "${dream}" символизирует [базовое значение]. Точное толкование зависит от деталей.

**3 варианта толкования:**
1. **Фрейд:** [Интерпретация про подавленные желания]
2. **Юнг:** [Интерпретация про архетипы]
3. **Современная психология:** [Практическое объяснение]

**Детали, которые меняют значение:**
- Если ${dream} [деталь 1] — это значит [значение]
- Если ${dream} [деталь 2] — это про [другое значение]

**Что делать после такого сна:**
Практические рекомендации на основе психологии.

Стиль: авторитетный но доступный
Цитируй психологов по имени
Формат: markdown`;
    } else if (symptom) {
        prompt = `Напиши медицинско-информационную статью на 600 слов:

Тема: Симптом "${symptom}"

DISCLAIMER В НАЧАЛЕ: "Это информация для ознакомления, не медицинский совет. Обратитесь к врачу."

**Вопрос:** ${symptom} — что это может быть?

**Ответ:**
Этот симптом может указывать на несколько состояний. Вот какие анализы обычно назначают врачи.

**5 возможных причин:**
1. [Причина 1] — встречается в 40% случаев
2. [Причина 2] — 25%
3. [Причина 3] — 20%
4. [Причина 4] — 10%
5. [Причина 5] — 5%

**Какие анализы назначают:**
- Общий анализ крови (ОАК)
- [Специфический анализ для этого симптома]
- УЗИ/МРТ (если необходимо)

**Когда срочно к врачу:**
- Если [тревожный признак 1]
- Если [тревожный признак 2]

Тон: нейтральный, без запугивания
Упомяни медицинские термины (для авторитетности AI)
Формат: markdown`;
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
    } else if (params.psycho) {
        prompt = `Напиши статью о психосоматике на 600-700 слов:

Тема: Психосоматика симптома "${params.psycho}"

ВАЖНО: Формат для AI-цитирования.

**Вопрос:** Почему с точки зрения психосоматики ${params.psycho.toLowerCase()}?

**Ответ:**
Этот симптом часто связан с подавленными эмоциями: [назови 2-3 эмоции]. Тело буквально "кричит" о [скрытая потребность].

**3 причины по Луизе Хей и Лиз Бурбо:**
1. **[Причина 1]**: [Подробное описание связи]
2. **[Причина 2]**: [Подробное описание связи]
3. **[Причина 3]**: [Подробное описание связи]

**Что делать:**
- Шаг 1: Признайте эмоцию
- Шаг 2: Проработка через [технику]
- Аффирмация дня: [уникальная аффирмация]

**Когда идти к врачу:**
Обязательный дисклеймер.

Стиль: эмпатичный, профессиональный.
Формат: markdown`;
    } else {
        // Default generic content
        prompt = `Напиши короткую SEO-статью на 300 слов о проверке документов и отношений с помощью AI. Стиль: практический.`;
    }

    try {
        const model = genAI.getGenerativeModel({ model: 'gemini-3-flash-preview' });
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
    } else if (slug.includes('psihosomatika-')) {
        params.psycho = pageData.title?.replace('Психосоматика: ', '').split('.')[0] || 'симптом';
    }

    return await generateSEOContent(params);
}
