import sentry_sdk
from fastapi import Request, Response
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

from src.core import get_settings

sentry_sdk.init(dsn=get_settings().SENTRY_DSN)


class SentryMiddlware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response    = await call_next(request)
            status_code = response.__dict__['status_code']
                        
            if status_code >= 400 and status_code < 500:
                with sentry_sdk.push_scope() as scope:
                    scope.set_context('request', request)
                    scope.user = {'IP Address': request.client.host}
                    sentry_sdk.capture_message(
                        f'{status_code} HTTP EXCEPTION'
                    )

            return response
        
        except Exception as error:
            with sentry_sdk.push_scope() as scope:
                scope.set_context('request', request)
                scope.user = {'IP Address': request.client.host}
                sentry_sdk.capture_exception(error)
            
            raise error
            