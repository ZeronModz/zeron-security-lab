from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class ApiResponse(BaseModel):
    success: bool = True
    data: dict | list | None = None
    error: dict | None = None
    request_id: str | None = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
    database: str = "connected"
    browser: str = "unavailable"
    cloudflare: str = "unavailable"
    recaptcha: str = "unavailable"


class SystemInfo(BaseModel):
    app_name: str
    version: str
    python_version: str
    platform: str
    uptime_seconds: int
    database_type: str


class SystemCapabilities(BaseModel):
    browser_enabled: bool
    cloudflare_enabled: bool
    recaptcha_enabled: bool
    supported_methods: list[str]
    max_request_size: int
    request_timeout: int


class WebFetchRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    method: HttpMethod = HttpMethod.GET
    headers: dict[str, str] = Field(default_factory=dict)
    cookies: dict[str, str] = Field(default_factory=dict)
    body: str | None = None
    timeout: int = Field(default=30, ge=1, le=120)
    follow_redirects: bool = True
    verify_ssl: bool = True
    user_agent: str | None = Field(default=None, max_length=500)
    ua_device: str | None = Field(default="desktop", max_length=20)
    ua_browser: str | None = Field(default=None, max_length=50)


class WebFetchResponse(BaseModel):
    url: str
    status_code: int
    response_time_ms: int
    headers: dict[str, str]
    body: str
    redirect_chain: list[dict] = Field(default_factory=list)
    cookies: dict[str, str] = Field(default_factory=dict)
    security_headers: dict[str, str | None] = Field(default_factory=dict)
    used_user_agent: str | None = None
    client_hints_sent: dict[str, str] = Field(default_factory=dict)


class WebRenderRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    wait_for: str = Field(default="load", max_length=50)
    javascript_enabled: bool = True
    viewport_width: int = Field(default=1920, ge=320, le=3840)
    viewport_height: int = Field(default=1080, ge=320, le=2160)
    timeout: int = Field(default=30000, ge=1000, le=120000)


class WebRenderResponse(BaseModel):
    url: str
    title: str
    html: str
    console_errors: list[str] = Field(default_factory=list)
    network_errors: list[str] = Field(default_factory=list)
    render_time_ms: int


class ScreenshotRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    full_page: bool = False
    width: int = Field(default=1920, ge=320, le=3840)
    height: int = Field(default=1080, ge=320, le=2160)
    timeout: int = Field(default=30000, ge=1000, le=120000)


class ScreenshotResponse(BaseModel):
    url: str
    screenshot_base64: str
    width: int
    height: int
    capture_time_ms: int


class ApiRequestModel(BaseModel):
    url: str = Field(..., max_length=2048)
    method: HttpMethod = HttpMethod.GET
    headers: dict[str, str] = Field(default_factory=dict)
    query_params: dict[str, str] = Field(default_factory=dict)
    body: str | None = None
    body_type: str = Field(default="raw", max_length=20)
    auth_type: str | None = Field(default=None, max_length=20)
    auth_value: str | None = None
    timeout: int = Field(default=30, ge=1, le=120)


class ApiAssertRequest(BaseModel):
    status_code: int | None = None
    headers_contain: dict[str, str] = Field(default_factory=dict)
    body_contains: list[str] = Field(default_factory=list)
    json_fields: dict[str, str] = Field(default_factory=dict)
    max_response_time_ms: int | None = None


class ApiAssertResult(BaseModel):
    passed: bool
    assertions: list[dict]


class TestRunCreate(BaseModel):
    target_url: str = Field(..., max_length=2048)
    test_type: str = Field(..., max_length=50)
    parameters: dict = Field(default_factory=dict)


class TestRunResponse(BaseModel):
    id: str
    test_type: str
    status: str
    target_url: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


class TargetCreate(BaseModel):
    url: str = Field(..., max_length=2048)
    name: str | None = Field(default=None, max_length=200)
    description: str | None = None
    is_authorized: bool = False


class TargetResponse(BaseModel):
    id: str
    url: str
    name: str | None
    description: str | None
    is_authorized: bool
    created_at: datetime


class CloudflareTestRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    proxy: str | None = None
    timeout: int = Field(default=60, ge=5, le=180)


class CloudflareTestResponse(BaseModel):
    success: bool
    target: str
    status_code: int | None = None
    response_time_ms: int
    html: str | None = None
    cookies: dict[str, str] = Field(default_factory=dict)
    user_agent: str | None = None
    browser: dict = Field(default_factory=dict)
    error: str | None = None


class RecaptchaTestRequest(BaseModel):
    url: str = Field(..., max_length=2048)
    site_key: str | None = None
    timeout: int = Field(default=30, ge=5, le=120)


class RecaptchaTestResponse(BaseModel):
    success: bool
    target: str
    token: str | None = None
    response_time_ms: int
    error: str | None = None
    detected: bool = False


class HistoryEntry(BaseModel):
    id: str
    test_type: str
    target_url: str | None
    status: str
    status_code: int | None
    response_time_ms: int | None
    created_at: datetime
