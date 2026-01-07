import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

let locales = ["en", "ru"];
let defaultLocale = "ru"; // Assuming RU audience is primary based on user prompt

function getLocale(request: NextRequest) {
    const acceptLanguage = request.headers.get("accept-language");
    if (acceptLanguage?.includes("ru")) return "ru";
    return "en";
}

export function middleware(request: NextRequest) {
    const { pathname } = request.nextUrl;

    // Check if there is any supported locale in the pathname
    const pathnameHasLocale = locales.some(
        (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
    );

    if (pathnameHasLocale) return;

    // Redirect if no locale
    const locale = getLocale(request);
    request.nextUrl.pathname = `/${locale}${pathname}`;
    // e.g. incoming request is /products
    // The new URL is now /en/products
    return NextResponse.redirect(request.nextUrl);
}

export const config = {
    matcher: [
        // Skip all internal paths (_next)
        "/((?!_next|favicon.ico|api|.*\\..*).*)",
    ],
};
