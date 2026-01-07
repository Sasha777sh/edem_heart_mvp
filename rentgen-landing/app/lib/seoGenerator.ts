
// 🚀 SEO GENERATOR 9000 (The Traffic Machine)

type SeoPage = {
    slug: string;
    title: string;
    h1: string;
    desc: string;
    category: string;
    startParam: string; // "dream", "med", "red_flag"
}

// 1. DATA MATRICES
const CITIES = ["Moscow", "SPB", "Dubai", "Bali", "London", "NY", "Berlin", "Paris", "Phuket", "Istanbul"]; // 10
const CONTRACT_TYPES = ["Lease", "Employment", "Freight", "Service", "Loan", "Marriage", "NDA"]; // 7
const MEDICAL_SYMPTOMS = ["Headache", "Fever", "Anxiety", "BackPain", "Insomnia", "Fatigue", "Rash"]; // 7
const DREAM_SYMBOLS = ["Snake", "Tooth", "Falling", "Flying", "Water", "Fire", "Ex", "Money", "Death", "Baby"]; // 10

// 2. GENERATOR FUNCTION
export function generateSeoPages(): SeoPage[] {
    const pages: SeoPage[] = [];

    // MATRIX A: CONTRACTS (City x Type) -> 10 x 7 = 70 pages
    CITIES.forEach(city => {
        CONTRACT_TYPES.forEach(type => {
            pages.push({
                slug: `check-${type.toLowerCase()}-contract-${city.toLowerCase()}`,
                title: `Check ${type} Contract in ${city} | AI Lawyer`,
                h1: `Legal Audit: ${type} Agreement in ${city}`,
                desc: `AI Risk analysis for ${type} contracts in ${city}. Find hidden fees and risks instantly.`,
                category: "Law",
                startParam: "paper"
            });
        });
    });

    // MATRIX B: DREAMS (Symbol x Context) -> 10 x 5 = 50 pages
    // ... (To be expanded to 9000 via larger lists)

    return pages;
}
