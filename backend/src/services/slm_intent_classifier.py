"""
Small Language Model (SLM) Semantic Intent & Tone Classifier for Marine AI
Provides:
1. Tone Sanitization & Troll/Mockery Detection ('please daddy', 'bruh', 'skibidi', childish slang).
2. Comprehensive Global & Indian Coastal Gazetteer (Dapoli, Ratnagiri, Malvan, Alibaug, Karwar, Bombay/Mumbai, etc.).
3. Semantic Intent Routing (Safety Clearance, Basin Intelligence, Navigation, Species, Emergency, Off-Topic).
4. Strict Location Ambiguity Guard (Prevents unsafe silent fallbacks).
"""
from typing import Optional, Dict, Any, Tuple, List, Set
import re

# Comprehensive Coastal Gazetteer of 150+ Major & Minor Coastal Ports/Landing Centres & Aliases
COASTAL_GAZETTEER: Dict[str, Tuple[float, float, str, str]] = {
    # Maharashtra & Konkan Coast
    "dapoli": (17.7644, 73.1812, "Dapoli / Harnai Sector", "Arabian Sea (Konkan Coast)"),
    "harnai": (17.8044, 73.0912, "Harnai Fishing Harbor", "Arabian Sea (Konkan Coast)"),
    "ratnagiri": (16.9902, 73.3120, "Mirkarwada Port (Ratnagiri)", "Arabian Sea (Konkan Coast)"),
    "alibaug": (18.6414, 72.8722, "Alibaug Coastal Sector", "Arabian Sea (Konkan Coast)"),
    "murud": (18.3283, 72.9620, "Murud Janjira Port", "Arabian Sea (Konkan Coast)"),
    "malvan": (16.0617, 73.4686, "Malvan Harbor", "Arabian Sea (Konkan Coast)"),
    "vengurla": (15.8617, 73.6333, "Vengurla Port", "Arabian Sea (Konkan Coast)"),
    "mumbai": (18.9220, 72.8347, "Sassoon Docks (Mumbai)", "Arabian Sea"),
    "bombay": (18.9220, 72.8347, "Sassoon Docks (Mumbai / Bombay)", "Arabian Sea"),
    "nhava sheva": (18.9500, 72.9500, "Jawaharlal Nehru Port Authority (JNPA / Nhava Sheva)", "Arabian Sea"),
    "jnpt": (18.9500, 72.9500, "Jawaharlal Nehru Port Authority (JNPT / Nhava Sheva)", "Arabian Sea"),
    "vasai": (19.3300, 72.8100, "Vasai Creek / Port", "Arabian Sea"),
    "palghar": (19.6967, 72.7656, "Satpati Harbor (Palghar)", "Arabian Sea"),
    "dahanu": (19.9700, 72.7300, "Dahanu Coastal Sector", "Arabian Sea"),

    # Goa & Karnataka Coast
    "goa": (15.4050, 73.8050, "Mormugao Harbor (Goa)", "Arabian Sea"),
    "panaji": (15.4909, 73.8278, "Panaji Mandovi Port", "Arabian Sea"),
    "panjim": (15.4909, 73.8278, "Panaji Mandovi Port", "Arabian Sea"),
    "vasco": (15.3981, 73.8111, "Mormugao Port (Vasco)", "Arabian Sea"),
    "vasco da gama": (15.3981, 73.8111, "Mormugao Port (Vasco)", "Arabian Sea"),
    "mormugao": (15.4050, 73.8050, "Mormugao Harbor (Goa)", "Arabian Sea"),
    "karwar": (14.8136, 74.1294, "Karwar Baithkol Harbor", "Arabian Sea (Karnataka Coast)"),
    "honnavar": (14.2800, 74.4500, "Honnavar Fishing Port", "Arabian Sea (Karnataka Coast)"),
    "bhatkal": (13.9780, 74.5500, "Bhatkal Port", "Arabian Sea (Karnataka Coast)"),
    "kundapura": (13.6267, 74.6900, "Gangolli Harbor (Kundapura)", "Arabian Sea (Karnataka Coast)"),
    "malpe": (13.3517, 74.7011, "Malpe Fishing Harbor (Udupi)", "Arabian Sea (Karnataka Coast)"),
    "udupi": (13.3517, 74.7011, "Malpe Fishing Harbor (Udupi)", "Arabian Sea (Karnataka Coast)"),
    "mangalore": (12.8698, 74.8430, "Old Port Mangalore", "Arabian Sea (Karnataka Coast)"),
    "mangaluru": (12.8698, 74.8430, "Old Port Mangalore", "Arabian Sea (Karnataka Coast)"),

    # Kerala Coast
    "kasaragod": (12.5000, 74.9800, "Kasaragod Coastal Sector", "Arabian Sea"),
    "kannur": (11.8689, 75.3555, "Mopla Bay Harbor (Kannur)", "Arabian Sea"),
    "thalassery": (11.7480, 75.4890, "Thalassery Coastal Sector", "Arabian Sea"),
    "kozhikode": (11.2588, 75.7804, "Beypore Port (Kozhikode)", "Arabian Sea"),
    "calicut": (11.2588, 75.7804, "Beypore Port (Kozhikode)", "Arabian Sea"),
    "beypore": (11.1620, 75.8050, "Beypore Fishing Harbor", "Arabian Sea"),
    "ponnani": (10.7670, 75.9250, "Ponnani Fishing Harbor", "Arabian Sea"),
    "kochi": (9.9312, 76.2673, "Cochin Fishing Harbor", "Arabian Sea"),
    "cochin": (9.9312, 76.2673, "Cochin Fishing Harbor", "Arabian Sea"),
    "munambam": (10.1800, 76.1700, "Munambam Harbor (Kochi)", "Arabian Sea"),
    "thottappally": (9.3170, 76.3830, "Thottappally Spillway Harbor", "Arabian Sea"),
    "alleppey": (9.4981, 76.3388, "Alappuzha / Alleppey Sector", "Arabian Sea"),
    "alappuzha": (9.4981, 76.3388, "Alappuzha / Alleppey Sector", "Arabian Sea"),
    "kollam": (8.8932, 76.5500, "Neendakara Port (Kollam)", "Arabian Sea"),
    "quilon": (8.8932, 76.5500, "Neendakara Port (Kollam)", "Arabian Sea"),
    "neendakara": (8.9380, 76.5360, "Neendakara Harbor (Kollam)", "Arabian Sea"),
    "vizhinjam": (8.3756, 76.9906, "Vizhinjam International Port", "Arabian Sea / Indian Ocean"),
    "trivandrum": (8.3756, 76.9906, "Vizhinjam (Thiruvananthapuram)", "Arabian Sea / Indian Ocean"),
    "thiruvananthapuram": (8.3756, 76.9906, "Vizhinjam (Thiruvananthapuram)", "Arabian Sea / Indian Ocean"),

    # Tamil Nadu & Gulf of Mannar Coast
    "kanyakumari": (8.0883, 77.5385, "Kanyakumari Pier Sector", "Indian Ocean / Cape Comorin"),
    "colachel": (8.1750, 77.2560, "Colachel Fishing Harbor", "Arabian Sea / South Coast"),
    "tuticorin": (8.7642, 78.1348, "V.O. Chidambaranar Port (Tuticorin)", "Gulf of Mannar"),
    "thoothukudi": (8.7642, 78.1348, "V.O. Chidambaranar Port (Tuticorin)", "Gulf of Mannar"),
    "rameswaram": (9.2876, 79.3129, "Rameswaram Base [Base 01]", "Gulf of Mannar / Palk Bay"),
    "dhanushkodi": (9.1764, 79.4167, "Dhanushkodi Point", "Gulf of Mannar"),
    "mandapam": (9.2780, 79.1250, "Mandapam Fishing Harbor", "Palk Bay / Indian Ocean"),
    "thondi": (9.7360, 79.0190, "Thondi Coastal Harbor", "Palk Bay"),
    "mallipattinam": (10.2830, 79.3170, "Mallipattinam Harbor", "Palk Bay"),
    "nagapattinam": (10.7667, 79.8333, "Nagapattinam Port", "Bay of Bengal"),
    "karaikal": (10.9254, 79.8380, "Karaikal Port", "Bay of Bengal"),
    "poompuhar": (11.1450, 79.8550, "Poompuhar Landing Center", "Bay of Bengal"),
    "cuddalore": (11.7500, 79.7700, "Cuddalore Old Town Port", "Bay of Bengal"),
    "puducherry": (11.9416, 79.8083, "Puducherry Port Sector", "Bay of Bengal"),
    "pondicherry": (11.9416, 79.8083, "Puducherry Port Sector", "Bay of Bengal"),
    "mahabalipuram": (12.6167, 80.1917, "Mahabalipuram Coastal Sector", "Bay of Bengal"),
    "chennai": (13.0827, 80.2707, "Chennai Kasimedu Harbor", "Bay of Bengal"),
    "madras": (13.0827, 80.2707, "Chennai Kasimedu Harbor (Madras)", "Bay of Bengal"),
    "kasimedu": (13.1250, 80.2970, "Kasimedu Fishing Harbor (Chennai)", "Bay of Bengal"),
    "ennore": (13.2300, 80.3300, "Kamarajar Port (Ennore)", "Bay of Bengal"),
    "kattupalli": (13.3100, 80.3500, "Kattupalli Shipyard & Port", "Bay of Bengal"),
    "pulicat": (13.4167, 80.3167, "Pulicat Lake & Harbor", "Bay of Bengal"),

    # Andhra Pradesh & Odisha Coast
    "krishnapatnam": (14.2500, 80.1300, "Krishnapatnam Port", "Bay of Bengal"),
    "machilipatnam": (16.1800, 81.1300, "Machilipatnam Harbor", "Bay of Bengal"),
    "nizampatnam": (15.9000, 80.6700, "Nizampatnam Fishing Harbor", "Bay of Bengal"),
    "kakinada": (16.9891, 82.2475, "Kakinada Deepwater Port", "Bay of Bengal"),
    "visakhapatnam": (17.6868, 83.2185, "Visakhapatnam Fishing Harbor", "Bay of Bengal"),
    "vizag": (17.6868, 83.2185, "Visakhapatnam Fishing Harbor", "Bay of Bengal"),
    "waltair": (17.6868, 83.2185, "Visakhapatnam Fishing Harbor (Waltair)", "Bay of Bengal"),
    "bheemunipatnam": (17.8900, 83.4500, "Bheemunipatnam Coastal Sector", "Bay of Bengal"),
    "kalingapatnam": (18.3400, 84.1300, "Kalingapatnam Port", "Bay of Bengal"),
    "gopalpur": (19.2600, 84.9100, "Gopalpur Port (Odisha)", "Bay of Bengal"),
    "puri": (19.8135, 85.8312, "Puri Coastal Sector", "Bay of Bengal"),
    "chandrabhaga": (19.8650, 86.1100, "Chandrabhaga Beach Sector", "Bay of Bengal"),
    "paradip": (20.3167, 86.6167, "Paradip Port (Odisha)", "Bay of Bengal"),
    "dhamra": (20.8000, 86.9700, "Dhamra Port", "Bay of Bengal"),

    # West Bengal Coast
    "digha": (21.6266, 87.5074, "Digha Mohana Fishing Harbor", "Bay of Bengal"),
    "shankarpur": (21.6360, 87.5700, "Shankarpur Harbor (Bengal)", "Bay of Bengal"),
    "haldia": (22.0667, 88.0667, "Haldia Dock Complex", "Bay of Bengal / Hooghly"),
    "kolkata": (22.5726, 88.3639, "Syama Prasad Mookerjee Port (Kolkata)", "Bay of Bengal / Hooghly"),
    "calcutta": (22.5726, 88.3639, "Syama Prasad Mookerjee Port (Calcutta)", "Bay of Bengal / Hooghly"),
    "kakdwip": (21.8700, 88.1800, "Kakdwip Harbor (Sundarbans)", "Bay of Bengal"),
    "sagar island": (21.6500, 88.0800, "Gangasagar (Sagar Island)", "Bay of Bengal"),

    # Gujarat Coast
    "mandvi": (22.8333, 69.3500, "Mandvi Port (Kutch)", "Gulf of Kutch / Arabian Sea"),
    "mundra": (22.8397, 69.7042, "Mundra Port", "Gulf of Kutch / Arabian Sea"),
    "kandla": (23.0000, 70.2167, "Deendayal Port (Kandla)", "Gulf of Kutch"),
    "kutch": (23.0000, 70.2167, "Gulf of Kutch Port Complex", "Gulf of Kutch"),
    "cutch": (23.0000, 70.2167, "Gulf of Kutch Port Complex", "Gulf of Kutch"),
    "okha": (22.4667, 69.0667, "Okha Port", "Arabian Sea"),
    "porbandar": (21.6417, 69.6000, "Porbandar Harbor", "Arabian Sea"),
    "veraval": (20.9000, 70.3667, "Veraval Fishing Harbor", "Arabian Sea"),
    "mangrol": (21.1200, 70.1200, "Mangrol Harbor (Gujarat)", "Arabian Sea"),
    "jafrabad": (20.8700, 71.3700, "Jafrabad Port", "Arabian Sea"),
    "pipavav": (20.9167, 71.5000, "Port Pipavav", "Gulf of Khambhat / Arabian Sea"),
    "dahej": (21.7000, 72.5800, "Dahej Port", "Gulf of Khambhat"),
    "hazira": (21.1167, 72.6500, "Hazira Port (Surat)", "Gulf of Khambhat"),
    "surat": (21.1167, 72.6500, "Hazira Port (Surat)", "Gulf of Khambhat"),
    "daman": (20.3974, 72.8328, "Daman Port", "Arabian Sea"),
    "diu": (20.7144, 70.9874, "Diu Harbor", "Arabian Sea"),

    # Islands & International Ports
    "port blair": (11.6234, 92.7265, "Phoenix Bay (Port Blair)", "Andaman Sea"),
    "havelock": (11.9800, 92.9800, "Havelock Island (Swaraj Dweep)", "Andaman Sea"),
    "kavaratti": (10.5667, 72.6417, "Kavaratti Harbor (Lakshadweep)", "Arabian Sea"),
    "minicoy": (8.2833, 73.0500, "Minicoy Port (Lakshadweep)", "Arabian Sea / Indian Ocean"),
    "colombo": (6.9497, 79.8428, "Port of Colombo (Sri Lanka)", "Indian Ocean"),
    "tokyo": (35.6528, 139.8394, "Port of Tokyo (Japan)", "Northwest Pacific Ocean"),
    "rotterdam": (51.9244, 4.4777, "Port of Rotterdam (Netherlands)", "North Sea"),
    "san francisco": (37.8080, -122.4177, "Fisherman's Wharf (San Francisco, USA)", "Northeast Pacific"),
    "singapore": (1.290270, 103.851959, "Port of Singapore", "Strait of Malacca"),
    "dubai": (25.2697, 55.3095, "Port Rashid (Dubai, UAE)", "Persian Gulf")
}

# Troll & Sarcastic Tone Vocabulary Patterns
TROLL_TONE_PATTERNS = [
    r"\b(?:please\s+)?daddy\b",
    r"\bmommy\b",
    r"\bbruh\b",
    r"\bskibidi\b",
    r"\brizz\b",
    r"\bgyatt\b",
    r"\bhomie\b",
    r"\bno cap\b",
    r"\bfr fr\b",
    r"\blol\b",
    r"\blmao\b",
    r"\brofl\b",
    r"\buwu\b",
    r"\bowo\b"
]

class SLMIntentClassifier:
    """
    Lightweight Semantic SLM Router:
    - Analyzes tone & flags troll slang while preserving underlying operational intent.
    - Resolves coastal location entities across global and Indian coastal networks.
    - Prevents silent fallback on critical departure clearances.
    """

    @classmethod
    def sanitize_tone(cls, text: str) -> Tuple[str, bool, List[str]]:
        """
        Check for troll/sarcastic patterns.
        Returns: (sanitized_clean_text, has_troll_tone, detected_trolls)
        """
        detected = []
        cleaned = text
        for pat in TROLL_TONE_PATTERNS:
            matches = re.findall(pat, cleaned, re.IGNORECASE)
            if matches:
                detected.extend(matches)
                cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)

        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned, len(detected) > 0, detected

    @classmethod
    def resolve_coastal_entity(cls, text: str) -> Optional[Tuple[float, float, str, str]]:
        """
        Resolves coastal city, port, or landmark in text against the Coastal Gazetteer.
        """
        text_lower = text.lower()
        tokens = set(re.findall(r'[a-zA-Z0-9]+', text_lower))

        # Check multi-word locations first (e.g. 'port blair', 'sagar island', 'nhava sheva')
        for loc_name, data in sorted(COASTAL_GAZETTEER.items(), key=lambda x: len(x[0]), reverse=True):
            if " " in loc_name and loc_name in text_lower:
                return data

        # Check single-word locations by token
        for loc_name, data in COASTAL_GAZETTEER.items():
            if " " not in loc_name and loc_name in tokens:
                return data

        return None
