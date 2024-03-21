from flask import Flask, Response, request
from prometheus_client import start_http_server, Counter, Histogram, Gauge, generate_latest
import time, random

app = Flask(__name__)

# Prometheus 指標
HTTP_REQUESTS_TOTAL = Counter('requests_total', 'num of total requests', ['route', 'status_code'])
HTTP_REQUESTS_IN_FLIGHT = Gauge('request_in_flight', 'num of in flight requests', ['route'])
LATENCY = Histogram('request_duration_seconds', 'Request latency', ['route'])
RESPONSE_SIZE = Histogram('response_size_bytes', 'Response size in bytes', ['route'])

@app.before_request
def before_request():
    endpoint = request.endpoint
    HTTP_REQUESTS_IN_FLIGHT.labels(route=endpoint).inc()

@app.after_request
def after_request(response):
    endpoint = request.endpoint
    HTTP_REQUESTS_IN_FLIGHT.labels(route=endpoint).dec()
    # Monitor response size
    response_size = len(response.data)
    RESPONSE_SIZE.labels(route=endpoint).observe(response_size)
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest())

@app.route('/')
@LATENCY.labels(route="/").time()
def index():
    time.sleep(random.random())
    HTTP_REQUESTS_TOTAL.labels(route="/", status_code='200').inc()
    return 'Hello, World!'

@app.route('/hello')
@LATENCY.labels(route="/hello").time()
def hello():
    status_code = random.choice([200, 404, 400, 500])
    HTTP_REQUESTS_TOTAL.labels(route="/hello", status_code=str(status_code)).inc()
    if status_code == 200:
        return 'Hello, World!', status_code
    else:
        return f'Error with status code {status_code}', status_code

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=3000)