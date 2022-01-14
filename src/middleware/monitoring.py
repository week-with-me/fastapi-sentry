import json
import sentry_sdk
from fastapi import Request, Response, HTTPException
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)

from src.core import get_settings

sentry_sdk.init(
    dsn          = get_settings().SENTRY_DSN,
    integrations = [SqlalchemyIntegration()],
    environment  = 'DEVELOP',
    release      = '0'
)


class AsyncIteratorWrapper:
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
        with sentry_sdk.configure_scope() as scope:        
            try:
                response    = await call_next(request)
                status_code = response.__dict__['status_code']
                            
                if status_code >= 400 and status_code < 500:
                        body_encode = [
                            data async for data \
                                in response.__dict__['body_iterator']
                        ]
                        response.__setattr__(
                            'body_iterator',
                            AsyncIteratorWrapper(body_encode)
                        )                    
                        body = json.loads(body_encode[0].decode())
                        scope.set_context('request', request)
                        scope.set_context('response', body)
                        scope.user = {'IP Address': request.client.host}
                        sentry_sdk.capture_exception(
                            HTTPException(
                                status_code = status_code,
                                detail      = body['detail']
                            )
                        )
                        
                return response
            
            except Exception as error:
                scope.set_context('request', request)
                scope.user = {'IP Address': request.client.host}
                sentry_sdk.capture_exception(error)
                
                raise error
                