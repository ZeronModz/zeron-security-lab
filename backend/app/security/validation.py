import ipaddress
import re
from urllib.parse import urlparse

import structlog

from app.core.config import get_settings

logger = structlog.get_logger()
settings = get_settings()

BLOCKED_NETWORKS = [
    ipaddress.ip_network(net.strip()) for net in settings.blocked_networks.split(",") if net.strip()
]

PRIVATE_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "[::1]"}


class ValidationError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


def validate_url(url: str) -> str:
    if not url or not url.strip():
        raise ValidationError("INVALID_URL", "URL cannot be empty")

    url = url.strip()

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValidationError("INVALID_SCHEME", "Only HTTP and HTTPS URLs are allowed")

    if not parsed.hostname:
        raise ValidationError("INVALID_URL", "URL must have a valid hostname")

    hostname = parsed.hostname.lower()

    if hostname in PRIVATE_HOSTNAMES:
        raise ValidationError("PRIVATE_TARGET", "Targets on private/local networks are not allowed")

    try:
        ip = ipaddress.ip_address(hostname)
        for network in BLOCKED_NETWORKS:
            if ip in network:
                raise ValidationError(
                    "PRIVATE_TARGET",
                    f"IP {hostname} is in a blocked network range ({network})",
                )
    except ValueError:
        pass

    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname):
        try:
            ip = ipaddress.ip_address(hostname)
            for network in BLOCKED_NETWORKS:
                if ip in network:
                    raise ValidationError(
                        "PRIVATE_TARGET",
                        f"IP {hostname} is in a blocked network range ({network})",
                    )
        except ValueError:
            pass

    allowed = settings.allowed_targets
    if allowed and hostname not in allowed and not any(hostname.endswith(f".{t}") for t in allowed):
        raise ValidationError(
            "TARGET_NOT_ALLOWED",
            f"Target '{hostname}' is not in the allowed targets list",
        )

    return url


def is_safe_url(url: str) -> bool:
    try:
        validate_url(url)
        return True
    except ValidationError:
        return False
