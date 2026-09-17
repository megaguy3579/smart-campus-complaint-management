def detect_category(text):
    """
    Detect the category of a campus complaint.
    """

    text = text.lower().strip()

    # -----------------------------------------
    # WI-FI / INTERNET
    # -----------------------------------------

    wifi_keywords = [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "router",
        "connection",
        "connectivity",
        "no internet",
        "internet not working"
    ]

    if any(word in text for word in wifi_keywords):
        return "Wi-Fi / Internet"

    # -----------------------------------------
    # FOOD / CANTEEN
    # -----------------------------------------

    food_keywords = [
        "food",
        "canteen",
        "cafeteria",
        "mess",
        "lunch",
        "breakfast",
        "dinner",
        "meal",
        "restaurant",
        "food quality",
        "bad food",
        "spoiled food",
        "stale food",
        "food poisoning",
        "unhygienic food",
        "food hygiene"
    ]

    if any(word in text for word in food_keywords):
        return "Food / Canteen"

    # -----------------------------------------
    # WATER EQUIPMENT
    # -----------------------------------------

    water_equipment_keywords = [
        "water cooler",
        "water dispenser",
        "drinking water machine",
        "water purifier",
        "ro purifier",
        "ro machine",
        "cooler not working"
    ]

    if any(word in text for word in water_equipment_keywords):
        return "Classroom Equipment"

    # -----------------------------------------
    # ELECTRICAL
    # -----------------------------------------

    electrical_keywords = [
        "electricity",
        "electric",
        "light",
        "bulb",
        "fan",
        "switch",
        "socket",
        "power",
        " ac ",
        "air conditioner",
        "air conditioning",
        "voltage",
        "short circuit"
    ]

    # Add spaces around text so "ac" doesn't match random words.
    electrical_text = " " + text + " "

    if any(
        word in electrical_text
        for word in electrical_keywords
    ):
        return "Electrical"

    # -----------------------------------------
    # CLASSROOM EQUIPMENT
    # -----------------------------------------

    equipment_keywords = [
        "projector",
        "computer",
        "desktop",
        "laptop",
        "speaker",
        "smart board",
        "smartboard",
        "lab equipment",
        "microphone",
        "printer",
        "scanner",
        "display",
        "monitor",
        "keyboard",
        "mouse"
    ]

    if any(word in text for word in equipment_keywords):
        return "Classroom Equipment"

    # -----------------------------------------
    # SANITATION
    # -----------------------------------------

    sanitation_keywords = [
        "toilet",
        "washroom",
        "bathroom",
        "garbage",
        "dustbin",
        "dirty",
        "cleaning",
        "sanitation",
        "smell",
        "waste",
        "unhygienic",
        "cleanliness"
    ]

    if any(word in text for word in sanitation_keywords):
        return "Sanitation"

    # -----------------------------------------
    # PLUMBING
    # -----------------------------------------

    plumbing_keywords = [
        "water leakage",
        "water leak",
        "pipe",
        "tap",
        "leak",
        "leakage",
        "drain",
        "faucet",
        "water supply",
        "no water",
        "overflow",
        "burst pipe"
    ]

    if any(word in text for word in plumbing_keywords):
        return "Plumbing"

    # -----------------------------------------
    # INFRASTRUCTURE
    # -----------------------------------------

    infrastructure_keywords = [
        "building",
        "wall",
        "door",
        "window",
        "ceiling",
        "floor",
        "road",
        "bench",
        "chair",
        "desk",
        "classroom",
        "roof",
        "stairs",
        "staircase",
        "crack"
    ]

    if any(word in text for word in infrastructure_keywords):
        return "Infrastructure"

    # -----------------------------------------
    # SECURITY
    # -----------------------------------------

    security_keywords = [
        "security",
        "theft",
        "stolen",
        "cctv",
        "camera",
        "gate",
        "unsafe",
        "intruder",
        "suspicious",
        "security guard"
    ]

    if any(word in text for word in security_keywords):
        return "Security"

    # -----------------------------------------
    # GENERAL
    # -----------------------------------------

    return "General"


def detect_priority(text):
    """
    Detect complaint priority based on severity keywords.
    """

    text = text.lower().strip()

    # -----------------------------------------
    # CRITICAL
    # -----------------------------------------

    critical_keywords = [
        "fire",
        "flood",
        "electric shock",
        "electrocution",
        "accident",
        "emergency",
        "danger",
        "dangerous",
        "burst pipe",
        "gas leak",
        "major fire",
        "life threatening",
        "food poisoning"
    ]

    if any(word in text for word in critical_keywords):
        return "Critical"

    # -----------------------------------------
    # HIGH
    # -----------------------------------------

    high_keywords = [
        "urgent",
        "unsafe",
        "theft",
        "stolen",
        "broken",
        "not working",
        "completely stopped",
        "major leak",
        "serious",
        "immediately",
        "cannot use",
        "can't use",
        "spoiled food",
        "stale food"
    ]

    if any(word in text for word in high_keywords):
        return "High"

    # -----------------------------------------
    # MEDIUM
    # -----------------------------------------

    medium_keywords = [
        "damaged",
        "problem",
        "issue",
        "slow",
        "leaking",
        "partially working",
        "sometimes",
        "bad food",
        "poor food quality"
    ]

    if any(word in text for word in medium_keywords):
        return "Medium"

    # -----------------------------------------
    # LOW
    # -----------------------------------------

    return "Low"