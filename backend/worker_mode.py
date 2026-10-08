"""
HeatShield AI - Outdoor Worker Safety Engine
Generates customized work-rest schedules, hydration quotas,
and occupational heat stress mitigations aligned with OSHA/NIOSH standards.
"""

from typing import Dict, Any, List, Optional
from heat_risk_engine import get_risk_category


def generate_worker_schedule(
    location_name: str = "Visakhapatnam",
    shift_start_hour: int = 9,
    shift_end_hour: int = 17,
    work_intensity: str = "heavy",  # light, moderate, heavy, extreme
    hourly_temperatures: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Computes an hourly worker safety plan across the designated shift.
    """
    if not hourly_temperatures:
        # Default representative summer afternoon curve if not supplied
        hourly_temperatures = [
            {"hour": h, "temp_c": 31.0 + (5.5 * math_sin_hour(h)), "humidity": 65 - (h * 1.5)}
            for h in range(24)
        ]

    temp_by_hour = {item["hour"]: item for item in hourly_temperatures}

    schedule_blocks = []
    total_water_liters = 0.0
    max_shift_risk_score = 0

    # Hourly progression through shift
    for h in range(shift_start_hour, shift_end_hour):
        h_data = temp_by_hour.get(h, {"temp_c": 36.0, "humidity": 60})
        temp = h_data.get("temp_c", 36.0)
        humidity = h_data.get("humidity", 60.0)

        # Base heat index for work
        base_strain = (temp - 25.0) * 3.5 + (humidity * 0.2)
        if work_intensity == "heavy":
            base_strain += 18.0
        elif work_intensity == "extreme":
            base_strain += 25.0
        elif work_intensity == "moderate":
            base_strain += 8.0

        hourly_score = max(10, min(100, int(round(base_strain))))
        if hourly_score > max_shift_risk_score:
            max_shift_risk_score = hourly_score

        cat, emoji, color = get_risk_category(hourly_score)

        # Work / Rest and Hydration calculation
        if hourly_score >= 81:
            work_rest = "20 min work / 40 min shaded rest per hour"
            water_ml = 1000
            advisory = "Halt non-essential heavy manual labor. Move all tasks under deep shade or postpone to morning."
        elif hourly_score >= 61:
            work_rest = "30 min work / 30 min shaded rest per hour"
            water_ml = 1000
            advisory = "Mandatory 30-min cooling breaks. Rotate high-exertion tasks among workers."
        elif hourly_score >= 41:
            work_rest = "45 min work / 15 min shaded rest per hour"
            water_ml = 750
            advisory = "Active caution. Enforce hydration checks every 20 minutes."
        elif hourly_score >= 21:
            work_rest = "50 min work / 10 min rest per hour"
            water_ml = 500
            advisory = "Normal operations with continuous hydration monitoring."
        else:
            work_rest = "Standard operational schedule"
            water_ml = 350
            advisory = "Baseline seasonal conditions."

        total_water_liters += (water_ml / 1000.0)

        start_str = format_worker_hour(h)
        end_str = format_worker_hour(h + 1)

        schedule_blocks.append({
            "hour_range": f"{start_str} – {end_str}",
            "hour_int": h,
            "temp_c": round(temp, 1),
            "humidity": round(humidity, 0),
            "risk_score": hourly_score,
            "risk_category": cat,
            "emoji": emoji,
            "color": color,
            "work_rest_ratio": work_rest,
            "hydration_rate": f"{water_ml} ml / hr",
            "advisory": advisory
        })

    shift_cat, shift_emoji, shift_color = get_risk_category(max_shift_risk_score)

    # General practical worker recommendations
    recommendations = [
        "Reduce strenuous activity during the peak risk hours (12:30 PM – 4:00 PM).",
        "Set up portable pop-up shade canopies with misting fans directly at the work perimeter.",
        f"Ensure every worker drinks at least {round(total_water_liters, 1)} L of water + electrolyte solution across the shift.",
        "Implement a buddy monitoring protocol: check for stumbling, slurred speech, or cessation of sweating.",
        "Ensure cold-pack first aid and shaded recovery zones are accessible within 60 seconds."
    ]

    return {
        "location": location_name,
        "shift_hours": f"{format_worker_hour(shift_start_hour)} – {format_worker_hour(shift_end_hour)}",
        "work_intensity": work_intensity.capitalize(),
        "shift_overall_risk": {
            "score": max_shift_risk_score,
            "category": shift_cat,
            "emoji": shift_emoji,
            "color": shift_color
        },
        "total_hydration_quota_liters": round(total_water_liters, 1),
        "schedule": schedule_blocks,
        "actionable_guidance": recommendations,
        "regulatory_disclaimer": "Safety recommendations are general occupational risk guidance based on NIOSH/OSHA thermal guidelines, not formal medical or legal determinations."
    }


def math_sin_hour(hour: int) -> float:
    """Simulates peak heating between 13:00 and 15:00."""
    import math
    return max(0.0, math.sin(max(0, (hour - 6)) / 14.0 * math.pi))


def format_worker_hour(hour: int) -> str:
    """Formats hour to string."""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"
