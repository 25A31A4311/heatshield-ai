/**
 * HeatShield AI - Frontend Application Core
 * Connects UI to deterministic risk engines, Leaflet map, Chart.js,
 * multilingual assistant, and Judge Demo scenarios.
 */

// Application State
const state = {
  currentLocation: {
    name: "Visakhapatnam, Andhra Pradesh",
    lat: 17.6868,
    lon: 83.2185
  },
  currentWeather: null,
  hourlyData: [],
  selectedDay: "today",
  profile: {
    occupation: "general_public",
    age_group: "adult_18_49",
    outdoor_exposure_hours: 3,
    activity_level: "moderate",
    cooling_access: "partial_fan",
    has_chronic_conditions: false
  },
  riskData: null,
  resources: [],
  resourceFilter: "all",
  activeScenario: "",
  language: "en",
  ttsEnabled: false,
  mapInstance: null,
  mapMarkers: [],
  routePolylines: [],
  chartInstance: null
};

// UI Translations Dictionary
const I18N = {
  en: {
    tab_dashboard: "Dashboard",
    tab_map: "Heat Map & POIs",
    tab_route: "Heat-Safe Route",
    tab_assistant: "AI Heat Assistant",
    tab_worker: "Outdoor Worker Mode",
    tab_community: "City Command Center",
    tab_climate: "Climate Trends & Grid",
    tab_agri: "Farm & Livestock",
    danger_window_title: "PEAK DANGER TIME WINDOW",
    why_risk_high: "Why Is The Risk High? (Contributing Factors)",
    what_to_do: "What Should You Do? (Action Plan)",
    disclaimer: "Informational risk estimate; not medical advice."
  },
  te: {
    tab_dashboard: "డ్యాష్‌బోర్డ్",
    tab_map: "హీట్ మ్యాప్ & వనరులు",
    tab_route: "సురక్షిత మార్గం",
    tab_assistant: "AI అసిస్టెంట్",
    tab_worker: "కార్మికుల మోడ్",
    tab_community: "నగర కమాండ్ సెంటర్",
    tab_climate: "శీతోష్ణస్థితి పోకడలు",
    tab_agri: "వ్యవసాయం & పశువులు",
    danger_window_title: "గరిష్ట ప్రమాద సమయ విండో",
    why_risk_high: "ప్రమాదం ఎందుకు ఎక్కువగా ఉంది?",
    what_to_do: "మీరు ఏమి చేయాలి? (చర్య ప్రణాళిక)",
    disclaimer: "సమాచార విశ్లేషణ మాత్రమే; వైద్య నిర్ధారణ కాదు."
  },
  hi: {
    tab_dashboard: "डैशबोर्ड",
    tab_map: "हीट मैप व केंद्र",
    tab_route: "सुरक्षित मार्ग",
    tab_assistant: "AI हीट सहायक",
    tab_worker: "श्रमिक सुरक्षा मोड",
    tab_community: "नगर कमान केंद्र",
    tab_climate: "जलवायु रुझान व ग्रिड",
    tab_agri: "कृषि एवं पशुपालन",
    danger_window_title: "चरम खतरे की समय खिड़की",
    why_risk_high: "जोखिम अधिक क्यों है? (कारक विश्लेषण)",
    what_to_do: "आपको क्या करना चाहिए? (कार्य योजना)",
    disclaimer: "सूचनात्मक अनुमान; कोई चिकित्सकीय सलाह नहीं।"
  }
};

// ==========================================
// INITIALIZATION
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupEventListeners();
  loadSavedProfile();
  initApplicationData();
});

function setupNavigation() {
  const tabBtns = document.querySelectorAll(".nav-tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const targetTab = btn.getAttribute("data-tab");
      document.querySelectorAll(".tab-content-panel").forEach(panel => {
        panel.classList.remove("active");
      });
      const activePanel = document.getElementById(targetTab);
      if (activePanel) {
        activePanel.classList.add("active");
      }

      // Re-invalidate map size when navigating to map tab
      if (targetTab === "tab-map" && state.mapInstance) {
        setTimeout(() => state.mapInstance.invalidateSize(), 200);
      }
      // Re-render chart if navigating to climate
      if (targetTab === "tab-climate") {
        renderClimateChart();
      }
    });
  });

  // Brand button returns to dashboard
  document.getElementById("brand-home-btn").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-dashboard"]').click();
  });
}

function setupEventListeners() {
  // Location change
  document.getElementById("location-select").addEventListener("change", (e) => {
    const val = e.target.value;
    handleLocationChange(val);
  });

  // Demo scenario selector
  document.getElementById("demo-scenario-select").addEventListener("change", (e) => {
    const scenario = e.target.value;
    if (scenario) {
      applyDemoScenario(scenario);
    }
  });

  // Language buttons
  document.querySelectorAll(".lang-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".lang-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const lang = btn.getAttribute("data-lang");
      setLanguage(lang);
    });
  });

  // Profile modal open/close
  document.getElementById("open-profile-btn").addEventListener("click", () => {
    document.getElementById("profile-modal").classList.add("open");
  });
  document.getElementById("close-profile-modal-btn").addEventListener("click", () => {
    document.getElementById("profile-modal").classList.remove("open");
  });

  // Profile form submit
  document.getElementById("profile-form").addEventListener("submit", (e) => {
    e.preventDefault();
    saveProfileFromForm();
    document.getElementById("profile-modal").classList.remove("open");
    recalculateRisk();
  });

  // Profile reset
  document.getElementById("btn-reset-profile").addEventListener("click", () => {
    localStorage.removeItem("heatshield_profile");
    state.profile = {
      occupation: "general_public",
      age_group: "adult_18_49",
      outdoor_exposure_hours: 3,
      activity_level: "moderate",
      cooling_access: "partial_fan",
      has_chronic_conditions: false
    };
    populateProfileForm();
    recalculateRisk();
  });

  // Alert modal open/close
  document.getElementById("alert-trigger-btn").addEventListener("click", () => {
    document.getElementById("alert-modal").classList.add("open");
  });
  document.getElementById("close-alert-modal-btn").addEventListener("click", () => {
    document.getElementById("alert-modal").classList.remove("open");
  });
  document.getElementById("btn-trigger-demo-alert").addEventListener("click", () => {
    triggerBrowserAlert("🔥 Extreme Heat Warning: Avoid outdoor exertion between 12:30 PM and 4:30 PM.");
    document.getElementById("alert-modal").classList.remove("open");
  });

  // Timeline day selector
  document.querySelectorAll(".timeline-day-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".timeline-day-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.selectedDay = btn.getAttribute("data-day");
      renderHourlyTimeline();
    });
  });

  // Quick Action Buttons on Dashboard
  document.getElementById("btn-goto-assistant").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-assistant"]').click();
  });
  document.getElementById("btn-goto-map").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-map"]').click();
  });
  document.getElementById("btn-goto-route").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-route"]').click();
  });
  document.getElementById("btn-goto-cooling").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-map"]').click();
    document.querySelector('.map-filter-chip[data-filter="cooling"]').click();
  });
  document.getElementById("view-all-resources-link").addEventListener("click", () => {
    document.querySelector('.nav-tab-btn[data-tab="tab-map"]').click();
  });

  // Map Filter Chips
  document.querySelectorAll(".map-filter-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".map-filter-chip").forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.resourceFilter = chip.getAttribute("data-filter");
      renderMapMarkers();
      renderResourcesSidebar();
    });
  });

  // Route calculation button
  document.getElementById("btn-calculate-route").addEventListener("click", handleCalculateRoute);

  // AI Chat send
  document.getElementById("btn-send-chat").addEventListener("click", handleSendChat);
  document.getElementById("chat-user-input").addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSendChat();
  });

  // Chat prompt chips
  document.querySelectorAll(".prompt-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-query");
      document.getElementById("chat-user-input").value = q;
      handleSendChat();
    });
  });

  // TTS Toggle
  document.getElementById("tts-audio-toggle").addEventListener("change", (e) => {
    state.ttsEnabled = e.target.checked;
  });

  // Worker Shift update
  document.getElementById("btn-update-worker-shift").addEventListener("click", updateWorkerShiftPlan);

  // Agriculture & Livestock buttons
  document.getElementById("btn-calc-crop").addEventListener("click", assessCropStress);
  document.getElementById("btn-calc-livestock").addEventListener("click", assessLivestockTHI);
}

// ==========================================
// CORE DATA LOADING & CALCULATION
// ==========================================
async function initApplicationData() {
  await fetchWeatherAndCalculate();
  await loadNearbyResources();
  initMap();
  updateWorkerShiftPlan();
  loadCommunityCommandData();
  loadClimateTrends();
}

async function fetchWeatherAndCalculate() {
  try {
    const lat = state.currentLocation.lat;
    const lon = state.currentLocation.lon;
    const scenario = state.activeScenario ? state.activeScenario.replace("scenario_", "") : "";
    
    const weatherUrl = `/api/weather?lat=${lat}&lon=${lon}${scenario ? `&scenario=${scenario}` : ""}`;
    const res = await fetch(weatherUrl);
    const data = await res.json();

    state.currentWeather = data.current;
    state.hourlyData = data.hourly_data;

    // Update location label
    if (data.location && data.location.name) {
      document.getElementById("hero-location-text").textContent = data.location.name;
    }
    
    // Update data badge
    const badge = document.getElementById("weather-source-badge");
    badge.textContent = data.data_status || "Live Open-Meteo API";
    if (data.is_live) {
      badge.className = "data-status-badge live";
    } else {
      badge.className = "data-status-badge demo";
    }

    await recalculateRisk();

  } catch (err) {
    console.warn("Weather fetch failed, utilizing resilient offline fallback:", err);
  }
}

async function recalculateRisk() {
  if (!state.currentWeather) return;

  const current = state.currentWeather;
  const payload = {
    temp_c: current.temp_c,
    humidity: current.humidity,
    apparent_temp_c: current.apparent_temp_c,
    wind_speed: current.wind_speed_kmh,
    uv_index: current.uv_index,
    hour: new Date().getHours(),
    profile: state.profile,
    hourly_data: state.hourlyData.slice(0, 24)
  };

  try {
    const res = await fetch("/api/risk/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const riskResult = await res.json();
    state.riskData = riskResult;
    renderDashboard();
  } catch (err) {
    console.error("Risk calculation error:", err);
  }
}

// ==========================================
// DASHBOARD RENDERING
// ==========================================
function renderDashboard() {
  if (!state.riskData) return;

  const env = state.riskData.environmental_risk;
  const pers = state.riskData.personal_risk;
  const danger = state.riskData.danger_window;
  const current = state.currentWeather;

  // 1. Hero Score
  const scoreVal = pers.personal_risk_score;
  document.getElementById("hero-score-val").textContent = scoreVal;
  document.getElementById("val-personal-score").textContent = `${scoreVal}/100`;
  document.getElementById("val-env-score").textContent = `${env.environmental_risk_score}/100`;

  // Circular gauge animation (circumference = 2 * PI * 60 = ~377)
  const offset = 377 - (377 * (scoreVal / 100));
  const ring = document.getElementById("score-progress-ring");
  ring.style.strokeDashoffset = offset;
  ring.style.stroke = pers.color;

  // Severity Pill & Box Style
  const pill = document.getElementById("hero-severity-pill");
  pill.style.background = pers.color;
  document.getElementById("hero-severity-emoji").textContent = pers.emoji;
  document.getElementById("hero-severity-label").textContent = `${pers.risk_category} HEAT RISK`;

  const heroBox = document.getElementById("hero-risk-card");
  heroBox.className = `card hero-risk-box ${pers.risk_category.toLowerCase().replace(" ", "-")}`;

  document.getElementById("hero-risk-summary").textContent = env.summary;

  // 2. Danger Window
  if (danger && danger.has_danger_window) {
    document.getElementById("hero-danger-window-text").textContent = danger.window_display;
    document.getElementById("hero-peak-hour-text").textContent = danger.peak_hour;
    document.getElementById("hero-peak-temp-text").textContent = `${danger.peak_temp_c}°C`;
  } else {
    document.getElementById("hero-danger-window-text").textContent = "No Extreme Danger Expected";
    document.getElementById("hero-peak-hour-text").textContent = danger ? danger.peak_hour : "--";
    document.getElementById("hero-peak-temp-text").textContent = `${current.temp_c}°C`;
  }

  // 3. Metrics Strip
  document.getElementById("metric-temp").textContent = `${current.temp_c}°C`;
  document.getElementById("metric-apparent").textContent = `${current.apparent_temp_c}°C`;
  document.getElementById("metric-humidity").textContent = `${current.humidity}%`;
  document.getElementById("metric-wind").textContent = `${current.wind_speed_kmh} km/h`;
  document.getElementById("metric-uv").textContent = current.uv_index;
  document.getElementById("metric-swbgt").textContent = `${env.metrics.swbgt_c}°C`;

  // 4. Contributing Factors
  const factorsList = document.getElementById("contributing-factors-list");
  factorsList.innerHTML = "";
  (env.contributing_factors || []).forEach(f => {
    const li = document.createElement("li");
    li.className = "factor-item";
    li.textContent = f;
    factorsList.appendChild(li);
  });
  (pers.vulnerability_reasons || []).forEach(r => {
    const li = document.createElement("li");
    li.className = "factor-item";
    li.style.borderLeftColor = "#3b82f6";
    li.textContent = `[Personal Modifier] ${r}`;
    factorsList.appendChild(li);
  });

  // 5. Actionable Recommendations
  const recContainer = document.getElementById("recommendations-list");
  recContainer.innerHTML = "";
  (pers.recommendations || []).forEach(rec => {
    const div = document.createElement("div");
    div.className = "recommendation-card";
    div.innerHTML = `
      <span class="rec-icon">⚡</span>
      <div>${rec}</div>
    `;
    recContainer.appendChild(div);
  });

  // Profile tag
  document.getElementById("rec-profile-tag").textContent = pers.profile_summary.occupation_title;
  document.getElementById("profile-btn-label").textContent = `Profile: ${pers.profile_summary.occupation_title}`;

  // 6. Hourly Timeline
  renderHourlyTimeline();
}

function renderHourlyTimeline() {
  if (!state.hourlyData || state.hourlyData.length === 0) return;

  const container = document.getElementById("hourly-timeline-container");
  container.innerHTML = "";

  const dayFilter = state.selectedDay;
  const filtered = state.hourlyData.filter(item => (item.day_label || "today") === dayFilter);

  filtered.forEach(h => {
    const card = document.createElement("div");
    const isPeak = h.apparent_temp_c >= 45 || h.temp_c >= 40;
    card.className = `hourly-timeline-card ${isPeak ? "danger-peak" : ""}`;

    const hourStr = formatHourDisplay(h.hour);
    // Simple category color
    let catColor = "#10b981";
    let catText = "LOW";
    if (h.temp_c >= 41) { catColor = "#dc2626"; catText = "EXTREME"; }
    else if (h.temp_c >= 37) { catColor = "#ef4444"; catText = "V.HIGH"; }
    else if (h.temp_c >= 32) { catColor = "#f97316"; catText = "HIGH"; }
    else if (h.temp_c >= 27) { catColor = "#f59e0b"; catText = "MOD"; }

    card.innerHTML = `
      <div class="hourly-time-label">${hourStr}</div>
      <div class="hourly-temp-label">${h.temp_c}°C</div>
      <div style="font-size: 0.7rem; color: var(--text-dim); margin-bottom: 4px;">Feels ${h.apparent_temp_c}°C</div>
      <span class="hourly-risk-badge" style="background: ${catColor};">${catText}</span>
    `;
    container.appendChild(card);
  });
}

function formatHourDisplay(hour) {
  if (hour === 0) return "12 AM";
  if (hour < 12) return `${hour} AM`;
  if (hour === 12) return "12 PM";
  return `${hour - 12} PM`;
}

// ==========================================
// INTERACTIVE MAP & POI ENGINE
// ==========================================
async function loadNearbyResources() {
  try {
    const lat = state.currentLocation.lat;
    const lon = state.currentLocation.lon;
    const res = await fetch(`/api/resources?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    state.resources = data.resources || [];
    renderDashboardQuickResources();
    renderResourcesSidebar();
    renderMapMarkers();
  } catch (err) {
    console.error("Resource fetch failed:", err);
  }
}

function initMap() {
  const mapEl = document.getElementById("map-view-canvas");
  if (!mapEl) return;

  // Check if Leaflet L is defined
  if (typeof L === "undefined") {
    renderCanvasFallbackMap(mapEl);
    return;
  }

  try {
    const lat = state.currentLocation.lat;
    const lon = state.currentLocation.lon;

    state.mapInstance = L.map("map-view-canvas").setView([lat, lon], 14);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
    }).addTo(state.mapInstance);

    // Add Heat Stress Zone Rings (Visualizing Urban Heat Island)
    const heatZoneCircle = L.circle([lat, lon], {
      color: "#ef4444",
      fillColor: "#ef4444",
      fillOpacity: 0.2,
      radius: 800
    }).addTo(state.mapInstance);
    heatZoneCircle.bindPopup("<strong>🔴 Hyperlocal Extreme Heat Zone</strong><br>Surface temperature elevated by asphalt density.");

    renderMapMarkers();

  } catch (err) {
    console.warn("Leaflet map initialization fallback:", err);
    renderCanvasFallbackMap(mapEl);
  }
}

function renderMapMarkers() {
  if (!state.mapInstance || typeof L === "undefined") return;

  // Clear existing markers
  state.mapMarkers.forEach(m => state.mapInstance.removeLayer(m));
  state.mapMarkers = [];

  const filter = state.resourceFilter;
  const filtered = filter === "all" ? state.resources : state.resources.filter(r => r.category === filter);

  filtered.forEach(r => {
    let iconEmoji = "📍";
    if (r.category === "water") iconEmoji = "🚰";
    else if (r.category === "cooling") iconEmoji = "🌳";
    else if (r.category === "medical") iconEmoji = "🏥";

    const customIcon = L.divIcon({
      html: `<div style="background:#1e293b; border:2px solid #38bdf8; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; font-size:16px; box-shadow:0 0 8px rgba(0,0,0,0.5);">${iconEmoji}</div>`,
      className: "custom-leaflet-icon",
      iconSize: [32, 32],
      iconAnchor: [16, 16]
    });

    const marker = L.marker([r.lat, r.lon], { icon: customIcon }).addTo(state.mapInstance);
    marker.bindPopup(`
      <div style="font-family:sans-serif; min-width:180px;">
        <strong style="color:#0f172a; font-size:13px;">${r.name}</strong><br>
        <span style="font-size:11px; color:#475569;">${r.cooling_type || r.category}</span><br>
        <span style="font-size:11px; color:#0284c7; font-weight:bold;">${r.distance_km} km away • ${r.open_hours}</span><br>
        <span style="font-size:10px; background:#e2e8f0; padding:2px 4px; border-radius:3px;">${r.data_status}</span>
      </div>
    `);

    state.mapMarkers.push(marker);
  });

  document.getElementById("map-counter-text").textContent = `Showing ${filtered.length} active resources`;
}

function renderResourcesSidebar() {
  const container = document.getElementById("map-sidebar-resource-list");
  if (!container) return;
  container.innerHTML = "";

  const filter = state.resourceFilter;
  const filtered = filter === "all" ? state.resources : state.resources.filter(r => r.category === filter);

  filtered.forEach(r => {
    const card = document.createElement("div");
    card.className = "resource-card";
    card.innerHTML = `
      <div class="resource-card-top">
        <span class="resource-card-name">${r.icon} ${r.name}</span>
        <span class="resource-card-dist">${r.distance_km} km</span>
      </div>
      <div class="resource-card-desc">${r.cooling_type || ""} • ${r.open_hours}</div>
      <div style="margin-top: 4px; display: flex; justify-content: space-between; align-items: center;">
        <span class="data-status-badge ${r.is_demo ? "demo" : "live"}">${r.data_status}</span>
        <button style="background:none; border:none; color:#38bdf8; font-size:0.75rem; cursor:pointer;" onclick="panToResource(${r.lat}, ${r.lon})">Locate on Map →</button>
      </div>
    `;
    container.appendChild(card);
  });
}

function renderDashboardQuickResources() {
  const container = document.getElementById("dashboard-quick-resources");
  if (!container) return;
  container.innerHTML = "";

  state.resources.slice(0, 3).forEach(r => {
    const div = document.createElement("div");
    div.className = "resource-card";
    div.innerHTML = `
      <div class="resource-card-top">
        <span class="resource-card-name">${r.icon} ${r.name}</span>
        <span class="resource-card-dist">${r.distance_km} km</span>
      </div>
      <div class="resource-card-desc">${r.cooling_type || ""} (${r.data_status})</div>
    `;
    container.appendChild(div);
  });
}

window.panToResource = function(lat, lon) {
  if (state.mapInstance) {
    state.mapInstance.setView([lat, lon], 16);
    document.querySelector('.nav-tab-btn[data-tab="tab-map"]').click();
  }
};

function renderCanvasFallbackMap(container) {
  container.innerHTML = `
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; color:#94a3b8; padding:2rem; text-align:center;">
      <div style="font-size:3rem; margin-bottom:1rem;">🗺️</div>
      <h3 style="color:#fff; margin-bottom:0.5rem;">Interactive Hyperlocal Heat Mesh</h3>
      <p style="font-size:0.85rem; max-width:400px; margin-bottom:1rem;">
        Map canvas rendered using local vector coordinates. Active Heat Island Center: ${state.currentLocation.name}.
      </p>
      <div style="background:#1e293b; padding:1rem; border-radius:8px; width:100%; max-width:480px; text-align:left;">
        <div style="font-size:0.8rem; color:#38bdf8; font-weight:700; margin-bottom:0.5rem;">GEO-COORDINATE POI MESH:</div>
        ${state.resources.slice(0, 4).map(r => `
          <div style="display:flex; justify-content:space-between; font-size:0.8rem; padding:4px 0; border-bottom:1px solid #334155;">
            <span>${r.icon} ${r.name}</span>
            <span style="color:#f59e0b;">${r.distance_km} km</span>
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

// ==========================================
// HEAT-SAFE ROUTE PLANNER
// ==========================================
async function handleCalculateRoute() {
  const startText = document.getElementById("route-start-input").value;
  const destText = document.getElementById("route-dest-input").value;

  const lat = state.currentLocation.lat;
  const lon = state.currentLocation.lon;
  const temp = state.currentWeather ? state.currentWeather.temp_c : 38.0;

  const payload = {
    start_lat: lat,
    start_lon: lon,
    dest_lat: lat + 0.015,
    dest_lon: lon - 0.010,
    temp_c: temp
  };

  try {
    const res = await fetch("/api/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const routeData = await res.json();
    renderRouteComparison(routeData);

    // If Leaflet is available, draw both paths
    if (state.mapInstance && typeof L !== "undefined") {
      drawRoutesOnMap(routeData);
    }
  } catch (err) {
    console.error("Route calculation error:", err);
  }
}

function renderRouteComparison(data) {
  const fastest = data.fastest_route;
  const safer = data.heat_safer_route;

  document.getElementById("fastest-time-val").innerHTML = `
    ${fastest.duration_minutes} mins <span style="font-size: 1rem; color: var(--text-muted);">(${fastest.distance_km} km)</span>
  `;
  document.getElementById("safer-time-val").innerHTML = `
    ${safer.duration_minutes} mins <span style="font-size: 1rem; color: var(--text-muted);">(${safer.distance_km} km, +${safer.time_penalty_minutes} min)</span>
  `;

  const fastestWarnList = document.getElementById("fastest-warnings-list");
  fastestWarnList.innerHTML = "";
  fastest.warnings.forEach(w => {
    const li = document.createElement("li");
    li.textContent = w;
    fastestWarnList.appendChild(li);
  });

  const saferBenefitsList = document.getElementById("safer-benefits-list");
  saferBenefitsList.innerHTML = "";
  safer.benefits.forEach(b => {
    const li = document.createElement("li");
    li.textContent = b;
    saferBenefitsList.appendChild(li);
  });
}

function drawRoutesOnMap(data) {
  // Clear old polylines
  state.routePolylines.forEach(p => state.mapInstance.removeLayer(p));
  state.routePolylines = [];

  const fastestPoly = L.polyline(data.fastest_route.waypoints, {
    color: "#ef4444",
    weight: 5,
    opacity: 0.85,
    dashArray: "8, 6"
  }).addTo(state.mapInstance);
  fastestPoly.bindPopup("<strong>Fastest Route</strong><br>High solar & asphalt exposure.");

  const saferPoly = L.polyline(data.heat_safer_route.waypoints, {
    color: "#10b981",
    weight: 6,
    opacity: 0.95
  }).addTo(state.mapInstance);
  saferPoly.bindPopup("<strong>Recommended Heat-Safer Route</strong><br>Shade canopy & water refill corridors.");

  state.routePolylines.push(fastestPoly, saferPoly);
  state.mapInstance.fitBounds(saferPoly.getBounds(), { padding: [40, 40] });
}

// ==========================================
// AI HEAT ASSISTANT
// ==========================================
async function handleSendChat() {
  const inputEl = document.getElementById("chat-user-input");
  const query = inputEl.value.trim();
  if (!query) return;

  inputEl.value = "";
  appendChatMessage("user", query);

  // Build context
  const context = {
    weather: { current: state.currentWeather },
    env_risk: state.riskData ? state.riskData.environmental_risk : {},
    personal_risk: state.riskData ? state.riskData.personal_risk : {},
    danger_window: state.riskData ? state.riskData.danger_window : {},
    profile: state.profile
  };

  try {
    const res = await fetch("/api/assistant/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, context, language: state.language })
    });
    const ans = await res.json();
    appendChatMessage("assistant", ans.response);

    if (ans.provider) {
      document.getElementById("ai-provider-badge").textContent = ans.provider;
    }

    // TTS Readout if enabled
    if (state.ttsEnabled && "speechSynthesis" in window) {
      speakText(ans.response);
    }

  } catch (err) {
    appendChatMessage("assistant", "Network connection to the AI engine was interrupted. Please review current danger windows on the Dashboard.");
  }
}

function appendChatMessage(sender, text) {
  const container = document.getElementById("chat-messages-box");
  const bubble = document.createElement("div");
  bubble.className = `chat-message-bubble ${sender}`;
  // Formatted markdown / linebreaks
  bubble.innerHTML = text.replace(/\n/g, "<br>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function speakText(text) {
  try {
    // Strip HTML and asterisks
    const clean = text.replace(/<[^>]*>?/gm, "").replace(/\*/g, "");
    const utterance = new SpeechSynthesisUtterance(clean);
    utterance.rate = 1.0;
    if (state.language === "hi") utterance.lang = "hi-IN";
    else if (state.language === "te") utterance.lang = "te-IN";
    else utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  } catch (e) {
    console.warn("TTS error:", e);
  }
}

// ==========================================
// OUTDOOR WORKER MODE
// ==========================================
async function updateWorkerShiftPlan() {
  const loc = document.getElementById("worker-location-name").value;
  const start = parseInt(document.getElementById("worker-shift-start").value);
  const end = parseInt(document.getElementById("worker-shift-end").value);
  const intensity = document.getElementById("worker-intensity").value;

  try {
    const res = await fetch(`/api/worker-schedule?location=${encodeURIComponent(loc)}&shift_start=${start}&shift_end=${end}&intensity=${intensity}`);
    const data = await res.json();

    document.getElementById("worker-overall-risk-label").textContent = `
      ${data.shift_overall_risk.emoji} ${data.shift_overall_risk.category} (${data.shift_overall_risk.score}/100)
    `;
    document.getElementById("worker-overall-risk-label").style.color = data.shift_overall_risk.color;
    document.getElementById("worker-hydration-quota-val").textContent = `🚰 ${data.total_hydration_quota_liters} Liters (Water + ORS)`;

    const rowsContainer = document.getElementById("worker-schedule-rows");
    rowsContainer.innerHTML = "";

    data.schedule.forEach(block => {
      const row = document.createElement("div");
      row.className = "worker-shift-row";
      row.innerHTML = `
        <div class="worker-shift-hour">⏰ ${block.hour_range}</div>
        <div style="font-size:0.85rem; color:#cbd5e1;">${block.temp_c}°C (${block.humidity}% RH)</div>
        <div class="worker-shift-ratio">${block.work_rest_ratio}</div>
        <div style="font-size:0.85rem; color:#38bdf8; font-weight:700;">💧 ${block.hydration_rate}</div>
        <div style="font-size:0.8rem; color:${block.color}; font-weight:700; width:100%; margin-top:4px;">${block.advisory}</div>
      `;
      rowsContainer.appendChild(row);
    });

    const guideList = document.getElementById("worker-guidance-list");
    guideList.innerHTML = "";
    data.actionable_guidance.forEach(g => {
      const li = document.createElement("li");
      li.textContent = g;
      guideList.appendChild(li);
    });

  } catch (err) {
    console.error("Worker schedule fetch error:", err);
  }
}

// ==========================================
// CITY COMMAND CENTER
// ==========================================
async function loadCommunityCommandData() {
  try {
    const res = await fetch("/api/community-command?city=Visakhapatnam&risk_score=90");
    const data = await res.json();

    document.getElementById("civic-status-val").textContent = data.heat_status;
    document.getElementById("civic-status-val").style.color = data.status_color;
    document.getElementById("civic-zones-val").textContent = `${data.metrics.high_risk_zones_count} Wards`;
    document.getElementById("civic-pop-val").textContent = data.metrics.estimated_vulnerable_population.toLocaleString();
    document.getElementById("civic-cooling-val").textContent = `${data.metrics.cooling_centers_active} Facilities`;
    document.getElementById("civic-water-val").textContent = `${data.metrics.water_refill_points_active} Stations`;
    document.getElementById("civic-med-val").textContent = `${data.metrics.medical_facilities_standby} Units`;

    // AI Priority Actions Grid
    const actionsGrid = document.getElementById("civic-actions-grid");
    actionsGrid.innerHTML = "";
    data.ai_priority_recommendations.forEach(act => {
      const card = document.createElement("div");
      card.className = "card";
      card.style.margin = "0";
      card.style.background = "#1a2234";
      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
          <span style="font-size:0.75rem; color:#38bdf8; font-weight:700;">${act.action_id} • ${act.category}</span>
          <span class="data-status-badge live">${act.status}</span>
        </div>
        <div style="font-size:0.95rem; font-weight:800; color:#fff; margin-bottom:0.35rem;">${act.title}</div>
        <div style="font-size:0.8rem; color:#cbd5e1; line-height:1.4;">${act.impact}</div>
      `;
      actionsGrid.appendChild(card);
    });

    // Wards Table
    const tbody = document.getElementById("civic-zones-tbody");
    tbody.innerHTML = "";
    data.zones.forEach(z => {
      const tr = document.createElement("tr");
      tr.style.borderBottom = "1px solid var(--border-color)";
      tr.innerHTML = `
        <td style="padding:0.6rem; font-weight:800; color:#ef4444;">#${z.priority_rank}</td>
        <td style="padding:0.6rem; color:#fff; font-weight:700;">${z.name}</td>
        <td style="padding:0.6rem; color:#f87171;">${z.surface_temp_c}°C</td>
        <td style="padding:0.6rem; color:#cbd5e1;">${z.population_vulnerable_estimate.toLocaleString()}</td>
        <td style="padding:0.6rem; color:#cbd5e1;">${z.cooling_access_rate_pct}%</td>
        <td style="padding:0.6rem; color:#cbd5e1;">${z.canopy_cover_pct}%</td>
        <td style="padding:0.6rem; font-size:0.75rem; color:#38bdf8;">${z.active_interventions_needed[0]}</td>
      `;
      tbody.appendChild(tr);
    });

  } catch (err) {
    console.error("Community command error:", err);
  }
}

// ==========================================
// CLIMATE TRENDS & ENERGY STRESS
// ==========================================
async function loadClimateTrends() {
  try {
    const res = await fetch("/api/historical-trends?region=Visakhapatnam");
    const data = await res.json();

    const list = document.getElementById("climate-insights-list");
    list.innerHTML = "";
    data.key_insights.forEach(ins => {
      const li = document.createElement("li");
      li.className = "factor-item";
      li.style.borderLeftColor = "#ef4444";
      li.textContent = ins;
      list.appendChild(li);
    });

    renderClimateChart(data.yearly_records);

  } catch (err) {
    console.error("Climate trends error:", err);
  }
}

function renderClimateChart(records) {
  if (typeof Chart === "undefined") return;

  const canvas = document.getElementById("climateTrendChart");
  if (!canvas) return;

  if (state.chartInstance) {
    state.chartInstance.destroy();
  }

  const defaultRecords = [
    { year: 2016, extreme_heat_days_over_40c: 14, avg_summer_max_c: 37.2 },
    { year: 2018, extreme_heat_days_over_40c: 15, avg_summer_max_c: 37.4 },
    { year: 2020, extreme_heat_days_over_40c: 19, avg_summer_max_c: 38.0 },
    { year: 2022, extreme_heat_days_over_40c: 28, avg_summer_max_c: 39.4 },
    { year: 2024, extreme_heat_days_over_40c: 37, avg_summer_max_c: 40.7 },
    { year: 2025, extreme_heat_days_over_40c: 41, avg_summer_max_c: 41.2 }
  ];

  const dataList = records || defaultRecords;
  const labels = dataList.map(r => r.year);
  const days = dataList.map(r => r.extreme_heat_days_over_40c);
  const temps = dataList.map(r => r.avg_summer_max_c);

  const ctx = canvas.getContext("2d");
  state.chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Extreme Heat Days (>40°C)",
          data: days,
          backgroundColor: "rgba(239, 68, 68, 0.75)",
          borderColor: "#ef4444",
          borderWidth: 1,
          yAxisID: "y"
        },
        {
          type: "line",
          label: "Avg Summer Max (°C)",
          data: temps,
          borderColor: "#f59e0b",
          backgroundColor: "#f59e0b",
          borderWidth: 2,
          yAxisID: "y1"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { color: "#1e293b" }, ticks: { color: "#94a3b8" } },
        y: {
          grid: { color: "#1e293b" },
          ticks: { color: "#94a3b8" },
          title: { display: true, text: "Days Count", color: "#94a3b8" }
        },
        y1: {
          position: "right",
          grid: { display: false },
          ticks: { color: "#f59e0b" },
          title: { display: true, text: "Temperature (°C)", color: "#f59e0b" }
        }
      },
      plugins: {
        legend: { labels: { color: "#cbd5e1" } }
      }
    }
  });
}

// ==========================================
// FARM & LIVESTOCK MODES
// ==========================================
async function assessCropStress() {
  const crop = document.getElementById("agri-crop-select").value;
  const stage = document.getElementById("agri-stage-select").value;
  const temp = state.currentWeather ? state.currentWeather.temp_c : 39.5;
  const hum = state.currentWeather ? state.currentWeather.humidity : 60.0;

  try {
    const res = await fetch("/api/agriculture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: "crop", crop, growth_stage: stage, temp_c: temp, humidity: hum })
    });
    const data = await res.json();

    document.getElementById("crop-status-pill").textContent = data.stress_level;
    document.getElementById("crop-status-pill").style.color = data.color;
    document.getElementById("crop-irrigation-window").textContent = `💧 Optimal Irrigation Window: ${data.recommended_irrigation_window}`;

    const list = document.getElementById("crop-guidance-list");
    list.innerHTML = "";
    data.guidance.forEach(g => {
      const li = document.createElement("li");
      li.textContent = g;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Crop error:", err);
  }
}

async function assessLivestockTHI() {
  const animal = document.getElementById("livestock-animal-select").value;
  const temp = state.currentWeather ? state.currentWeather.temp_c : 39.0;
  const hum = state.currentWeather ? state.currentWeather.humidity : 68.0;

  try {
    const res = await fetch("/api/agriculture", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: "livestock", animal_type: animal, temp_c: temp, humidity: hum })
    });
    const data = await res.json();

    document.getElementById("livestock-thi-val").textContent = data.thi_score;
    document.getElementById("livestock-status-pill").textContent = data.status;
    document.getElementById("livestock-status-pill").style.color = data.color;

    const list = document.getElementById("livestock-guidance-list");
    list.innerHTML = "";
    data.guidance.forEach(g => {
      const li = document.createElement("li");
      li.textContent = g;
      list.appendChild(li);
    });
  } catch (err) {
    console.error("Livestock error:", err);
  }
}

// ==========================================
// DEMO SCENARIOS (JUDGE DEMO HARNESS)
// ==========================================
async function applyDemoScenario(scenarioKey) {
  state.activeScenario = scenarioKey;
  const tag = document.getElementById("scenario-active-tag");
  tag.textContent = `DEMO SCENARIO: ${scenarioKey.toUpperCase()}`;
  tag.className = "data-status-badge demo";

  if (scenarioKey === "scenario_normal") {
    state.currentLocation = { name: "Moderate Climate Zone", lat: 51.5074, lon: -0.1278 };
    state.profile = {
      occupation: "office_worker",
      age_group: "adult_18_49",
      outdoor_exposure_hours: 1,
      activity_level: "sedentary",
      cooling_access: "full_ac",
      has_chronic_conditions: false
    };
  } else if (scenarioKey === "scenario_extreme_heatwave") {
    state.currentLocation = { name: "Visakhapatnam, Andhra Pradesh", lat: 17.6868, lon: 83.2185 };
    state.profile = {
      occupation: "general_public",
      age_group: "adult_18_49",
      outdoor_exposure_hours: 3,
      activity_level: "moderate",
      cooling_access: "partial_fan",
      has_chronic_conditions: false
    };
  } else if (scenarioKey === "scenario_outdoor_worker") {
    state.currentLocation = { name: "Visakhapatnam Port District", lat: 17.6868, lon: 83.2185 };
    state.profile = {
      occupation: "construction_worker",
      age_group: "adult_18_49",
      outdoor_exposure_hours: 8,
      activity_level: "strenuous",
      cooling_access: "no_cooling",
      has_chronic_conditions: false
    };
  } else if (scenarioKey === "scenario_elderly_vulnerable") {
    state.currentLocation = { name: "New Delhi Urban Core", lat: 28.6139, lon: 77.2090 };
    state.profile = {
      occupation: "elderly_retired",
      age_group: "elderly_65_plus",
      outdoor_exposure_hours: 1,
      activity_level: "sedentary",
      cooling_access: "no_cooling",
      has_chronic_conditions: true
    };
  } else if (scenarioKey === "scenario_extreme_no_cooling") {
    state.currentLocation = { name: "Phoenix Metro, Arizona", lat: 33.4484, lon: -112.0740 };
    state.profile = {
      occupation: "general_public",
      age_group: "adult_50_64",
      outdoor_exposure_hours: 4,
      activity_level: "moderate",
      cooling_access: "no_cooling",
      has_chronic_conditions: true
    };
  }

  populateProfileForm();
  await fetchWeatherAndCalculate();
  await loadNearbyResources();
  if (state.mapInstance) {
    state.mapInstance.setView([state.currentLocation.lat, state.currentLocation.lon], 14);
  }
}

function handleLocationChange(locKey) {
  if (locKey === "gps") {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => {
          state.currentLocation = {
            name: "Current GPS Position",
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
          };
          fetchWeatherAndCalculate();
          loadNearbyResources();
        },
        err => {
          alert("Geolocation permission denied. Reverting to Visakhapatnam reference.");
          document.getElementById("location-select").value = "visakhapatnam";
        }
      );
    }
  } else if (locKey === "delhi") {
    state.currentLocation = { name: "New Delhi, India", lat: 28.6139, lon: 77.2090 };
  } else if (locKey === "phoenix") {
    state.currentLocation = { name: "Phoenix, USA", lat: 33.4484, lon: -112.0740 };
  } else if (locKey === "mild") {
    state.currentLocation = { name: "Temperate Zone", lat: 51.5074, lon: -0.1278 };
  } else {
    state.currentLocation = { name: "Visakhapatnam, Andhra Pradesh", lat: 17.6868, lon: 83.2185 };
  }

  state.activeScenario = "";
  document.getElementById("scenario-active-tag").textContent = "CALIBRATED BASELINE / LIVE";
  fetchWeatherAndCalculate();
  loadNearbyResources();
}

// ==========================================
// PROFILE PERSISTENCE
// ==========================================
function loadSavedProfile() {
  const saved = localStorage.getItem("heatshield_profile");
  if (saved) {
    try {
      state.profile = JSON.parse(saved);
    } catch (e) {}
  }
  populateProfileForm();
}

function populateProfileForm() {
  document.getElementById("prof-occupation").value = state.profile.occupation;
  document.getElementById("prof-age-group").value = state.profile.age_group;
  document.getElementById("prof-exposure").value = state.profile.outdoor_exposure_hours;
  document.getElementById("prof-activity").value = state.profile.activity_level;
  document.getElementById("prof-cooling").value = state.profile.cooling_access;
  document.getElementById("prof-chronic").checked = state.profile.has_chronic_conditions;
}

function saveProfileFromForm() {
  state.profile = {
    occupation: document.getElementById("prof-occupation").value,
    age_group: document.getElementById("prof-age-group").value,
    outdoor_exposure_hours: parseFloat(document.getElementById("prof-exposure").value),
    activity_level: document.getElementById("prof-activity").value,
    cooling_access: document.getElementById("prof-cooling").value,
    has_chronic_conditions: document.getElementById("prof-chronic").checked
  };
  localStorage.setItem("heatshield_profile", JSON.stringify(state.profile));
}

// ==========================================
// LANGUAGE SWITCHER (i18n)
// ==========================================
function setLanguage(lang) {
  state.language = lang;
  const dict = I18N[lang] || I18N["en"];

  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Re-run chat sample if in assistant tab
  if (lang === "te") {
    document.getElementById("chat-user-input").placeholder = "ఉష్ణ భద్రతా ప్రశ్న అడగండి (ఉదా: 3 గంటలకు బయటకు వెళ్లవచ్చా?)...";
  } else if (lang === "hi") {
    document.getElementById("chat-user-input").placeholder = "गर्मी सुरक्षा से जुड़ा प्रश्न पूछें (उदा: क्या मैं दोपहर 2 बजे बाहर जा सकता हूँ?)...";
  } else {
    document.getElementById("chat-user-input").placeholder = "Ask a heat safety question (e.g. Can I walk outside at 2 PM?)...";
  }
}

// ==========================================
// NOTIFICATIONS & ALERTS
// ==========================================
function triggerBrowserAlert(message) {
  if ("Notification" in window && Notification.permission === "granted") {
    new Notification("🔥 HeatShield AI Alert", {
      body: message,
      icon: "/favicon.ico"
    });
  } else if ("Notification" in window && Notification.permission !== "denied") {
    Notification.requestPermission().then(perm => {
      if (perm === "granted") {
        new Notification("🔥 HeatShield AI Alert", { body: message });
      }
    });
  }
  // Also show prominent alert banner update
  document.getElementById("alert-banner-text").innerHTML = `<strong>SIMULATED DEMO ALERT:</strong> ${message}`;
}
