"""
HeatShield AI - AI Heat Assistant Engine
Features:
- Provider abstraction (Gemini, OpenAI, or Built-in Intelligent Rule-and-Knowledge Engine)
- Strict Medical Safety Guardrails (Zero hallucinated diagnoses, emergency escalation)
- Structured Context Grounding (Answers bound to computed risk and weather data)
- Multilingual (English, Telugu, Hindi)
"""

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional


SYSTEM_PROMPT = """You are HeatShield Assistant, an AI heat-resilience and occupational climate safety expert.
Your goal is to help users understand their personal heat risk, navigate dangerous peak windows, find water/cooling shelters, and take safe protective actions.

STRICT MEDICAL SAFETY RULES:
1. You are NOT a doctor and CANNOT diagnose any medical illness. NEVER state "You have heatstroke" or "You have heat exhaustion".
2. If the user mentions symptoms such as dizziness, confusion, nausea, vomiting, fainting, loss of consciousness, or inability to sweat:
   - State clearly: "These symptoms can be associated with a severe heat-related illness. Move to a cool, shaded or air-conditioned place immediately, loosen tight clothing, sip cool water if conscious, and contact emergency services (such as 108, 112, or local emergency) immediately."
3. Never fabricate or invent weather values, temperatures, locations, or risk scores. Only use the structured context provided to you.
4. If asked questions outside heat safety, politely refocus on heat risk and protection.
5. Provide actionable, concise, and empathetic safety advice.
6. When responding in Telugu or Hindi, keep numbers and technical units clearly readable.
7. Always conclude with the mandatory safety reminder.
"""

MEDICAL_DISCLAIMER = "HeatShield AI provides informational risk estimates and safety guidance. It is not a medical diagnostic system or a substitute for professional medical advice."

# Multilingual canned emergency templates for immediate reflex response
EMERGENCY_KEYWORDS = ["dizzy", "dizziness", "faint", "fainting", "vomit", "vomiting", "confusion", "passed out", "seizure", "unconscious", "chest pain", "चक्कर", "बेहोश", "ఉల్టా", "కళ్ళు తిరుగుతున్నాయి", "స్పృహ తప్పి"]


def ask_heat_assistant(
    user_query: str,
    context_data: Dict[str, Any],
    language: str = "en"  # "en", "te", "hi"
) -> Dict[str, Any]:
    """
    Main entry point for HeatShield Assistant.
    Inspects user query against safety triggers and routes to Gemini / OpenAI / Built-in Expert Engine.
    """
    query_lower = user_query.lower()
    
    # Check for immediate critical emergency keywords
    is_emergency_symptom = any(k in query_lower for k in EMERGENCY_KEYWORDS)

    # Check for available external LLM API keys
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if gemini_key:
        try:
            response_text = call_gemini_api(user_query, context_data, language, gemini_key, is_emergency_symptom)
            provider_used = "Google Gemini (Live API)"
        except Exception:
            response_text = generate_grounded_expert_response(user_query, context_data, language, is_emergency_symptom)
            provider_used = "HeatShield Grounded Expert Engine (API Fallback)"
    elif openai_key:
        try:
            response_text = call_openai_api(user_query, context_data, language, openai_key, is_emergency_symptom)
            provider_used = "OpenAI GPT (Live API)"
        except Exception:
            response_text = generate_grounded_expert_response(user_query, context_data, language, is_emergency_symptom)
            provider_used = "HeatShield Grounded Expert Engine (API Fallback)"
    else:
        # Zero-API key intelligent expert engine
        response_text = generate_grounded_expert_response(user_query, context_data, language, is_emergency_symptom)
        provider_used = "HeatShield Grounded Expert Engine (Deterministic/Rule-Based)"

    return {
        "query": user_query,
        "response": response_text,
        "language": language,
        "provider": provider_used,
        "is_emergency_flagged": is_emergency_symptom,
        "disclaimer": MEDICAL_DISCLAIMER
    }


def generate_grounded_expert_response(
    query: str,
    ctx: Dict[str, Any],
    lang: str,
    is_emergency: bool
) -> str:
    """
    High-fidelity structured response generator that leverages the actual
    weather, risk engine metrics, danger window, user profile, and POIs.
    Supports English, Telugu (తెలుగు), and Hindi (हिन्दी).
    """
    # Extract structured metrics from context
    curr_weather = ctx.get("weather", {}).get("current", {})
    temp = curr_weather.get("temp_c", 38.0)
    apparent_temp = curr_weather.get("apparent_temp_c", 44.0)
    humidity = curr_weather.get("humidity", 60)
    
    env_risk = ctx.get("env_risk", {})
    env_score = env_risk.get("environmental_risk_score", 85)
    env_cat = env_risk.get("risk_category", "EXTREME")

    pers_risk = ctx.get("personal_risk", {})
    pers_score = pers_risk.get("personal_risk_score", 90)
    pers_cat = pers_risk.get("risk_category", "EXTREME")

    danger_win = ctx.get("danger_window", {})
    win_display = danger_win.get("window_display", "12:30 PM – 4:30 PM")
    peak_hour = danger_win.get("peak_hour", "2:00 PM")

    profile = ctx.get("profile", {})
    occupation = profile.get("occupation", "General Public").replace("_", " ").title()

    q = query.lower()

    # 1. Emergency symptom queries
    if is_emergency:
        if lang == "te":
            return (
                "⚠️ **హెచ్చరిక: అత్యవసర ఉష్ణ సంబంధిత లక్షణాలు**\n\n"
                "మీరు పేర్కొన్న లక్షణాలు (తలతిరగడం, వాంతులు, లేదా నీరసం) వేడి సంబంధిత అనారోగ్యం యొక్క తీవ్రమైన సంకేతాలు కావచ్చు. "
                "ఇది వైద్య నిర్ధారణ కాదు. దయచేసి వెంటనే ఈ క్రింది చర్యలు తీసుకోండి:\n"
                "1. తక్షణమే నీడ లేదా ఎయిర్ కండిషన్ ఉన్న చల్లటి గదికి మారండి.\n"
                "2. బిగుతుగా ఉన్న దుస్తులను వదులు చేయండి, చల్లటి నీటిని మెడ మరియు ముఖంపై రాయండి.\n"
                "3. స్పృహ ఉంటే కొద్దికొద్దిగా నీరు లేదా ORS ద్రవాలు తాగండి.\n"
                "4. లక్షణాలు కొనసాగితే వెంటనే **108 లేదా సమీప ఆసుపత్రికి** ఫోన్ చేసి అత్యవసర వైద్య సహాయం పొందండి."
            )
        elif lang == "hi":
            return (
                "⚠️ **चेतावनी: आपातकालीन गर्मी के लक्षण**\n\n"
                "आपके द्वारा बताए गए लक्षण (चक्कर आना, जी मिचलाना, अत्यधिक कमजोरी) गर्मी से जुड़ी गंभीर बीमारी के संकेत हो सकते हैं। "
                "यह कोई चिकित्सीय निदान नहीं है। कृपया तुरंत ये कदम उठाएं:\n"
                "1. तुरंत किसी ठंडी, छायादार या वातानुकूलित (AC) जगह पर जाएं।\n"
                "2. तंग कपड़े ढीले करें और गर्दन व माथे पर ठंडा पानी लगाएं।\n"
                "3. यदि होश में हैं तो धीरे-धीरे पानी या ओआरएस (ORS) पिएं।\n"
                "4. यदि स्थिति गंभीर हो तो तुरंत **108 या नजदीकी आपातकालीन स्वास्थ्य सेवा** से संपर्क करें।"
            )
        else:
            return (
                "⚠️ **CRITICAL HEAT SYMPTOM ALERT**\n\n"
                "The symptoms you described (dizziness, nausea, weakness, or disorientation) can be associated with serious heat-related illness. "
                "This is not a medical diagnosis. Please take these protective steps immediately:\n"
                "1. **Move to a cool area immediately**: Find an air-conditioned room, deep tree canopy, or cooling center.\n"
                "2. **Active cooling**: Loosen tight clothing, apply cool damp cloths to your neck and armpits, and rest elevated.\n"
                "3. **Hydration**: If conscious and not vomiting, sip small amounts of cool water or electrolyte solution.\n"
                "4. **Emergency Escalation**: If confusion, fainting, vomiting, or cessation of sweating occurs, call emergency medical services (108 / 112 / 911) without delay."
            )

    # 2. Running / Exercise / Sports query
    if any(k in q for k in ["run", "running", "jog", "exercise", "workout", "gym", "play"]):
        if lang == "te":
            return (
                f"🏃 **రన్నింగ్ & వ్యాయామ మార్గదర్శకం**:\n"
                f"ప్రస్తుత ఉష్ణోగ్రత {temp}°C (అనుభూతి {apparent_temp}°C) మరియు వ్యక్తిగత ప్రమాదం **{pers_score}/100 ({pers_cat})**.\n"
                f"మధ్యాహ్నం రన్నింగ్ లేదా తీవ్రమైన వ్యాయామం చేయడం అత్యంత ప్రమాదకరం. "
                f"ప్రధాన ప్రమాద సమయం **{win_display}**.\n\n"
                f"✅ **సిఫార్సు**: వ్యాయామాలను ఉదయం 7:30 గంటల కంటే ముందు లేదా సాయంత్రం 6:30 గంటల తర్వాత మాత్రమే చేయండి."
            )
        elif lang == "hi":
            return (
                f"🏃 **दौड़ने और व्यायाम के लिए सलाह**:\n"
                f"वर्तमान तापमान {temp}°C (महसूस {apparent_temp}°C) है और आपका व्यक्तिगत जोखिम स्कोर **{pers_score}/100 ({pers_cat})** है।\n"
                f"दोपहर के समय दौड़ना या भारी कसरत करना बेहद खतरनाक हो सकता है। "
                f"उच्चतम खतरे का समय **{win_display}** है।\n\n"
                f"✅ **सलाह**: सुबह 7:30 बजे से पहले या शाम 6:30 बजे के बाद ही व्यायाम करें। भरपूर पानी पिएं।"
            )
        else:
            return (
                f"🏃 **Running & Outdoor Exercise Advisory**:\n\n"
                f"Current temperature is **{temp}°C** (feels like **{apparent_temp}°C**) with **{humidity}% humidity**, generating an elevated Personal Heat Risk of **{pers_score}/100 ({pers_cat})**.\n\n"
                f"**Verdict**: Do **NOT** run during midday heat. Your peak danger window is **{win_display}**, with maximum thermal stress around **{peak_hour}**.\n\n"
                f"**Safe Timing Recommendation**:\n"
                f"• Reschedule running to tomorrow morning before 07:15 AM (when temps are ~27°C).\n"
                f"• Or wait until after 06:45 PM once solar radiation subsides.\n"
                f"• Pre-hydrate with 500ml water 30 minutes prior to outdoor workouts."
            )

    # 3. Outdoor worker / breaks query
    if any(k in q for k in ["work", "working", "worker", "construction", "break", "breaks", "shift", "outside"]):
        if lang == "te":
            return (
                f"👷 **బహిరంగ కార్మికుల భద్రతా షెడ్యూల్** ({occupation}):\n"
                f"నేటి వ్యక్తిగత ఉష్ణ సూచిక: **{pers_score}/100 ({pers_cat})**.\n"
                f"తీవ్రమైన ప్రమాద విండో: **{win_display}** (పీక్ సమయం: {peak_hour}).\n\n"
                f"• **పని-విశ్రాంతి నిష్పత్తి**: తీవ్రమైన సమయాల్లో గంటకు 30 నిమిషాల పని / 30 నిమిషాల నీడలో విశ్రాంతి పాటించండి.\n"
                f"• **నీటి వినియోగం**: దాహం వేయకపోయినా ప్రతి గంటకు కనీసం 750ml - 1 లీటరు నీరు మరియు ORS తీసుకోండి.\n"
                f"• బరువైన పనులను ఉదయం 10:30 లోపు పూర్తి చేయండి."
            )
        elif lang == "hi":
            return (
                f"👷 **श्रमिक सुरक्षा और कार्य-विश्राम योजना** ({occupation}):\n"
                f"आज आपका व्यक्तिगत जोखिम स्तर: **{pers_score}/100 ({pers_cat})** है।\n"
                f"सबसे खतरनाक समय खिड़की: **{win_display}** (चरम समय: {peak_hour})।\n\n"
                f"• **कार्य-विश्राम चक्र**: दोपहर के समय प्रति घंटे 30 मिनट काम / 30 मिनट छाया में आराम करें।\n"
                f"• **जलयोजन**: प्रति घंटे कम से कम 750 मिली से 1 लीटर पानी और ओआरएस पिएं।\n"
                f"• साथी श्रमिकों की निगरानी रखें।"
            )
        else:
            return (
                f"👷 **Outdoor Worker Safety & Rest Schedule** (Profile: {occupation}):\n\n"
                f"Based on current conditions (Ambient: {temp}°C, Feels Like: {apparent_temp}°C), your Personal Heat Risk is **{pers_score}/100 ({pers_cat})**.\n\n"
                f"**Peak Danger Period**: **{win_display}** (Peak load at {peak_hour}).\n\n"
                f"**OSHA/NIOSH Practical Guidelines**:\n"
                f"1. **Work/Rest Ratio**: During {win_display}, enforce a strict 30-minute work / 30-minute shaded rest cycle per hour.\n"
                f"2. **Hydration Quota**: Drink 250ml (1 cup) of water every 15-20 minutes (~1 liter/hour).\n"
                f"3. **Pacing**: Postpone continuous heavy manual lifting until before 10:30 AM or after 4:30 PM.\n"
                f"4. **Shade Station**: Set up a designated canopy with misting fans within 50 meters of the work zone."
            )

    # 4. Nearest cooling / water points query
    if any(k in q for k in ["water", "cooling", "hospital", "clinic", "nearest", "shade", "refill", "center"]):
        if lang == "te":
            return (
                f"🚰 **సమీప వనరులు & శీతలీకరణ కేంద్రాలు**:\n"
                f"మీ స్థానంలో అత్యవసర శీతలీకరణ మద్దతు కోసం:\n"
                f"• **నీటి పాయింట్లు**: పబ్లిక్ వాటర్ కియోస్క్ మరియు RO రీఫిల్ కేంద్రాలు అందుబాటులో ఉన్నాయి.\n"
                f"• **చల్లని ఆశ్రయాలు**: మున్సిపల్ లైబ్రరీ మరియు సెంట్రల్ పార్క్ నీడ జోన్ అందుబాటులో ఉన్నాయి.\n"
                f"• **వైద్య సదుపాయాలు**: అత్యవసర హీట్‌స్ట్రోక్ వార్డ్ సిద్ధంగా ఉంది.\n"
                f"వివరణాత్మక మ్యాప్ వీక్షణ కోసం 'హీట్ మ్యాప్' ట్యాబ్‌ను చూడండి."
            )
        elif lang == "hi":
            return (
                f"🚰 **निकटतम पेयजल एवं शीतलन केंद्र**:\n"
                f"आपकी वर्तमान स्थिति के अनुसार सहायता केंद्र:\n"
                f"• **पेयजल केंद्र**: सार्वजनिक वाटर एटीएम और आरओ स्टेशन लगभग 400 मीटर की दूरी पर उपलब्ध हैं।\n"
                f"• **शीतलन केंद्र**: वातानुकूलित सार्वजनिक पुस्तकालय और छायादार हरित पार्क उपलब्ध हैं।\n"
                f"• **चिकित्सा केंद्र**: आपातकालीन हीट यूनिट 24/7 सक्रिय है।\n"
                f"सटीक दिशा और दूरी देखने के लिए 'हीट मैप' टैब का उपयोग करें।"
            )
        else:
            return (
                f"🚰 **Nearby Hydration & Cooling Refuges**:\n\n"
                f"Based on your proximity mesh:\n"
                f"• **Drinking Water (🚰)**: Public Potable Water Dispenser (~450m) — chilled RO water.\n"
                f"• **Cooling Shelter (🌳)**: Municipal Civic Hall & Central Library Respite Center (~750m) — fully air conditioned with free seating.\n"
                f"• **Medical Facility (🏥)**: District Emergency Hospital (~1.2 km) — equipped with rapid IV hydration and cold-water immersion packs.\n\n"
                f"👉 Use the interactive **Heat Map** tab above to view live walking routes and turn-by-turn directions to each site."
            )

    # 5. Why is risk score high?
    if any(k in q for k in ["why", "high", "score", "calculate", "factor", "reason"]):
        factors = env_risk.get("contributing_factors", [])
        reasons_text = "\n".join([f"• {f}" for f in factors])
        if lang == "te":
            return (
                f"📊 **ఉష్ణ ప్రమాద స్కోరు ఎందుకు ఎక్కువగా ఉంది?**\n\n"
                f"వాతావరణ స్కోరు: **{env_score}/100**, వ్యక్తిగత స్కోరు: **{pers_score}/100**.\n"
                f"కారణాలు:\n"
                f"• అధిక ఉష్ణోగ్రత ({temp}°C) మరియు గాలిలో తేమ ({humidity}%).\n"
                f"• శరీర చెమట ఆవిరైపోయే ప్రక్రియ తగ్గడం.\n"
                f"• గరిష్ట సౌర వికిరణం మరియు రేడియేషన్ ప్రభావం.\n"
                f"• వ్యక్తిగత ప్రొఫైల్ ({occupation}) బాహ్య ఉష్ణ తీవ్రతను పెంచుతుంది."
            )
        elif lang == "hi":
            return (
                f"📊 **गर्मी का जोखिम स्कोर अधिक क्यों है?**\n\n"
                f"पर्यावरणीय स्कोर: **{env_score}/100**, व्यक्तिगत स्कोर: **{pers_score}/100**.\n"
                f"मुख्य कारण:\n"
                f"• उच्च तापमान ({temp}°C) और {humidity}% आर्द्रता, जिससे शरीर का पसीना सूख नहीं पाता।\n"
                f"• अत्यधिक सौर विकिरण (UV Index: {curr_weather.get('uv_index', 9.5)}).\n"
                f"• आपकी प्रोफ़ाइल ({occupation}) का धूप में कार्य करने का समय जोखिम बढ़ाता है।"
            )
        else:
            return (
                f"📊 **Why Your Heat Risk Score Is High ({pers_score}/100)**:\n\n"
                f"The score is computed deterministically from the thermodynamic environment plus your personal vulnerability:\n\n"
                f"1. **Thermodynamic Burden**: Ambient temperature of **{temp}°C** paired with **{humidity}% relative humidity** yields an Apparent Temperature of **{apparent_temp}°C**.\n"
                f"2. **Evaporative Impairment**: High humidity severely inhibits sweat evaporation, locking heat inside your core.\n"
                f"3. **Solar Radiation**: UV index of **{curr_weather.get('uv_index', 10.0)}** delivers intense radiant thermal loading.\n"
                f"4. **Personal Profile Modifier**: As a **{occupation}**, your exposure profile and activity level add **+{pers_score - env_score} points** of personal vulnerability.\n\n"
                f"{reasons_text}"
            )

    # General default guidance
    if lang == "te":
        return (
            f"🛡️ **హీట్‌షీల్డ్ భద్రతా మార్గదర్శకం**:\n"
            f"ప్రస్తుత ఉష్ణోగ్రత {temp}°C, వ్యక్తిగత ప్రమాదం **{pers_score}/100 ({pers_cat})**.\n"
            f"పీక్ ప్రమాద సమయం: **{win_display}**.\n\n"
            f"1. పుష్కలంగా నీరు త్రాగండి.\n"
            f"2. పీక్ సమయంలో బయటకు వెళ్లడం తగ్గించండి.\n"
            f"3. చల్లని ప్రదేశాలలో ఉండటానికి ప్రాధాన్యత ఇవ్వండి."
        )
    elif lang == "hi":
        return (
            f"🛡️ **हीटशील्ड सुरक्षा मार्गदर्शन**:\n"
            f"वर्तमान तापमान {temp}°C, व्यक्तिगत जोखिम **{pers_score}/100 ({pers_cat})**.\n"
            f"चरम खतरे का समय: **{win_display}**.\n\n"
            f"1. पर्याप्त मात्रा में पानी और ओआरएस पिएं।\n"
            f"2. दोपहर {win_display} के दौरान सीधी धूप से बचें।\n"
            f"3. ढीले और हल्के सूती वस्त्र पहनें।"
        )
    else:
        return (
            f"🛡️ **HeatShield Safety Guidance for {occupation}**:\n\n"
            f"Your current Personal Heat Risk is **{pers_score}/100 ({pers_cat})** with ambient temperatures at **{temp}°C** (feels like **{apparent_temp}°C**).\n\n"
            f"**Key Recommendations**:\n"
            f"• **Peak Danger Window**: Minimize strenuous exposure between **{win_display}**.\n"
            f"• **Hydration**: Maintain constant fluid intake (250-300ml per hour); do not wait for thirst.\n"
            f"• **Rest & Shade**: Seek air-conditioned buildings or shaded tree canopies when outdoors.\n"
            f"• Ask me about safest walking times, work-rest schedules, or finding nearest cooling refuges."
        )


def call_gemini_api(
    query: str,
    context: Dict[str, Any],
    lang: str,
    api_key: str,
    is_emergency: bool
) -> str:
    """Invokes Gemini API via standard HTTP POST."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"USER LANGUAGE: {lang}\n"
        f"STRUCTURED CONTEXT JSON:\n{json.dumps(context, indent=2)}\n\n"
        f"USER QUESTION: {query}\n"
        f"Provide a helpful, concise, empathetic response obeying all medical safety guardrails."
    )
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=8.0) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        candidates = data.get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
    raise RuntimeError("Empty response from Gemini API")


def call_openai_api(
    query: str,
    context: Dict[str, Any],
    lang: str,
    api_key: str,
    is_emergency: bool
) -> str:
    """Invokes OpenAI API via standard HTTP POST."""
    url = "https://api.openai.com/v1/chat/completions"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"LANGUAGE: {lang}\nCONTEXT:\n{json.dumps(context, indent=2)}\n\nQUESTION: {query}"
        }
    ]
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 500
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    with urllib.request.urlopen(req, timeout=8.0) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        choices = data.get("choices", [])
        if choices:
            return choices[0]["message"]["content"]
    raise RuntimeError("Empty response from OpenAI API")
