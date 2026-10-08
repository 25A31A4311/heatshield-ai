"""
HeatShield AI - Server Integration Tests (Socket-Free In-Memory Harness)
Tests HeatShieldRequestHandler endpoints, routing, JSON serialization,
and error handling without requiring network sockets.
"""

import unittest
import sys
import os
import json
import io

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_dir)

from server import HeatShieldRequestHandler


class DummySocket:
    def __init__(self, data_bytes=b""):
        self.rfile = io.BytesIO(data_bytes)
        self.wfile = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        if "r" in mode:
            return self.rfile
        return self.wfile

    def sendall(self, data):
        self.wfile.write(data)


class MockServer:
    def __init__(self):
        self.server_name = "localhost"
        self.server_port = 8000


def simulate_request(method: str, path: str, body: dict = None):
    """Simulates an HTTP request against HeatShieldRequestHandler."""
    body_bytes = json.dumps(body).encode("utf-8") if body is not None else b""
    req_lines = [
        f"{method} {path} HTTP/1.1",
        "Host: localhost:8000",
        f"Content-Length: {len(body_bytes)}",
        "Content-Type: application/json",
        "",
        ""
    ]
    raw_header = "\r\n".join(req_lines).encode("utf-8")
    full_req = raw_header + body_bytes

    sock = DummySocket(full_req)
    server = MockServer()

    # Instantiate handler
    handler = HeatShieldRequestHandler(sock, ("127.0.0.1", 12345), server)
    
    # Read output
    output_bytes = sock.wfile.getvalue()
    parts = output_bytes.split(b"\r\n\r\n", 1)
    header_part = parts[0].decode("utf-8", errors="ignore")
    body_part = parts[1].decode("utf-8", errors="ignore") if len(parts) > 1 else ""

    status_line = header_part.splitlines()[0]
    status_code = int(status_line.split()[1])

    data = None
    if "application/json" in header_part:
        data = json.loads(body_part)

    return status_code, data, body_part


class TestServerHandler(unittest.TestCase):

    def test_health_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["app"], "HeatShield AI")
        self.assertIn("heat_risk_engine", data["engines_active"])

    def test_scenarios_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/scenarios")
        self.assertEqual(status, 200)
        self.assertEqual(data["count"], 5)
        self.assertEqual(data["scenarios"][0]["id"], "scenario_normal")

    def test_weather_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/weather?lat=17.6868&lon=83.2185")
        self.assertEqual(status, 200)
        self.assertIn("current", data)
        self.assertIn("hourly_data", data)

    def test_resources_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/resources?lat=17.7126&lon=83.3240")
        self.assertEqual(status, 200)
        self.assertGreater(data["total_found"], 0)
        self.assertIn("counts", data)

    def test_worker_schedule_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/worker-schedule?location=Visakhapatnam&shift_start=9&shift_end=17&intensity=heavy")
        self.assertEqual(status, 200)
        self.assertEqual(len(data["schedule"]), 8)

    def test_community_command_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/community-command?city=Visakhapatnam&risk_score=90")
        self.assertEqual(status, 200)
        self.assertEqual(data["heat_status"], "EXTREME")
        self.assertTrue(len(data["zones"]) >= 3)

    def test_risk_calculate_endpoint(self):
        body = {
            "temp_c": 40.0,
            "humidity": 65.0,
            "wind_speed": 10.0,
            "uv_index": 10.0,
            "hour": 14,
            "profile": {
                "occupation": "construction_worker",
                "age_group": "adult_18_49",
                "outdoor_exposure_hours": 7,
                "activity_level": "strenuous",
                "cooling_access": "no_cooling"
            }
        }
        status, data, _ = simulate_request("POST", "/api/risk/calculate", body)
        self.assertEqual(status, 200)
        self.assertGreaterEqual(data["personal_risk"]["personal_risk_score"], 80)
        self.assertTrue(data["danger_window"]["has_danger_window"])

    def test_route_endpoint(self):
        body = {
            "start_lat": 17.7126,
            "start_lon": 83.3240,
            "dest_lat": 17.7280,
            "dest_lon": 83.3150,
            "temp_c": 39.0
        }
        status, data, _ = simulate_request("POST", "/api/route", body)
        self.assertEqual(status, 200)
        self.assertIn("fastest_route", data)
        self.assertIn("heat_safer_route", data)

    def test_assistant_chat_endpoint(self):
        body = {
            "query": "Where can I find cooling and water?",
            "context": {
                "weather": {"current": {"temp_c": 39.0, "apparent_temp_c": 47.0, "humidity": 60}},
                "danger_window": {"window_display": "12:30 PM – 4:30 PM", "peak_hour": "2:00 PM"},
                "personal_risk": {"personal_risk_score": 88, "risk_category": "EXTREME"},
                "profile": {"occupation": "general_public"}
            },
            "language": "en"
        }
        status, data, _ = simulate_request("POST", "/api/assistant/chat", body)
        self.assertEqual(status, 200)
        self.assertIn("Cooling Shelter", data["response"])

    def test_not_found_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/nonexistent")
        self.assertEqual(status, 404)
        self.assertTrue(data["error"])

    def test_static_files_served(self):
        # Root index.html
        status, _, body = simulate_request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("HEATSHIELD AI", body)

        # styles.css
        status, _, body = simulate_request("GET", "/styles.css")
        self.assertEqual(status, 200)
        self.assertIn("--bg-dark", body)

        # app.js
        status, _, body = simulate_request("GET", "/app.js")
        self.assertEqual(status, 200)
        self.assertIn("HeatShield AI", body)

    def test_geocode_endpoint(self):
        status, data, _ = simulate_request("GET", "/api/geocode?q=hyderabad")
        self.assertEqual(status, 200)
        self.assertGreater(data["count"], 0)
        self.assertIn("Hyderabad", data["results"][0]["name"])


if __name__ == "__main__":
    unittest.main()
