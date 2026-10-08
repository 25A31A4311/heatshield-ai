"""
HeatShield AI - Danger Window Engine
Analyzes hourly environmental and forecast timelines to identify
the continuous Peak Danger Window and risk progression across days.
"""

from typing import List, Dict, Any, Optional
from heat_risk_engine import calculate_environmental_heat_risk, get_risk_category
from vulnerability_engine import evaluate_personal_vulnerability


def analyze_danger_window(
    hourly_data: List[Dict[str, Any]],
    user_profile: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Inputs:
    - hourly_data: list of dicts with:
        {"time": "2026-10-08T14:00", "temp_c": 39.5, "humidity": 62, "wind_speed": 12, "uv_index": 9.2, "hour": 14}
    - user_profile: user vulnerability parameters.
    
    Returns:
    - danger_window: {"start": "12:00 PM", "end": "16:30 PM", "peak_hour": "14:00", "peak_score": 92}
    - hourly_timeline: list of processed hours with both environmental & personal scores
    - summary: descriptive danger window text
    """
    if not hourly_data:
        return {
            "danger_window": None,
            "hourly_timeline": [],
            "summary": "No hourly data available."
        }

    processed_hours = []
    high_risk_hours = []

    for item in hourly_data:
        hour_int = item.get("hour", 12)
        temp = item.get("temp_c", 30.0)
        humidity = item.get("humidity", 50.0)
        wind = item.get("wind_speed", 10.0)
        uv = item.get("uv_index", 5.0)
        apparent_temp = item.get("apparent_temp_c", None)

        env_risk = calculate_environmental_heat_risk(
            temperature=temp,
            humidity=humidity,
            apparent_temperature=apparent_temp,
            wind_speed=wind,
            uv_index=uv,
            time_of_day_hour=hour_int
        )

        pers_risk = evaluate_personal_vulnerability(
            environmental_score=env_risk["environmental_risk_score"],
            user_profile=user_profile
        )

        hour_display = format_hour_12(hour_int)
        score = pers_risk["personal_risk_score"]

        processed_entry = {
            "time_iso": item.get("time", f"T{hour_int:02d}:00"),
            "hour": hour_int,
            "hour_display": hour_display,
            "temp_c": temp,
            "apparent_temp_c": env_risk["metrics"]["apparent_temperature_c"],
            "humidity": humidity,
            "uv_index": uv,
            "wind_speed": wind,
            "env_score": env_risk["environmental_risk_score"],
            "personal_score": score,
            "category": pers_risk["risk_category"],
            "emoji": pers_risk["emoji"],
            "color": pers_risk["color"],
            "is_dangerous": score >= 50
        }
        processed_hours.append(processed_entry)

        if score >= 50:
            high_risk_hours.append(processed_entry)

    # Determine continuous danger window
    if high_risk_hours:
        start_hour = min(h["hour"] for h in high_risk_hours)
        end_hour = max(h["hour"] for h in high_risk_hours)
        peak_entry = max(high_risk_hours, key=lambda h: h["personal_score"])

        # Format window
        start_str = format_hour_12(start_hour)
        # End hour usually extends through that hour
        end_str = format_hour_12(min(23, end_hour + 1))

        danger_window = {
            "has_danger_window": True,
            "start_time": start_str,
            "end_time": end_str,
            "window_display": f"{start_str} – {end_str}",
            "peak_hour": peak_entry["hour_display"],
            "peak_score": peak_entry["personal_score"],
            "peak_temp_c": peak_entry["temp_c"],
            "peak_category": peak_entry["category"],
            "duration_hours": (end_hour - start_hour + 1),
            "severity_level": peak_entry["category"]
        }
        summary = (
            f"PEAK DANGER WINDOW: {danger_window['window_display']}. "
            f"Highest risk ({peak_entry['personal_score']}/100 - {peak_entry['category']}) expected at {peak_entry['hour_display']} "
            f"when temperatures reach {peak_entry['temp_c']}°C."
        )
    else:
        # If no hour exceeds 50, find the warmest hour
        peak_entry = max(processed_hours, key=lambda h: h["personal_score"])
        danger_window = {
            "has_danger_window": False,
            "start_time": peak_entry["hour_display"],
            "end_time": peak_entry["hour_display"],
            "window_display": "No Extreme Danger Window Expected",
            "peak_hour": peak_entry["hour_display"],
            "peak_score": peak_entry["personal_score"],
            "peak_temp_c": peak_entry["temp_c"],
            "peak_category": peak_entry["category"],
            "duration_hours": 0,
            "severity_level": peak_entry["category"]
        }
        summary = f"Conditions remain manageable today. Warmest period around {peak_entry['hour_display']} ({peak_entry['personal_score']}/100 - {peak_entry['category']})."

    return {
        "danger_window": danger_window,
        "hourly_timeline": processed_hours,
        "summary": summary
    }


def format_hour_12(hour: int) -> str:
    """Converts 24-hr integer (0-23) to 12-hr formatted string (e.g. 14 -> '2:00 PM')."""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"
