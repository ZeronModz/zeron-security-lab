import time

import httpx
import structlog

from app.adapters.ua_adapter import get_random_headers, generate_user_agent
from app.core.config import get_settings
from app.security.validation import validate_url, ValidationError

logger = structlog.get_logger()
settings = get_settings()

SECURITY_HEADERS = [
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "x-xss-protection",
    "referrer-policy",
    "permissions-policy",
    "cross-origin-opener-policy",
    "cross-origin-resource-policy",
]


class WebTestingService:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.request_timeout, connect=10),
            follow_redirects=False,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        )

    async def fetch(self, request) -> dict:
        validate_url(request.url)

        if request.user_agent:
            ua_data = generate_user_agent(
                device=request.ua_device or "desktop",
                browser=request.ua_browser or ["chrome", "edge"],
            )
            headers = ua_data["headers"].copy()
            headers["User-Agent"] = request.user_agent
        elif request.headers:
            headers = dict(request.headers)
        else:
            headers = get_random_headers()

        headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        headers.setdefault("Accept-Language", "en-US,en;q=0.9")
        headers.setdefault("Accept-Encoding", "gzip, deflate, br")
        headers.setdefault("Connection", "keep-alive")
        headers.setdefault("Upgrade-Insecure-Requests", "1")
        headers.setdefault("Sec-Fetch-Dest", "document")
        headers.setdefault("Sec-Fetch-Mode", "navigate")
        headers.setdefault("Sec-Fetch-Site", "none")
        headers.setdefault("Sec-Fetch-User", "?1")

        start = time.time()
        redirect_chain = []
        current_url = request.url
        max_redirects = 10

        for _ in range(max_redirects):
            try:
                response = await self.client.request(
                    method=request.method.value,
                    url=current_url,
                    headers=headers,
                    cookies=request.cookies or {},
                    content=request.body,
                    follow_redirects=False,
                )

                if response.status_code in (301, 302, 303, 307, 308):
                    redirect_chain.append({
                        "url": current_url,
                        "status": response.status_code,
                    })
                    location = response.headers.get("location", "")
                    if not location:
                        break
                    if location.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(current_url)
                        location = f"{parsed.scheme}://{parsed.netloc}{location}"
                    current_url = location
                    if not request.follow_redirects:
                        break
                    continue

                elapsed_ms = int((time.time() - start) * 1000)
                headers_dict = dict(response.headers)
                security = {h: headers_dict.get(h) for h in SECURITY_HEADERS}

                return {
                    "url": str(response.url),
                    "status_code": response.status_code,
                    "response_time_ms": elapsed_ms,
                    "headers": headers_dict,
                    "body": response.text[:settings.max_request_size],
                    "redirect_chain": redirect_chain,
                    "cookies": dict(response.cookies),
                    "security_headers": security,
                    "used_user_agent": headers.get("User-Agent", ""),
                    "client_hints_sent": {k: v for k, v in headers.items() if k.startswith("sec-ch-ua")},
                }

            except httpx.TimeoutException:
                raise ValidationError("TIMEOUT", f"Request timed out after {request.timeout}s")
            except httpx.RequestError as e:
                raise ValidationError("REQUEST_ERROR", str(e))

        raise ValidationError("REDIRECT_ERROR", "Too many redirects")

    async def render(self, request) -> dict:
        validate_url(request.url)

        headers = get_random_headers()
        headers.setdefault("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

        start = time.time()
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(request.timeout / 1000, connect=10)
            ) as client:
                response = await client.get(
                    request.url,
                    headers=headers,
                )

                elapsed_ms = int((time.time() - start) * 1000)
                html = response.text[:settings.max_request_size]

                title = ""
                if "<title>" in html.lower():
                    import re
                    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                    if match:
                        title = match.group(1).strip()

                return {
                    "url": str(response.url),
                    "title": title,
                    "html": html,
                    "console_errors": [],
                    "network_errors": [],
                    "render_time_ms": elapsed_ms,
                }
        except Exception as e:
            raise ValidationError("RENDER_ERROR", str(e))

    async def screenshot(self, request) -> dict:
        validate_url(request.url)
        return {
            "url": request.url,
            "screenshot_base64": "",
            "width": request.width,
            "height": request.height,
            "capture_time_ms": 0,
            "note": "Screenshot requires browser engine. Deploy with browser support on Railway.",
        }

    async def close(self):
        await self.client.aclose()


web_service = WebTestingService()
