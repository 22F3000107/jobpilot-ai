from flask import Blueprint, jsonify, request

jobs_bp = Blueprint("jobs", __name__)

# Sample job listings for testing
# These are illustrative, not real job openings.
jobs_data = [
    {
        "id": 1,
        "title": "Data Analyst Intern",
        "company": "Tech Solutions",
        "location": "Bengaluru",
        "job_type": "Internship",
        "experience": "Fresher",
        "skills": ["Python", "SQL", "Excel", "Power BI"],
        "match_score": 92,
        "apply_url": "https://example.com/apply/1"
    },
    {
        "id": 2,
        "title": "Machine Learning Intern",
        "company": "AI Innovations",
        "location": "Remote",
        "job_type": "Internship",
        "experience": "Fresher",
        "skills": ["Python", "Machine Learning", "Scikit-learn"],
        "match_score": 87,
        "apply_url": "https://example.com/apply/2"
    },
    {
        "id": 3,
        "title": "Python Developer",
        "company": "Software Labs",
        "location": "Bengaluru",
        "job_type": "Full-time",
        "experience": "0-1 years",
        "skills": ["Python", "Flask", "SQL", "REST API"],
        "match_score": 85,
        "apply_url": "https://example.com/apply/3"
    },
    {
        "id": 4,
        "title": "Business Analyst Intern",
        "company": "Business Analytics Co.",
        "location": "Remote",
        "job_type": "Internship",
        "experience": "Fresher",
        "skills": ["SQL", "Excel", "Data Analysis"],
        "match_score": 80,
        "apply_url": "https://example.com/apply/4"
    }
]


# Get all jobs
@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    return jsonify({
        "success": True,
        "total": len(jobs_data),
        "jobs": jobs_data
    })


# Get a single job by ID
@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = next(
        (job for job in jobs_data if job["id"] == job_id),
        None
    )

    if not job:
        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    return jsonify({
        "success": True,
        "job": job
    })


# Search jobs
@jobs_bp.route("/search", methods=["GET"])
def search_jobs():
    keyword = request.args.get("keyword", "").lower()
    location = request.args.get("location", "").lower()
    job_type = request.args.get("job_type", "").lower()

    filtered_jobs = []

    for job in jobs_data:
        matches_keyword = (
            not keyword
            or keyword in job["title"].lower()
            or keyword in job["company"].lower()
            or any(keyword in skill.lower() for skill in job["skills"])
        )

        matches_location = (
            not location
            or location in job["location"].lower()
        )

        matches_type = (
            not job_type
            or job_type == job["job_type"].lower()
        )

        if matches_keyword and matches_location and matches_type:
            filtered_jobs.append(job)

    return jsonify({
        "success": True,
        "total": len(filtered_jobs),
        "jobs": filtered_jobs
    })