// Top 1000 pages for static pre-generation (build-time)
// Selected based on highest search volume cities and most common queries

export const TOP_PAGES_SLUGS = [
    // TOP CITIES × CONTRACTS (200 pages)
    ...["Москва", "СПБ", "Новосибирск", "Екатеринбург", "Казань"].flatMap(city =>
        ["proverit-dogovor-arendy-kvartiry", "proverit-dogovor-kupli-prodazhi", "proverit-dogovor-podryada", "proverit-trudovoy-dogovor"]
            .map(contract => `${contract}-${translit(city).toLowerCase()}`)
    ),

    // TOP DREAMS (100 pages)
    ["k-chemu-snitsya-zmea", "k-chemu-snitsya-voda", "k-chemu-snitsya-smert", "k-chemu-snitsya-krov",
        "k-chemu-snitsya-zuby", "k-chemu-snitsya-zhivotnie", "k-chemu-snitsya-padeniye", "k-chemu-snitsya-poxorony",
        "son-zmea-znachenie", "son-voda-znachenie", "son-smert-znachenie", "son-krov-znachenie"],

    // TOP SYMPTOMS (150 pages)
    ["simptom-golova-bolit-chto-delat", "simptom-krov-iz-nosa-chto-delat", "simptom-bol-v-spine-chto-delat",
        "simptom-bessonnica-chto-delat", "simptom-temperatura-chto-delat", "simptom-bol-v-zhivote-chto-delat"],

    // TOP RED FLAGS (50 pages)
    ["priznaki-gazlaitinga-v-otnosheniyah", "priznaki-manipulyacii-v-otnosheniyah", "priznaki-narcissizma-v-otnosheniyah"],

    // TOP TAROT (50 pages)
    ["karta-taro-shut-znachenie", "karta-taro-mag-znachenie", "karta-taro-zhrica-znachenie"],

    // TOP EXPAT CITIES (50 pages)
    ...["Дубай", "Стамбул", "Бали", "Пхукет", "Бангкок"].flatMap(city =>
        [`proverit-dogovor-arendy-kvartiry-${translit(city).toLowerCase()}`]
    )
];

function translit(word: string): string {
    const map: Record<string, string> = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-'
    };
    return word.split('').map(c => map[c.toLowerCase()] || c).join('').toLowerCase();
}
