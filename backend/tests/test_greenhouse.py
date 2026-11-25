
import unittest
from unittest.mock import patch, Mock

from app import app
from routes.jobs import fetch_greenhouse_jobs


class TestGreenhouseIntegration(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        # Prevent cached results from affecting individual tests.
        from routes import jobs
        jobs.GREENHOUSE_CACHE.clear()

    @patch("routes.jobs.requests.get")
    def test_greenhouse_job_normalization(self, mock_get):
        list_response = Mock()
        list_response.json.return_value = {
            "jobs": [{
                "id": 12345,
                "title": "Data Scientist",
                "location": {"name": "Bengaluru, Karnataka, India"},
                "content": "Python, Machine Learning",
                "absolute_url": "https://example.com/job/12345",
            }]
        }
        list_response.raise_for_status.return_value = None

        detail_response = Mock()
        detail_response.json.return_value = {
            "id": 12345,
            "title": "Data Scientist",
            "location": {"name": "Bengaluru, Karnataka, India"},
            "first_published": "2026-11-24T10:00:00Z",
            "content": "Python and Machine Learning experience required.",
            "absolute_url": "https://example.com/job/12345",
        }
        detail_response.raise_for_status.return_value = None

        mock_get.side_effect = [list_response, detail_response]

        with patch(
            "routes.jobs.GREENHOUSE_BOARD_TOKENS",
            ["testcompany"],
        ):
            jobs = fetch_greenhouse_jobs(
                keyword="data scientist",
                location="Bengaluru",
            )

        self.assertEqual(len(jobs), 1)

        job = jobs[0]
        self.assertEqual(job["title"], "Data Scientist")
        self.assertEqual(job["company"], "testcompany")
        self.assertEqual(job["source"], "Greenhouse")
        self.assertEqual(job["created"], "2026-11-24T10:00:00Z")
        self.assertEqual(
            job["apply_url"],
            "https://example.com/job/12345",
        )
        self.assertIsNone(job["salary_min"])
        self.assertIsNone(job["salary_max"])

    @patch("routes.jobs.requests.get")
    def test_remote_non_india_job_is_excluded(self, mock_get):
        response = Mock()
        response.json.return_value = {
            "jobs": [{
                "id": 200,
                "title": "Data Scientist",
                "location": {"name": "Remote, Canada"},
            }]
        }
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        with patch(
            "routes.jobs.GREENHOUSE_BOARD_TOKENS",
            ["testcompany"],
        ):
            jobs = fetch_greenhouse_jobs(
                keyword="data scientist",
                location="Bengaluru",
            )

        self.assertEqual(jobs, [])
        self.assertEqual(mock_get.call_count, 1)

    @patch("routes.jobs.fetch_greenhouse_jobs")
    @patch("routes.jobs.fetch_adzuna_jobs")
    def test_duplicate_prefers_greenhouse(
        self,
        mock_adzuna,
        mock_greenhouse,
    ):
        adzuna_job = {
            "id": "adzuna-1",
            "title": "Data Scientist",
            "company": "Sigmoid",
            "location": "Bengaluru, Karnataka",
            "source": "Adzuna",
            "created": "2026-11-24T10:00:00Z",
        }

        greenhouse_job = {
            "id": "greenhouse-1",
            "title": "Data Scientist",
            "company": "Sigmoid",
            "location": "Bengaluru, Karnataka",
            "source": "Greenhouse",
            "created": "2026-11-24T10:00:00Z",
            "apply_url": "https://example.com/job/1",
        }

        mock_adzuna.return_value = [adzuna_job]
        mock_greenhouse.return_value = [greenhouse_job]

        response = self.client.get(
            "/api/jobs/?keyword=data%20scientist"
            "&location=Bengaluru&days=30"
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["jobs"][0]["source"], "Greenhouse")
        self.assertEqual(data["source"], "Greenhouse")

    @patch("routes.jobs.requests.get")
    def test_greenhouse_api_failure_returns_empty_list(self, mock_get):
        import requests

        mock_get.side_effect = requests.RequestException(
            "Simulated API failure"
        )

        with patch(
            "routes.jobs.GREENHOUSE_BOARD_TOKENS",
            ["testcompany"],
        ):
            jobs = fetch_greenhouse_jobs(
                keyword="data scientist",
                location="Bengaluru",
            )

        self.assertEqual(jobs, [])

    @patch("routes.jobs.requests.get")
    def test_malformed_json_returns_empty_list(self, mock_get):
        response = Mock()
        response.json.side_effect = ValueError("Invalid JSON")
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        with patch(
            "routes.jobs.GREENHOUSE_BOARD_TOKENS",
            ["testcompany"],
        ):
            jobs = fetch_greenhouse_jobs(
                keyword="data scientist",
                location="Bengaluru",
            )

        self.assertEqual(jobs, [])


if __name__ == "__main__":
    unittest.main()
