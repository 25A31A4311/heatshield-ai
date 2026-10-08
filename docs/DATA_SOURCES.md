# HeatShield AI — Data Sources & Transparency Report

Integrity of data is fundamental to HeatShield AI. The platform maintains strict transparency by tagging every piece of information with an identifiable status:
* **Live**: Real-time programmatic API fetch.
* **Municipal Verified**: Calibrated datasets cross-referenced against public directories.
* **Estimated**: Algorithmic models derived from peer-reviewed scientific literature.
* **DEMO DATA / DEMO SCENARIO**: Synthetic test data for edge testing and judge demonstrations.

---

## 1. Meteorological & Forecast Data
* **Provider**: [Open-Meteo API](https://open-meteo.com)
* **Access**: Free, public, zero-authentication JSON endpoints.
* **Variables Extracted**:
  * `temperature_2m` (2-meter air temperature in °C)
  * `relative_humidity_2m` (Relative humidity in %)
  * `apparent_temperature` (Feels-like temperature in °C)
  * `wind_speed_10m` (Surface wind velocity in km/h)
  * `uv_index` (Direct solar ultraviolet index)
* **Fallback Mode**: If offline or during network dropouts, HeatShield AI gracefully falls back to calibrated reference baselines for representative climate centers (Visakhapatnam, New Delhi, Phoenix, Mild Zone) clearly labeled `Calibrated Baseline Reference (Offline/Demo Mode)`.

---

## 2. Spatial Mapping & Points of Interest (POIs)
* **Map Tiles**: [OpenStreetMap](https://www.openstreetmap.org) via [Leaflet.js](https://leafletjs.com).
* **Cooling Centers & Water Refill Hubs**:
  * Verified records for key anchor cities (Visakhapatnam GVMC Heat Action Plan, New Delhi NDMC Public Kiosks, Phoenix Heat Relief Network).
  * Surrounding topological mesh synthesized around custom coordinates is visibly badged as `DEMO DATA`.

---

## 3. Climatological Historical Baselines
* **Baseline Dataset**: ERA5 Reanalysis / NOAA Climatological Normals.
* **Metrics**: 10-year trends of extreme heat days ($>40^\circ\text{C}$), summer maximum temperatures, and night-time heat retention.

---

## 4. Occupational Safety Standards
* **Guidelines**: NIOSH Criteria for a Recommended Standard: Occupational Exposure to Heat and Hot Environments / OSHA Technical Manual (Section III: Chapter 4 - Heat Stress).
* **Work/Rest Schedules**: Based on metabolic rate classifications (Light, Moderate, Heavy, Strenuous).
