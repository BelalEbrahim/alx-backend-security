from django.utils.timezone import now
from .models import RequestLog


class IPLoggingMiddleware:
    """Middleware to log IP address, timestamp, and path of each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client IP
        ip_address = self.get_client_ip(request)
        path = request.path

        # Save log to DB
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=path
        )

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP, considering possible proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # In case of multiple IPs, take the first one
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
