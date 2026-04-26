"""
Интеграция новых функций в игру - можно вызывать из gaame.py
Этот файл НЕ изменяет основной код, а только предоставляет функции для импорта
"""

import random
from modules.ai import AIModule, DifficultyManager, ComboSystem
from modules.powerups import PowerUpManager, MagnetPower, TimeSlowPower
from modules.particles import ParticleSystem
from modules.audio import AudioManager


class NewFeatures:
    """Новые функции для интеграции"""
    
    def __init__(self):
        self.ai = AIModule()
        self.difficulty = DifficultyManager()
        self.combo = ComboSystem()
        self.powerups = PowerUpManager()
        
        # Состояние
        self.combo_display_timer = 0
        self.last_combo_count = 0
    
    def update(self, score: int, is_playing: bool = True):
        """Обновить все новые системы"""
        if is_playing:
            # Обновить уровень сложности
            self.difficulty.update_level(score)
            
            # Обновить комбо
            self.combo.update()
    
    def on_obstacle_passed(self):
        """Вызывать когда игрок прошел препятствие"""
        self.combo.add_obstacle_passed()
        
        if self.combo.combo_count > 1:
            self.last_combo_count = self.combo.combo_count
            self.combo_display_timer = 60  # 1 секунда
    
    def get_combo_bonus(self, base_points: int) -> int:
        """Получить бонусные очки с учетом комбо"""
        return self.combo.get_bonus_points(base_points)
    
    def get_combo_text(self) -> str:
        """Получить текст комбо для отображения"""
        if self.last_combo_count > 1:
            return f"x{self.last_combo_count} COMBO!"
        return None
    
    def activate_power(self, power_name: str) -> bool:
        """Активировать способность"""
        return self.powerups.activate(power_name)
    
    def get_active_powers(self) -> list:
        """Получить список активных способностей"""
        return self.powerups.get_active()
    
    def get_slow_factor(self) -> float:
        """Получить множитель замедления"""
        slow_power = self.powerups.power_ups.get("time_slow")
        if slow_power and slow_power.active:
            return slow_power.slow_factor
        return 1.0
    
    def is_magnet_active(self) -> bool:
        """Проверить активен ли магнит"""
        return self.powerups.is_active("magnet")


# Глобальный экземпляр для удобства
new_features = NewFeatures()


def get_combo_system() -> ComboSystem:
    """Получить систему комбо"""
    return new_features.combo


def get_powerup_manager() -> PowerUpManager:
    """Получить менеджер бонусов"""
    return new_features.powerups


def get_difficulty_manager() -> DifficultyManager:
    """Получить менеджер сложности"""
    return new_features.difficulty


# Пример использования в игре (можно добавить в любом месте):
# from modules.new_features import get_combo_system, get_powerup_manager
# combo = get_combo_system()
# combo.on_obstacle_passed()  # прибавить к комбо
# bonus_points = combo.get_bonus_points(10)  # получить бонус