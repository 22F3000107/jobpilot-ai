from flask import Blueprint, request, jsonify
from models import db, SavedJob

saved_jobs_bp = Blueprint("saved_jobs", __name__)


# GET: Retrieve all saved jobs
@saved_jobs_bp.route("/", methods=["GET"])
def get_saved_jobs():
    saved_jobs = SavedJob.query.order_by(
        SavedJob.saved_at.desc()
    ).all()

    return jsonify([job.to_dict() for job in saved_jobs]), 200


# POST: Save a job
@saved_jobs_bp.route("/", methods=["POST"])
def save_job():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body is required"}), 400

    required_fields = ["job_id", "title", "company"]

    for field in required_fields:
        if not data.get(field) and data.get(field) != 0:
            return jsonify({
                "message": f"{field} is required"
            }), 400

    # Prevent saving the same job twice
    existing_job = SavedJob.query.filter_by(
        job_id=data["job_id"]
    ).first()

    if existing_job:
        return jsonify({
            "message": "Job is already saved",
            "job": existing_job.to_dict()
        }), 200

    saved_job = SavedJob(
        job_id=data["job_id"],
        title=data["title"],
        company=data["company"],
        location=data.get("location", ""),
        job_type=data.get("job_type", ""),
        skills=data.get("skills", []),
        match_score=data.get("match_score", 0),
    )

    db.session.add(saved_job)
    db.session.commit()

    return jsonify({
        "message": "Job saved successfully",
        "job": saved_job.to_dict()
    }), 201


# DELETE: Remove a saved job
@saved_jobs_bp.route("/<int:saved_job_id>", methods=["DELETE"])
def delete_saved_job(saved_job_id):
    saved_job = db.session.get(SavedJob, saved_job_id)

    if not saved_job:
        return jsonify({"message": "Saved job not found"}), 404

    db.session.delete(saved_job)
    db.session.commit()

    return jsonify({
        "message": "Saved job removed successfully"
    }), 200