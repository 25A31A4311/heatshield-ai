"""
HeatShield AI - Agricultural & Livestock Heat Safety Engine
Computes crop heat vulnerability, evapotranspiration stress,
and Livestock Temperature-Humidity Index (THI).
"""

from typing import Dict, Any, List


def calculate_crop_heat_stress(
    crop_name: str = "Paddy / Rice",
    growth_stage: str = "Flowering / Pollination",
    temp_c: float = 39.5,
    humidity: float = 60.0,
    soil_moisture_level: str = "moderate"  # low, moderate, optimal
) -> Dict[str, Any]:
    """
    Evaluates crop thermal risk and irrigation timing.
    High heat (>35°C) during flowering causes spikelet sterility and pollen desiccation.
    """
    # Critical thresholds by crop
    crop_thresholds = {
        "paddy / rice": {"critical_temp": 35.0, "vulnerable_stage": "Flowering / Pollination"},
        "wheat": {"critical_temp": 32.0, "vulnerable_stage": "Grain Filling"},
        "cotton": {"critical_temp": 38.0, "vulnerable_stage": "Boll Formation"},
        "maize / corn": {"critical_temp": 36.0, "vulnerable_stage": "Tasseling / Silking"},
        "tomatoes / vegetables": {"critical_temp": 34.0, "vulnerable_stage": "Fruit Set"},
        "groundnut / peanuts": {"critical_temp": 35.0, "vulnerable_stage": "Pegging"}
    }

    norm_crop = crop_name.lower().strip()
    config = crop_thresholds.get(norm_crop, {"critical_temp": 35.0, "vulnerable_stage": "Flowering"})

    temp_excess = max(0.0, temp_c - config["critical_temp"])
    stage_multiplier = 1.4 if "flower" in growth_stage.lower() or "pollin" in growth_stage.lower() else 1.0

    soil_penalty = 15.0 if soil_moisture_level == "low" else (0.0 if soil_moisture_level == "optimal" else 8.0)

    raw_stress = min(100, int(round((temp_excess * 7.5 + soil_penalty) * stage_multiplier + 25)))

    if raw_stress >= 75:
        level = "CRITICAL CROP THERMAL THREAT"
        color = "#DC2626"
        advice = [
            f"High danger of blossom drop and pollen sterility: Ambient temperature ({temp_c}°C) exceeds critical threshold ({config['critical_temp']}°C).",
            "Schedule irrigation exclusively during early morning (04:00 - 07:30 AM) or post-sunset to prevent root shock and boiling water effect in root zone.",
            "Maintain standing water depth (3-5 cm) in paddy basins to buffer canopy microclimate by 2-3°C.",
            "Deploy light foliar anti-transpirant spray (such as kaolin clay or potassium chloride) if available to diminish leaf temperature."
        ]
    elif raw_stress >= 50:
        level = "MODERATE HEAT STRESS"
        color = "#F97316"
        advice = [
            "Monitor soil tensiometers closely; evapotranspiration rates are elevated by ~40%.",
            "Mulch unshaded soil around crop rows to conserve subterranean moisture.",
            "Avoid spraying agrochemicals or fertilizers during midday heat to prevent leaf scorching."
        ]
    else:
        level = "LOW / NORMAL CROP RISK"
        color = "#10B981"
        advice = [
            "Thermal conditions within tolerable physiological thresholds for this crop stage.",
            "Maintain standard seasonal irrigation cycle."
        ]

    return {
        "crop": crop_name,
        "growth_stage": growth_stage,
        "stress_score": raw_stress,
        "stress_level": level,
        "color": color,
        "critical_threshold_c": config["critical_temp"],
        "recommended_irrigation_window": "04:30 AM – 07:30 AM or 06:30 PM – 08:30 PM",
        "guidance": advice,
        "disclaimer": "Agricultural recommendations are general agronomic heat guidance. Consult local agricultural extension officers for specific field conditions."
    }


def calculate_livestock_thi(
    animal_type: str = "Dairy Cattle",
    temp_c: float = 38.0,
    humidity: float = 65.0
) -> Dict[str, Any]:
    """
    Computes Temperature-Humidity Index (THI) for Livestock.
    Standard NRC / Thom formula:
    THI = (1.8 * T + 32) - ((0.55 - 0.0055 * RH) * (1.8 * T - 26))
    """
    thi = (1.8 * temp_c + 32.0) - ((0.55 - 0.0055 * humidity) * (1.8 * temp_c - 26.0))
    thi = round(thi, 1)

    if thi >= 84:
        status = "EMERGENCY LIVESTOCK STRESS"
        color = "#7F1D1D"
        warnings = [
            "Severe risk of animal mortality and dramatic milk production plunge (>30%).",
            "Activate high-velocity exhaust fans and evaporative soaking sprinklers immediately.",
            "Provide unlimited chilled, clean drinking water in deep shaded troughs within 5 meters of animals.",
            "Suspend all handling, vaccination, or transport until temperatures drop significantly after nightfall."
        ]
    elif thi >= 79:
        status = "DANGER THERMAL STRESS"
        color = "#DC2626"
        warnings = [
            "Animals exhibit rapid open-mouth panting, reduced feed intake, and clustering near shade.",
            "Provide electrolyte supplements in drinking water.",
            "Ensure shade netting blocks at least 80% of solar radiation over open yards."
        ]
    elif thi >= 72:
        status = "ALERT / MILD HEAT STRESS"
        color = "#F59E0B"
        warnings = [
            "Mild respiration elevation observed. Keep water stations clean and full.",
            "Ensure adequate barn cross-ventilation."
        ]
    else:
        status = "NORMAL / THERMAL COMFORT"
        color = "#10B981"
        warnings = [
            "Livestock thermal comfort zone. Normal productivity maintained."
        ]

    return {
        "animal_type": animal_type,
        "thi_score": thi,
        "status": status,
        "color": color,
        "ambient_temp_c": temp_c,
        "humidity_pct": humidity,
        "guidance": warnings,
        "disclaimer": "Livestock THI is an informational thermal index and does not substitute for veterinarian care or clinical diagnosis."
    }
