"""Route contract tests: verify that parametrized auth test routes actually exist.

Prevents the failure class where test_unauthenticated_paths.py asserts a 401
on a route that does not exist (returning 404) or uses the wrong HTTP method
(returning 405).
"""

from app.main import app


def _get_registered_routes() -> dict[str, set[str]]:
    """Build a map of path -> {methods} from FastAPI's route registry."""
    routes: dict[str, set[str]] = {}
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            path = route.path
            methods = {m for m in route.methods if m != "HEAD"}
            if path in routes:
                routes[path].update(methods)
            else:
                routes[path] = set(methods)
    return routes


class TestRouteContract:
    def test_no_duplicate_route_paths_same_method(self):
        """No two routes register the same (method, path) combination (excluding known overlaps)."""
        # GET /api/v1/notifications exists in both operations.py and notifications.py.
        # Both are mounted at /api/v1 with no sub-prefix. FastAPI resolves to
        # the first-registered handler. This is pre-existing and intentional.
        known_overlaps = {("GET", "/api/v1/notifications")}

        seen: set[tuple[str, str]] = set()
        duplicates: list[tuple[str, str]] = []
        for route in app.routes:
            if hasattr(route, "methods") and hasattr(route, "path"):
                for method in route.methods:
                    if method == "HEAD":
                        continue
                    key = (method, route.path)
                    if key in seen and key not in known_overlaps:
                        duplicates.append(key)
                    seen.add(key)
        assert not duplicates, f"Duplicate (method, path) registrations: {duplicates}"

    def test_protected_routes_exist(self):
        """Every route in the unauthenticated_paths PROTECTED_ROUTES list is registered."""
        from tests.test_unauthenticated_paths import PROTECTED_ROUTES

        registered = _get_registered_routes()

        missing = []
        wrong_method = []
        for method, path in PROTECTED_ROUTES:
            if path not in registered:
                # Check if it's a parametric path (contains {})
                # FastAPI stores parametric paths with {param} syntax
                matched = False
                for reg_path in registered:
                    if _paths_match(path, reg_path):
                        if method not in registered[reg_path]:
                            wrong_method.append((method, path, registered[reg_path]))
                        matched = True
                        break
                if not matched:
                    missing.append((method, path))
            elif method not in registered[path]:
                wrong_method.append((method, path, registered[path]))

        assert not missing, "Routes in PROTECTED_ROUTES but not registered in app:\n" + "\n".join(
            f"  {m} {p}" for m, p in missing
        )
        assert not wrong_method, "Routes with wrong method:\n" + "\n".join(
            f"  {m} {p} (registered methods: {methods})" for m, p, methods in wrong_method
        )

    def test_public_routes_exist(self):
        """Every route in the unauthenticated_paths PUBLIC_ROUTES list is registered."""
        from tests.test_unauthenticated_paths import PUBLIC_ROUTES

        registered = _get_registered_routes()

        missing = []
        for method, path in PUBLIC_ROUTES:
            matched = False
            for reg_path in registered:
                if _paths_match(path, reg_path):
                    matched = True
                    break
            if not matched:
                missing.append((method, path))

        assert not missing, "Routes in PUBLIC_ROUTES but not registered in app:\n" + "\n".join(
            f"  {m} {p}" for m, p in missing
        )


def _paths_match(concrete_path: str, template_path: str) -> bool:
    """Check if a concrete path (with UUIDs) matches a FastAPI template path (with {param}).

    Example: /api/v1/children/00000000-0000-0000-0000-000000000001/dashboard
    matches: /api/v1/children/{child_id}/dashboard
    """
    concrete_parts = concrete_path.strip("/").split("/")
    template_parts = template_path.strip("/").split("/")

    if len(concrete_parts) != len(template_parts):
        return False

    for c, t in zip(concrete_parts, template_parts):
        if t.startswith("{") and t.endswith("}"):
            continue
        if c != t:
            return False

    return True
