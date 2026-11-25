from flask import Blueprint, jsonify, request
from extensions import limiter
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
import re
import requests
import time



def is_job_within_date_range(created, days=1, now=None):
    """
    Check whether a job was posted within the selected date range.
    Reject missing, invalid and future timestamps.
    """

    if not created:
        return False

    try:
        posted_date = datetime.fromisoformat(
            created.replace("Z", "+00:00")
        )

        if posted_date.tzinfo is None:
            posted_date = posted_date.replace(tzinfo=timezone.utc)

        current_time = now or datetime.now(timezone.utc)
        cutoff_date = current_time - timedelta(days=days)

        return cutoff_date <= posted_date <= current_time

    except (ValueError, TypeError, AttributeError):
        return False


load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

GREENHOUSE_BOARD_TOKENS = [
    token.strip()
    for token in os.getenv("GREENHOUSE_BOARD_TOKENS", "").split(",")
    if token.strip()
]

GREENHOUSE_CACHE = {}

jobs_bp = Blueprint("jobs", __name__)



# Cache Adzuna responses for 5 minutes
ADZUNA_CACHE = {}
CACHE_TTL = 300
MAX_CACHE_ENTRIES = 100

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

    # 1. Check explicit experience ranges first.
    # Examples: 0-1 years, 2-5 years, 3 to 6 yrs
    range_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:-|–|to)\s*"
        r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\b",
        lower_text,
    )

    if range_match:
        min_years = float(range_match.group(1))
        max_years = float(range_match.group(2))

        if max_years <= 1:
            return "Fresher"

        return f"{min_years:g}-{max_years:g} years"

    # 2. Check requirements such as 2+ years or 5+ yrs.
    plus_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*\+\s*(?:years?|yrs?)\b",
        lower_text,
    )

    if plus_match:
        years = float(plus_match.group(1))
        return f"{years:g}+ years"

    # 3. Check single experience requirements.
    # Examples: minimum 2 years, 3 years of experience,
    # experience required: 4 years.
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

    # 4. Use fresher indicators only when no numeric
    # experience requirement was found.
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
    ]

    if any(term in lower_text for term in fresher_terms):
        return "Fresher"

    return "Not specified"


if __name__ == "__main__":
    test_cases = [
        ("Entry-level role, 0-1 years of experience", "Fresher"),
        ("Minimum 2 years of experience required", "2+ years"),
        ("Experience: 3-6 years", "3-6 years"),
        ("Candidates with 5+ years experience", "5+ years"),
        ("Recent graduates welcome", "Fresher"),
        ("We are looking for a data analyst", "Not specified"),
    ]

    skill_test = """
    We are hiring a Data Analyst with Python, SQL, Excel,
    Power BI, Pandas, NumPy, and Machine Learning skills.
    Experience with data visualization and reporting is preferred.
    """

    print("SKILL TEST:", extract_skills(skill_test))

    for description, expected in test_cases:
        actual = extract_experience(description)
        result = "PASS" if actual == expected else "FAIL"

        print(
            f"{result}: {description}\n"
            f"  Expected: {expected} | Actual: {actual}"
        )
        
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

    cache_key = (keyword.strip().lower(), location.strip().lower())
    current_time = time.monotonic()

    cached = ADZUNA_CACHE.get(cache_key)

    if cached and current_time - cached["timestamp"] < CACHE_TTL:
        print("Returning cached Adzuna jobs")
        return cached["jobs"]

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


        # Remove expired entries before caching new results
        now = time.monotonic()

        expired_keys = [
            key for key, value in ADZUNA_CACHE.items()
            if now - value["timestamp"] >= CACHE_TTL
        ]

        for key in expired_keys:
            del ADZUNA_CACHE[key]

        # Evict the oldest entry when the cache is full
        if cache_key not in ADZUNA_CACHE and len(ADZUNA_CACHE) >= MAX_CACHE_ENTRIES:
            oldest_key = min(
                ADZUNA_CACHE,
                key=lambda key: ADZUNA_CACHE[key]["timestamp"]
            )
            del ADZUNA_CACHE[oldest_key]

        ADZUNA_CACHE[cache_key] = {
             "timestamp": time.monotonic(),
             "jobs": normalized_jobs,
        }

        print("Adzuna jobs cached for 5 minutes")

        return normalized_jobs

    except requests.RequestException as error:
        print(f"Adzuna API error: {error}")
        return []


def fetch_greenhouse_jobs(keyword="", location=""):
    """
    Fetch jobs from configured Greenhouse company boards
    and normalize them into JobPilot's internal format.
    """

    cache_key = (
        keyword.strip().lower(),
        location.strip().lower(),
    )

    current_time = time.monotonic()
    cached = GREENHOUSE_CACHE.get(cache_key)

    if cached and current_time - cached["timestamp"] < CACHE_TTL:
        print("Returning cached Greenhouse jobs")
        return cached["jobs"]

    normalized_jobs = []

    company_names = {
        "sahajsoftware": "Sahaj Software",
        "commerceiq": "CommerceIQ",
        "cloudflare": "Cloudflare",
        "sigmoid": "Sigmoid",
        "gitlab": "GitLab",
        "emergentlabsinc": "Emergent Labs",
    }

    keyword_terms = [
        term.lower()
        for term in keyword.split()
        if term.strip()
    ]

    for board_token in GREENHOUSE_BOARD_TOKENS:

        list_url = (
            f"https://boards-api.greenhouse.io/v1/boards/"
            f"{board_token}/jobs"
        )

        try:
            response = requests.get(
                list_url,
                params={"content": "true"},
                timeout=15,
            )
            response.raise_for_status()

            jobs = response.json().get("jobs", [])

        except (requests.RequestException, ValueError) as error:
            print(f"Greenhouse board error ({board_token}): {error}")
            continue

        for job in jobs:

            title = job.get("title") or ""

            job_location = (
                (job.get("location") or {}).get("name") or ""
            )

            description = job.get("content") or ""

            title_lower = title.lower()

            # Match all words from the requested keyword.
            if keyword_terms and not all(
               term in title_lower for term in keyword_terms
            ):
                continue

            # Match the requested location or India-eligible remote roles.
            location_lower = location.lower()
            job_location_lower = job_location.lower()

            location_matches = (
                not location
                or location_lower in job_location_lower
            )

            remote_india_eligible = (
                "remote" in job_location_lower
                and "india" in job_location_lower
            )

            if not location_matches and not remote_india_eligible:
                continue

            job_id = job.get("id")

            if not job_id:
                continue

            detail_url = f"{list_url}/{job_id}"

            try:
                detail_response = requests.get(
                    detail_url,
                    timeout=15,
                )
                detail_response.raise_for_status()

                details = detail_response.json()

            except (requests.RequestException, ValueError) as error:
                print(
                    f"Greenhouse job detail error "
                    f"({board_token}/{job_id}): {error}"
                )
                continue

            # Use original publication date, not last updated date.
            created = details.get("first_published")

            if not created:
                continue

            full_description = (
                details.get("content") or description
            )

            full_title = details.get("title") or title

            full_location = (
                (details.get("location") or {}).get("name")
                or job_location
                or "Location not specified"
            )

            normalized_jobs.append({
                "id": f"greenhouse-{board_token}-{job_id}",
                "title": full_title,
                "company": company_names.get(
                    board_token,
                    board_token,
                ),
                "location": full_location,
                "job_type": "Other",
                "experience": extract_experience(full_description),
                "skills": extract_skills(
                    f"{full_title} {full_description}"
                ),
                "match_score": 0,
                "apply_url": (
                    details.get("absolute_url")
                    or job.get("absolute_url", "")
                ),
                "description": full_description,
                "source": "Greenhouse",
                "created": created,
                "salary_min": None,
                "salary_max": None,
            })

    # Remove expired cache entries.
    now = time.monotonic()

    expired_keys = [
        key
        for key, value in GREENHOUSE_CACHE.items()
        if now - value["timestamp"] >= CACHE_TTL
    ]

    for key in expired_keys:
        del GREENHOUSE_CACHE[key]

    # Keep the cache within its configured size.
    if (
        cache_key not in GREENHOUSE_CACHE
        and len(GREENHOUSE_CACHE) >= MAX_CACHE_ENTRIES
    ):
        oldest_key = min(
            GREENHOUSE_CACHE,
            key=lambda key: GREENHOUSE_CACHE[key]["timestamp"],
        )
        del GREENHOUSE_CACHE[oldest_key]

    GREENHOUSE_CACHE[cache_key] = {
        "timestamp": time.monotonic(),
        "jobs": normalized_jobs,
    }

    print(
        f"Greenhouse: {len(normalized_jobs)} jobs fetched "
        "and cached for 5 minutes"
    )

    return normalized_jobs



# Get all jobs
@jobs_bp.route("/", methods=["GET"])
@limiter.limit("10 per minute")
def get_jobs():
    keyword = request.args.get(
        "keyword",
        "data analyst"
    )

    location = request.args.get(
        "location",
        "Bengaluru"
    )

    adzuna_jobs = fetch_adzuna_jobs(
       keyword=keyword,
       location=location,
    )

    greenhouse_jobs = fetch_greenhouse_jobs(
       keyword=keyword,
       location=location,
    )

    external_jobs = adzuna_jobs + greenhouse_jobs

    print(
        f"Job sources: Adzuna={len(adzuna_jobs)}, "
        f"Greenhouse={len(greenhouse_jobs)}, "
        f"Combined={len(external_jobs)}"
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

    


    
    # Job freshness filter: 1, 3, 7, or 30 days
    try:
        days = int(request.args.get("days", 1))
    except (ValueError, TypeError):
        days = 1

    if days not in (1, 3, 7, 30):
        days = 1


    filtered_jobs = []

    for job in external_jobs:
        title = (job.get("title") or "").lower()

        # Keep only relevant job titles.
        if not any(term in title for term in relevant_terms):
            continue

        # Validate job posting date.
        if not is_job_within_date_range(
            job.get("created"),
            days=days,
        ):
            continue

        filtered_jobs.append(job)
    

        # Deduplicate jobs using company, title, and location.
    unique_jobs = {}

    for job in filtered_jobs:
        dedup_key = (
            " ".join((job.get("company") or "").lower().split()),
            " ".join((job.get("title") or "").lower().split()),
            " ".join((job.get("location") or "").lower().split()),
        )

        existing_job = unique_jobs.get(dedup_key)

        if existing_job is None:
            unique_jobs[dedup_key] = job

        # Prefer Greenhouse because it provides a direct employer
        # application link when the same job exists on both sources.
        elif (
            job.get("source") == "Greenhouse"
            and existing_job.get("source") != "Greenhouse"
        ):
            unique_jobs[dedup_key] = job

    final_jobs = list(unique_jobs.values())

    # Identify the sources contributing to the final results.
    source_names = {
        job.get("source")
        for job in final_jobs
        if job.get("source")
    }

    source_label = " + ".join(
        source
        for source in ("Adzuna", "Greenhouse")
        if source in source_names
    ) or "Adzuna + Greenhouse"

    if final_jobs:
        return jsonify({
            "success": True,
            "source": source_label,
            "total": len(final_jobs),
            "jobs": final_jobs,
        })

    return jsonify({
        "success": True,
        "source": source_label,
        "total": 0,
        "jobs": [],
        "message": "No matching jobs found in the selected time period."
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
@limiter.limit("10 per minute")
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