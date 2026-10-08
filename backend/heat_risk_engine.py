"""
HeatShield AI - Deterministic Hyperlocal Heat Risk Engine
Calculates explainable, multi-factor environmental heat risk (0-100).
Based on Rothfusz Heat Index, Steadman Apparent Temperature,
and simplified Wet-Bulb Globe Temperature (sWBGT) models.
"""

import math
from typing import Dict, Any, List, Tuple


def calculate_heat_index(temp_c: float, humidity: float) -> float:
    """
    Computes the NOAA Heat Index using Rothfusz regression equation.
    Input: temp_c in Celsius, humidity in % (0-100).
    Output: Heat Index in Celsius.
    """
    temp_f = (temp_c * 9.0 / 5.0) + 32.0

    # Simple formula first
    hi_f = 0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (humidity * 0.094))

    # If HI >= 80°F, use full Rothfusz equation
    if hi_f >= 80.0:
        hi_f = (
            -42.379
            + 2.04901523 * temp_f
            + 10.14333127 * humidity
            - 0.22475541 * temp_f * humidity
            - 0.00683783 * (temp_f**2)
            - 0.05481717 * (humidity**2)
            + 0.00122874 * (temp_f**2) * humidity
            + 0.00085282 * temp_f * (humidity**2)
            - 0.00000199 * (temp_f**2) * (humidity**2)
        )
        # Adjustments
        if humidity < 13.0 and 80.0 <= temp_f <= 112.0:
            adjustment = ((13.0 - humidity) / 4.0) * math.sqrt((17.0 - abs(temp_f - 95.0)) / 17.0)
            hi_f -= adjustment
        elif humidity > 85.0 and 80.0 <= temp_f <= 87.0:
            adjustment = ((humidity - 85.0) / 10.0) * ((87.0 - temp_f) / 5.0)
            hi_f += adjustment

    # Convert back to Celsius
    hi_c = (hi_f - 32.0) * 5.0 / 9.0
    return round(hi_c, 1)


def calculate_vapor_pressure(temp_c: float, humidity: float) -> float:
    """Calculates water vapor pressure in hPa from temp and relative humidity."""
    saturation_vp = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    return (humidity / 100.0) * saturation_vp


def calculate_swbgt(temp_c: float, humidity: float) -> float:
    """
    Simplified Wet Bulb Globe Temperature (sWBGT) in °C.
    Formula widely used by sports and occupational safety:
    sWBGT = 0.567 * Ta + 0.393 * e + 3.94 (e in hPa)
    """
    e = calculate_vapor_pressure(temp_c, humidity)
    swbgt = (0.567 * temp_c) + (0.393 * e) + 3.94
    return round(swbgt, 1)


def get_risk_category(score: float) -> Tuple[str, str, str]:
    """
    Returns (Category Name, Severity Emoji, Color Hex).
    0-20: LOW
    21-40: MODERATE
    41-60: HIGH
    61-80: VERY HIGH
    81-100: EXTREME
    """
    if score <= 20:
        return "LOW", "🟢", "#10B981"
    elif score <= 40:
        return "MODERATE", "🟡", "#F59E0B"
    elif score <= 60:
        return "HIGH", "🟠", "#F97316"
    elif score <= 80:
        return "VERY HIGH", "🔴", "#EF4444"
    else:
        return "EXTREME", "🚨", "#7F1D1D"


def calculate_environmental_heat_risk(
    temperature: float,
    humidity: float,
    apparent_temperature: float = None,
    wind_speed: float = 5.0,
    uv_index: float = 6.0,
    time_of_day_hour: int = 14,
    solar_radiation: float = None
) -> Dict[str, Any]:
    """
    Multi-factor deterministic Heat Risk calculation (0-100).
    Considers:
    - Temperature & Humidity (Heat Index & sWBGT)
    - Apparent / Feels-Like temperature
    - Wind speed (cooling relief when <37°C, but convective heating when >=37°C!)
    - UV Index / Solar radiant load
    - Diurnal solar peak hours (11:30 AM - 16:30 PM)
    """
    if apparent_temperature is None:
        apparent_temperature = calculate_heat_index(temperature, humidity)

    swbgt = calculate_swbgt(temperature, humidity)

    # 1. Base thermal load from apparent temperature
    # 20°C -> 0, 27°C -> 20, 32°C -> 40, 40°C -> 65, 48°C -> 85, 54°C+ -> 100
    if apparent_temperature <= 22:
        base_score = max(0.0, (apparent_temperature - 15) * 2.0)
    elif apparent_temperature <= 27:
        base_score = 14.0 + (apparent_temperature - 22.0) * 1.6
    elif apparent_temperature <= 32:
        base_score = 22.0 + (apparent_temperature - 27.0) * 3.6
    elif apparent_temperature <= 40:
        base_score = 40.0 + (apparent_temperature - 32.0) * 3.125
    elif apparent_temperature <= 50:
        base_score = 65.0 + (apparent_temperature - 40.0) * 2.5
    else:
        base_score = 90.0 + min(10.0, (apparent_temperature - 50.0) * 1.5)

    factors_explanation = []

    # 2. Humidity impact
    humidity_penalty = 0.0
    if humidity >= 70 and temperature >= 30:
        humidity_penalty = min(12.0, (humidity - 65) * 0.4)
        factors_explanation.append(
            f"Elevated humidity ({humidity:.0f}%) significantly impedes sweat evaporation, intensifying thermal stress."
        )
    elif humidity <= 20 and temperature >= 38:
        # Arid heat causes rapid dehydration without sweat awareness
        humidity_penalty = 5.0
        factors_explanation.append(
            f"Extremely dry air ({humidity:.0f}%) accelerates invisible fluid loss and dehydration."
        )

    # 3. Wind speed factor
    wind_effect = 0.0
    if temperature >= 37.5:
        # Above skin temperature (~35-37°C), strong winds act as forced convection heating!
        if wind_speed > 15:
            wind_effect = min(8.0, (wind_speed - 15) * 0.3)
            factors_explanation.append(
                f"High air velocity ({wind_speed:.1f} km/h) above skin temperature causes convective advective heating."
            )
    else:
        # Below 37°C, wind aids sweat evaporation and cooling
        if wind_speed >= 10:
            wind_effect = -max(2.0, min(8.0, wind_speed * 0.25))
            factors_explanation.append(
                f"Moderate breeze ({wind_speed:.1f} km/h) provides modest evaporative cooling relief."
            )
        elif wind_speed < 4:
            wind_effect = 4.0
            factors_explanation.append(
                f"Stagnant air ({wind_speed:.1f} km/h) traps a hot microclimate around the body."
            )

    # 4. UV / Solar radiation factor
    solar_effect = 0.0
    if uv_index >= 11:
        solar_effect = 10.0
        factors_explanation.append(
            f"Extreme UV index ({uv_index:.1f}) delivers intense direct radiant thermal loading."
        )
    elif uv_index >= 8:
        solar_effect = 6.0
        factors_explanation.append(
            f"Very High UV index ({uv_index:.1f}) increases solar skin absorption."
        )
    elif uv_index >= 6:
        solar_effect = 3.0

    # 5. Time of day (solar zenith peak)
    diurnal_effect = 0.0
    if 12 <= time_of_day_hour <= 16:
        diurnal_effect = 5.0
        factors_explanation.append("Peak solar elevation hours (12:00-16:00) compound ground surface heat re-radiation.")
    elif 11 <= time_of_day_hour <= 17:
        diurnal_effect = 2.5

    # Composite Score Calculation
    raw_score = base_score + humidity_penalty + wind_effect + solar_effect + diurnal_effect
    final_score = max(0, min(100, int(round(raw_score))))

    category, emoji, color = get_risk_category(final_score)

    if not factors_explanation:
        factors_explanation.append("Current ambient weather parameters are within baseline seasonal variations.")

    summary_text = (
        f"Environmental risk is {category} ({final_score}/100). "
        f"Temperature is {temperature:.1f}°C (feels like {apparent_temperature:.1f}°C) with {humidity:.0f}% humidity."
    )

    return {
        "environmental_risk_score": final_score,
        "risk_category": category,
        "emoji": emoji,
        "color": color,
        "metrics": {
            "temperature_c": round(temperature, 1),
            "apparent_temperature_c": round(apparent_temperature, 1),
            "humidity_percent": round(humidity, 1),
            "wind_speed_kmh": round(wind_speed, 1),
            "uv_index": round(uv_index, 1),
            "swbgt_c": round(swbgt, 1),
            "time_of_day_hour": time_of_day_hour
        },
        "contributing_factors": factors_explanation,
        "summary": summary_text,
        "disclaimer": "AI risk estimate / prototype. Informational decision support only; not a medical diagnosis."
    }
