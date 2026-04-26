"""
Модуль частиц - системы частиц для эффектов
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from .config import (
    VIRTUAL_WIDTH,
    VIRTUAL_HEIGHT,
    FPS,
    RAIN_THRESHOLD,
    THUNDER_THRESHOLD,
    BUFF_PARTICLE_SPAWN_INTERVAL,
    MARIHUANA_SHAKE_INTENSITY,
    FIRE_ANIMATION_DURATION,
)


class Particle:
    """Базовая частица"""
    
    def __init__(
        self,
        x: float,
        y: float,
        vel_x: float,
        vel_y: float,
        lifetime: int,
        color: Tuple[int, int, int],
        size: int = 4
    ):
        self.x: float = x
        self.y: float = y
        self.vel_x: float = vel_x
        self.vel_y: float = vel_y
        self.lifetime: int = lifetime
        self.max_lifetime: int = lifetime
        self.color: Tuple[int, int, int] = color
        self.size: int = size
    
    def update(self, slowdown_factor: float = 1.0) -> bool:
        """Обновить частицу. Возвращает False если частица мертва"""
        self.x += self.vel_x * slowdown_factor
        self.y += self.vel_y * slowdown_factor
        self.lifetime -= 1
        return self.lifetime > 0
    
    def get_alpha(self) -> int:
        """Получить прозрачность"""
        return int(255 * (self.lifetime / self.max_lifetime))
    
    def get_position(self) -> Tuple[int, int]:
        """Получить позицию"""
        return (int(self.x), int(self.y))


class RainParticle(Particle):
    """Частица дождя"""
    
    def __init__(self, x: float, y: float):
        super().__init__(
            x, y,
            0,
            random.randint(10, 20),
            -1,  # Бесконечное время жизни
            (100, 150, 255),
            2
        )
    
    def reset(self) -> None:
        """Сбросить позицию"""
        self.x = random.randint(0, VIRTUAL_WIDTH)
        self.y = random.randint(-VIRTUAL_HEIGHT, 0)
        self.vel_y = random.randint(10, 20)


class SplashParticle(Particle):
    """Частица брызг"""
    
    def __init__(self, x: float, y: float):
        angle = random.uniform(0, math.pi)
        speed = random.uniform(5, 10)
        super().__init__(
            x, y,
            math.cos(angle) * speed,
            -math.sin(angle) * speed,
            random.randint(20, 40),
            (100, 150, 255),
            3
        )


class BuffParticle(Particle):
    """Частица баффа"""
    
    def __init__(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int]
    ):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        super().__init__(
            x, y,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            random.randint(40, 80),
            color,
            4
        )


class ExplosionParticle(Particle):
    """Частица взрыва"""
    
    def __init__(self, x: float, y: float):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 8)
        color = (
            random.randint(150, 255),
            random.randint(50, 150),
            random.randint(0, 100)
        )
        super().__init__(
            x, y,
            math.cos(angle) * speed,
            math.sin(angle) * speed,
            random.randint(40, 80),
            color,
            8
        )


class FireParticle:
    """Частица огня"""
    
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.lifetime: int = FIRE_ANIMATION_DURATION
        self.max_lifetime: int = FIRE_ANIMATION_DURATION
        self.image: Optional[pygame.Surface] = None
    
    def update(self) -> bool:
        """Обновить частицу"""
        self.lifetime -= 1
        return self.lifetime > 0
    
    def get_progress(self) -> float:
        """Получить прогресс (0.0 - 1.0)"""
        return self.lifetime / self.max_lifetime
    
    def get_position(self) -> Tuple[int, int]:
        """Получить позицию"""
        return (int(self.x), int(self.y))


class ParticleSystem:
    """Система управления частицами"""
    
    def __init__(self):
        # Дождь
        self.rain_particles: List[RainParticle] = []
        self.max_rain: int = 100
        
        # Брызги
        self.splash_particles: List[SplashParticle] = []
        
        # Баффы
        self.buff_particles: List[BuffParticle] = []
        
        # Взрывы
        self.explosion_particles: List[ExplosionParticle] = []
        
        # Огонь
        self.fire_particles: List[FireParticle] = []
        
        # Трейл
        self.trail_particles: List[Particle] = []
        
        # Таймеры
        self.particle_timer: int = 0
        
        # Звезды
        self.stars: List[List] = []
        self.init_stars()
    
    def init_stars(self) -> None:
        """Инициализировать звезды"""
        self.stars = [
            [
                random.randint(0, VIRTUAL_WIDTH),
                random.randint(0, VIRTUAL_HEIGHT),
                random.randint(1, 3),
            ]
            for _ in range(50)
        ]
    
    # === Дождь ===
    
    def spawn_rain(self) -> None:
        """Спавн частиц дождя"""
        if len(self.rain_particles) < self.max_rain:
            x = random.randint(0, VIRTUAL_WIDTH)
            y = random.randint(-VIRTUAL_HEIGHT, 0)
            self.rain_particles.append(RainParticle(x, y))
    
    def update_rain(self, slowdown_factor: float = 1.0) -> None:
        """Обновить дождь"""
        for particle in self.rain_particles:
            particle.y += particle.vel_y * slowdown_factor
            if particle.y > VIRTUAL_HEIGHT:
                particle.reset()
        
        if len(self.rain_particles) > 200:
            self.rain_particles = self.rain_particles[-200:]
    
    def draw_rain(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать дождь"""
        for particle in self.rain_particles:
            pygame.draw.line(
                screen,
                (100, 150, 255),
                (int(particle.x + shake_x), int(particle.y + shake_y)),
                (int(particle.x + shake_x), int(particle.y + 10 + shake_y)),
                2,
            )
    
    # === Брызги ===
    
    def spawn_splash(self, x: float, y: float) -> None:
        """Спавн брызг"""
        for _ in range(10):
            self.splash_particles.append(SplashParticle(x, y))
    
    def update_splash(self, slowdown_factor: float = 1.0) -> None:
        """Обновить брызги"""
        for particle in self.splash_particles[:]:
            particle.update(slowdown_factor)
            particle.vel_y += 0.5 * slowdown_factor
            if particle.lifetime <= 0 or particle.y > VIRTUAL_HEIGHT:
                self.splash_particles.remove(particle)
        
        if len(self.splash_particles) > 200:
            self.splash_particles = self.splash_particles[-200:]
    
    def draw_splash(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать брызги"""
        for particle in self.splash_particles:
            alpha = particle.get_alpha()
            color = (*particle.color, alpha)
            pygame.draw.circle(
                screen,
                (particle.color[0], particle.color[1], particle.color[2], alpha),
                (int(particle.x + shake_x), int(particle.y + shake_y)),
                particle.size,
            )
    
    # === Баффы ===
    
    def spawn_buff_particle(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int],
        count: int = 1
    ) -> None:
        """Спавн частиц баффа"""
        for _ in range(count):
            self.buff_particles.append(BuffParticle(x, y, color))
    
    def update_buff_particles(self, slowdown_factor: float = 1.0) -> None:
        """Обновить частицы баффов"""
        for particle in self.buff_particles[:]:
            if not particle.update(slowdown_factor):
                self.buff_particles.remove(particle)
        
        if len(self.buff_particles) > 500:
            self.buff_particles = self.buff_particles[-500:]
    
    def draw_buff_particles(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать частицы баффов"""
        for particle in self.buff_particles:
            alpha = particle.get_alpha()
            color = (*particle.color, alpha)
            pygame.draw.circle(
                screen,
                color,
                (int(particle.x + shake_x), int(particle.y + shake_y)),
                particle.size,
            )
    
    # === Взрывы ===
    
    def spawn_explosion(self, x: float, y: float) -> None:
        """Спавн взрыва"""
        self.explosion_particles.clear()
        for _ in range(100):
            self.explosion_particles.append(ExplosionParticle(x, y))
    
    def update_explosions(self, slowdown_factor: float = 1.0) -> None:
        """Обновить взрывы"""
        for particle in self.explosion_particles[:]:
            if not particle.update(slowdown_factor):
                self.explosion_particles.remove(particle)
        
        if len(self.explosion_particles) > 200:
            self.explosion_particles = self.explosion_particles[-200:]
    
    def draw_explosions(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать взрывы"""
        for p in self.explosion_particles:
            alpha = max(0, min(255, int(255 * (p.lifetime / 60))))
            size = max(2, 8 * (1 - p.lifetime / 60))
            color = (*p.color, alpha)
            pygame.draw.circle(
                screen,
                color,
                (int(p.x + shake_x), int(p.y + shake_y)),
                int(size),
            )
    
    # === Огонь ===
    
    def spawn_fire(self, x: float, y: float) -> None:
        """Спавн огня"""
        self.fire_particles.append(FireParticle(x, y))
    
    def update_fire(self) -> None:
        """Обновить огонь"""
        for particle in self.fire_particles[:]:
            if not particle.update():
                self.fire_particles.remove(particle)
        
        if len(self.fire_particles) > 50:
            self.fire_particles = self.fire_particles[-50:]
    
    def draw_fire(
        self,
        screen: pygame.Surface,
        fire_image: Optional[pygame.Surface],
        shake_x: int = 0,
        shake_y: int = 0
    ) -> None:
        """Отрисовать огонь"""
        for fa in self.fire_particles:
            if fire_image:
                progress = fa.get_progress()
                scale = 1.0 + 0.5 * (1 - progress)
                alpha = int(255 * progress)
                scaled_fire = pygame.transform.scale(
                    fire_image, (int(100 * scale), int(100 * scale))
                )
                surf = scaled_fire.copy()
                surf.set_alpha(alpha)
                screen.blit(
                    surf,
                    (
                        int(fa.x - (100 * scale - 100) // 2 + shake_x),
                        int(fa.y - (100 * scale - 100) // 2 + shake_y),
                    ),
                )
    
    # === Звезды ===
    
    def update_stars(self, slowdown_factor: float = 1.0) -> None:
        """Обновить звезды"""
        for star in self.stars:
            star[0] += star[2] * 0.05 * slowdown_factor
            if star[0] > VIRTUAL_WIDTH:
                star[0] = 0
                star[1] = random.randint(0, VIRTUAL_HEIGHT)
    
    def draw_stars(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать звезды"""
        for star in self.stars:
            brightness = int(200 * (star[2] / 3))
            pygame.draw.circle(
                screen,
                (brightness, brightness, brightness),
                (int(star[0] + shake_x), int(star[1] + shake_y)),
                star[2],
            )
    
    # === Трейл ===
    
    def add_trail(
        self,
        x: float,
        y: float,
        color: Tuple[int, int, int]
    ) -> None:
        """Добавить частицу трейла"""
        self.trail_particles.append(Particle(
            x, y,
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            40,
            color,
            4
        ))
    
    def update_trail(self) -> None:
        """Обновить трейл"""
        for particle in self.trail_particles[:]:
            if not particle.update(1.0):
                self.trail_particles.remove(particle)
        
        if len(self.trail_particles) > 100:
            self.trail_particles = self.trail_particles[-100:]
    
    def draw_trail(self, screen: pygame.Surface, shake_x: int = 0, shake_y: int = 0) -> None:
        """Отрисовать трейл"""
        for p in self.trail_particles:
            alpha = int(255 * (p.lifetime / 40))
            color = (*p.color, alpha)
            pygame.draw.circle(
                screen,
                color,
                (int(p.x + shake_x), int(p.y + shake_y)),
                p.size,
            )
    
    # === Общие методы ===
    
    def clear(self) -> None:
        """Очистить все частицы"""
        self.rain_particles.clear()
        self.splash_particles.clear()
        self.buff_particles.clear()
        self.explosion_particles.clear()
        self.fire_particles.clear()
        self.trail_particles.clear()
    
    def reset(self) -> None:
        """Сбросить систему"""
        self.clear()
        self.init_stars()
    
    @staticmethod
    def get_buff_color(buff_type: str) -> Tuple[int, int, int]:
        """Получить цвет для типа баффа"""
        colors = {
            "points": (255, 215, 0),
            "double_points": (255, 215, 0),
            "slow": (0, 191, 255),
            "slow_down": (0, 191, 255),
            "invincibility": (255, 0, 255),
            "score_boost": (0, 255, 128),
            "life": (255, 0, 0),
            "shield": (128, 128, 255),
            "laser": (255, 0, 0),
            "fire": (255, 69, 0),
            "dvd": (255, 0, 255),
            "marihuana": (0, 255, 0),
        }
        return colors.get(buff_type, (255, 255, 255))