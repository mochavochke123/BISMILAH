"""
Модуль аудио - управление музыкой и звуками
"""

import pygame
from typing import Optional, Dict


class SoundManager:
    """Менеджер звуков"""
    
    def __init__(self, volume: float = 1.0):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.volume: float = volume
    
    def load(self, name: str, filepath: str) -> bool:
        """Загрузить звук"""
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.volume)
            self.sounds[name] = sound
            return True
        except Exception as e:
            print(f"Warning: Could not load sound {filepath}: {e}")
            return False
    
    def play(self, name: str) -> None:
        """Воспроизвести звук"""
        if name in self.sounds:
            self.sounds[name].play()
    
    def set_volume(self, volume: float) -> None:
        """Установить громкость"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def adjust_volume(self, delta: float) -> None:
        """Изменить громкость"""
        self.set_volume(self.volume + delta)
    
    def get(self, name: str) -> Optional[pygame.mixer.Sound]:
        """Получить звук"""
        return self.sounds.get(name)


class AudioManager:
    """Менеджер аудио - музыка и звуки"""
    
    def __init__(self):
        pygame.mixer.init()
        
        self.volume: float = 1.0
        self.current_music: Optional[str] = None
        self.music_stage: int = 0
        
        # Звуки
        self.sound_manager: SoundManager = SoundManager(self.volume)
        self._load_sounds()
    
    def _load_sounds(self) -> None:
        """Загрузить звуки"""
        self.sound_manager.load("death", "dead.mp3")
        self.sound_manager.load("screamer", "screamer.mp3")
        self.sound_manager.load("explosion", "explosion.mp3")
        self.sound_manager.load("dr", "dr.mp3")
        self.sound_manager.load("bonus", "bonus.mp3")
        self.sound_manager.load("q", "q.mp3")
        self.sound_manager.load("q1", "q1.mp3")
    
    def play_music(self, filename: str) -> None:
        """Воспроизвести музыку"""
        if self.current_music != filename:
            pygame.mixer.music.stop()
            try:
                pygame.mixer.music.load(filename)
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1)
                self.current_music = filename
            except Exception as e:
                print(f"Warning: Could not load music {filename}: {e}")
                self.current_music = None
    
    def stop_music(self) -> None:
        """Остановить музыку"""
        pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self) -> None:
        """Пауза музыки"""
        pygame.mixer.music.pause()
    
    def unpause_music(self) -> None:
        """Возобновить музыку"""
        pygame.mixer.music.unpause()
    
    def set_volume(self, volume: float) -> None:
        """Установить громкость"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
        self.sound_manager.set_volume(self.volume)
    
    def adjust_volume(self, delta: float) -> None:
        """Изменить громкость"""
        self.set_volume(self.volume + delta)
    
    # === Звуки ===
    
    def play_death(self) -> None:
        """Звук смерти"""
        self.sound_manager.play("death")
    
    def play_screamer(self) -> None:
        """Звук скримера"""
        self.sound_manager.play("screamer")
    
    def play_explosion(self) -> None:
        """Звук взрыва"""
        self.sound_manager.play("explosion")
    
    def play_dr(self) -> None:
        """Звук DR"""
        self.sound_manager.play("dr")
    
    def play_bonus(self) -> None:
        """Звук бонуса"""
        self.sound_manager.play("bonus")
    
    def play_q(self) -> None:
        """Звук Q"""
        self.sound_manager.play("q")
    
    def play_q1(self) -> None:
        """Звук Q1"""
        self.sound_manager.play("q1")
    
    # === Утилиты ===
    
    def set_music_volume(self, volume: float) -> None:
        """Установить громкость музыки"""
        pygame.mixer.music.set_volume(volume)
    
    def get_music_volume(self) -> float:
        """Получить громкость музыки"""
        return pygame.mixer.music.get_volume()
    
    def is_music_playing(self) -> bool:
        """Проверить играет ли музыка"""
        return pygame.mixer.music.get_busy()
    
    def fadeout(self, time_ms: int = 1000) -> None:
        """Плавное затухание музыки"""
        pygame.mixer.music.fadeout(time_ms)
    
    def update_music_by_score(self, score: int, death_music_played: bool = False) -> None:
        """Обновить музыку в зависимости от счета"""
        if death_music_played:
            return
        
        old_stage = self.music_stage
        
        if score >= 1000:
            self.music_stage = 7
        elif score >= 800:
            self.music_stage = 6
        elif score >= 400:
            self.music_stage = 5
        elif score >= 250:
            self.music_stage = 4
        elif score >= 100:
            self.music_stage = 3
        else:
            self.music_stage = 0
        
        # Сменить музыку если стадия изменилась
        if self.music_stage != old_stage:
            if self.music_stage == 0:
                self.play_music("rr.mp3")
            elif self.music_stage == 3:
                self.play_music("rrr.mp3")
            elif self.music_stage == 4:
                self.play_music("fon.mp3")
            elif self.music_stage == 5:
                self.play_music("dr.mp3")
            elif self.music_stage == 6:
                self.play_music("fos.mp3")