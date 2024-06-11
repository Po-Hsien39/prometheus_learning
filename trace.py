from opentelemetry.instrumentation.flask import FlaskInstrumentor
import logging
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import os
from opentelemetry import propagate

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:8027"
os.environ["OTEL_TRACES_EXPORTER"] = "console,otlp"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http"
os.environ["OTEL_SERVICE_NAME"] = "shop-order-ocr"
os.environ["OTEL_METRICS_EXPORTER"] = "none"
os.environ["OTEL_PROPAGATORS"] = "tracecontext"

set_tracer_provider(TracerProvider())
get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter())
)
get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
propagate.set_global_textmap(TraceContextTextMapPropagator())