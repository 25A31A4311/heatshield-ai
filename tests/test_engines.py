"""
HeatShield AI - Comprehensive Test Suite
Validates all deterministic engines, vulnerability modifiers,
medical safety escalation, multilingual assistant, and routing algorithms.
"""

import unittest
import sys
import os

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_dir)

from heat_risk_engine import calculate_environmental_heat_risk, get_risk_category, calculate_heat_index, calculate_swbgt
from vulnerability_engine import evaluate_personal_vulnerability
from danger_window_engine import analyze_danger_window
from routing_engine import calculate_routes
from poi_engine import find_nearby_resources, haversine_distance_km
from worker_mode import generate_worker_schedule
from community_engine import get_community_command_data
from historical_engine import get_historical_climate_trends
from energy_stress_engine import calculate_energy_stress
from agriculture_engine import calculate_crop_heat_stress, calculate_livestock_thi
from ai_assistant_engine import ask_heat_assistant, MEDICAL_DISCLAIMER


class TestHeatShieldEngines(unittest.TestCase):

    def test_risk_categories(self):
        """Verify defined risk categories and boundaries."""
        self.assertEqual(get_risk_category(15)[0], "LOW")
        self.assertEqual(get_risk_category(30)[0], "MODERATE")
        self.assertEqual(get_risk_category(50)[0], "HIGH")
        self.assertEqual(get_risk_category(75)[0], "VERY HIGH")
        self.assertEqual(get_risk_category(92)[0], "EXTREME")

    def test_heat_risk_engine_determinism(self):
        """Test environmental heat risk score calculation and multi-factor impacts."""
        # Mild day
        res_mild = calculate_environmental_heat_risk(
            temperature=22.0, humidity=40.0, wind_speed=12.0, uv_index=3.0, time_of_day_hour=10
        )
        self.assertLessEqual(res_mild["environmental_risk_score"], 25)
        self.assertIn(res_mild["risk_category"], ["LOW", "MODERATE"])

        # Severe heatwave (e.g. 42°C, 65% humidity)
        res_extreme = calculate_environmental_heat_risk(
            temperature=42.0, humidity=65.0, wind_speed=6.0, uv_index=11.0, time_of_day_hour=14
        )
        self.assertGreaterEqual(res_extreme["environmental_risk_score"], 80)
        self.assertEqual(res_extreme["risk_category"], "EXTREME")
        self.assertTrue(len(res_extreme["contributing_factors"]) > 0)
        self.assertIn("AI risk estimate", res_extreme["disclaimer"])

    def test_vulnerability_engine_differentiation(self):
        """Verify that the SAME weather conditions yield different risk scores for different profiles."""
        base_env_score = 75  # Very High ambient weather

        # Office Worker: AC, low exposure, sedentary
        office_profile = {
            "occupation": "office_worker",
            "age_group": "adult_18_49",
            "outdoor_exposure_hours": 1,
            "activity_level": "sedentary",
            "cooling_access": "full_ac",
            "has_chronic_conditions": False
        }
        res_office = evaluate_personal_vulnerability(base_env_score, office_profile)

        # Construction Worker: outdoor 8 hours, strenuous exertion, no cooling
        worker_profile = {
            "occupation": "construction_worker",
            "age_group": "adult_18_49",
            "outdoor_exposure_hours": 8,
            "activity_level": "strenuous",
            "cooling_access": "no_cooling",
            "has_chronic_conditions": False
        }
        res_worker = evaluate_personal_vulnerability(base_env_score, worker_profile)

        # Elderly Resident: 67 years old, no cooling, medical condition
        elderly_profile = {
            "occupation": "elderly_retired",
            "age_group": "elderly_65_plus",
            "outdoor_exposure_hours": 1,
            "activity_level": "sedentary",
            "cooling_access": "no_cooling",
            "has_chronic_conditions": True
        }
        res_elderly = evaluate_personal_vulnerability(base_env_score, elderly_profile)

        # Construction worker and Elderly must have significantly higher risk than Office worker
        self.assertGreater(res_worker["personal_risk_score"], res_office["personal_risk_score"])
        self.assertGreater(res_elderly["personal_risk_score"], res_office["personal_risk_score"])
        self.assertGreaterEqual(res_worker["personal_risk_score"], 85)
        self.assertTrue(len(res_worker["recommendations"]) >= 3)
        self.assertTrue(len(res_elderly["recommendations"]) >= 3)

    def test_danger_window_engine(self):
        """Test continuous peak danger window identification."""
        hourly_data = [
            {"hour": 8, "temp_c": 28.0, "humidity": 70, "apparent_temp_c": 31, "wind_speed": 10, "uv_index": 3},
            {"hour": 10, "temp_c": 33.0, "humidity": 65, "apparent_temp_c": 38, "wind_speed": 10, "uv_index": 7},
            {"hour": 12, "temp_c": 38.0, "humidity": 62, "apparent_temp_c": 47, "wind_speed": 12, "uv_index": 10},
            {"hour": 14, "temp_c": 41.5, "humidity": 58, "apparent_temp_c": 52, "wind_speed": 14, "uv_index": 11},
            {"hour": 16, "temp_c": 39.0, "humidity": 60, "apparent_temp_c": 48, "wind_speed": 12, "uv_index": 8},
            {"hour": 18, "temp_c": 34.0, "humidity": 65, "apparent_temp_c": 40, "wind_speed": 10, "uv_index": 2},
            {"hour": 20, "temp_c": 30.0, "humidity": 72, "apparent_temp_c": 34, "wind_speed": 8, "uv_index": 0}
        ]
        result = analyze_danger_window(hourly_data)
        window = result["danger_window"]
        self.assertTrue(window["has_danger_window"])
        self.assertIn("PM", window["window_display"])
        self.assertGreaterEqual(window["peak_score"], 70)
        self.assertEqual(len(result["hourly_timeline"]), len(hourly_data))

    def test_routing_engine(self):
        """Test fastest vs heat-safer route generation and exposure reduction."""
        routes = calculate_routes(
            start_lat=17.7126, start_lon=83.3240,
            dest_lat=17.7280, dest_lon=83.3150,
            current_temp_c=39.0
        )
        fastest = routes["fastest_route"]
        safer = routes["heat_safer_route"]

        self.assertLess(fastest["distance_km"], safer["distance_km"])
        self.assertGreater(fastest["heat_exposure_index"], safer["heat_exposure_index"])
        self.assertGreater(safer["shade_coverage_percent"], fastest["shade_coverage_percent"])
        self.assertGreater(safer["exposure_reduction_percent"], 25)
        self.assertTrue(len(fastest["waypoints"]) >= 2)
        self.assertTrue(len(safer["waypoints"]) >= 2)

    def test_poi_engine(self):
        """Test nearby water, cooling, and medical resources discovery."""
        res = find_nearby_resources(user_lat=17.7126, user_lon=83.3240)
        self.assertGreater(res["total_found"], 0)
        self.assertGreaterEqual(res["counts"]["water"], 1)
        self.assertGreaterEqual(res["counts"]["cooling"], 1)
        self.assertGreaterEqual(res["counts"]["medical"], 1)
        # Check distance order
        distances = [r["distance_km"] for r in res["resources"]]
        self.assertEqual(distances, sorted(distances))

    def test_medical_safety_escalation_in_assistant(self):
        """Verify strict medical safety guardrails: no fake diagnosis, immediate emergency escalation."""
        ctx = {
            "weather": {"current": {"temp_c": 41.0, "apparent_temp_c": 50.0, "humidity": 65}},
            "env_risk": {"environmental_risk_score": 90, "risk_category": "EXTREME"},
            "personal_risk": {"personal_risk_score": 95, "risk_category": "EXTREME"},
            "danger_window": {"window_display": "12:00 PM – 4:30 PM", "peak_hour": "2:00 PM"},
            "profile": {"occupation": "construction_worker"}
        }

        # Emergency symptom query
        ans = ask_heat_assistant("I feel dizzy and have vomited twice while working", ctx, language="en")
        self.assertTrue(ans["is_emergency_flagged"])
        # Must NEVER state "You have heatstroke"
        self.assertNotIn("You have heatstroke", ans["response"])
        self.assertNotIn("You have heat stroke", ans["response"])
        # Must encourage emergency help
        self.assertTrue("emergency" in ans["response"].lower() or "108" in ans["response"])
        self.assertEqual(ans["disclaimer"], MEDICAL_DISCLAIMER)

    def test_multilingual_assistant(self):
        """Verify Telugu and Hindi responses."""
        ctx = {
            "weather": {"current": {"temp_c": 39.0, "apparent_temp_c": 47.0, "humidity": 60}},
            "env_risk": {"environmental_risk_score": 85, "risk_category": "EXTREME"},
            "personal_risk": {"personal_risk_score": 88, "risk_category": "EXTREME"},
            "danger_window": {"window_display": "12:30 PM – 4:30 PM", "peak_hour": "2:00 PM"},
            "profile": {"occupation": "general_public"}
        }

        # Telugu
        ans_te = ask_heat_assistant("Can I go running at 3 PM?", ctx, language="te")
        self.assertEqual(ans_te["language"], "te")
        self.assertTrue("వ్యాయామ" in ans_te["response"] or "రన్నింగ్" in ans_te["response"] or "ప్రమాదం" in ans_te["response"])

        # Hindi
        ans_hi = ask_heat_assistant("Can I go running at 3 PM?", ctx, language="hi")
        self.assertEqual(ans_hi["language"], "hi")
        self.assertTrue("दौड़ने" in ans_hi["response"] or "जोखिम" in ans_hi["response"] or "व्यायाम" in ans_hi["response"])

    def test_worker_schedule_engine(self):
        """Test OSHA/NIOSH outdoor worker safety plan generation."""
        schedule = generate_worker_schedule(
            location_name="Visakhapatnam", shift_start_hour=9, shift_end_hour=17, work_intensity="heavy"
        )
        self.assertEqual(len(schedule["schedule"]), 8)
        self.assertGreater(schedule["total_hydration_quota_liters"], 3.0)
        self.assertTrue("work_rest_ratio" in schedule["schedule"][0])

    def test_community_command_center(self):
        """Test municipal command center micro-zone ranking."""
        data = get_community_command_data("Visakhapatnam", current_risk_score=92)
        self.assertEqual(data["heat_status"], "EXTREME")
        self.assertTrue(len(data["zones"]) >= 3)
        # Zone 1 should be highest priority
        self.assertEqual(data["zones"][0]["priority_rank"], 1)
        self.assertTrue(len(data["ai_priority_recommendations"]) >= 3)

    def test_historical_trends_and_grid_stress(self):
        """Test historical trends and cooling grid demand."""
        hist = get_historical_climate_trends("Visakhapatnam")
        self.assertEqual(len(hist["yearly_records"]), 10)
        self.assertTrue(len(hist["key_insights"]) >= 3)

        grid = calculate_energy_stress(temperature_c=42.0, humidity=60.0, current_hour=15)
        self.assertIn("GRID STRAIN", grid["stress_level"])
        self.assertEqual(grid["expected_peak_window"], "2:00 PM – 6:00 PM")

    def test_agricultural_and_livestock_modes(self):
        """Test crop heat stress and livestock THI calculation."""
        crop = calculate_crop_heat_stress("Paddy / Rice", "Flowering / Pollination", temp_c=39.5, humidity=65.0)
        self.assertGreaterEqual(crop["stress_score"], 60)
        self.assertIn("04:30 AM", crop["recommended_irrigation_window"])

        thi = calculate_livestock_thi("Dairy Cattle", temp_c=39.0, humidity=70.0)
        self.assertGreater(thi["thi_score"], 80)
        self.assertIn("STRESS", thi["status"])


if __name__ == "__main__":
    unittest.main()
