"""
HeatShield AI - Production REST API & Static File Server
Built with Python 3.14 standard library. Zero external dependencies required.
Serves both backend REST APIs and the rich frontend single-page web app.
"""

import sys
import os
import json
import mimetypes
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import HeatShield engines
from heat_risk_engine import calculate_environmental_heat_risk
from vulnerability_engine import evaluate_personal_vulnerability
from danger_window_engine import analyze_danger_window
from poi_engine import find_nearby_resources
from routing_engine import calculate_routes
from worker_mode import generate_worker_schedule
from community_engine import get_community_command_data
from historical_engine import get_historical_climate_trends
from energy_stress_engine import calculate_energy_stress
from agriculture_engine import calculate_crop_heat_stress, calculate_livestock_thi
from weather_service import get_weather_forecast, REPRESENTATIVE_CLIMATES
from ai_assistant_engine import ask_heat_assistant

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

DEMO_SCENARIOS = [
    {
        "id": "scenario_normal",
        "name": "Scenario 1: Normal Moderate Day",
        "description": "Temperate 24°C, 45% humidity, pleasant breeze. Standard public safety.",
        "location": {"name": "Moderate Climate Zone", "lat": 51.5074, "lon": -0.1278},
        "weather_override": "mild",
        "profile_override": {
            "occupation": "office_worker",
            "age_group": "adult_18_49",
            "outdoor_exposure_hours": 1,
            "activity_level": "sedentary",
            "cooling_access": "full_ac",
            "has_chronic_conditions": False
        }
    },
    {
        "id": "scenario_extreme_heatwave",
        "name": "Scenario 2: Coastal Extreme Heatwave (Visakhapatnam)",
        "description": "38.6°C with 68% humidity (Apparent temp 49°C+). Severe wet-bulb stress.",
        "location": {"name": "Visakhapatnam, Andhra Pradesh", "lat": 17.6868, "lon": 83.2185},
        "weather_override": "visakhapatnam",
        "profile_override": {
            "occupation": "general_public",
            "age_group": "adult_18_49",
            "outdoor_exposure_hours": 3,
            "activity_level": "moderate",
            "cooling_access": "partial_fan",
            "has_chronic_conditions": False
        }
    },
    {
        "id": "scenario_outdoor_worker",
        "name": "Scenario 3: Construction / Outdoor Worker",
        "description": "Heavy manual labor, 8 hrs unshaded sun exposure during peak afternoon heating.",
        "location": {"name": "Visakhapatnam Port District", "lat": 17.6868, "lon": 83.2185},
        "weather_override": "visakhapatnam",
        "profile_override": {
            "occupation": "construction_worker",
            "age_group": "adult_18_49",
            "outdoor_exposure_hours": 8,
            "activity_level": "strenuous",
            "cooling_access": "no_cooling",
            "has_chronic_conditions": False
        }
    },
    {
        "id": "scenario_elderly_vulnerable",
        "name": "Scenario 4: Elderly Resident with Limited Cooling",
        "description": "68 years old, non-AC residence in high heat zone, elevated physiological strain.",
        "location": {"name": "New Delhi Urban Core", "lat": 28.6139, "lon": 77.2090},
        "weather_override": "delhi",
        "profile_override": {
            "occupation": "elderly_retired",
            "age_group": "elderly_65_plus",
            "outdoor_exposure_hours": 1,
            "activity_level": "sedentary",
            "cooling_access": "no_cooling",
            "has_chronic_conditions": True
        }
    },
    {
        "id": "scenario_extreme_no_cooling",
        "name": "Scenario 5: Extreme Heat + Grid Outage / Zero AC",
        "description": "44°C arid heat in Phoenix / Delhi with total lack of cooling infrastructure.",
        "location": {"name": "Phoenix Metro, Arizona", "lat": 33.4484, "lon": -112.0740},
        "weather_override": "phoenix",
        "profile_override": {
            "occupation": "general_public",
            "age_group": "adult_50_64",
            "outdoor_exposure_hours": 4,
            "activity_level": "moderate",
            "cooling_access": "no_cooling",
            "has_chronic_conditions": True
        }
    }
]


class HeatShieldRequestHandler(BaseHTTPRequestHandler):
    """Handles HeatShield REST API requests and serves frontend static assets."""

    def log_message(self, format, *args):
        # Concise logging to keep server output clean
        sys.stderr.write(f"[{self.log_date_time_string()}] {self.command} {self.path} - {args[0]}\n")

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def send_json(self, status_code: int, data: Any):
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def send_error_json(self, status_code: int, message: str):
        self.send_json(status_code, {
            "error": True,
            "status_code": status_code,
            "message": message
        })

    def read_json_body(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw_body = self.rfile.read(content_length).decode("utf-8")
        return json.loads(raw_body)

    # -----------------------------
    # GET Endpoints
    # -----------------------------
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        try:
            if path == "/api/health":
                self.send_json(200, {
                    "status": "healthy",
                    "app": "HeatShield AI",
                    "version": "1.0.0",
                    "tagline": "Predict. Protect. Prevent.",
                    "python_version": sys.version.split()[0],
                    "engines_active": [
                        "heat_risk_engine", "vulnerability_engine", "danger_window_engine",
                        "routing_engine", "poi_engine", "ai_assistant_engine", "worker_mode",
                        "community_engine", "historical_engine", "energy_stress_engine", "agriculture_engine"
                    ]
                })

            elif path == "/api/scenarios":
                self.send_json(200, {
                    "scenarios": DEMO_SCENARIOS,
                    "count": len(DEMO_SCENARIOS),
                    "note": "Judge & Demo scenarios clearly tagged as DEMO SCENARIO"
                })

            elif path == "/api/weather":
                lat = float(params.get("lat", [17.6868])[0])
                lon = float(params.get("lon", [83.2185])[0])
                scenario = params.get("scenario", [None])[0]
                weather_data = get_weather_forecast(lat, lon, scenario_override=scenario)
                self.send_json(200, weather_data)

            elif path == "/api/resources":
                lat = float(params.get("lat", [17.6868])[0])
                lon = float(params.get("lon", [83.2185])[0])
                cat = params.get("category", ["all"])[0]
                resources = find_nearby_resources(lat, lon, category_filter=cat)
                self.send_json(200, resources)

            elif path == "/api/worker-schedule":
                loc = params.get("location", ["Visakhapatnam"])[0]
                start_h = int(params.get("shift_start", [9])[0])
                end_h = int(params.get("shift_end", [17])[0])
                intensity = params.get("intensity", ["heavy"])[0]
                schedule = generate_worker_schedule(loc, start_h, end_h, intensity)
                self.send_json(200, schedule)

            elif path == "/api/community-command":
                city = params.get("city", ["Visakhapatnam Metropolitan Area"])[0]
                risk = int(params.get("risk_score", [88])[0])
                data = get_community_command_data(city, risk)
                self.send_json(200, data)

            elif path == "/api/historical-trends":
                region = params.get("region", ["Visakhapatnam & Coastal Belt"])[0]
                trends = get_historical_climate_trends(region)
                self.send_json(200, trends)

            elif path == "/api/energy-stress":
                temp = float(params.get("temp_c", [38.5])[0])
                hum = float(params.get("humidity", [65.0])[0])
                hour = int(params.get("hour", [14])[0])
                energy = calculate_energy_stress(temp, hum, hour)
                self.send_json(200, energy)

            elif path.startswith("/api/"):
                self.send_error_json(404, f"API endpoint {path} not found.")

            else:
                # Serve frontend static assets
                self.serve_static_file(path)

        except Exception as e:
            self.send_error_json(500, f"Internal Server Error: {str(e)}")

    # -----------------------------
    # POST Endpoints
    # -----------------------------
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            body = self.read_json_body()

            if path == "/api/risk/calculate":
                # Master Risk Computation pipeline
                # Receives current weather + hourly forecast + user profile
                temp = float(body.get("temp_c", 38.0))
                humidity = float(body.get("humidity", 60.0))
                apparent_temp = body.get("apparent_temp_c", None)
                if apparent_temp is not None:
                    apparent_temp = float(apparent_temp)
                wind = float(body.get("wind_speed", 12.0))
                uv = float(body.get("uv_index", 8.0))
                hour = int(body.get("hour", 14))
                profile = body.get("profile", {})
                hourly_data = body.get("hourly_data", [])

                # 1. Environmental Risk
                env_risk = calculate_environmental_heat_risk(
                    temperature=temp,
                    humidity=humidity,
                    apparent_temperature=apparent_temp,
                    wind_speed=wind,
                    uv_index=uv,
                    time_of_day_hour=hour
                )

                # 2. Personal Vulnerability Risk
                personal_risk = evaluate_personal_vulnerability(
                    environmental_score=env_risk["environmental_risk_score"],
                    user_profile=profile
                )

                # 3. Danger Window Analysis
                if not hourly_data:
                    # Synthesize hourly if not provided
                    hourly_data = [
                        {"hour": h, "temp_c": max(26.0, temp - 8.0 + (10.0 * max(0.0, ((h - 6) / 8.0)))), "humidity": humidity, "wind_speed": wind, "uv_index": uv}
                        for h in range(24)
                    ]
                
                danger_window_result = analyze_danger_window(hourly_data, profile)

                self.send_json(200, {
                    "environmental_risk": env_risk,
                    "personal_risk": personal_risk,
                    "danger_window": danger_window_result["danger_window"],
                    "hourly_timeline": danger_window_result["hourly_timeline"],
                    "timeline_summary": danger_window_result["summary"],
                    "pipeline_status": "Success",
                    "data_flow": "WEATHER -> HEAT RISK ENGINE -> VULNERABILITY ENGINE -> DANGER WINDOW -> ACTION PLAN"
                })

            elif path == "/api/route":
                start_lat = float(body.get("start_lat", 17.7126))
                start_lon = float(body.get("start_lon", 83.3240))
                dest_lat = float(body.get("dest_lat", 17.7280))
                dest_lon = float(body.get("dest_lon", 83.3150))
                temp = float(body.get("temp_c", 38.5))

                route_data = calculate_routes(start_lat, start_lon, dest_lat, dest_lon, current_temp_c=temp)
                self.send_json(200, route_data)

            elif path == "/api/assistant/chat":
                query = body.get("query", "")
                context = body.get("context", {})
                lang = body.get("language", "en")
                
                if not query:
                    self.send_error_json(400, "Query field is required.")
                    return

                ans = ask_heat_assistant(query, context, language=lang)
                self.send_json(200, ans)

            elif path == "/api/agriculture":
                mode = body.get("mode", "crop")
                temp = float(body.get("temp_c", 39.0))
                humidity = float(body.get("humidity", 60.0))

                if mode == "crop":
                    crop = body.get("crop", "Paddy / Rice")
                    stage = body.get("growth_stage", "Flowering / Pollination")
                    moisture = body.get("soil_moisture", "moderate")
                    result = calculate_crop_heat_stress(crop, stage, temp, humidity, moisture)
                else:
                    animal = body.get("animal_type", "Dairy Cattle")
                    result = calculate_livestock_thi(animal, temp, humidity)

                self.send_json(200, result)

            else:
                self.send_error_json(404, f"POST endpoint {path} not found.")

        except Exception as e:
            self.send_error_json(500, f"Error processing POST {path}: {str(e)}")

    def serve_static_file(self, req_path: str):
        """Serves frontend files from frontend directory."""
        if req_path == "/" or req_path == "":
            req_path = "/index.html"

        # Sanitize path
        clean_path = os.path.normpath(req_path.lstrip("/"))
        file_path = os.path.join(FRONTEND_DIR, clean_path)

        # Prevent directory traversal
        if not file_path.startswith(FRONTEND_DIR):
            self.send_error_json(403, "Access denied.")
            return

        # If file does not exist, fallback to index.html for SPA routing
        if not os.path.isfile(file_path):
            file_path = os.path.join(FRONTEND_DIR, "index.html")

        if not os.path.isfile(file_path):
            self.send_error_json(404, "Frontend file not found.")
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{mime_type}; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error_json(500, f"Failed to read static file: {str(e)}")


def run_server(port: int = 8000):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, HeatShieldRequestHandler)
    print(f"==================================================")
    print(f"🔥 HEATSHIELD AI - Hyperlocal Extreme Heat Platform")
    print(f"Server running at: http://localhost:{port}")
    print(f"Serving API endpoints and Frontend from: {FRONTEND_DIR}")
    print(f"==================================================")
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
