"""
Интеграционные утилиты для gaame
Эти функции можно использовать для постепенной миграции кода
"""

from .config import *
from typing import Any


class ScoreManager:
    """Менеджер очков — можно использовать вместо простых переменных"""
    
    def __init__(self):
        self.score: int = 0
        self.multiplier: int = 1
        self.high_score: int = 0
        self._load_high_score()
    
    def _load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0
    
    def add_points(self, points: int = 1):
        """Добавить очки"""
        self.score += points * self.multiplier
    
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))


class GameMode:
    """Класс режима игры"""
    
    def __init__(self, mode_dict: dict):
        self.name = mode_dict["name"]
        self.obstacle_speed = mode_dict["obstacle_speed"]
        self.gravity = mode_dict["gravity"]
        self.jump_force = mode_dict["jump_force"]
        self.jump_hold = mode_dict["jump_hold"]
        self.bonus_chance = mode_dict["bonus_chance"]
        self.spawn_interval = mode_dict["spawn_interval"]
        self.high_prob = mode_dict["high_prob"]
    
    @staticmethod
    def get_modes():
        """Получить все режимы"""
        return MODES
    
    @staticmethod
    def get_mode_by_name(name: str):
        """Получить режим по имени"""
        for mode in MODES:
            if mode["name"] == name:
                return GameMode(mode)
        return GameMode(MODES[0])


class ConfigHelper:
    """Утилиты для работы с конфигурацией"""
    
    @staticmethod
    def get_screen_size():
        """Размер экрана"""
        return (VIRTUAL_WIDTH, VIRTUAL_HEIGHT)
    
    @staticmethod
    def get_player_size():
        """Размер игрока"""
        return PLAYER_SIZE
    
    @staticmethod
    def get_bonus_size():
        """Размер бонуса"""
        return BONUS_SIZE
    
    @staticmethod
    def get_fps():
        """Частота кадров"""
        return FPS
    
    @staticmethod
    def get_ground_y():
        """Y координата земли"""
        return VIRTUAL_HEIGHT - PLAYER_SIZE - 10


# Функции-утилиты для быстрого доступа
def create_player(x: int, y: int, keys: dict = None) -> 'Player':
    """Создать игрока (требует интеграции player.py)"""
    from .player import Player
    return Player(x, y, keys=keys)


def create_obstacle_factory(score: int = 0) -> 'ObstacleFactory':
    """Создать фабрику препятствий"""
    from .obstacle import ObstacleFactory
    return ObstacleFactory(score=score)


def create_bonus_factory(score: int = 0) -> 'BonusFactory':
    """Создать фабрику бонусов"""
    from .bonus import BonusFactory
    return BonusFactory(score=score)


def create_particle_system() -> 'ParticleSystem':
    """Создать систему частиц"""
    from .particles import ParticleSystem
    return ParticleSystem()