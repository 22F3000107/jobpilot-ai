# 🚀 JobPilot AI

### AI-Inspired Job Discovery & Application Tracking Platform

[🌐 Live Demo](https://jobpilot-ai-flax.vercel.app) · [💻 GitHub Repository](https://github.com/22F3000107/jobpilot-ai)

JobPilot AI is a full-stack job discovery and application tracking platform built with **Vue.js, Flask, and Python**.

It helps job seekers discover relevant opportunities, evaluate job matches, manage saved jobs, and track applications through a centralized dashboard.

The platform integrates the **Adzuna Jobs API** for external job listings and uses a rule-based matching system to evaluate opportunities against a candidate's profile.

## ✨ Key Features

- **Job Discovery:** Search external job listings using keywords, locations, and posting dates.
- **Job Matching:** Evaluate opportunities using skills, role relevance, location, and experience.
- **Match Breakdown:** Understand how different factors contribute to a job's match score.
- **Advanced Filtering:** Filter by job type, minimum match score, posting age, and remote preference.
- **Career Profile:** Manage skills, education, preferred roles, locations, and experience level.
- **Saved Jobs:** Organize interesting opportunities for later review.
- **Application Tracker:** Track applications, statuses, and progress.
- **Dashboard Analytics:** View application statistics, interview counts, and follow-up reminders.
- **Public Demo Mode:** Explore the application without modifying demo data.

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | Vue 3, JavaScript, Bootstrap 5 |
| Build Tool | Vite |
| API Client | Axios |
| Backend | Python, Flask |
| Database | SQLAlchemy, SQLite |
| PostgreSQL Support | psycopg |
| External API | Adzuna Jobs API |
| API Protection | Flask-Limiter |
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| Version Control | Git, GitHub |

## 🏗️ Architecture

```text
             JobPilot AI
                  |
          Vue 3 Frontend
             (Vercel)
                  |
             Axios HTTP
                  |
             Flask API
              (Render)
                  |
       +----------+----------+
       |          |          |
   Job Search   Profile   Application
      API         API       Tracker
       |          |          |
   Adzuna API   SQLAlchemy Database
```


The frontend communicates with the Flask REST API, which handles job discovery, profile management, saved jobs, and application tracking.



## 📁 Project Structure


```text
jobpilot-ai/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   ├── requirements.txt
│   └── routes/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## ⚙️ Local Development

### Prerequisites

- Python 3
- Node.js and npm
- Git
- Adzuna API credentials for external job searches

### 1. Clone the repository


```bash
git clone https://github.com/22F3000107/jobpilot-ai.git
cd jobpilot-ai
```


### 2. Set up the backend


```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


Create a `.env` file or export the required environment variables:


```dotenv
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
DATABASE_URL=sqlite:///jobpilot.db
FRONTEND_URL=http://localhost:5173
DEMO_MODE=false
RATELIMIT_STORAGE_URI=memory://
```


Start the Flask server:


```bash
python app.py
```


The API will run at:

`http://127.0.0.1:5000`

Health endpoint:

`http://127.0.0.1:5000/api/health`

### 3. Set up the frontend

Open another terminal:


```bash
cd jobpilot-ai/frontend
npm ci
```


Create `frontend/.env.local`:


```dotenv
VITE_API_BASE_URL=http://127.0.0.1:5000/api
VITE_DEMO_MODE=false
```


Start the frontend:


```bash
npm run dev
```


Open the local URL displayed by Vite, usually:

`http://localhost:5173`

## 🔌 API Endpoints

| Endpoint                        | Purpose                 |
| ------------------------------- | ----------------------- |
| `GET /api/health`               | Backend health check    |
| `GET /api/jobs/`                | Search job listings     |
| `GET /api/profile/`             | Retrieve career profile |
| `POST /api/profile/`            | Save career profile     |
| `GET /api/saved-jobs/`          | Retrieve saved jobs     |
| `POST /api/saved-jobs/`         | Save a job              |
| `DELETE /api/saved-jobs/<id>`   | Remove a saved job      |
| `GET /api/applications/`        | Retrieve applications   |
| `POST /api/applications/`       | Create an application   |
| `PATCH /api/applications/<id>`  | Update an application   |
| `DELETE /api/applications/<id>` | Delete an application   |

## 🔒 Public Demo Mode

The deployed version operates in read-only demo mode.

Visitors can explore job listings, match scores, dashboard statistics, and profile sections without modifying application data.

Profile updates, saved-job modifications, and application modifications are restricted by the backend when `DEMO_MODE=true`.

The public demo is intended for portfolio demonstration rather than personal multi-user account management.

## 🌍 Deployment

Frontend: Vercel

[https://jobpilot-ai-flax.vercel.app](https://jobpilot-ai-flax.vercel.app?utm_source=chatgpt.com)

Backend: Render

[https://jobpilot-ai-ivm3.onrender.com](https://jobpilot-ai-ivm3.onrender.com?utm_source=chatgpt.com)

The backend uses Gunicorn for production serving. The Render free-tier service may take additional time to respond after inactivity.

## 🔮 Future Improvements

- User authentication and individual accounts
- Personalized job recommendations
- Resume-to-job matching
- Application reminders and notifications
- More job data sources
- Improved matching and ranking algorithms

## 👨‍💻 Developer

Deepak Kumar

BS in Data Science and Applications — IIT Madras

[GitHub](https://github.com/22F3000107?utm_source=chatgpt.com) · [Live Project](https://jobpilot-ai-flax.vercel.app?utm_source=chatgpt.com)
