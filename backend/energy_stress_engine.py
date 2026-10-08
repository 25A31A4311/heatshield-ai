"""
HeatShield AI - Energy Grid Stress Engine
Estimates potential peak electricity demand pressure and cooling load
strains driven by severe ambient thermal conditions.
"""

from typing import Dict, Any


def calculate_energy_stress(
    temperature_c: float,
    humidity: float,
    current_hour: int = 14
) -> Dict[str, Any]:
    """
    Computes cooling degree hours and estimated grid demand pressure.
    Peak stress typically clusters between 2:00 PM – 6:00 PM when residential
    and commercial cooling compressors peak simultaneously.
    """
    # Cooling degree index above base 24°C
    cooling_delta = max(0.0, temperature_c - 24.0)
    humidity_factor = max(0.0, (humidity - 50.0) * 0.1)
    
    # Hour multiplier: peak between 14:00 (2 PM) and 18:00 (6 PM)
    if 14 <= current_hour <= 18:
        hour_multiplier = 1.35
    elif 11 <= current_hour < 14:
        hour_multiplier = 1.15
    elif 19 <= current_hour <= 22:
        hour_multiplier = 1.20  # Evening residential surge
    else:
        hour_multiplier = 0.85

    stress_index = min(100, int(round((cooling_delta * 4.2 + humidity_factor) * hour_multiplier)))

    if stress_index >= 80:
        stress_level = "CRITICAL GRID STRAIN"
        emoji = "⚡🚨"
        color = "#DC2626"
        recommendations = [
            "Voluntary demand reduction: pre-cool indoor rooms prior to 1:30 PM, then ease thermostat to 25-26°C.",
            "Postpone heavy electrical appliances (laundry, dishwashers, water pumps) until after 7:30 PM.",
            "Municipal contingency: keep emergency backup power ready at hospitals and cooling centers."
        ]
    elif stress_index >= 55:
        stress_level = "HIGH ENERGY STRESS"
        emoji = "⚡🟠"
        color = "#F97316"
        recommendations = [
            "Anticipated peak cooling load between 2:00 PM – 6:00 PM.",
            "Set air conditioner thermostats to an energy-resilient 24°C - 26°C with ceiling fan circulation.",
            "Close blinds and curtains to diminish radiative solar load on cooling units."
        ]
    elif stress_index >= 30:
        stress_level = "MODERATE ENERGY LOAD"
        emoji = "⚡🟡"
        color = "#F59E0B"
        recommendations = [
            "Normal summer cooling demand. Grid reserves within standard operating thresholds."
        ]
    else:
        stress_level = "LOW ENERGY STRESS"
        emoji = "⚡🟢"
        color = "#10B981"
        recommendations = [
            "Baseline electrical demand. No grid thermal stress anticipated."
        ]

    return {
        "stress_level": stress_level,
        "stress_score": stress_index,
        "emoji": emoji,
        "color": color,
        "expected_peak_window": "2:00 PM – 6:00 PM",
        "cooling_demand_index": round(cooling_delta, 1),
        "guidance": recommendations,
        "disclaimer": "Informational estimate based on ambient temperature and cooling degree demand. Does not represent direct electrical utility SCADA telemetry."
    }
