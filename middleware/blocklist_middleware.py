from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
import logging

logger = logging.getLogger("uvicorn")


class BlockListMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, blocked_ips):
        """Middleware to block requests from specific IPs."""
        super().__init__(app)
        self.blocked_ips = blocked_ips

    async def dispatch(self, request: Request, call_next):
        """Intercept the request and block it if the IP is in the blocklist."""
        ip = request.client.host
        try:
            with open("ip_addresses.txt", "r") as f:
                unique_ips = f.read().splitlines()
            if ip not in unique_ips:
                with open("ip_addresses.txt", "a") as f:
                    f.write(f"{ip}\n")
        except FileNotFoundError:
            with open("ip_addresses.txt", "a") as f:
                f.write(f"{ip}\n")

        logger.info(f"Received a request from IP: {ip}")
        if ip in self.blocked_ips:
            logger.warning(f"Blocked a request from IP: {ip}")
            return JSONResponse({"error": "Access denied."}, status_code=403)

        response = await call_next(request)
        return response
