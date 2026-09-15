import time

import httpx
import structlog

from app.core.config import get_settings
from app.security.validation import validate_url, ValidationError

logger = structlog.get_logger()
settings = get_settings()

# Based on: https://github.com/sarperavci/GoogleRecaptchaBypass
# License: MIT (inherited from upstream)
# This adapter wraps the reCAPTCHA testing functionality.
# The actual bypass uses DrissionPage + audio recognition.
# On Termux/Android, this provides the API interface.

# Google reCAPTCHA official test keys
TEST_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
TEST_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"


class RecaptchaAdapter:
    """
    Adapter for GoogleRecaptchaBypass.
    Provides authorized CAPTCHA testing with official test keys,
    manual verification support, and structured errors.
    """

    def __init__(self):
        self.server_url = "http://localhost:8001"
        self.timeout = settings.recaptcha_timeout
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=10))

    async def health_check(self) -> dict:
        try:
            response = await self.client.get(f"{self.server_url}/health")
            return {
                "available": response.status_code == 200,
                "server_url": self.server_url,
                "version": "0.1.0",
                "engine": "drissionpage",
                "status": "healthy" if response.status_code == 200 else "degraded",
                "test_keys_available": True,
            }
        except Exception as e:
            return {
                "available": False,
                "server_url": self.server_url,
                "version": "0.1.0",
                "engine": "drissionpage",
                "status": "unavailable",
                "error": str(e),
                "note": "reCAPTCHA testing requires a Linux server with DrissionPage and ffmpeg. "
                "Deploy the backend on Railway or a VPS.",
                "test_keys_available": True,
                "manual_mode": True,
            }

    async def test_recaptcha(self, url: str, site_key: str | None = None, timeout: int | None = None) -> dict:
        validate_url(url)

        start = time.time()
        effective_site_key = site_key or TEST_SITE_KEY

        try:
            response = await self.client.post(
                f"{self.server_url}/solve",
                json={"url": url, "site_key": effective_site_key},
                timeout=timeout or self.timeout,
            )
            elapsed_ms = int((time.time() - start) * 1000)
            data = response.json()

            return {
                "success": response.status_code == 200 and data.get("success", False),
                "target": url,
                "token": data.get("token"),
                "response_time_ms": elapsed_ms,
                "error": data.get("error"),
                "detected": data.get("detected", False),
            }
        except httpx.TimeoutException:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": "Request timed out",
                "manual_mode_available": True,
            }
        except Exception as e:
            return {
                "success": False,
                "target": url,
                "response_time_ms": int((time.time() - start) * 1000),
                "error": str(e),
                "manual_mode_available": True,
            }

    async def verify_token(self, token: str, secret_key: str | None = None) -> dict:
        effective_secret = secret_key or TEST_SECRET_KEY

        try:
            response = await self.client.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    "secret": effective_secret,
                    "response": token,
                },
                timeout=10,
            )
            data = response.json()

            return {
                "success": data.get("success", False),
                "score": data.get("score"),
                "action": data.get("action"),
                "error_codes": data.get("error-codes", []),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    async def check_displayed(self, url: str) -> dict:
        validate_url(url)

        try:
            response = await self.client.post(
                f"{self.server_url}/check",
                json={"url": url},
                timeout=15,
            )
            data = response.json()

            return {
                "success": True,
                "target": url,
                "captcha_displayed": data.get("displayed", False),
                "captcha_type": data.get("type", "unknown"),
            }
        except Exception as e:
            return {
                "success": False,
                "target": url,
                "error": str(e),
                "note": "Cannot check CAPTCHA display without browser engine",
            }

    async def close(self):
        await self.client.aclose()


recaptcha_adapter = RecaptchaAdapter()
