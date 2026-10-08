# HeatShield AI — System Architecture & Scientific Methodology

## 1. Core Paradigm: DATA → RISK → PERSON → ACTION

Traditional weather platforms report raw meteorological observations:
```
Temperature: 42°C | Humidity: 65%
```
HeatShield AI answers the fundamental human questions:
* **Who is at risk?**
* **When will the danger be highest?**
* **How dangerous is the situation for this specific person?**
* **What should they do?**
* **Where can they find water, shade, cooling, or medical help?**

```
┌─────────────────────────┐
│  WEATHER & ENV DATA     │ (Open-Meteo API / Live Sensor Grid)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│    HEAT RISK ENGINE     │ (Rothfusz HI, Steadman AT, sWBGT, UV Load)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  VULNERABILITY ENGINE   │ (Age, Occupation, Activity, Cooling Access)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│  HYPERLOCAL RISK SCORE  │ (0 - 100 Normalized Scale)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│   DANGER TIME WINDOW    │ (Continuous Peak Risk Interval e.g. 12:30-4:30 PM)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ TAILORED ACTION GUIDANCE│ (Specific, Practical Safety Decisions)
└────────────┬────────────┘
             ▼
┌────────────────────────────────────────────────────────┐
│ SAFE ROUTING • POI MESH • AI ASSISTANT • CIVIC COMMAND │
└────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical & Scientific Formulations

### 2.1 Environmental Heat Risk Engine (`heat_risk_engine.py`)

#### Rothfusz Regression Equation (Heat Index)
The base thermodynamic temperature index is derived from the Rothfusz 9-parameter polynomial regression:
$$HI = -42.379 + 2.04901523 \cdot T + 10.14333127 \cdot R - 0.22475541 \cdot T \cdot R - 0.00683783 \cdot T^2 - 0.05481717 \cdot R^2 + 0.00122874 \cdot T^2 \cdot R + 0.00085282 \cdot T \cdot R^2 - 0.00000199 \cdot T^2 \cdot R^2$$
Where $T$ is dry-bulb temperature in °F and $R$ is relative humidity in %.

#### Simplified Wet Bulb Globe Temperature (sWBGT)
For outdoor occupational and athletic strain:
$$e = \frac{RH}{100} \cdot 6.112 \cdot \exp\left(\frac{17.67 \cdot T_a}{T_a + 243.5}\right)$$
$$sWBGT = 0.567 \cdot T_a + 0.393 \cdot e + 3.94$$
Where $T_a$ is ambient dry-bulb temperature (°C) and $e$ is water vapor pressure (hPa).

#### Convective Inversion Phenomenon
At air temperatures exceeding mean skin temperature ($\sim 37.5^\circ\text{C}$), high wind speeds reverse from evaporative cooling to **forced convective heating**, accelerating core heat acquisition. The engine programmatically switches wind vector penalties when $T_a \ge 37.5^\circ\text{C}$.

### 2.2 Personal Vulnerability Engine (`vulnerability_engine.py`)
Computes normalized score $\Delta$ based on physiological thermoregulation:
* **Age modifier**: Elderly ($65+$) thermoregulatory impairment ($+18$ pts), young children under $5$ ($+14$ pts).
* **Occupation & Sun Exposure**: High metabolic labor outdoors ($+16$ to $+25$ pts) vs. indoor AC office ($-12$ pts).
* **Cooling Access**: No AC residential deficit ($+16$ pts).
* **Chronic Health Conditions**: Cardiovascular/renal strain modifier ($+12$ pts).

### 2.3 Danger Window Engine (`danger_window_engine.py`)
Identifies the continuous contiguous hours wherein personal risk meets or exceeds severe thresholds ($\ge 50$), extracting the peak hour and continuous interval (e.g. `12:30 PM – 4:30 PM`).

### 2.4 Heat-Safer Routing Engine (`routing_engine.py`)
Optimizes pedestrian corridors by penalizing solar irradiance and asphalt heat re-radiation, prioritizing tree canopy buffers and drinking water checkpoints. Reduces estimated radiant heat exposure by $30\text{--}45\%$.

### 2.5 Livestock Temperature-Humidity Index (`agriculture_engine.py`)
$$THI = (1.8 \cdot T_a + 32) - \left[(0.55 - 0.0055 \cdot RH) \cdot (1.8 \cdot T_a - 26)\right]$$
* $THI \ge 84$: Emergency Livestock Stress (mortality threat, severe milk yield collapse).
* $THI \ge 79$: Danger thermal stress (open-mouth panting, shade seeking).

---

## 3. Medical Safety Guardrails

HeatShield AI enforces strict non-diagnostic safety guardrails:
1. **Never diagnoses diseases**: The system explicitly prohibits claiming "You have heatstroke."
2. **Emergency Reflex**: If severe symptoms (confusion, vomiting, loss of consciousness, fainting, inability to sweat) are mentioned, the assistant immediately escalates to calling emergency numbers (**108 / 112 / 911**) and applying active cooling.
3. **Mandatory Disclaimer**: Displayed visibly across all outputs and API responses:
   > *HeatShield AI provides informational risk estimates and safety guidance. It is not a medical diagnostic system or a substitute for professional medical advice.*
