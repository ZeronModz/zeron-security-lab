import time

import httpx
import structlog

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

        start = time.time()
        redirect_chain = []
        current_url = request.url
        max_redirects = 10

        for _ in range(max_redirects):
            try:
                response = await self.client.request(
                    method=request.method.value,
                    url=current_url,
                    headers=request.headers or {},
                    cookies=request.cookies or {},
                    content=request.body,
                    follow_redirects=False,
                )

                if response.status_code in (301, 302, 303, 307, 308):
                    redirect_chain.append(current_url)
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
                }

            except httpx.TimeoutException:
                raise ValidationError("TIMEOUT", f"Request timed out after {request.timeout}s")
            except httpx.RequestError as e:
                raise ValidationError("REQUEST_ERROR", str(e))

        raise ValidationError("REDIRECT_ERROR", "Too many redirects")

    async def render(self, request) -> dict:
        validate_url(request.url)

        start = time.time()
        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(request.timeout / 1000, connect=10)
            ) as client:
                response = await client.get(
                    request.url,
                    headers={"User-Agent": "ZeronSecurityLab/1.0"},
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
