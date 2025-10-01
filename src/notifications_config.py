NOTIFICATION_NUMBERS = {
    "name": "number",  # Example: "Gilad": 972543234567
}

PULL_COOLDOWN = 60 * 5  # fetch roborock status every 5 minutes
NOTIFICATION_COOLDOWN = 60 * 60 * 24  # Maximum one notification per day
NO_NOTIFY_HOURS = (2, 6)  # do not notify between 2 AM and 6 AM (will notify at 6 AM)

STATUS_MESSAGES = {
    "water_shortage": "💧 Hi {name}, I'm out of clean water! Please refill my tank so I can keep cleaning.",
    "dirty_tank_missing": "🧽 Hi {name}, the dirty water tank is missing! Please put it back so I can continue.",
    "waste_water_tank_full": "🚱 Hi {name}, the dirty water tank is full! Please empty it so I can keep cleaning.",
    "basin_blocked": "⚠️ Hi {name}, the basin is blocked! Please check and clean me so I can keep working.",
}
