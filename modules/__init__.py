"""
gaame modules - для новых функций и расширений
"""

from .config import *
from .particles import ParticleSystem
from .audio import AudioManager
from .integration import ScoreManager, GameMode, ConfigHelper
from .ai import AIModule, DifficultyManager, ComboSystem
from .powerups import PowerUpManager, SpecialEffects, MagnetPower, TimeSlowPower
from .new_features import NewFeatures, new_features, get_combo_system, get_powerup_manager, get_difficulty_manager

__all__ = [
    # Константы
    "FPS", "VIRTUAL_WIDTH", "VIRTUAL_HEIGHT", "PLAYER_SIZE", "BONUS_SIZE", "MODES",
    # Системы
    "ParticleSystem", "AudioManager",
    # Утилиты
    "ScoreManager", "GameMode", "ConfigHelper",
    # ИИ
    "AIModule", "DifficultyManager", "ComboSystem",
    # Бонусы
    "PowerUpManager", "SpecialEffects", "MagnetPower", "TimeSlowPower",
    # Новые функции
    "NewFeatures", "new_features", "get_combo_system", "get_powerup_manager", "get_difficulty_manager",
]