from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

    education = db.Column(db.String(250))
    skills = db.Column(db.JSON, default=list)

    preferred_roles = db.Column(db.JSON, default=list)
    preferred_locations = db.Column(db.JSON, default=list)

    experience_level = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

class SavedJob(db.Model):
    __tablename__ = "saved_jobs"

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    job_type = db.Column(db.String(100))
    skills = db.Column(db.JSON)
    match_score = db.Column(db.Integer, default=0)

    saved_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "job_type": self.job_type,
            "skills": self.skills or [],
            "match_score": self.match_score,
            "saved_at": (
                self.saved_at.isoformat()
                if self.saved_at else None
            ),
        }

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # Job information
    job_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    job_type = db.Column(db.String(100))

    # Application tracking
    status = db.Column(
        db.String(50),
        nullable=False,
        default="Applied"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    notes = db.Column(db.Text)
    # Follow-up reminder date
    follow_up_date = db.Column(db.Date)

    # Optional job application link
    apply_url = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "job_type": self.job_type,
            "status": self.status,
            "applied_at": (
                self.applied_at.isoformat()
                if self.applied_at else None
            ),
            "notes": self.notes,
            "follow_up_date": (
               self.follow_up_date.isoformat()
               if self.follow_up_date else None
            ),
           "apply_url": self.apply_url,
        }

