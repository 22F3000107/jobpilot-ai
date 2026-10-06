from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import os
import re
import requests


load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

jobs_bp = Blueprint("jobs", __name__)

KNOWN_SKILLS = [
    # Programming
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",

    # Data / Analytics
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Data Analysis",
    "Data Analytics",
    "Data Science",
    "Statistics",
    "Business Analysis",
    "Business Intelligence",
    "Data Visualization",
    "Reporting",
    "Dashboard",
    "ETL",

    # Python / Data Libraries
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Seaborn",
    "Scikit-learn",
    "XGBoost",
    "LightGBM",
    "SciPy",

    # Machine Learning / AI
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Generative AI",
    "GenAI",
    "NLP",
    "Natural Language Processing",
    "Computer Vision",
    "OpenCV",
    "TensorFlow",
    "PyTorch",
    "LLM",
    "Large Language Models",
    "RAG",

    # Backend / Web
    "Flask",
    "FastAPI",
    "Django",
    "REST API",
    "REST APIs",
    "HTML",
    "CSS",
    "Vue.js",
    "React",
    "Node.js",

    # Databases
    "MySQL",
    "PostgreSQL",
    "SQLite",
    "MongoDB",
    "Redis",

    # Big Data
    "Spark",
    "Hadoop",
    "BigQuery",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",

    # Development Tools
    "Git",
    "GitHub",
    "Jira",
]



def extract_skills(text):
    text = text or ""
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        skill_lower = skill.lower()

        # Exact phrase / word-boundary match
        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def extract_experience(text):
    text = text or ""
    lower_text = text.lower()

    # Fresher / entry-level indicators
    fresher_terms = [
        "fresher",
        "freshers",
        "fresh graduate",
        "fresh graduates",
        "recent graduate",
        "recent graduates",
        "entry-level",
        "entry level",
        "no experience required",
        "without experience",
        "0 years",
        "0.00 years",
        "0-1 years",
        "0–1 years",
        "0 to 1 years",
        "0.00-1.00 years",
        "0.00–1.00 years",
    ]

    if any(term in lower_text for term in fresher_terms):
        return "Fresher"

    # Experience ranges such as:
    # 3-6 years
    # 0.00-1.00 years
    # 2 to 5 years
    range_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:-|–|to)\s*"
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        lower_text,
    )

    if range_match:
        min_years = range_match.group(1)
        max_years = range_match.group(2)

        if float(max_years) <= 1:
            return "Fresher"

        return f"{min_years}-{max_years} years"

    # Expressions such as:
    # 5+ years
    # 2+ yrs
    plus_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\b",
        lower_text,
    )

    if plus_match:
        return f"{plus_match.group(1)}+ years"

    # Expressions such as:
    # 2 years experience
    # 2 years of experience
    # minimum 2 years
    # at least 2 years
    single_match = re.search(
        r"(?:minimum|min|at least|"
        r"experience|experienced|"
        r"requires?|required)"
        r"[^.\n]{0,50}?"
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        lower_text,
    )

    if single_match:
        years = float(single_match.group(1))

        if years <= 1:
            return "Fresher"

        return f"{years:g}+ years"

    return "Not specified"

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



def normalize_contract_type(job):
    contract_time = job.get("contract_time")
    contract_type = job.get("contract_type")

    if contract_time == "full_time":
        return "Full-time"

    if contract_time == "part_time":
        return "Part-time"

    if contract_type == "contract":
        return "Contract"

    if contract_type == "permanent":
        return "Full-time"

    return "Other"

def fetch_adzuna_jobs(keyword="", location=""):
    """
    Fetch jobs from Adzuna and convert them
    into JobPilot's internal job format.
    """

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return []

    url = (
        "https://api.adzuna.com/v1/api/jobs/in/search/1"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 20,
        "content-type": "application/json",
    }

    if keyword:
        params["what"] = keyword

    if location:
        params["where"] = location

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        normalized_jobs = []

        for job in data.get("results", []):
            company = job.get("company") or {}
            job_location = job.get("location") or {}

            description = job.get("description", "")
            title = job.get("title", "")
            print("\n==============================")
            print("JOB:", title)
            print("COMPANY:", company.get("display_name", "Unknown Company"))
            print("DESCRIPTION:")
            print(description)
            print("LOWER DESCRIPTION:")
            print(description.lower())
            print("==============================\n")
            skills = extract_skills(f"{title} {description}")
            print("EXTRACTED SKILLS:", skills)

            normalized_jobs.append({
               "id": f"adzuna-{job.get('id')}",
               "title": title,
                "company": company.get(
                    "display_name",
                    "Unknown Company"
                ),
                "location": job_location.get(
                    "display_name",
                    "Unknown Location"
                ),
                "job_type": normalize_contract_type(job),
                "experience": extract_experience(description),
                "skills": skills,
                "match_score": 0,
                "apply_url": job.get("redirect_url", ""),
                "description": job.get("description", ""),
                "source": "Adzuna",
                "created": job.get("created"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
            })

        return normalized_jobs

    except requests.RequestException as error:
        print(f"Adzuna API error: {error}")
        return []

# Get all jobs
@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    keyword = request.args.get(
        "keyword",
        "data analyst"
    )

    location = request.args.get(
        "location",
        "Bengaluru"
    )

    external_jobs = fetch_adzuna_jobs(
        keyword=keyword,
        location=location,
    )

    # Keep only roles relevant to your target careers
    relevant_terms = [
        "data analyst",
        "data scientist",
        "business analyst",
        "machine learning",
        "python developer",
        "data engineer",
        "ai engineer",
        "software engineer",
        "software developer",
        "bi analyst",
    ]

    filtered_jobs = [
        job for job in external_jobs
        if any(
            term in job["title"].lower()
            for term in relevant_terms
        )
    ]

    if filtered_jobs:
        return jsonify({
            "success": True,
            "source": "Adzuna",
            "total": len(filtered_jobs),
            "jobs": filtered_jobs,
        })

    return jsonify({
        "success": True,
        "source": "Sample",
        "total": len(jobs_data),
        "jobs": jobs_data,
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


@jobs_bp.route("/external", methods=["GET"])
def get_external_jobs():
    keyword = request.args.get("keyword", "data analyst")
    location = request.args.get("location", "Bengaluru")

    jobs = fetch_adzuna_jobs(
        keyword=keyword,
        location=location,
    )

    return jsonify({
        "success": True,
        "source": "Adzuna",
        "total": len(jobs),
        "jobs": jobs,
    })