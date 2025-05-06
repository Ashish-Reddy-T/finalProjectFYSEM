"""
Configuration module for 'The Line: A Border Journey'

This module contains global configuration settings for the game.
"""

# Game version
VERSION = "1.0.0"

# Game settings
MAX_TURNS = 30
ENABLE_SOUND = False
ENABLE_WEATHER = True
ENABLE_TIME_CYCLE = True
ENABLE_SAVE_GAME = False  # Future potential, but for now: Not yet implemented

# Difficulty settings
DIFFICULTY = "normal"  # "easy", "normal", "hard"
DIFFICULTY_MODIFIERS = {
    "easy": {
        "resource_consumption": 0.7,
        "starting_resources": 1.3,
        "event_chance": 0.7,
        "patrol_intensity": 0.7
    },
    "normal": {
        "resource_consumption": 1.0,
        "starting_resources": 1.0,
        "event_chance": 1.0,
        "patrol_intensity": 1.0
    },
    "hard": {
        "resource_consumption": 1.3,
        "starting_resources": 0.7,
        "event_chance": 1.3,
        "patrol_intensity": 1.3
    }
}

# Text display settings
TEXT_SPEED = 0.001  # Seconds per character in slow printing
ENABLE_TEXT_EFFECTS = True

# Debug settings
DEBUG = False
DEBUG_START_LOCATION = None  # Set to location ID to start at specific location
DEBUG_INVENTORY = []  # Starting inventory for debugging