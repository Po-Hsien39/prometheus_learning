from flask import Flask, request
from flask_cors import CORS
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import time, random
import logging
from pythonjsonlogger import jsonlogger
from model import add_task, get_all_tasks, delete_task
import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import logging

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
CORS(app)

# Prometheus 指標
HTTP_REQUESTS_TOTAL = Counter('requests_total', 'num of total requests', ['route', 'status_code'])
HTTP_REQUESTS_IN_FLIGHT = Gauge('request_in_flight', 'num of in flight requests', ['route'])
LATENCY = Histogram('request_duration_seconds', 'Request latency', ['route'])
RESPONSE_SIZE = Histogram('response_size_bytes', 'Response size in bytes', ['route'])

# 設定日誌記錄器以使用 JSON 格式
logger = logging.getLogger("jsonLogger")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

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
    logger.info({'message': 'Request processed', 'route': endpoint, 'status_code': response.status_code, 'response_size': response_size})
    return response

@app.route('/')
def index():
    with LATENCY.labels(route="/").time():
        time.sleep(random.random())
        HTTP_REQUESTS_TOTAL.labels(route="/", status_code='200').inc()
        return 'Hello, World!'

@app.route('/hello')
def hello():
    with LATENCY.labels(route="/hello").time():
        status_code = random.choice([200, 404, 400, 500])
        HTTP_REQUESTS_TOTAL.labels(route="/hello", status_code=str(status_code)).inc()
        if status_code == 200:
            return 'Hello, World!', status_code
        else:
            return f'Error with status code {status_code}', status_code
    
@app.route('/todos', methods=['GET'])
def getTodo():
    result = get_all_tasks()
    res = []
    for task in result:
        res.append({"Id": task.id, "task": task.task})
    return res

@app.route('/todo', methods=['POST'])
def createTodo():
    content = request.json['content']
    if not content:
        return 'Not provide content', 400
    add_task(content)
    return "success"

@app.route('/todo', methods=['DELETE'])
def deleteTodo():
    print("=======================\n")
    id = request.json['id']
    if not id:
        return 'Not provide task id', 400
    delete_task(id)
    return "success"

if __name__ == '__main__':
    # initialize_database()
    start_http_server(8000)
    app.run(host='0.0.0.0', port=4000)