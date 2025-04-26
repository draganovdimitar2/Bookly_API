from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging

# Set up logger
logger = logging.getLogger('uvicorn.access')

logger.disabled = True


def register_middleware(app: FastAPI):
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.perf_counter()  # High-precision timer (better precision that time.time())

        response = await call_next(request)
        processing_time = time.perf_counter() - start_time  # how long the request took to process

        message = (
            f'{request.client.host} - {request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time:.3f}s')
        print(message)
        return response
