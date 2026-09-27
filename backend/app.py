from flask import Flask, jsonify
from flask_cors import CORS

from routes.jobs import jobs_bp

app = Flask(__name__)

CORS(app)

# Register the jobs API
app.register_blueprint(jobs_bp, url_prefix="/api/jobs")


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to JobPilot AI API!",
        "status": "running"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)