"""
Новые бонусы и эффекты для игры
"""

import random
import pygame
from typing import Optional


class PowerUp:
    """Улучшенный базовый класс бонуса"""
    
    def __init__(self, name: str, duration: int, color: tuple):
        self.name = name
        self.duration = duration  # в кадрах
        self.time_remaining = duration
        self.active = False
        self.color = color
    
    def activate(self):
        """Активировать бонус"""
        self.active = True
        self.time_remaining = self.duration
    
    def update(self) -> bool:
        """Обновить бонус. Возвращает True если активен"""
        if self.active:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.active = False
        return self.active
    
    def get_progress(self) -> float:
        """Получить прогресс (0.0 - 1.0)"""
        if self.duration == 0:
            return 1.0
        return self.time_remaining / self.duration


class MagnetPower(PowerUp):
    """Магнит - притягивает бонусы"""
    
    def __init__(self):
        super().__init__("Магнит", 600, (255, 0, 255))  # 10 секунд
        self.radius = 200
    
    def get_attraction_force(self, bonus_x: float, bonus_y: float, player_x: float, player_y: float) -> tuple:
        """Получить силу притяжения к игроку"""
        dx = player_x - bonus_x
        dy = player_y - bonus_y
        distance = (dx**2 + dy**2)**0.5
        
        if distance < self.radius and distance > 0:
            strength = (1.0 - distance / self.radius) * 5
            return (dx / distance * strength, dy / distance * strength)
        return (0, 0)


class TimeSlowPower(PowerUp):
    """Замедлен��е времени"""
    
    def __init__(self):
        super().__init__("Замедление", 480, (0, 191, 255))  # 8 секунд
        self.slow_factor = 0.5
    
    def get_slow_factor(self) -> float:
        """Получить множитель замедления"""
        if self.active:
            return self.slow_factor
        return 1.0


class ScoreMultiplier(PowerUp):
    """Множитель очков"""
    
    def __init__(self, multiplier: int = 2):
        super().__init__("Множитель", 600, (255, 215, 0))  # 10 секунд
        self.multiplier = multiplier
    
    def get_score_multiplier(self) -> int:
        if self.active:
            return self.multiplier
        return 1


class ShieldPower(PowerUp):
    """Улучшенный щит - отражает снаряды"""
    
    def __init__(self):
        super().__init__("Щит", 720, (128, 128, 255))  # 12 секунд
        self.reflects_projectiles = True


class TeleportPower(PowerUp):
    """Телепортация - мгновенное перемещение"""
    
    def __init__(self):
        super().__init__("Телепорт", 300, (0, 255, 128))  # 5 секунд
        self.cooldown = 60  # 1 секунда между использованиями
        self.last_use = 0
    
    def can_use(self, current_frame: int) -> bool:
        return current_frame - self.last_use >= self.cooldown
    
    def use(self, current_frame: int):
        self.last_use = current_frame


class PowerUpManager:
    """Менеджер всех бонусов"""
    
    def __init__(self):
        self.power_ups = {
            "magnet": MagnetPower(),
            "time_slow": TimeSlowPower(),
            "score_multiplier": ScoreMultiplier(3),
            "shield": ShieldPower(),
            "teleport": TeleportPower(),
        }
        self.active_list = []
    
    def activate(self, power_name: str) -> bool:
        """Активировать бонус по имени"""
        if power_name in self.power_ups:
            self.power_ups[power_name].activate()
            return True
        return False
    
    def update(self):
        """Обновить все активные бонусы"""
        self.active_list = []
        for name, power in self.power_ups.items():
            if power.update():
                self.active_list.append(name)
    
    def get_active(self) -> list:
        """Получить список активных бонусов"""
        return self.active_list
    
    def is_active(self, power_name: str) -> bool:
        """Проверить активен ли бонус"""
        return self.power_ups.get(power_name, PowerUp("", 0, (0,0,0))).active


class SpecialEffects:
    """Спецэффекты для бонусов"""
    
    @staticmethod
    def create_portal_effect(surface: pygame.Surface, x: int, y: int, radius: int, color: tuple):
        """Эффект портала"""
        pygame.draw.circle(surface, color, (x, y), radius, 3)
        pygame.draw.circle(surface, color, (x, y), radius // 2, 2)
        pygame.draw.circle(surface, color, (x, y), radius // 4, 1)
    
    @staticmethod
    def create_magnet_effect(surface: pygame.Surface, x: int, y: int, radius: int, progress: float):
        """Эффект магнита"""
        alpha = int(127 * progress)
        color = (255, 0, 255, alpha)
        
        for i in range(3):
            r = int(radius * (1 - i * 0.3))
            pygame.draw.circle(surface, color, (x, y), r, 2)
    
    @staticmethod
    def create_time_warp(surface: pygame.Surface, width: int, height: int, progress: float):
        """Эффект замедления времени"""
        alpha = int(50 * progress)
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 100, 200, alpha))
        surface.blit(overlay, (0, 0))


__all__ = [
    "PowerUp",
    "MagnetPower", 
    "TimeSlowPower",
    "ScoreMultiplier",
    "ShieldPower",
    "TeleportPower",
    "PowerUpManager",
    "SpecialEffects",
]