import time

import httpx
import structlog

from app.core.config import get_settings
from app.security.validation import validate_url, ValidationError

logger = structlog.get_logger()
settings = get_settings()

# Based on: https://github.com/sarperavci/CloudflareBypassForScraping
# License: MIT - Copyright (c) 2024 Sarper AVCI
# This adapter wraps the CloudflareBypassForScraping server API.
# The actual browser-based bypass requires a Linux environment with
# CloakBrowser (patched Chromium). On Termux/Android, this adapter
# provides the API interface and delegates to a remote server.


class CloudflareAdapter:
    """
    Adapter for CloudflareBypassForScraping.
    Wraps the upstream server API with health checks, timeouts,
    structured errors, and SSRF protection.
    """

    def __init__(self):
        self.server_url = "http://localhost:8000"
        self.timeout = settings.cloudflare_timeout
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=10))

    async def health_check(self) -> dict:
        try:
            response = await self.client.get(f"{self.server_url}/cookies", params={"url": "https://example.com"})
            data = response.json()
            is_cf_server = "cookies" in data or "user_agent" in data
            return {
                "available": is_cf_server,
                "server_url": self.server_url,
                "version": "2.0",
                "engine": "cloakbrowser",
                "status": "healthy" if is_cf_server else "unavailable",
                "note": None if is_cf_server else "CloudflareBypassForScraping server not running on this host.",
            }
        except Exception as e:
            return {
                "available": False,
                "server_url": self.server_url,
                "version": "2.0",
                "engine": "cloakbrowser",
                "status": "unavailable",
                "error": str(e),
                "note": "Cloudflare bypass requires CloudflareBypassForScraping server running on the same host.",
            }

    async def test_url(self, url: str, proxy: str | None = None, timeout: int | None = None) -> dict:
        validate_url(url)

        start = time.time()
        params = {"url": url}
        if proxy:
            params["proxy"] = proxy

        try:
            response = await self.client.get(
                f"{self.server_url}/cookies",
                params=params,
                timeout=timeout or self.timeout,
            )
            elapsed_ms = int((time.time() - start) * 1000)
            data = response.json()

            return {
                "success": response.status_code == 200,
                "target": url,
                "status_code": data.get("status_code"),
                "response_time_ms": elapsed_ms,
                "html": data.get("html"),
                "cookies": data.get("cookies", {}),
                "user_agent": data.get("user_agent"),
                "browser": {
                    "engine": "cloakbrowser",
                    "version": "2.0",
                },
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": "Request timed out",
            }
        except Exception as e:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": str(e),
            }

    async def get_html(self, url: str, proxy: str | None = None) -> dict:
        validate_url(url)

        start = time.time()
        try:
            response = await self.client.post(
                f"{self.server_url}/html",
                json={"url": url, "proxy": proxy},
                timeout=self.timeout,
            )
            elapsed_ms = int((time.time() - start) * 1000)
            data = response.json()

            return {
                "success": response.status_code == 200,
                "target": url,
                "status_code": data.get("status_code"),
                "response_time_ms": elapsed_ms,
                "html": data.get("html", ""),
                "browser": {
                    "engine": "cloakbrowser",
                    "version": "2.0",
                },
            }
        except Exception as e:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": str(e),
            }

    async def get_cookies(self, url: str, proxy: str | None = None) -> dict:
        validate_url(url)

        start = time.time()
        params = {"url": url}
        if proxy:
            params["proxy"] = proxy

        try:
            response = await self.client.get(
                f"{self.server_url}/cookies",
                params=params,
                timeout=self.timeout,
            )
            elapsed_ms = int((time.time() - start) * 1000)
            data = response.json()

            return {
                "success": response.status_code == 200,
                "target": url,
                "response_time_ms": elapsed_ms,
                "cookies": data.get("cookies", {}),
                "user_agent": data.get("user_agent"),
            }
        except Exception as e:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": str(e),
            }

    async def close(self):
        await self.client.aclose()


cloudflare_adapter = CloudflareAdapter()
