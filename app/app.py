from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import random
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Home page
@app.route('/')
def home():
    return jsonify({
        "message": "AI DevOps Pipeline is LIVE!",
        "status": "healthy",
        "version": "1.0.0"
    })

# Health check - Kubernetes pings this
@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

# Simulates slow response
@app.route('/slow')
def slow():
    time.sleep(random.uniform(1.0, 3.0))
    return jsonify({"message": "Slow response simulated!"})

# Simulates error
@app.route('/error')
def error():
    return jsonify({"error": "Simulated 500 error!"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)