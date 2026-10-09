# 🔥 HEATSHIELD AI

### Predict. Protect. Prevent.
> **AI-Powered Hyperlocal Extreme-Heat Risk, Vulnerability & Action Intelligence Platform**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests: 25 Passing](https://img.shields.io/badge/Tests-25%20Passed-success.svg)](tests/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Active%20Online-brightgreen.svg)](https://waterproof-introduction-realtors-prospects.trycloudflare.com)

> 🌐 **Live Public Application**: **[https://waterproof-introduction-realtors-prospects.trycloudflare.com](https://waterproof-introduction-realtors-prospects.trycloudflare.com)**



---

## 1. Project Overview

**HeatShield AI** is a climate-tech decision intelligence platform built to save lives during extreme heat emergencies.

The goal is **NOT** to build another weather dashboard. 

A conventional weather app tells you:
> *Temperature: 42°C*

**HeatShield AI answers the questions that save lives:**
* **Who is at risk?**
* **When will the danger be highest?**
* **How dangerous is the situation for this specific person?**
* **What should they do?**
* **Where can they find water, shade, cooling, or medical help?**

By integrating multi-factor thermodynamic modeling, privacy-conscious personal vulnerability profiling, continuous peak danger windows, safe-route navigation, and a grounded AI assistant, HeatShield AI converts raw weather data into actionable safety decisions.

---

## 2. The Problem

Extreme heat is humanity's deadliest weather-related hazard, causing more fatalities annually than hurricanes, floods, and tornadoes combined. Yet:
1. **Generic meteorological reporting fails human physiology**: Stating that it is 42°C offers zero actionable guidance to a construction worker on hot asphalt versus an elderly citizen living without air conditioning.
2. **Timing is everything**: People succumb to heatstroke during predictable, continuous peak hours (e.g., 12:30 PM – 4:30 PM), but lack automated danger-window forecasting.
3. **Navigational apps default to lethal paths**: Google Maps and standard navigators guide pedestrians via the shortest arterial roads—maximizing unshaded asphalt radiation and UV exposure.
4. **Lack of resource visibility**: Citizens and delivery workers have no real-time visibility into verified drinking water refill stations, shaded public refuges, or cold-immersion emergency clinics.

---

## 3. Why This Matters

As climate change accelerates, extreme heat events are occurring earlier in the year, lasting longer, and reaching unprecedented wet-bulb temperatures. Urban heat islands intensify ambient conditions by $+3^\circ\text{C}$ to $+6^\circ\text{C}$. Without hyper-personalized, action-oriented intelligence, the most vulnerable—outdoor laborers, delivery drivers, elderly individuals, and marginalized communities—bear the highest burden of preventable morbidity and mortality.

---

## 4. The Solution: DATA → RISK → PERSON → ACTION

HeatShield AI operates on a rigorous, human-centered pipeline:

```
USER LOCATION
      ↓
WEATHER + ENVIRONMENTAL DATA (Temperature, Humidity, Wind, UV, sWBGT)
      ↓
DETERMINISTIC HEAT RISK ENGINE (Rothfusz HI, Steadman AT, Thermal Radiation)
      ↓
PERSONAL VULNERABILITY ENGINE (Age, Occupation, Activity, AC Access, Health)
      ↓
HYPERLOCAL RISK SCORE (0 – 100 Normalized Scale)
      ↓
PEAK DANGER TIME WINDOW (e.g. 12:30 PM – 4:30 PM)
      ↓
PERSONALIZED ACTIONABLE RECOMMENDATIONS (Hydration, Rest Cycles, Shaded Routing)
      ↓
SAFE ROUTES + WATER / COOLING / MEDICAL POI MESH
      ↓
AI HEAT ASSISTANT (Multilingual, Voice TTS, Non-Diagnostic Medical Guardrails)
      ↓
PROACTIVE ADVISORIES & CIVIC COMMAND
```

---

## 5. Main Features

### 🌟 Feature 1: Hyperlocal Heat Risk Score (0–100)
* Deterministic, explainable calculation combining temperature, relative humidity, apparent temperature, wind speed, solar UV irradiance, and time of day.
* Standardized severity scale:
  * `0 – 20` 🟢 **LOW**
  * `21 – 40` 🟡 **MODERATE**
  * `41 – 60` 🟠 **HIGH**
  * `61 – 80` 🔴 **VERY HIGH**
  * `81 – 100` 🚨 **EXTREME**
* Explainability breakdown: details exactly how high humidity, stagnant airflow, or extreme UV load contributed to the score.

### 👤 Feature 2: Personal Vulnerability Engine
* Privacy-conscious profile inputs: occupation, age bracket, outdoor exposure hours, exertion level, and air conditioning access.
* Demonstrates physiological variance:
  * **Office Worker** (25 yrs, indoor AC) $\rightarrow$ **Personal Risk: 52/100 (HIGH)**
  * **Construction Worker** (32 yrs, 8 hrs outdoor sun, heavy exertion) $\rightarrow$ **Personal Risk: 95/100 (EXTREME)**
  * **Elderly Resident** (68 yrs, no AC, chronic sensitivity) $\rightarrow$ **Personal Risk: 92/100 (EXTREME)**

### ⏰ Feature 3: Continuous Peak Danger Time Window
* Automatically scans hourly forecasts to identify continuous dangerous periods (e.g., **12:30 PM – 4:30 PM**).
* Pinpoints peak danger hour, expected maximum temperature, and hourly timeline for **Today**, **Tomorrow**, and the **Next 3 Days**.

### 🗺️ Feature 4: Hyperlocal Heat Map & Resource POIs
* Interactive Leaflet + OpenStreetMap canvas rendering urban heat zones.
* Geocoded markers with distances and opening hours:
  * 🚰 **Water Points**: Public drinking water kiosks and filtered RO dispensers.
  * 🌳 **Cooling Centers**: Air-conditioned civic libraries, community centers, and shaded banyan parks.
  * 🏥 **Medical Facilities**: Hospitals and clinics equipped with heat-exhaustion triage and IV hydration.
* Clear status badges: distinguishes `Municipal Verified` from `DEMO DATA`.

### 🚶 Feature 5: Heat-Safer Route Planner
* Evaluates walking routes between Origin and Destination:
  * **Fastest Direct Route**: Minimal time (15 mins), severe unshaded asphalt exposure (88/100).
  * **Recommended Heat-Safer Route**: Weaves through tree canopy shade and passes drinking water refill checkpoints (+4 mins, **42% lower heat exposure**).

### 🤖 Feature 6: Grounded AI Heat Assistant ("HeatShield Assistant")
* Natural language interactive assistant with provider abstraction (Google Gemini, OpenAI GPT, or zero-key Grounded Rule-Based Engine).
* **Strict Medical Safety Guardrails**: Never diagnoses diseases. Immediately escalates severe symptoms (dizziness, nausea, fainting, lack of sweat) to emergency services (**108 / 112 / 911**).
* Multilingual support: **English**, **తెలుగు (Telugu)**, and **हिन्दी (Hindi)**.
* Integrated Web Speech API Text-to-Speech (TTS) voice readout.

### 👷 Feature 7: Outdoor Worker Shift Dashboard
* Field supervisor matrix aligned with OSHA and NIOSH occupational thermal criteria.
* Generates hourly work-to-rest cycles (e.g., *30 min work / 30 min shaded rest*) and exact shift hydration quotas (e.g., *6.5 Liters of water + ORS*).

### 🏛️ Feature 8: City Heat Command Center
* Municipal command dashboard for disaster management authorities and city planners.
* Ward-by-ward **Heat Vulnerability Index (HVI)** ranking.
* Automated AI priority emergency actions (mobile water tanker dispatch, midday labor moratorium enforcement, emergency cooling shelter activation).

### 📈 Feature 9: 10-Year Climate Trends & Grid Stress
* Visualizes 10-year trends of extreme heat days ($>40^\circ\text{C}$) to demonstrate systemic chronic climate escalation.
* Energy grid cooling strain indicator estimating peak compressor stress between **2:00 PM – 6:00 PM**.

### 🌾 Feature 10: Farm & Livestock Heat Modes
* **Crop Advisor**: Evaluates critical physiological thresholds (e.g., Paddy flowering $>35^\circ\text{C}$ spikelet sterility risk) and recommends optimal early morning irrigation windows.
* **Livestock THI**: Computes Temperature-Humidity Index (THI) for dairy cattle, poultry, and sheep to protect animal welfare and milk yield.

### ⚡ Feature 11: 1-Click Judge Demo Scenarios
* Presets for rapid hackathon evaluation:
  1. *Scenario 1: Normal Mild Day (24°C)*
  2. *Scenario 2: Coastal Extreme Heatwave (Visakhapatnam, 49°C Feel)*
  3. *Scenario 3: Construction / Outdoor Worker (8hr Sun)*
  4. *Scenario 4: Elderly Resident (No AC / High Risk)*
  5. *Scenario 5: Extreme Heat + Grid Outage / Zero AC Access*

---

## 6. Architecture & Data Flow

```
                      ┌──────────────────────┐
                      │    Open-Meteo API    │
                      │  (Live / Calibrated) │
                      └──────────┬───────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HEATSHIELD REST API SERVER                   │
│                                                                 │
│  ┌────────────────────────┐         ┌────────────────────────┐  │
│  │   heat_risk_engine     │         │  vulnerability_engine  │  │
│  │ (Rothfusz HI & sWBGT)  │         │ (Age, Work, AC Factor) │  │
│  └───────────┬────────────┘         └───────────┬────────────┘  │
│              │                                  │               │
│              └─────────────────┬────────────────┘               │
│                                ▼                                │
│                     ┌────────────────────┐                      │
│                     │ danger_window_eng  │                      │
│                     │ (Continuous Peak)  │                      │
│                     └──────────┬─────────┘                      │
│                                │                                │
│        ┌───────────────────────┼───────────────────────┐        │
│        ▼                       ▼                       ▼        │
│  ┌───────────┐           ┌───────────┐           ┌───────────┐  │
│  │routing_eng│           │poi_engine │           │ai_assitant│  │
│  └───────────┘           └───────────┘           └───────────┘  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT WEB APPLICATION                      │
│                                                                 │
│   • Dashboard Gauge & Factors       • Interactive Leaflet Map   │
│   • Heat-Safe Route Visualizer      • Worker Mode Table         │
│   • City Command Center             • Multilingual AI Chat & TTS│
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. Tech Stack

| Layer | Technologies | Rationale |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ (Standard Library `http.server`, `urllib`, `json`, `math`) | Zero-dependency deployment; rock-solid deterministic scientific computation; zero pip breakages. |
| **Frontend** | Semantic HTML5, Custom Design System CSS, Modern Vanilla JavaScript (ES6+) | Instant load times, high-contrast dark climate-tech aesthetics, zero build step required. |
| **Mapping** | Leaflet.js & OpenStreetMap | Open-source geospatial visualization, custom marker popups, polyline route overlay. |
| **Data Viz** | Chart.js | Responsive 10-year historical climate trend bar/line visualization. |
| **AI Layer** | Provider Abstraction (Google Gemini / OpenAI GPT / Grounded Rule Engine) | Graceful offline and zero-key fallback with strict safety guardrails. |
| **Speech** | Web Speech API | Client-side Text-to-Speech (TTS) voice readout in English, Telugu, and Hindi. |

---

## 8. Data Sources & Transparency

* **Weather**: [Open-Meteo Free API](https://open-meteo.com) (`temperature_2m`, `relative_humidity_2m`, `apparent_temperature`, `wind_speed_10m`, `uv_index`).
* **Spatial POIs**: OpenStreetMap Overpass API & Municipal Heat Action Plan Directories.
* **Historical Data**: ERA5 Reanalysis and NOAA Climatological Normals.
* **Occupational Standards**: NIOSH/OSHA Heat Stress Guidelines.
* **Data Quality Tagging**: Every resource is transparently tagged as `Live`, `Municipal Verified`, `Estimated`, or `DEMO DATA`.

---

## 9. Installation & Running Locally

### Prerequisites
* Python 3.10 or higher.
* Any modern web browser (Chrome, Firefox, Safari, Edge).

### Quick Start (Zero External Pip Packages Required!)
```bash
# 1. Clone the repository
git clone https://github.com/your-username/heatshield-ai.git
cd heatshield-ai

# 2. Start the local server
python3 start.py 8000
```
Open your browser and navigate to:
```
http://localhost:8000
```

### Running with Docker (Optional)
```bash
docker build -t heatshield-ai .
docker run -p 8000:8000 heatshield-ai
```

---

## 10. Environment Variables

Create a `.env` file in the project root if you wish to configure live LLM providers (optional):
```env
PORT=8000
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
> *Note: HeatShield AI functions 100% out-of-the-box even without any API keys thanks to its built-in Grounded Expert Rule-Based Engine.*

---

## 11. Testing & Verification

HeatShield AI includes an automated test suite with **23 unit and integration tests** covering all mathematical engines, vulnerability modifiers, routing algorithms, multilingual outputs, and API routes.

To run the test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

### Test Results
```
test_assistant_chat_endpoint ... ok
test_community_command_endpoint ... ok
test_health_endpoint ... ok
test_not_found_endpoint ... ok
test_resources_endpoint ... ok
test_risk_calculate_endpoint ... ok
test_route_endpoint ... ok
test_scenarios_endpoint ... ok
test_static_files_served ... ok
test_weather_endpoint ... ok
test_worker_schedule_endpoint ... ok
test_agricultural_and_livestock_modes ... ok
test_community_command_center ... ok
test_danger_window_engine ... ok
test_heat_risk_engine_determinism ... ok
test_historical_trends_and_grid_stress ... ok
test_medical_safety_escalation_in_assistant ... ok
test_multilingual_assistant ... ok
test_poi_engine ... ok
test_risk_categories ... ok
test_routing_engine ... ok
test_vulnerability_engine_differentiation ... ok
test_worker_schedule_engine ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.019s

OK
```

---

## 12. 3-Minute Hackathon Demo Script

For a detailed, step-by-step presentation script designed for hackathon judges, refer to [docs/HACKATHON_DEMO_SCRIPT.md](docs/HACKATHON_DEMO_SCRIPT.md).

1. **Step 1 (0:00 - 0:30)**: Open Dashboard $\rightarrow$ Show 87/100 Extreme Heat Risk Score and the core problem statement.
2. **Step 2 (0:30 - 0:55)**: Select *"Scenario 3: Outdoor Worker"* $\rightarrow$ Watch risk surge to 95/100 with Danger Window locked to 12:30 – 4:30 PM.
3. **Step 3 (0:55 - 1:25)**: Open *"Heat Map & POIs"* $\rightarrow$ Inspect nearby water refill points (🚰) and AC respite shelters (🌳).
4. **Step 4 (1:25 - 1:55)**: Open *"Heat-Safe Route"* $\rightarrow$ Compare Fastest (red) vs Heat-Safer Route (green, -42% heat load).
5. **Step 5 (1:55 - 2:25)**: Open *"AI Heat Assistant"* $\rightarrow$ Test safety guardrails, ask break schedule, demonstrate Telugu/Hindi and voice TTS.
6. **Step 6 (2:25 - 2:55)**: View *"Outdoor Worker Mode"* and *"City Command Center"* ward vulnerability ranking.
7. **Step 7 (2:55 - 3:00)**: Conclude: *"Not another weather app. A climate safety intelligence system."*

---

## 13. Limitations & Future Improvements

### Current Limitations
1. **Shade Data Resolution**: Tree canopy shade along routes is currently algorithmically estimated based on street canyon orientation and solar azimuth; integration with LiDAR urban canopy data would provide centimeter-level shade accuracy.
2. **Live Water Point Telemetry**: Real-time water dispenser tank levels currently rely on verified municipal schedules rather than live IoT flow meters.
3. **Indoor Temperature Sensing**: In-home thermal stress is modeled through building insulation archetypes rather than indoor smart thermostats.

### Future Roadmap
* **IoT Sensor Integration**: Ingest real-time municipal LoRaWAN wet-bulb sensors.
* **SMS & WhatsApp Alerts**: Twilio / Gupshup automated broadcast alerts for non-smartphone populations in rural agricultural belts.
* **Satellite Thermal Land Surface Temp (LST)**: Real-time integration of Landsat-9 and Sentinel-3 high-resolution thermal infrared bands.
* **Wearable Integration**: Sync heart-rate and core temperature estimates from smartwatches to dynamically alert wearers of acute heat strain.

---

## 14. Safety Disclaimer

> **IMPORTANT MEDICAL & REGULATORY NOTICE:**  
> HeatShield AI provides informational risk estimates and climate safety guidance based on thermodynamic models and peer-reviewed occupational thresholds. **It is not a medical diagnostic system, veterinary clinic, or a substitute for professional healthcare or emergency services.** If you or someone near you experiences confusion, loss of consciousness, persistent vomiting, or cessation of sweating during extreme heat, **call emergency medical services immediately (108 / 112 / 911)** and move the person into a shaded or air-conditioned area.

---

## 15. License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
