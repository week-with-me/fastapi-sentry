import json
import sentry_sdk
from fastapi import Request, Response
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

from src.core import get_settings

sentry_sdk.init(dsn=get_settings().SENTRY_DSN, traces_sample_rate=1.0)


class AsyncInteratorWrapper:
    def __init__(self, object) -> None:
        self._iter = iter(object)
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        try:
            value = next(self._iter)
        except StopIteration:
            raise StopAsyncIteration
        return value


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
                    body_encode = [
                        data async for data \
                            in response.__dict__['body_iterator']
                    ]
                    response.__setattr__(
                        'body_iterator',
                        AsyncInteratorWrapper(body_encode)
                    )                    
                    body = json.loads(body_encode[0].decode())
                    scope.set_context('response', body)
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
            