import unittest
from datetime import datetime, timezone, timedelta

from routes.jobs import is_job_within_date_range


class TestJobFreshness(unittest.TestCase):

    def setUp(self):
        self.now = datetime(2026, 11, 17, 12, 0, tzinfo=timezone.utc)

    def test_job_posted_2_hours_ago(self):
        posted = (self.now - timedelta(hours=2)).isoformat()
        self.assertTrue(is_job_within_date_range(posted, days=1, now=self.now))

    def test_job_posted_23_hours_ago(self):
        posted = (self.now - timedelta(hours=23)).isoformat()
        self.assertTrue(is_job_within_date_range(posted, days=1, now=self.now))

    def test_job_posted_25_hours_ago(self):
        posted = (self.now - timedelta(hours=25)).isoformat()
        self.assertFalse(is_job_within_date_range(posted, days=1, now=self.now))

    def test_future_dated_job_is_rejected(self):
        posted = (self.now + timedelta(hours=1)).isoformat()
        self.assertFalse(is_job_within_date_range(posted, days=1, now=self.now))

    def test_missing_date_is_rejected(self):
        self.assertFalse(is_job_within_date_range(None, days=1, now=self.now))

    def test_invalid_date_is_rejected(self):
        self.assertFalse(is_job_within_date_range("not-a-date", days=1, now=self.now))

    def test_naive_timestamp_is_treated_as_utc(self):
        posted = (self.now - timedelta(hours=2)).replace(tzinfo=None).isoformat()
        self.assertTrue(is_job_within_date_range(posted, days=1, now=self.now))


if __name__ == "__main__":
    unittest.main()
