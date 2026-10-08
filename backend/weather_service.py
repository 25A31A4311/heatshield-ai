"""
HeatShield AI - Weather Data Service
Connects to Open-Meteo API for live real-time hourly forecasts
and provides calibrated reference data for offline/demo resilience.
"""

import json
import urllib.request
import urllib.error
import math
from typing import Dict, Any, Optional, List
from datetime import datetime


# Calibrated representative climate baselines for offline/demo reliability
REPRESENTATIVE_CLIMATES = {
    "visakhapatnam": {
        "city": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "country": "India",
        "lat": 17.6868,
        "lon": 83.2185,
        "current": {
            "temp_c": 38.6,
            "humidity": 68.0,
            "apparent_temp_c": 49.2,
            "wind_speed_kmh": 14.5,
            "uv_index": 10.4,
            "weather_condition": "Severe Heat & Coastal Humidity"
        },
        "base_curve": [29.0, 28.5, 28.0, 28.0, 28.5, 29.5, 31.0, 33.2, 35.8, 37.4, 38.6, 38.9, 38.4, 37.8, 36.5, 34.8, 33.0, 31.8, 31.0, 30.5, 30.0, 29.8, 29.5, 29.2]
    },
    "delhi": {
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "lat": 28.6139,
        "lon": 77.2090,
        "current": {
            "temp_c": 43.5,
            "humidity": 38.0,
            "apparent_temp_c": 48.1,
            "wind_speed_kmh": 16.0,
            "uv_index": 11.2,
            "weather_condition": "Arid Heatwave / Loo Winds"
        },
        "base_curve": [31.0, 30.0, 29.0, 29.0, 30.0, 32.0, 35.0, 38.0, 41.0, 42.8, 43.5, 43.8, 43.0, 42.0, 40.5, 38.5, 36.8, 35.2, 34.0, 33.0, 32.5, 32.0, 31.5, 31.2]
    },
    "phoenix": {
        "city": "Phoenix",
        "state": "Arizona",
        "country": "United States",
        "lat": 33.4484,
        "lon": -112.0740,
        "current": {
            "temp_c": 44.0,
            "humidity": 18.0,
            "apparent_temp_c": 44.5,
            "wind_speed_kmh": 12.0,
            "uv_index": 11.8,
            "weather_condition": "Extreme Desert Heat"
        },
        "base_curve": [32.0, 31.0, 30.0, 29.5, 30.0, 32.5, 35.5, 39.0, 41.5, 43.2, 44.0, 44.5, 44.0, 43.2, 41.8, 39.5, 37.8, 36.0, 34.5, 33.8, 33.2, 32.8, 32.5, 32.0]
    },
    "mild": {
        "city": "Pleasant / Temperate Zone",
        "state": "Moderate",
        "country": "Global",
        "lat": 51.5074,
        "lon": -0.1278,
        "current": {
            "temp_c": 23.5,
            "humidity": 45.0,
            "apparent_temp_c": 23.0,
            "wind_speed_kmh": 14.0,
            "uv_index": 4.5,
            "weather_condition": "Mild & Comfortable"
        },
        "base_curve": [15.0, 14.5, 14.0, 14.0, 14.5, 15.5, 17.0, 19.0, 21.0, 22.5, 23.5, 23.8, 23.4, 22.8, 21.5, 20.0, 18.5, 17.2, 16.5, 16.0, 15.8, 15.5, 15.2, 15.0]
    }
}


def get_weather_forecast(lat: float, lon: float, scenario_override: Optional[str] = None) -> Dict[str, Any]:
    """
    Attempts to fetch live real-time forecast data from Open-Meteo.
    If network is unavailable or scenario_override is provided,
    falls back cleanly to calibrated reference data with clear attribution.
    """
    if scenario_override and scenario_override in REPRESENTATIVE_CLIMATES:
        return build_calibrated_weather_payload(REPRESENTATIVE_CLIMATES[scenario_override], data_mode="DEMO SCENARIO")

    # If coordinates match a preset city closely
    chosen_preset = None
    min_dist = 999999.0
    for key, city in REPRESENTATIVE_CLIMATES.items():
        dist = ((lat - city["lat"])**2 + (lon - city["lon"])**2)**0.5
        if dist < min_dist:
            min_dist = dist
            chosen_preset = city

    # Try live Open-Meteo API with short timeout
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m"
            f"&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,uv_index"
            f"&timezone=auto&forecast_days=3"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "HeatShieldAI/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as response:
            if response.status == 200:
                raw = json.loads(response.read().decode("utf-8"))
                return parse_open_meteo_response(raw, lat, lon)
    except Exception as e:
        # Graceful fallback: Network unreachable, sandbox restriction, or API timeout
        pass

    # Fallback to calibrated climate
    fallback_city = chosen_preset if chosen_preset else REPRESENTATIVE_CLIMATES["visakhapatnam"]
    return build_calibrated_weather_payload(
        fallback_city,
        data_mode="Calibrated Baseline Reference (Offline/Demo Mode)",
        custom_lat=lat,
        custom_lon=lon
    )


def parse_open_meteo_response(raw: Dict[str, Any], lat: float, lon: float) -> Dict[str, Any]:
    """Parses live Open-Meteo API JSON response into standardized HeatShield schema."""
    curr = raw.get("current", {})
    hourly = raw.get("hourly", {})
    
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    humidities = hourly.get("relative_humidity_2m", [])
    apparent_temps = hourly.get("apparent_temperature", [])
    winds = hourly.get("wind_speed_10m", [])
    uvs = hourly.get("uv_index", [])

    hourly_timeline = []
    # Take first 24 hours for Today, and next 48 hours for Tomorrow/Day 3
    limit = min(72, len(times))
    for i in range(limit):
        t_str = times[i]
        # Extract hour
        try:
            h_int = int(t_str.split("T")[1].split(":")[0])
        except Exception:
            h_int = i % 24
            
        day_offset = i // 24
        day_label = "today" if day_offset == 0 else ("tomorrow" if day_offset == 1 else "day3")

        hourly_timeline.append({
            "time": t_str,
            "hour": h_int,
            "day_label": day_label,
            "temp_c": round(temps[i], 1) if i < len(temps) else 30.0,
            "humidity": round(humidities[i], 0) if i < len(humidities) else 50.0,
            "apparent_temp_c": round(apparent_temps[i], 1) if i < len(apparent_temps) else 32.0,
            "wind_speed": round(winds[i], 1) if i < len(winds) else 10.0,
            "uv_index": round(uvs[i], 1) if i < len(uvs) else 5.0
        })

    current_temp = curr.get("temperature_2m", 35.0)
    current_humidity = curr.get("relative_humidity_2m", 60.0)
    current_apparent = curr.get("apparent_temperature", current_temp + 4.0)
    current_wind = curr.get("wind_speed_10m", 12.0)

    # Estimate UV for current hour
    now_hour = datetime.now().hour
    current_uv = 9.5 if (11 <= now_hour <= 15) else (4.0 if (8 <= now_hour <= 17) else 0.0)

    return {
        "location": {
            "name": f"Coordinates ({lat:.4f}, {lon:.4f})",
            "lat": lat,
            "lon": lon
        },
        "current": {
            "temp_c": round(current_temp, 1),
            "humidity": round(current_humidity, 0),
            "apparent_temp_c": round(current_apparent, 1),
            "wind_speed_kmh": round(current_wind, 1),
            "uv_index": round(current_uv, 1),
            "condition": "Partly Cloudy / High Thermal Load"
        },
        "hourly_data": hourly_timeline,
        "data_status": "Live Open-Meteo API",
        "is_live": True
    }


def build_calibrated_weather_payload(
    climate_preset: Dict[str, Any],
    data_mode: str = "Calibrated Baseline Reference (Offline Mode)",
    custom_lat: Optional[float] = None,
    custom_lon: Optional[float] = None
) -> Dict[str, Any]:
    """Generates structured 72-hour forecast based on calibrated climatological curve."""
    lat = custom_lat if custom_lat is not None else climate_preset["lat"]
    lon = custom_lon if custom_lon is not None else climate_preset["lon"]
    curr = climate_preset["current"]
    curve = climate_preset["base_curve"]

    hourly_timeline = []
    days = ["today", "tomorrow", "day3"]

    for d_idx, day_name in enumerate(days):
        # subtle day variance
        day_variation = 0.0 if d_idx == 0 else (0.8 if d_idx == 1 else -0.5)
        for h in range(24):
            base_temp = curve[h] + day_variation
            # Humidity inversely correlates with temperature
            rel_humidity = max(25.0, min(85.0, 85.0 - (base_temp - 24.0) * 2.8))
            # Wind speed fluctuates
            wind = 8.0 + (math.sin(h / 3.0) * 4.0)
            # UV curve
            if 6 <= h <= 18:
                uv = max(0.0, math.sin((h - 6) / 12.0 * math.pi) * curr["uv_index"])
            else:
                uv = 0.0

            hourly_timeline.append({
                "time": f"2026-10-0{8+d_idx}T{h:02d}:00",
                "hour": h,
                "day_label": day_name,
                "temp_c": round(base_temp, 1),
                "humidity": round(rel_humidity, 0),
                "apparent_temp_c": round(base_temp + ((rel_humidity - 40.0) * 0.18), 1),
                "wind_speed": round(wind, 1),
                "uv_index": round(uv, 1)
            })

    return {
        "location": {
            "name": f"{climate_preset['city']}, {climate_preset['state']}",
            "lat": lat,
            "lon": lon
        },
        "current": curr,
        "hourly_data": hourly_timeline,
        "data_status": data_mode,
        "is_live": False
    }
