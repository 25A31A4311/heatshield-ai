"""
HeatShield AI - City / Community Command Center Engine
Provides municipal authorities and disaster management teams with
hyperlocal vulnerability mapping, resource gap analysis,
and AI priority response action plans.
"""

from typing import Dict, Any, List


def get_community_command_data(
    city_name: str = "Visakhapatnam Metropolitan Area",
    current_risk_score: int = 88
) -> Dict[str, Any]:
    """
    Returns citywide heat intelligence, vulnerable micro-zones, and prioritized interventions.
    """
    status_label = "EXTREME" if current_risk_score >= 80 else ("VERY HIGH" if current_risk_score >= 60 else "HIGH")
    status_color = "#7F1D1D" if current_risk_score >= 80 else ("#EF4444" if current_risk_score >= 60 else "#F97316")

    # Micro-zones with Heat Vulnerability Index (HVI)
    zones = [
        {
            "id": "zone-1",
            "name": "Ward 14 - Port Logistics & Informal Settlement Belt",
            "heat_index_score": 93,
            "surface_temp_c": 44.2,
            "population_vulnerable_estimate": 4820,
            "cooling_access_rate_pct": 14,
            "canopy_cover_pct": 6,
            "priority_rank": 1,
            "urgency": "CRITICAL",
            "active_interventions_needed": [
                "Deploy 3 municipal mobile water tankers to transit bottlenecks",
                "Activate local school gymnasiums as air-conditioned emergency respite shelters",
                "Enforce midday work stoppage for unshaded manual laborers"
            ]
        },
        {
            "id": "zone-2",
            "name": "Ward 22 - Central Commercial & Market Bazaar",
            "heat_index_score": 89,
            "surface_temp_c": 42.8,
            "population_vulnerable_estimate": 3150,
            "cooling_access_rate_pct": 28,
            "canopy_cover_pct": 11,
            "priority_rank": 2,
            "urgency": "HIGH",
            "active_interventions_needed": [
                "Install temporary shade tarpaulins across open-air market alleys",
                "Distribute ORS (Oral Rehydration Salts) packets at bus terminals",
                "Direct mobile medical van for rapid heat-exhaustion screening"
            ]
        },
        {
            "id": "zone-3",
            "name": "Ward 31 - Industrial Freight Corridor",
            "heat_index_score": 87,
            "surface_temp_c": 43.1,
            "population_vulnerable_estimate": 2400,
            "cooling_access_rate_pct": 22,
            "canopy_cover_pct": 8,
            "priority_rank": 3,
            "urgency": "HIGH",
            "active_interventions_needed": [
                "Provide shaded rest pods for delivery drivers and truck operators",
                "Refill industrial hydration points with clean chilled water"
            ]
        },
        {
            "id": "zone-4",
            "name": "Ward 08 - Coastal Residential & University Quarter",
            "heat_index_score": 74,
            "surface_temp_c": 37.5,
            "population_vulnerable_estimate": 980,
            "cooling_access_rate_pct": 65,
            "canopy_cover_pct": 34,
            "priority_rank": 4,
            "urgency": "MODERATE",
            "active_interventions_needed": [
                "Open university library auditoriums to vulnerable senior citizens",
                "Maintain coastal park misting stations"
            ]
        }
    ]

    total_pop_vulnerable = sum(z["population_vulnerable_estimate"] for z in zones)

    ai_priority_recommendations = [
        {
            "action_id": "ACT-01",
            "title": "Immediate Water Tanker Deployment (Priority Zone 1)",
            "impact": "Supplies emergency hydration to 4,800+ vulnerable residents and street vendors.",
            "status": "Recommended Immediately",
            "category": "Hydration"
        },
        {
            "action_id": "ACT-02",
            "title": "Mandatory Construction Moratorium (12:00 PM – 4:00 PM)",
            "impact": "Shields ~6,500 outdoor laborers from life-threatening peak wet-bulb heat stress.",
            "status": "Action Dispatched",
            "category": "Policy"
        },
        {
            "action_id": "ACT-03",
            "title": "Open 8 Civic Air-Conditioned Emergency Respite Centers",
            "impact": "Provides continuous cooling relief to low-income elders and unsheltered residents.",
            "status": "Shelters Active",
            "category": "Shelter"
        },
        {
            "action_id": "ACT-04",
            "title": "Ambulance Triage Pre-positioning with Cold Immersion Bags",
            "impact": "Reduces time-to-treatment for severe heat illness by an estimated 18 minutes.",
            "status": "Standby Alert",
            "category": "Medical"
        }
    ]

    return {
        "city_name": city_name,
        "heat_status": status_label,
        "status_color": status_color,
        "metrics": {
            "high_risk_zones_count": len(zones),
            "estimated_vulnerable_population": total_pop_vulnerable,
            "cooling_centers_active": 8,
            "water_refill_points_active": 31,
            "medical_facilities_standby": 12,
            "grid_peak_strain_forecast": "High (Peak 2:00 PM - 5:30 PM)"
        },
        "zones": zones,
        "ai_priority_recommendations": ai_priority_recommendations,
        "disclaimer": "AI Heat Command Center outputs are algorithmic decision-support estimates for civic planners, not official executive proclamations."
    }
