from enum import Enum, auto

class DifficultySettings(Enum):
    
    PIT_PROBABILITY = auto() 
    HEALING_POTION_PROBABILITY = auto() 
    VISION_POTION_PROBABILITY = auto() 
    SUGGESTION_POTION_PROBABILITY = auto() 
    MAGIC_KEY_PROBABILITY = auto() 
    LOCKED_DOOR_PROBABILITY = auto() 
    MIN_HEALING_POTION_VALUE = auto() 
    MAX_HEALING_POTION_VALUE = auto() 
    MIN_PIT_DAMAGE = auto() 
    MAX_PIT_DAMAGE = auto() 
    MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE = auto() 
    

DIFFICULTY_SETTINGS = {
    "easy": {
        DifficultySettings.PIT_PROBABILITY : 0.1,
        DifficultySettings.HEALING_POTION_PROBABILITY : 0.15,
        DifficultySettings.VISION_POTION_PROBABILITY : 0.15,
        DifficultySettings.SUGGESTION_POTION_PROBABILITY : 0.15,
        DifficultySettings.MAGIC_KEY_PROBABILITY : 0.15,
        DifficultySettings.LOCKED_DOOR_PROBABILITY : 0.25,
        DifficultySettings.MIN_HEALING_POTION_VALUE : 5,
        DifficultySettings.MAX_HEALING_POTION_VALUE : 15,
        DifficultySettings.MIN_PIT_DAMAGE : 1,
        DifficultySettings.MAX_PIT_DAMAGE : 20,
        DifficultySettings.MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE : 5,
    },
    "medium": {
        DifficultySettings.PIT_PROBABILITY : 0.15, 
        DifficultySettings.HEALING_POTION_PROBABILITY : 0.15,
        DifficultySettings.VISION_POTION_PROBABILITY : 0.15,
        DifficultySettings.SUGGESTION_POTION_PROBABILITY : 0.15,
        DifficultySettings.MAGIC_KEY_PROBABILITY : 0.15,
        DifficultySettings.LOCKED_DOOR_PROBABILITY : 0.25,
        DifficultySettings.MIN_HEALING_POTION_VALUE : 5,
        DifficultySettings.MAX_HEALING_POTION_VALUE : 15,
        DifficultySettings.MIN_PIT_DAMAGE : 1,
        DifficultySettings.MAX_PIT_DAMAGE : 20,
        DifficultySettings.MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE : 6,
    },
    "hard": {
        DifficultySettings.PIT_PROBABILITY : 0.15, 
        DifficultySettings.HEALING_POTION_PROBABILITY : 0.15,
        DifficultySettings.VISION_POTION_PROBABILITY : 0.15,
        DifficultySettings.SUGGESTION_POTION_PROBABILITY : 0.15,
        DifficultySettings.MAGIC_KEY_PROBABILITY : 0.15,
        DifficultySettings.LOCKED_DOOR_PROBABILITY : 0.25,
        DifficultySettings.MIN_HEALING_POTION_VALUE : 5,
        DifficultySettings.MAX_HEALING_POTION_VALUE : 15,
        DifficultySettings.MIN_PIT_DAMAGE : 1,
        DifficultySettings.MAX_PIT_DAMAGE : 20,
        DifficultySettings.MIN_ENTRANCE_EXIT_MANHATTAN_DISTANCE : 7,
    },
}
