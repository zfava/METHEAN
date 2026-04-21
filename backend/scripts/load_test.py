"""Basic load test for METHEAN API.

Usage:
  pip install locust
  locust -f scripts/load_test.py --host http://localhost:8000

Headless:
  locust -f scripts/load_test.py --host http://localhost:8000 --headless -u 100 -r 10 --run-time 60s
"""

from locust import HttpUser, between, task


class MetheanParent(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """Register and login to get auth cookies."""
        import time

        email = f"load-{time.time_ns()}@test.methean.app"
        resp = self.client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "LoadTest123!",
                "household_name": "Load Test Family",
                "display_name": "Load Tester",
            },
        )
        if resp.status_code != 201:
            # Try login
            self.client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": "LoadTest123!"},
            )

    @task(3)
    def get_health(self):
        self.client.get("/health")

    @task(2)
    def get_children(self):
        self.client.get("/api/v1/children")

    @task(2)
    def get_governance_rules(self):
        self.client.get("/api/v1/governance/rules")

    @task(1)
    def get_governance_queue(self):
        self.client.get("/api/v1/governance/queue?limit=10")

    @task(1)
    def get_subjects(self):
        self.client.get("/api/v1/subjects")

    @task(1)
    def get_notifications(self):
        self.client.get("/api/v1/notifications?limit=5")
