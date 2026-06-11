"""Locust load test for the METHEAN API.

Simulates a parent session across the weighted real surface: heavy on
the learn-context fetch and the two dashboards, lighter on governance
and curriculum reads, light on the family record. Each simulated user
registers once in on_start (cookie auth, the same flow the frontend
uses) and seeds one child with one approved activity so every read
endpoint returns real work, not empty-table fast paths.

Canonical run (documented in docs/load-test-results.md):

  cd backend
  pip install locust
  locust -f scripts/load_test.py --host http://localhost:8000 \
    --headless -u 100 -r 10 --run-time 60s
"""

import time

from locust import HttpUser, between, task


class MetheanParent(HttpUser):
    wait_time = between(1, 3)

    child_id = None
    activity_id = None

    def _headers(self):
        return {"Content-Type": "application/json", **self._csrf}

    def on_start(self) -> None:
        """Register a fresh household and seed one child plus one
        approved activity through the public API, exactly as the app
        would."""
        self._csrf = {}
        email = f"load-{time.time_ns()}@test.methean.app"
        resp = self.client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "password": "LoadTest123!",
                "household_name": "Load Test Family",
                "display_name": "Load Tester",
            },
            name="POST /auth/register (login)",
        )
        if resp.status_code not in (200, 201):
            self.client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": "LoadTest123!"},
                name="POST /auth/login",
            )
        csrf = self.client.cookies.get("csrf_token")
        if csrf:
            self._csrf = {"X-CSRF-Token": csrf}

        child = self.client.post(
            "/api/v1/children",
            json={"first_name": "Loady"},
            headers=self._headers(),
            name="(seed) POST /children",
        ).json()
        self.child_id = child.get("id")

        subject = self.client.post(
            "/api/v1/subjects",
            json={"name": "Mathematics"},
            headers=self._headers(),
            name="(seed) POST /subjects",
        ).json()
        lmap = self.client.post(
            "/api/v1/learning-maps",
            json={"subject_id": subject.get("id"), "name": "Load Map"},
            headers=self._headers(),
            name="(seed) POST /learning-maps",
        ).json()
        node = self.client.post(
            f"/api/v1/learning-maps/{lmap.get('id')}/nodes",
            json={"node_type": "concept", "title": "Load Node"},
            headers=self._headers(),
            name="(seed) POST /nodes",
        ).json()

        today = time.strftime("%Y-%m-%d")
        activity = self.client.post(
            "/api/v1/activities",
            json={
                "child_id": self.child_id,
                "title": "Load practice",
                "activity_type": "practice",
                "scheduled_date": today,
                "estimated_minutes": 20,
                "node_id": node.get("id"),
            },
            headers=self._headers(),
            name="(seed) POST /activities",
        ).json()
        self.activity_id = activity.get("id")

    # Weighted read surface: learn context and dashboards heavy,
    # governance and curriculum medium, record and health light.

    @task(5)
    def learn_context(self) -> None:
        if not self.activity_id:
            return
        self.client.get(
            f"/api/v1/activities/{self.activity_id}/learn?child_id={self.child_id}",
            name="GET /activities/{id}/learn",
        )

    @task(4)
    def child_dashboard(self) -> None:
        if not self.child_id:
            return
        self.client.get(
            f"/api/v1/children/{self.child_id}/dashboard",
            name="GET /children/{id}/dashboard",
        )

    @task(3)
    def parent_dashboard_aggregate(self) -> None:
        """The parent dashboard's primary aggregate reads."""
        self.client.get("/api/v1/children", name="GET /children")
        if self.child_id:
            self.client.get(
                f"/api/v1/children/{self.child_id}/today",
                name="GET /children/{id}/today",
            )

    @task(2)
    def governance_queue(self) -> None:
        self.client.get("/api/v1/governance/queue?limit=10", name="GET /governance/queue")

    @task(2)
    def annual_curriculum_read(self) -> None:
        if not self.child_id:
            return
        self.client.get(
            f"/api/v1/children/{self.child_id}/curricula",
            name="GET /children/{id}/curricula",
        )

    @task(1)
    def family_record_read(self) -> None:
        if not self.child_id:
            return
        self.client.get(
            f"/api/v1/children/{self.child_id}/family-record",
            name="GET /children/{id}/family-record",
        )

    @task(1)
    def health(self) -> None:
        self.client.get("/health", name="GET /health")
