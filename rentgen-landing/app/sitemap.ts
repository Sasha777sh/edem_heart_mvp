import { MetadataRoute } from 'next'
import { seoPages } from './lib/seoPages'

export default function sitemap(): MetadataRoute.Sitemap {
    const baseUrl = 'https://rentgen.chatedem.com'

    // Static Routes (Matrix of Langs)
    const staticRoutes = ['ru', 'en', 'es', 'pt'].flatMap(lang => [
        {
            url: `${baseUrl}/${lang}`,
            lastModified: new Date(),
            changeFrequency: 'daily' as const,
            priority: 0.9,
        }
    ])

    // Add Root
    staticRoutes.push({
        url: baseUrl,
        lastModified: new Date(),
        changeFrequency: 'daily' as const,
        priority: 1,
    })

    // SEO Dynamic Routes (Matrix of Pages x Langs)
    const seoRoutes = seoPages.flatMap(page =>
        ['ru', 'en', 'es', 'pt'].map(lang => ({
            url: `${baseUrl}/${lang}/${page.slug}`,
            lastModified: new Date(),
            changeFrequency: 'weekly' as const,
            priority: 0.8,
        }))
    )

    return [...staticRoutes, ...seoRoutes]
}
