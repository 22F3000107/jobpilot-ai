from flask import Blueprint, request, jsonify
from datetime import date
from models import db, Application

applications_bp = Blueprint("applications", __name__)

VALID_STATUSES = [
    "Applied",
    "Assessment",
    "Interview",
    "Offer",
    "Rejected",
]


# GET: Retrieve all applications
@applications_bp.route("/", methods=["GET"])
def get_applications():
    applications = Application.query.order_by(
        Application.applied_at.desc()
    ).all()

    return jsonify([app.to_dict() for app in applications]), 200


# POST: Add a new application
@applications_bp.route("/", methods=["POST"])
def create_application():
    data = request.get_json() or {}

    required_fields = ["job_id", "title", "company"]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": f"{field} is required"
            }), 400

      
    # Prevent duplicate applications for the same job
    existing_application = Application.query.filter_by(
        job_id=data["job_id"]
    ).first()

    if existing_application:
        return jsonify({
            "message": "This job is already in your applications.",
            "application": existing_application.to_dict(),
        }), 409
        

    
    application = Application(
        job_id=data["job_id"],
        title=data["title"],
        company=data["company"],
        location=data.get("location"),
        job_type=data.get("job_type"),
        status="Applied",
        notes=data.get("notes"),
        follow_up_date=(
           date.fromisoformat(data["follow_up_date"])
           if data.get("follow_up_date")
           else None
        ),
        apply_url=data.get("apply_url"),
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application added successfully",
        "application": application.to_dict(),
    }), 201


# PATCH: Update application status or notes
@applications_bp.route("/<int:application_id>", methods=["PATCH"])
def update_application(application_id):
    application = db.session.get(Application, application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    data = request.get_json() or {}

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return jsonify({
                "message": "Invalid status",
                "valid_statuses": VALID_STATUSES,
            }), 400

        application.status = data["status"]

    if "notes" in data:
        application.notes = data["notes"]

    if "follow_up_date" in data:
        try:
            application.follow_up_date = (
              date.fromisoformat(data["follow_up_date"])
              if data["follow_up_date"]
              else None
            )
        except (ValueError, TypeError):
            return jsonify({
               "message": "Invalid follow-up date. Use YYYY-MM-DD format."
            }), 400

    db.session.commit()

    return jsonify({
        "message": "Application updated successfully",
        "application": application.to_dict(),
    }), 200


# DELETE: Remove an application
@applications_bp.route("/<int:application_id>", methods=["DELETE"])
def delete_application(application_id):
    application = db.session.get(Application, application_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    db.session.delete(application)
    db.session.commit()

    return jsonify({
        "message": "Application deleted successfully"
    }), 200