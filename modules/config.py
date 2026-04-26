"""
Конфигурация игры - все игровые константы
"""

# Настройки экрана
FPS: int = 80
VIRTUAL_WIDTH: int = 1300
VIRTUAL_HEIGHT: int = 750

# Размеры персонажей и объектов
PLAYER_SIZE: int = 120
PLAYER_HITBOX_SCALE: float = 0.7
BONUS_SIZE: int = 150
SKATEBOARD_WIDTH: int = 150
SKATEBOARD_HEIGHT: int = 30
SKATEBOARD_OFFSET_Y: int = 35

# Физика персонажа
PLAYER_ACCEL: float = 1.0
PLAYER_FRICTION: float = 0.9
MAX_SPEED: int = 10
MAX_JUMP_TIME: int = 30
TERMINAL_VELOCITY: int = 20

# Настройки скейтборда
SKATEBOARD_ROTATION_SPEED: int = 15
SKATEBOARD_TRICKS: dict = {
    "kickflip": {"rotation": 360, "duration": 30, "weight": 0.3},
    "hardflip": {"rotation": 720, "duration": 40, "weight": 0.2},
    "heelflip": {"rotation": 360, "duration": 30, "weight": 0.3},
    "tre_flip": {"rotation": 1080, "duration": 50, "weight": 0.2},
}
SKATEBOARD_DEFAULT_COLORS: list = [
    (255, 0, 0),   # Red
    (0, 0, 255),   # Blue
    (0, 255, 0),   # Green
    (255, 255, 0), # Yellow
    (255, 165, 0), # Orange
]

# Анимации
JUMP_ANIMATION_DURATION: int = 40
DEATH_ANIMATION_DURATION: int = 120
GAME_OVER_ANIMATION_DURATION: int = 120

# Пороги событий - дождь и погода
RAIN_THRESHOLD: int = 50
THUNDER_THRESHOLD: int = 100
LIGHTNING_INTERVAL: int = 240
SUN_THRESHOLD: int = 50

# Пороги - босс и скримеры
BOSS_THRESHOLD_START: int = 260
BOSS_THRESHOLD_END: int = 400
BOSS_SPAWN_INTERVAL: int = 200
BOSS_FADE_DURATION: int = 60
BOSS_SIZE: int = 200
BOSS_MAX_HEALTH: int = 100
BOSS_DAMAGE_LASER: int = 10
BOSS_DAMAGE_FIRE: int = 5
BOSS_MOVEMENT_SPEED: float = 0.05
BOSS_PROJECTILE_SPEED: float = 1.9

# Скримеры
SCREAMER_INTERVAL: int = 1800
SCREAMER_DURATION: int = 30
SCREAMER_THRESHOLD: int = 150

# NPC и специальные режимы
NPC_THRESHOLD: int = 1000
NPC_INTERVAL: int = 150
TOLD_SPAWN_CHANCE: float = 0.15
ANGEL_THRESHOLD: int = 200

# Звездное небо
STARFIELD_DENSITY: int = 50
MILESTONE_INTERVAL: int = 50

# Скейтборд
WING_FLAP_SPEED: float = 0.2

# Бонусы - шансы
LIFE_BONUS_CHANCE: float = 0.06
SHIELD_BONUS_CHANCE: float = 0.1
TRAP_CHANCE: float = 0.05
SPIKE_CHANCE: float = 0.1
BONUS_NOTIFICATION_DURATION: int = 180

# Бонусы - длительность (в кадрах)
SHIELD_DURATION: int = 20 * FPS
MARIHUANA_DURATION: int = 14 * FPS
MARIHUANA_SHAKE_INTENSITY: int = 5
MARIHUANA_ANIM_FPS: int = 8

# Бонусы - эффекты
LASER_RANGE: int = 350
LASER_THICKNESS: int = 10
LASER_BOSS_COOLDOWN: int = 30
FIRE_RANGE: int = 300
FIRE_DURATION: int = 10 * FPS
FIRE_BURN_CHANCE: float = 0.05
FIRE_ANIMATION_DURATION: int = 30
PLAYER_FIRE_SPAWN_CHANCE: float = 0.1
DVD_DURATION: int = 10 * FPS

# Частицы
BUFF_PARTICLE_SPAWN_INTERVAL: int = 5
MILESTONE_FLASH_DURATION: int = 30
MILESTONE_TEXT_DURATION: int = 120
TRANSITION_DURATION: int = 60
DIFFICULTY_THRESHOLD: int = 100
DIFFICULTY_TEXT_DURATION: int = 120

# Препятствия
OBSTACLE_VISUAL_SCALE: float = 1.2
OBSTACLE_HITBOX_SCALE: float = 0.95

# Режимы игры
MODES: list = [
    {
        "name": "Нормальный",
        "obstacle_speed": 12,
        "gravity": 1.8,
        "jump_force": -36,
        "jump_hold": -0.6,
        "bonus_chance": 0.15,
        "spawn_interval": (70, 140),
        "high_prob": 0.5,
    },
    {
        "name": "Быстрый",
        "obstacle_speed": 16,
        "gravity": 1.5,
        "jump_force": -36,
        "jump_hold": -0.6,
        "bonus_chance": 0.25,
        "spawn_interval": (70, 140),
        "high_prob": 0.5,
    },
    {
        "name": "Уклонение",
        "obstacle_speed": 7,
        "gravity": 1.8,
        "jump_force": -36,
        "jump_hold": -0.6,
        "bonus_chance": 0.15,
        "spawn_interval": (55, 110),
        "high_prob": 0.0,
    },
]

# Управление по умолчанию
DEFAULT_KEYS_P1: dict = {
    "left": "K_a",
    "right": "K_d",
    "jump": "K_w",
    "crouch": "K_s",
}

DEFAULT_KEYS_P2: dict = {
    "left": "K_j",
    "right": "K_l",
    "jump": "K_i",
    "crouch": "K_k",
}

# Файлы ассетов
INITIAL_BACKGROUND_FILES: list = ["y.jpg", "anu.jpg"]
GAME_BACKGROUND_FILES: list = ["ddd.png", "ddd1.jpg"]
CHAR_BACKGROUND_FILES: list = ["foog.jpg", "foog1.jpg", "foog2.jpg"]
MODE_BACKGROUND_FILES: list = ["fff.png", "t.png", "tt.png", "ttt.png"]
CHARACTER_FILES: list = ["eee.jpg", "www.jpg"]
NPC_BACKGROUND_FILES: list = ["npc.jpg", "npc1.jpg", "npc2.jpg"]
TOLD_IMAGE_FILES: list = ["told.png", "told1.png"]
SKATEBOARD_FILES: list = [
    "skateboard.png",
    "skateboard1.png",
    "skateboard2.png",
    "skateboard3.png",
    "skateboard4.png",
]

# Интервалы смены фонов
CHAR_BACKGROUND_SWITCH_INTERVAL: int = 7 * FPS
MODE_BACKGROUND_SWITCH_INTERVAL: int = 5 * FPS

# DVD режим
DVD_CLEAR_OBSTACLES: bool = True
DVD_NO_SPAWN: bool = True