import random

try:
    import ua_generator
    UA_GENERATOR_AVAILABLE = True
except ImportError:
    UA_GENERATOR_AVAILABLE = None

DESKTOP_BROWSERS = ["chrome", "edge", "firefox", "safari"]
MOBILE_BROWSERS = ["chrome", "edge"]
PLATFORMS = ["windows", "macos", "linux"]
MOBILE_PLATFORMS = ["android", "ios"]


def generate_user_agent(
    device: str = "desktop",
    browser: str | list[str] | None = None,
    platform: str | list[str] | None = None,
) -> dict:
    if not UA_GENERATOR_AVAILABLE:
        return _fallback_user_agent()

    if device == "mobile":
        if browser is None:
            browser = MOBILE_BROWSERS
        if platform is None:
            platform = MOBILE_PLATFORMS
    else:
        if browser is None:
            browser = DESKTOP_BROWSERS
        if platform is None:
            platform = PLATFORMS

    ua = ua_generator.generate(device=device, browser=browser, platform=platform)
    headers = ua.headers.get()

    return {
        "user_agent": ua.text,
        "headers": headers,
        "platform": ua.platform,
        "browser": ua.browser,
        "client_hints": {
            "brands": ua.ch.brands if hasattr(ua.ch, "brands") else None,
            "mobile": ua.ch.mobile if hasattr(ua.ch, "mobile") else None,
            "platform": ua.ch.platform if hasattr(ua.ch, "platform") else None,
            "platform_version": ua.ch.platform_version if hasattr(ua.ch, "platform_version") else None,
            "architecture": ua.ch.architecture if hasattr(ua.ch, "architecture") else None,
            "bitness": ua.ch.bitness if hasattr(ua.ch, "bitness") else None,
        },
    }


def get_random_headers(custom_headers: dict | None = None) -> dict:
    ua_data = generate_user_agent()
    headers = ua_data["headers"].copy()
    headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
    headers.setdefault("Accept-Language", "en-US,en;q=0.9")
    headers.setdefault("Accept-Encoding", "gzip, deflate, br")
    headers.setdefault("Connection", "keep-alive")
    headers.setdefault("Upgrade-Insecure-Requests", "1")
    headers.setdefault("Sec-Fetch-Dest", "document")
    headers.setdefault("Sec-Fetch-Mode", "navigate")
    headers.setdefault("Sec-Fetch-Site", "none")
    headers.setdefault("Sec-Fetch-User", "?1")

    if custom_headers:
        headers.update(custom_headers)

    return headers


def get_api_headers(custom_headers: dict | None = None) -> dict:
    ua_data = generate_user_agent(device="desktop", browser=["chrome", "edge"])
    headers = ua_data["headers"].copy()
    headers.setdefault("Accept", "application/json, text/plain, */*")
    headers.setdefault("Accept-Language", "en-US,en;q=0.9")

    if custom_headers:
        headers.update(custom_headers)

    return headers


def _fallback_user_agent() -> dict:
    fallback_uas = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    ]
    ua = random.choice(fallback_uas)
    return {
        "user_agent": ua,
        "headers": {"User-Agent": ua},
        "platform": "unknown",
        "browser": "unknown",
        "client_hints": {},
    }
