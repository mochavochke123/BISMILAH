"""
Модуль ИИ для игры - умные враги и поведение
"""

import random
import math
from typing import Optional, Tuple


class AIModule:
    """Модуль искусственного интеллекта для врагов"""
    
    def __init__(self):
        self.enemies = []
        self.difficulty = 1.0
    
    def set_difficulty(self, level: float):
        """Установить сложность (0.0 - 2.0)"""
        self.difficulty = max(0.0, min(2.0, level))
    
    def get_behavior(self, enemy_x: float, enemy_y: float, player_x: float, player_y: float) -> str:
        """
        Определить поведение врага на основе позиции игрока
        Возвращает: "attack", "retreat", "dodge", "patrol"
        """
        dx = player_x - enemy_x
        dy = player_y - enemy_y
        distance = math.hypot(dx, dy)
        
        # Простое поведение на основе расстояния
        if distance < 200:
            return "attack"
        elif distance < 400:
            if random.random() < 0.3 * self.difficulty:
                return "dodge"
            return "patrol"
        else:
            return "patrol"
    
    def predict_player_position(self, player_x: float, player_y: float, player_vel_x: float) -> Tuple[float, float]:
        """
        Предсказать позицию игрока через короткое время
        """
        prediction_time = 0.5  # секунды
        future_x = player_x + player_vel_x * prediction_time * self.difficulty
        future_y = player_y  # без вертикального предсказания
        return (future_x, future_y)
    
    def calculate_attack_angle(self, from_x: float, from_y: float, to_x: float, to_y: float) -> float:
        """Рассчитать угол атаки с отклонением"""
        dx = to_x - from_x
        dy = to_y - from_y
        base_angle = math.atan2(dy, dx)
        
        # Добавить немного случайности в зависимости от сложности
        deviation = (1.0 - self.difficulty) * 0.3
        deviation *= random.uniform(-1, 1)
        
        return base_angle + deviation
    
    def should_spawn_obstacle(self, score: int, spawn_interval: int) -> bool:
        """Решить нужно ли спавнить препятствие"""
        spawn_chance = 1.0 / spawn_interval
        spawn_chance *= (1.0 + self.difficulty * 0.5)
        
        return random.random() < spawn_chance


class DifficultyManager:
    """Менеджер сложности - адаптивная сложность"""
    
    def __init__(self):
        self.base_level = 1.0
        self.current_level = 1.0
        self.max_level = 2.0
        self.score_thresholds = [50, 100, 200, 400, 800, 1000]
        self.player_stats = {
            "deaths": 0,
            "bonuses_collected": 0,
            "obstacles_passed": 0,
        }
    
    def update_level(self, score: int):
        """Обновить уровень сложности на основе счета"""
        # Увеличиваем сложность с ростом счета
        if score < 100:
            self.current_level = 1.0
        elif score < 250:
            self.current_level = 1.2
        elif score < 500:
            self.current_level = 1.4
        elif score < 800:
            self.current_level = 1.6
        else:
            self.current_level = 1.8
        
        return self.current_level
    
    def adapt_to_player(self, lives_lost: bool, bonus_collected: bool):
        """
        Адаптировать сложность к производительности игрока
        """
        if lives_lost:
            self.current_level = max(1.0, self.current_level - 0.1)
            self.player_stats["deaths"] += 1
        
        if bonus_collected:
            self.current_level = min(self.max_level, self.current_level + 0.05)
            self.player_stats["bonuses_collected"] += 1
    
    def get_speed_multiplier(self) -> float:
        """Множитель скорости для текущей сложности"""
        return 1.0 + (self.current_level - 1.0) * 0.5
    
    def get_spawn_multiplier(self) -> float:
        """Множитель частоты спавна"""
        return 1.0 + (self.current_level - 1.0) * 0.3


class ComboSystem:
    """Система комбо-очков"""
    
    def __init__(self):
        self.combo_count = 0
        self.combo_timer = 0
        self.max_combo_time = 180  # 3 секунды при 60 FPS
        self.multiplier = 1
    
    def update(self):
        """Обновить таймер комбо"""
        if self.combo_timer > 0:
            self.combo_timer -= 1
        else:
            self.combo_count = 0
            self.multiplier = 1
    
    def add_obstacle_passed(self):
        """Добавить пройденное препятствие к комбо"""
        self.combo_count += 1
        self.combo_timer = self.max_combo_time
        self.multiplier = min(self.combo_count, 10)
    
    def reset(self):
        """Сбросить комбо"""
        self.combo_count = 0
        self.combo_timer = 0
        self.multiplier = 1
    
    def get_bonus_points(self, base_points: int) -> int:
        """Получить бонусные очки с учетом комбо"""
        return base_points * self.multiplier


__all__ = ["AIModule", "DifficultyManager", "ComboSystem"]