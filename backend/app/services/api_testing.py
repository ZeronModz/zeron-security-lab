import json
import time

import httpx
import structlog

from app.adapters.ua_adapter import get_api_headers
from app.core.config import get_settings
from app.security.validation import validate_url, ValidationError

logger = structlog.get_logger()
settings = get_settings()


class ApiTestingService:
    def __init__(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(settings.request_timeout, connect=10),
            follow_redirects=True,
        )

    async def send_request(self, request) -> dict:
        validate_url(request.url)

        if request.headers:
            headers = dict(request.headers)
        else:
            headers = get_api_headers()

        if request.auth_type and request.auth_value:
            if request.auth_type == "bearer":
                headers["Authorization"] = f"Bearer {request.auth_value}"
            elif request.auth_type == "basic":
                import base64
                cred = base64.b64encode(request.auth_value.encode()).decode()
                headers["Authorization"] = f"Basic {cred}"
            elif request.auth_type == "api_key":
                headers["X-API-Key"] = request.auth_value

        body = None
        if request.body:
            if request.body_type == "json":
                headers.setdefault("Content-Type", "application/json")
                body = request.body.encode()
            elif request.body_type == "form":
                headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
                body = request.body.encode()
            elif request.body_type == "raw":
                body = request.body.encode()

        start = time.time()
        try:
            response = await self.client.request(
                method=request.method.value,
                url=request.url,
                headers=headers,
                content=body,
                params=request.query_params or {},
            )

            elapsed_ms = int((time.time() - start) * 1000)

            response_body = response.text[:settings.max_request_size]
            try:
                response_json = response.json()
            except Exception:
                response_json = None

            return {
                "url": str(response.url),
                "status_code": response.status_code,
                "response_time_ms": elapsed_ms,
                "headers": dict(response.headers),
                "body": response_body,
                "json": response_json,
                "cookies": dict(response.cookies),
            }
        except httpx.TimeoutException:
            raise ValidationError("TIMEOUT", f"Request timed out after {request.timeout}s")
        except httpx.RequestError as e:
            raise ValidationError("REQUEST_ERROR", str(e))

    async def assert_response(self, response_data: dict, assertions) -> dict:
        results = []
        all_passed = True

        if assertions.status_code is not None:
            passed = response_data.get("status_code") == assertions.status_code
            results.append({
                "type": "status_code",
                "expected": assertions.status_code,
                "actual": response_data.get("status_code"),
                "passed": passed,
            })
            if not passed:
                all_passed = False

        for header_name, expected_value in assertions.headers_contain.items():
            actual = response_data.get("headers", {}).get(header_name.lower(), "")
            passed = expected_value.lower() in actual.lower() if actual else False
            results.append({
                "type": "header",
                "field": header_name,
                "expected": expected_value,
                "actual": actual,
                "passed": passed,
            })
            if not passed:
                all_passed = False

        for expected_text in assertions.body_contains:
            body = response_data.get("body", "")
            passed = expected_text in body
            results.append({
                "type": "body_contains",
                "expected": expected_text,
                "passed": passed,
            })
            if not passed:
                all_passed = False

        for json_path, expected_value in assertions.json_fields.items():
            json_data = response_data.get("json")
            if json_data is None:
                results.append({
                    "type": "json_field",
                    "field": json_path,
                    "expected": expected_value,
                    "actual": None,
                    "passed": False,
                })
                all_passed = False
                continue

            actual = self._get_json_value(json_data, json_path)
            passed = str(actual) == str(expected_value)
            results.append({
                "type": "json_field",
                "field": json_path,
                "expected": expected_value,
                "actual": actual,
                "passed": passed,
            })
            if not passed:
                all_passed = False

        if assertions.max_response_time_ms is not None:
            actual_time = response_data.get("response_time_ms", 0)
            passed = actual_time <= assertions.max_response_time_ms
            results.append({
                "type": "response_time",
                "expected": f"<= {assertions.max_response_time_ms}ms",
                "actual": f"{actual_time}ms",
                "passed": passed,
            })
            if not passed:
                all_passed = False

        return {"passed": all_passed, "assertions": results}

    def _get_json_value(self, data, path: str):
        parts = path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    async def close(self):
        await self.client.aclose()


api_service = ApiTestingService()
