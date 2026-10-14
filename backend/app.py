import os
from flask import Flask, jsonify
from flask_cors import CORS

from models import db, SavedJob
from routes.jobs import jobs_bp
from routes.profile import profile_bp
from routes.saved_jobs import saved_jobs_bp
from routes.applications import applications_bp

app = Flask(__name__)

app.config["DEMO_MODE"] = os.getenv("DEMO_MODE", "false").lower() == "true"

database_url = os.getenv("DATABASE_URL", "sqlite:///jobpilot.db")

# Convert PostgreSQL URL to the psycopg 3 driver
if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


frontend_origins = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173,http://127.0.0.1:5173"
).split(",")

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                origin.strip()
                for origin in frontend_origins
                if origin.strip()
            ]
        }
    }
)

db.init_app(app)

app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
app.register_blueprint(profile_bp, url_prefix="/api/profile")
app.register_blueprint(
    saved_jobs_bp,
    url_prefix="/api/saved-jobs"
)
app.register_blueprint(
    applications_bp,
    url_prefix="/api/applications"
)


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to JobPilot AI API!",
        "status": "running"
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5000)