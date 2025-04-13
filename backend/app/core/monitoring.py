"""
Monitoring configuration for the application.
"""

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Info
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from app.core.config import settings
from app.core.logging import logger

# Define custom metrics
REQUESTS_TOTAL = Counter(
    "app_requests_total",
    "Total number of requests by path and method",
    ["path", "method"]
)

RESPONSES_TOTAL = Counter(
    "app_responses_total",
    "Total number of responses by path, method, and status code",
    ["path", "method", "status_code"]
)

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "Request duration in seconds by path and method",
    ["path", "method"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))
)

APP_INFO = Info(
    "app_info",
    "Application information"
)

def setup_monitoring(app: FastAPI) -> None:
    """
    Set up monitoring for the application.
    
    Args:
        app: FastAPI application
    """
    # Set application info
    APP_INFO.info({
        "app_name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    })
    
    # Set up Prometheus instrumentation
    instrumentator = Instrumentator()
    
    # Add default metrics
    instrumentator.add(metrics.latency())
    instrumentator.add(metrics.requests())
    instrumentator.add(metrics.requests_size())
    instrumentator.add(metrics.responses_size())
    instrumentator.add(metrics.combined_size())
    
    # Add custom metrics handler
    @instrumentator.instrument_app(app)
    def custom_metrics_handler(app: FastAPI):
        @app.middleware("http")
        async def monitor_requests(request, call_next):
            path = request.url.path
            method = request.method
            
            # Increment request counter
            REQUESTS_TOTAL.labels(path=path, method=method).inc()
            
            # Measure request duration
            with REQUEST_DURATION.labels(path=path, method=method).time():
                response = await call_next(request)
            
            # Increment response counter
            RESPONSES_TOTAL.labels(
                path=path,
                method=method,
                status_code=response.status_code
            ).inc()
            
            return response
    
    # Expose metrics endpoint
    instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)
    
    logger.info("Monitoring setup complete")
