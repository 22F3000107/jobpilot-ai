from flask import Blueprint, request, jsonify
from models import db, UserProfile

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
def get_profile():
    profile = UserProfile.query.first()

    if not profile:
        return jsonify({"message": "No profile found"}), 404

    return jsonify({
        "id": profile.id,
        "full_name": profile.full_name,
        "email": profile.email,
        "education": profile.education,
        "skills": profile.skills or [],
        "preferred_roles": profile.preferred_roles or [],
        "preferred_locations": profile.preferred_locations or [],
        "experience_level": profile.experience_level,
    }), 200


@profile_bp.route("/", methods=["POST"])
def save_profile():
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()

    if not full_name or not email:
        return jsonify({
            "error": "Full name and email are required"
        }), 400

    profile = UserProfile.query.filter_by(email=email).first()

    if not profile:
        profile = UserProfile(
            full_name=full_name,
            email=email
        )
        db.session.add(profile)

    profile.full_name = full_name
    profile.email = email
    profile.education = data.get("education", "")
    profile.skills = data.get("skills", [])
    profile.preferred_roles = data.get("preferred_roles", [])
    profile.preferred_locations = data.get("preferred_locations", [])
    profile.experience_level = data.get("experience_level", "")

    db.session.commit()

    return jsonify({
        "message": "Profile saved successfully",
        "profile": {
            "id": profile.id,
            "full_name": profile.full_name,
            "email": profile.email,
            "education": profile.education,
            "skills": profile.skills,
            "preferred_roles": profile.preferred_roles,
            "preferred_locations": profile.preferred_locations,
            "experience_level": profile.experience_level,
        }
    }), 201