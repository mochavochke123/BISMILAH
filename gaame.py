# -*- coding: utf-8 -*-
import math
import warnings

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import pygame
import random
import platform
import os
import tkinter as tk
from tkinter import filedialog
from io import BytesIO
from PIL import Image
import datetime
import json

pygame.init()
pygame.mixer.init()
FPS = 80
PLAYER_SIZE = 120
PLAYER_HITBOX_SCALE = 0.7
BONUS_SIZE = 150
PLAYER_ACCEL = 1.0
PLAYER_FRICTION = 0.9
MAX_SPEED = 10
MAX_JUMP_TIME = 30
GAME_OVER_ANIMATION_DURATION = 120
RAIN_THRESHOLD = 50
THUNDER_THRESHOLD = 100
LIGHTNING_INTERVAL = 240
OBSTACLE_VISUAL_SCALE = 1.2
OBSTACLE_HITBOX_SCALE = 0.95
JUMP_ANIMATION_DURATION = 40
DEATH_ANIMATION_DURATION = 120
SUN_THRESHOLD = 50
ANGEL_THRESHOLD = 200
SCREAMER_THRESHOLD = 150
STARFIELD_DENSITY = 50
MILESTONE_INTERVAL = 50
MILESTONE_FLASH_DURATION = 30
MILESTONE_TEXT_DURATION = 120
TRANSITION_DURATION = 60
DIFFICULTY_THRESHOLD = 100
DIFFICULTY_TEXT_DURATION = 120
WING_FLAP_SPEED = 0.2
SCREAMER_INTERVAL = 1800
SCREAMER_DURATION = 30
LIFE_BONUS_CHANCE = 0.06
SHIELD_BONUS_CHANCE = 0.1
BONUS_NOTIFICATION_DURATION = 180
TRAP_CHANCE = 0.05
SPIKE_CHANCE = 0.1
TERMINAL_VELOCITY = 20
SHIELD_DURATION = 20 * FPS
LASER_RANGE = 350
LASER_THICKNESS = 10
BUFF_PARTICLE_SPAWN_INTERVAL = 5
FIRE_RANGE = 300
FIRE_BURN_CHANCE = 0.05
FIRE_DURATION = 10 * FPS
FIRE_ANIMATION_DURATION = 30
PLAYER_FIRE_SPAWN_CHANCE = 0.1
BOSS_THRESHOLD_START = 260
BOSS_THRESHOLD_END = 400
BOSS_SPAWN_INTERVAL = 200
BOSS_FADE_DURATION = 60
BOSS_PROJECTILE_SPEED = 1.9
BOSS_SIZE = 200
BOSS_MAX_HEALTH = 100
BOSS_DAMAGE_LASER = 10
BOSS_DAMAGE_FIRE = 5
BOSS_MOVEMENT_SPEED = 0.05
LASER_BOSS_COOLDOWN = 30
NPC_THRESHOLD = 1000
NPC_INTERVAL = 150
TOLD_SPAWN_CHANCE = 0.15
DVD_DURATION = 10 * FPS
DVD_CLEAR_OBSTACLES = True
DVD_NO_SPAWN = True
MARIHUANA_DURATION = 14 * FPS
MARIHUANA_SHAKE_INTENSITY = 5
MARIHUANA_ANIM_FPS = 8
# Skateboard settings
SKATEBOARD_WIDTH = 150
SKATEBOARD_HEIGHT = 30
SKATEBOARD_OFFSET_Y = 35  # Отступ от низа персонажа
SKATEBOARD_ROTATION_SPEED = 15
SKATEBOARD_TRICKS = {
    "kickflip": {"rotation": 360, "duration": 30, "weight": 0.3},
    "hardflip": {"rotation": 720, "duration": 40, "weight": 0.2},
    "heelflip": {"rotation": 360, "duration": 30, "weight": 0.3},
    "tre_flip": {"rotation": 1080, "duration": 50, "weight": 0.2},
}


class Game:
    def __init__(self):
        self.virtual_width = 1300
        self.virtual_height = 750
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.virtual_width, self.virtual_height))
        self.virtual_screen = pygame.Surface(
            (self.virtual_width, self.virtual_height), pygame.SRCALPHA
        )
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 36, bold=True)
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.small_font = pygame.font.SysFont("arial", 24)
        self.state = "welcome"
        self.selected_character = None
        self.selected_character2 = None
        self.current_mode = None
        self.coop_mode = False
        # Player 1
        self.player1_x = 150
        self.player1_y = self.virtual_height - PLAYER_SIZE - 10
        self.player1_vel_x = 0
        self.player1_vel_y = 0
        self.player1_is_jumping = False
        self.player1_is_crouching = False
        self.player1_was_on_ground = True
        self.player1_jump_timer = 0
        self.player1_jump_animation_timer = 0
        self.player1_death_animation_timer = 0
        self.player1_is_dead = False
        self.player1_lives = 1
        self.player1_invincibility = False
        self.player1_invincibility_timer = 0
        self.player1_shield_active = False
        self.player1_shield_timer = 0
        self.player1_double_jump_available = False
        # Player 2 (for co-op)
        self.player2_x = 150
        self.player2_y = self.virtual_height - PLAYER_SIZE - 10
        self.player2_vel_x = 0
        self.player2_vel_y = 0
        self.player2_is_jumping = False
        self.player2_is_crouching = False
        self.player2_was_on_ground = True
        self.player2_jump_timer = 0
        self.player2_jump_animation_timer = 0
        self.player2_death_animation_timer = 0
        self.player2_is_dead = False
        self.player2_lives = 1
        self.player2_invincibility = False
        self.player2_invincibility_timer = 0
        self.player2_shield_active = False
        self.player2_shield_timer = 0
        self.player2_double_jump_available = False
        self.starting_lives = 1
        self.obstacles = []
        self.bonuses = []
        self.rain_particles = []
        self.splash_particles = []
        self.stars = [
            [
                random.randint(0, self.virtual_width),
                random.randint(0, self.virtual_height),
                random.randint(1, 3),
            ]
            for _ in range(STARFIELD_DENSITY)
        ]
        self.trail_particles = []
        self.buff_particles = []
        self.explosion_particles = []
        self.lasers = []
        self.fire_animations = []
        self.boss_active = False
        self.boss_x = self.virtual_width
        self.boss_y = self.virtual_height // 2 - BOSS_SIZE // 2
        self.boss_health = BOSS_MAX_HEALTH
        self.boss_alpha = 255
        self.boss_fade_timer = 0
        self.boss_spawn_timer = 0
        self.boss_projectiles = []
        self.boss_defeat_timer = 0
        self.bonus_notification = None
        self.bonus_notification_timer = 0
        self.milestone_flash = 0
        self.last_milestone = 0
        self.milestone_text_timer = 0
        self.current_milestone = 0
        self.difficulty_text_timer = 0
        self.current_difficulty_level = 0
        self.screamer_timer = SCREAMER_INTERVAL
        self.screamer_flash = 0
        self.score = 0
        self.high_score = 0
        self.spawn_timer = 0
        self.next_spawn_interval = 0
        self.double_points = False
        self.slow_down = False
        self.laser_active = False
        self.fire_active = False
        self.fire_timer = 0
        self.player_fire_spawn_timer = 0
        self.marihuana_active = False
        self.marihuana_timer = 0
        self.marihuana_anim_timer = 0
        self.score_multiplier = 1
        self.bonus_timer = 0
        self.game_over_timer = 0
        self.lightning_timer = 0
        self.lightning_flash = 0
        self.paused = False
        self.is_angel = False
        self.wing_flap_timer = 0
        self.current_music = None
        self.music_stage = 0
        self.game_background = None
        self.initial_game_background = None
        self.current_anu_bg = None
        self.anu_backgrounds = []
        self.initial_background_files = ["y.jpg", "anu.jpg", "anu1.jpg", "anu2.jpg"]
        self.game_background_files = ["ddd.png", "ddd1.jpg", "ddd2.jpg", "ddd3.jpg"]
        # Load backgrounds at startup
        init_bg = random.choice(self.initial_background_files)
        self.initial_game_background = self.load_image(init_bg)
        if self.initial_game_background:
            self.initial_game_background = pygame.transform.scale(self.initial_game_background, (self.virtual_width, self.virtual_height))
        game_bg = random.choice(self.game_background_files)
        self.game_background = self.load_image(game_bg)
        if self.game_background:
            self.game_background = pygame.transform.scale(self.game_background, (self.virtual_width, self.virtual_height))
        self.toy_background = None
        self.blood_background = None
        self.game_over_image = None
        self.obstacle_texture = None
        self.screamer_image = None
        self.death_sound = None
        self.screamer_sound = None
        self.wing_image = None
        self.heart_image = None
        self.shield_image = None
        self.bonus_sound = None
        self.spike_texture = None
        self.points_image = None
        self.slow_image = None
        self.invincibility_image = None
        self.score_boost_image = None
        self.laser_image = None
        self.fire_buff_image = None
        self.fire_animation_image = None
        self.boss_image = None
        self.crest_image = None
        self.crest_frames = []
        self.crest_anim_timer = 0
        self.crest_anim_fps = 8
        self.monster_frames = []
        self.monster_anim_timer = 0
        self.monster_anim_fps = 8
        self.marihuana_frames = []
        self.hop_image = None
        self.wau_image = None
        self.zxc_image = None
        self.csk_image = None
        self.ricc_image = None
        self.dadep_image = None
        self.hoppe_image = None
        self.zvb_image = None
        self.volume_icon = None
        self.load_custom_icon = None
        self.help_icon = None
        self.help_background = None
        self.trap_image = None
        self.secret_image = None
        self.buff_particle_timer = 0
        self.score_timer = 0
        self.explosion_sound = None
        self.dr_sound = None
        self.laser_boss_timer = 0
        self.volume = 1.0
        self.custom_skateboard_loaded = False
        self.slowdown_triggered = False
        self.slowdown_triggered2 = False
        self.slowdown_timer2 = 0
        self.q_sound = None
        self.q1_sound = None
        self.CHARACTERS = []
        self.char_bg_files = ["foog.jpg", "foog1.jpg", "foog2.jpg"]
        self.mode_bg_files = ["fff.png", "t.png", "tt.png", "ttt.png"]
        self.char_backgrounds = []
        self.mode_backgrounds = []
        self.char_current_background_index = 0
        self.char_next_background_index = 0
        self.char_background_timer = 0
        self.char_transition_timer = 0
        self.char_transition_alpha = 0
        self.mode_current_background_index = 0
        self.mode_next_background_index = 0
        self.mode_background_timer = 0
        self.mode_transition_alpha = 0
        self.mode_transition_timer = 0
        self.CHAR_BACKGROUND_SWITCH_INTERVAL = 7 * FPS
        self.MODE_BACKGROUND_SWITCH_INTERVAL = 5 * FPS
        self.MODES = [
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
        self.help_scroll_offset = 0
        self.help_scroll_speed = 20
        self.controls_scroll_offset = 0
        self.controls_scroll_speed = 20
        self.npc_backgrounds = []
        self.current_npc_index = 0
        self.told_images = []
        self.dvd_image = None
        self.dvd_active = False
        self.dvd_timer = 0
        self.ops_musics = ["ops.mp3", "ops1.mp3", "ops2.mp3", "ops3.mp3", "ops4.mp3"]
        self.current_ops_index = 0
        self.custom_loaded = False
        self.death_music_played = False
        self.keys_p1 = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "crouch": pygame.K_s,
        }
        self.keys_p2 = {
            "left": pygame.K_j,
            "right": pygame.K_l,
            "jump": pygame.K_i,
            "crouch": pygame.K_k,
        }
        self.remapping_active = False
        self.remapping_player = None
        self.remapping_action = None
        self.controls_state = "menu"
        self.load_high_score()
        self.load_controls()
        self.load_characters()
        self.load_music()
        self.set_all_volumes()
        self.sf_background = None
        self.sf1_image = None
        self.sf2_image = None
        self.tron_image = None
        self.sasha_image = None
        self.assets_loaded = False
        self.welcome_image = None
        self.welcome_frames = []
        self.welcome_frame_timer = 0
        self.welcome_fps = 10
        self.slowdown_timer = 0
        self.animation_timer = 0
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)
        # Skateboard selection
        self.selected_skateboard = 0  # индекс выбранного скейтборда
        self.skateboard_skins = []
        self.skateboard_images = []
        self.skateboard_default_colors = [
            (255, 0, 0),  # Red
            (0, 0, 255),  # Blue
            (0, 255, 0),  # Green
            (255, 255, 0),  # Yellow
            (255, 165, 0),  # Orange
        ]
        # Player skateboard states
        self.player1_trick_timer = 0
        self.player1_current_trick = None
        self.player1_skateboard_rotation = 0
        if self.coop_mode:
            self.player2_trick_timer = 0
            self.player2_current_trick = None
            self.player2_skateboard_rotation = 0
        self.skateboard_particle_timer = 0
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)
        # load_skateboard_assets() removed 


    def load_controls(self):
        try:
            with open("controls.json", "r") as f:
                data = json.load(f)
                self.keys_p1 = {
                    k: pygame.key.key_code(v) if isinstance(v, str) else v
                    for k, v in data.get("p1", self.keys_p1).items()
                }
                self.keys_p2 = {
                    k: pygame.key.key_code(v) if isinstance(v, str) else v
                    for k, v in data.get("p2", self.keys_p2).items()
                }
        except:
            pass

    def save_controls(self):
        data = {
            "p1": {k: pygame.key.name(v) for k, v in self.keys_p1.items()},
            "p2": {k: pygame.key.name(v) for k, v in self.keys_p2.items()},
        }
        with open("controls.json", "w") as f:
            json.dump(data, f)

    def load_image(self, file):
        try:
            return pygame.image.load(file)
        except:
            print(f"Warning: Could not load image {file}")
            return None

    def load_gif_frames(self, file, scale_size):
        frames = []
        try:
            gif = Image.open(file)
            frame_index = 0
            while True:
                frame = gif.copy().convert("RGBA")
                pygame_frame = pygame.image.fromstring(
                    frame.tobytes(), frame.size, frame.mode
                )
                pygame_frame = pygame.transform.scale(pygame_frame, scale_size)
                frames.append(pygame_frame)
                frame_index += 1
                gif.seek(frame_index)
        except EOFError:
            pass
        except Exception as e:
            print(f"Warning: Could not load GIF {file}: {e}")
            # Fallback: create a single empty frame
            fallback = pygame.Surface(scale_size)
            fallback.fill((255, 255, 255))
            frames = [fallback]
        return frames

    def load_assets(self):
        # Backgrounds
        self.char_backgrounds = [self.load_image(f) for f in self.char_bg_files]
        for i in range(len(self.char_backgrounds)):
            if self.char_backgrounds[i]:
                self.char_backgrounds[i] = pygame.transform.scale(
                    self.char_backgrounds[i], (self.virtual_width, self.virtual_height)
                )
        self.mode_backgrounds = [self.load_image(f) for f in self.mode_bg_files]
        for i in range(len(self.mode_backgrounds)):
            if self.mode_backgrounds[i]:
                self.mode_backgrounds[i] = pygame.transform.scale(
                    self.mode_backgrounds[i], (self.virtual_width, self.virtual_height)
                )
        # Game backgrounds - load all ddd backgrounds
        self.game_background = self.load_image("ddd.jpg")
        if self.game_background:
            self.game_background = pygame.transform.scale(
                self.game_background, (self.virtual_width, self.virtual_height)
            )
        # Also load ddd jpg list for score 150-249
        self.ddd_backgrounds = []
        for f in ["ddd.jpg", "ddd1.jpg", "ddd2.jpg", "ddd3.jpg"]:
            img = self.load_image(f)
            if img:
                self.ddd_backgrounds.append(pygame.transform.scale(img, (self.virtual_width, self.virtual_height)))
        # Also load anu backgrounds for score 0-149
        self.anu_backgrounds = []
        for f in ["anu.jpg", "anu1.jpg", "anu2.jpg"]:
            img = self.load_image(f)
            if img:
                self.anu_backgrounds.append(pygame.transform.scale(img, (self.virtual_width, self.virtual_height)))
        # Pick random anu background for game start
        if self.anu_backgrounds:
            self.current_anu_bg = random.choice(self.anu_backgrounds)
        self.toy_background = self.load_image("toy.jpg")
        if self.toy_background:
            self.toy_background = pygame.transform.scale(
                self.toy_background, (self.virtual_width, self.virtual_height)
            )
        self.blood_background = self.load_image("blood.jpg")
        if self.blood_background:
            self.blood_background = pygame.transform.scale(
                self.blood_background, (self.virtual_width, self.virtual_height)
            )
        # Images
        self.game_over_image = self.load_image("q.png")
        if self.game_over_image:
            self.game_over_image.set_alpha(0)
        self.obstacle_texture = self.load_image("w.png")
        self.screamer_image = self.load_image("screamer.png")
        if self.screamer_image:
            self.screamer_image = pygame.transform.scale(
                self.screamer_image, (self.virtual_width // 2, self.virtual_height // 2)
            )
        self.wing_image = self.load_image("wing.png")
        if self.wing_image:
            self.wing_image = pygame.transform.scale(
                self.wing_image, (PLAYER_SIZE, PLAYER_SIZE)
            )
        self.heart_image = self.load_image("heart.png")
        if self.heart_image:
            self.heart_image = pygame.transform.scale(
                self.heart_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.shield_image = self.load_image("shield.png")
        if self.shield_image:
            self.shield_image = pygame.transform.scale(
                self.shield_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.spike_texture = self.load_image("spike.jpg")
        self.points_image = self.load_image("points.png")
        if self.points_image:
            self.points_image = pygame.transform.scale(
                self.points_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.slow_image = self.load_image("slow.png")
        if self.slow_image:
            self.slow_image = pygame.transform.scale(
                self.slow_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.invincibility_image = self.load_image("invincibility.png")
        if self.invincibility_image:
            self.invincibility_image = pygame.transform.scale(
                self.invincibility_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.monster_frames = self.load_gif_frames(
            "monster.gif", (BONUS_SIZE, BONUS_SIZE)
        )
        self.score_boost_image = (
            self.monster_frames[0]
            if self.monster_frames
            else self.load_image("score_boost.png")
        )
        if self.score_boost_image:
            self.score_boost_image = pygame.transform.scale(
                self.score_boost_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.laser_image = self.load_image("laser.png")
        if self.laser_image:
            self.laser_image = pygame.transform.scale(
                self.laser_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.fire_buff_image = self.load_image("igl.png")
        if self.fire_buff_image:
            self.fire_buff_image = pygame.transform.scale(
                self.fire_buff_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.fire_animation_image = self.load_image("fire.png")
        self.boss_image = self.load_image("angel.png")
        if self.boss_image:
            self.boss_image = pygame.transform.scale(
                self.boss_image, (BOSS_SIZE, BOSS_SIZE)
            )
        self.crest_frames = self.load_gif_frames("m.gif", (50, 50))
        self.crest_image = (
            self.crest_frames[0] if self.crest_frames else self.load_image("m.gif")
        )
        self.marihuana_frames = self.load_gif_frames(
            "marihuana.gif", (BONUS_SIZE, BONUS_SIZE)
        )
        self.csk_image = self.load_image("podmost.png")
        if self.csk_image:
            self.csk_image = pygame.transform.scale(self.csk_image, (50, 50))
        self.hop_image = self.load_image("hop.png")
        self.hoppe_image = self.load_image("hoppe.png")
        if self.hoppe_image:
            self.hoppe_image = pygame.transform.scale(
                self.hoppe_image, (self.virtual_width, self.virtual_height)
            )
        self.wau_image = self.load_image("wau.png")
        self.zxc_image = self.load_image("zxc.png")
        self.ricc_image = self.load_image("ricc.png")
        self.dadep_image = self.load_image("dadep.png")
        self.zvb_image = self.load_image("zvb.png")
        self.volume_icon = self.load_image("gjk.png")
        if self.volume_icon:
            self.volume_icon = pygame.transform.scale(self.volume_icon, (100, 100))
        self.load_custom_icon = self.load_image("bnm.jpg")
        if self.load_custom_icon:
            self.load_custom_icon = pygame.transform.scale(
                self.load_custom_icon, (100, 100)
            )
        self.help_icon = self.load_image("ggl.png")
        if self.help_icon:
            self.help_icon = pygame.transform.scale(self.help_icon, (240, 200))
        self.help_background = self.load_image("ggl1.jpg")
        if self.help_background:
            self.help_background = pygame.transform.scale(
                self.help_background, (self.virtual_width, self.virtual_height)
            )
        self.trap_image = self.load_image("lovushk.png")
        self.secret_image = self.load_image("secret.png")
        self.sf_background = self.load_image("sf4.jpg")
        if self.sf_background:
            self.sf_background = pygame.transform.scale(
                self.sf_background, (self.virtual_width, self.virtual_height)
            )
        self.sf1_image = self.load_image("sf1.png")
        self.sf2_image = self.load_image("sf2.png")
        self.tron_image = self.load_image("tron.png")
        self.sasha_image = self.load_image("sasha.png")
        if self.sasha_image:
            self.sasha_image = pygame.transform.scale(
                self.sasha_image, (self.virtual_width, self.virtual_height)
            )
        npc_files = ["npc.jpg", "npc1.jpg", "npc2.jpg"]
        self.npc_backgrounds = [self.load_image(f) for f in npc_files]
        for i in range(len(self.npc_backgrounds)):
            if self.npc_backgrounds[i]:
                self.npc_backgrounds[i] = pygame.transform.scale(
                    self.npc_backgrounds[i], (self.virtual_width, self.virtual_height)
                )
        told_files = ["told.png", "told1.png"]
        self.told_images = [self.load_image(f) for f in told_files]
        self.dvd_image = self.load_image("dvd.png")
        if self.dvd_image:
            self.dvd_image = pygame.transform.scale(
                self.dvd_image, (BONUS_SIZE, BONUS_SIZE)
            )
        self.welcome_frames = self.load_gif_frames(
            "welcome.gif", (self.virtual_width, self.virtual_height)
        )
        fallback = self.load_image("welcome.jpg")
        if fallback:
            self.welcome_image = pygame.transform.scale(
                fallback, (self.virtual_width, self.virtual_height)
            )
        # Sounds
        self.death_sound = self.load_sound("dead.mp3")
        self.screamer_sound = self.load_sound("screamer.mp3")
        self.explosion_sound = self.load_sound("explosion.mp3")
        self.dr_sound = self.load_sound("dr.mp3")
        self.bonus_sound = self.load_sound("bonus.mp3")
        self.q_sound = self.load_sound("q.mp3")
        if self.q_sound:
            self.q_sound.set_volume(self.volume * 2.0)
        self.q1_sound = self.load_sound("q1.mp3")
        if self.q1_sound:
            self.q1_sound.set_volume(self.volume * 2.0)
        # load_skateboard_assets() removed

    def load_skateboard_assets(self):
        """Загрузи скейтборды из папки или создай стандартные"""
        self.skateboard_skins.clear()
        self.skateboard_images.clear()

        # Стандартные скейтборды по цветам
        skateboard_files = [
            "skateboard.png",
            "skateboard1.png",
            "skateboard2.png",
            "skateboard3.png",
            "skateboard4.png",
        ]

        for i, filename in enumerate(skateboard_files):
            image = self.load_image(filename)
            if image:
                image = pygame.transform.scale(
                    image, (SKATEBOARD_WIDTH, SKATEBOARD_HEIGHT)
                )
                self.skateboard_images.append(image)
                self.skateboard_skins.append(
                    {"name": f"Skateboard {i+1}", "image": image}
                )
            else:
                # Fallback: создай простой прямоугольник
                color = self.skateboard_default_colors[
                    i % len(self.skateboard_default_colors)
                ]
                self.skateboard_skins.append(
                    {"name": f"Skateboard {i+1}", "color": color, "image": None}
                )
                self.skateboard_images.append(None)

    def load_sound(self, file):
        try:
            sound = pygame.mixer.Sound(file)
            sound.set_volume(self.volume)
            return sound
        except Exception as e:
            print(f"Warning: Could not load sound {file}: {e}")
            return None

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def load_characters(self):
        self.CHARACTERS.clear()
        images = ["eee.jpg", "www.jpg"]
        colors = [(255, 0, 0), (0, 0, 255)]
        styles = ["filled", "outlined"]
        for i, img in enumerate(images):
            char = {"name": f"brawler{i+1}"}
            image = self.load_image(img)
            if image:
                image = pygame.transform.scale(image, (150, 150))
                char["image"] = image
            else:
                char["style"] = styles[i]
                char["color"] = colors[i]
            self.CHARACTERS.append(char)

    def load_custom_image(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.png *.gif")]
        )
        if file_path:
            try:
                image = pygame.image.load(file_path)
                image = pygame.transform.scale(image, (150, 150))
                self.CHARACTERS = [
                    c for c in self.CHARACTERS if c.get("name") != "Custom"
                ]
                self.CHARACTERS.append({"name": "Custom", "image": image})
                self.load_custom_icon = pygame.transform.scale(image, (100, 100))
                self.custom_loaded = True
            except Exception as e:
                print(f"Warning: Could not load custom image {file_path}: {e}")
        root.destroy()

    def play_music(self, filename):
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

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None

    def load_music(self):
        self.play_music("rr.mp3")

    def set_all_volumes(self):
        pygame.mixer.music.set_volume(self.volume)
        for sound in [
            self.death_sound,
            self.screamer_sound,
            self.explosion_sound,
            self.dr_sound,
            self.bonus_sound,
        ]:
            if sound:
                sound.set_volume(self.volume)
        for sound in [self.q_sound, self.q1_sound]:
            if sound:
                sound.set_volume(self.volume * 2.0)

    def adjust_volume(self, delta):
        self.volume = max(0.0, min(1.0, self.volume + delta))
        self.set_all_volumes()

    def get_shimmer_color(self, t):
        r = int(127 + 127 * math.sin(t * 0.05))
        g = int(127 + 127 * math.sin(t * 0.05 + 2))
        b = int(127 + 127 * math.sin(t * 0.05 + 4))
        return (r, g, b)

    def get_animated_frame(self, frames, timer, fps):
        if frames and len(frames) > 0:
            return frames[(timer // (FPS // fps)) % len(frames)]
        return None

    def spawn_rain(self):
        if len(self.rain_particles) < 100:
            x = random.randint(0, self.virtual_width)
            y = random.randint(-self.virtual_height, 0)
            speed = random.randint(10, 20)
            self.rain_particles.append([x, y, speed])

    def update_rain(self, slowdown_factor):
        for particle in self.rain_particles[:]:
            particle[1] += particle[2] * slowdown_factor
            if particle[1] > self.virtual_height:
                self.rain_particles.remove(particle)
                particle[0] = random.randint(0, self.virtual_width)
                particle[1] = random.randint(-self.virtual_height, 0)
                particle[2] = random.randint(10, 20)
                self.rain_particles.append(particle)
        # Limit particles to prevent accumulation
        if len(self.rain_particles) > 200:
            self.rain_particles = self.rain_particles[-200:]

    def draw_rain(self, shake_x, shake_y):
        for particle in self.rain_particles:
            pygame.draw.line(
                self.virtual_screen,
                (100, 150, 255),
                (particle[0] + shake_x, particle[1] + shake_y),
                (particle[0] + shake_x, particle[1] + 10 + shake_y),
                2,
            )

    def spawn_splash(self, x, y):
        if RAIN_THRESHOLD <= self.score < 200:
            for _ in range(10):
                angle = random.uniform(0, math.pi)
                speed = random.uniform(5, 10)
                vx = math.cos(angle) * speed
                vy = -math.sin(angle) * speed
                lifetime = random.randint(20, 40)
                self.splash_particles.append([x, y, vx, vy, lifetime])

    def update_splash(self, slowdown_factor):
        for particle in self.splash_particles[:]:
            particle[0] += particle[2] * slowdown_factor
            particle[1] += particle[3] * slowdown_factor
            particle[3] += 0.5 * slowdown_factor
            particle[4] -= 1
            if particle[4] <= 0 or particle[1] > self.virtual_height:
                self.splash_particles.remove(particle)
        # Limit particles
        if len(self.splash_particles) > 200:
            self.splash_particles = self.splash_particles[-200:]

    def draw_splash(self, shake_x, shake_y):
        for particle in self.splash_particles:
            alpha = int(255 * (particle[4] / 40))
            pygame.draw.circle(
                self.virtual_screen,
                (100, 150, 255, alpha),
                (int(particle[0] + shake_x), int(particle[1] + shake_y)),
                3,
            )

    def spawn_buff_particles(self, x, y, buff_type, num_particles=10):
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
        color = colors.get(buff_type, (255, 255, 255))
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.randint(40, 80)
            self.buff_particles.append([x, y, vx, vy, lifetime, color])

    def update_buff_particles(self, slowdown_factor):
        for particle in self.buff_particles[:]:
            particle[0] += particle[2] * slowdown_factor
            particle[1] += particle[3] * slowdown_factor
            particle[4] -= 1
            if particle[4] <= 0:
                self.buff_particles.remove(particle)
        # Limit particles
        if len(self.buff_particles) > 500:
            self.buff_particles = self.buff_particles[-500:]

    def draw_buff_particles(self, shake_x, shake_y):
        for particle in self.buff_particles:
            alpha = int(255 * (particle[4] / 80))
            pygame.draw.circle(
                self.virtual_screen,
                (*particle[5], alpha),
                (int(particle[0] + shake_x), int(particle[1] + shake_y)),
                4,
            )

    def draw_buff_glow(self, x, y, size):
        glow_radius = int(size * 1.05)
        glow_alpha = int(100 + 50 * math.sin(self.animation_timer * 0.3))
        glow_color = (255, 255, 0, glow_alpha)
        glow_surface = pygame.Surface(
            (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            glow_surface, glow_color, (glow_radius, glow_radius), glow_radius, 2
        )
        self.virtual_screen.blit(
            glow_surface, (x - glow_radius + size // 2, y - glow_radius + size // 2)
        )

    def trigger_milestone_effect(self):
        self.milestone_flash = MILESTONE_FLASH_DURATION
        self.milestone_text_timer = MILESTONE_TEXT_DURATION
        self.current_milestone = self.score // MILESTONE_INTERVAL * MILESTONE_INTERVAL
        for _ in range(30):
            x = random.randint(0, self.virtual_width)
            y = random.randint(0, self.virtual_height)
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            lifetime = random.randint(40, 80)
            color = self.get_shimmer_color(self.animation_timer)
            self.buff_particles.append([x, y, vx, vy, lifetime, color])
        self.player1_shield_active = True
        self.player1_shield_timer = SHIELD_DURATION
        if self.coop_mode:
            self.player2_shield_active = True
            self.player2_shield_timer = SHIELD_DURATION

    def draw_milestone_flash(self, shake_x, shake_y):
        if self.milestone_flash > 0:
            flash_alpha = int(100 * (self.milestone_flash / MILESTONE_FLASH_DURATION))
            flash_surface = pygame.Surface(
                (self.virtual_width, self.virtual_height), pygame.SRCALPHA
            )
            flash_surface.fill((255, 255, 200, flash_alpha))
            self.virtual_screen.blit(flash_surface, (shake_x, shake_y))
            self.milestone_flash -= 1
        if self.milestone_text_timer > 0:
            alpha = int(
                255
                * min(self.milestone_text_timer / (MILESTONE_TEXT_DURATION / 2), 1.0)
            )
            if self.milestone_text_timer < MILESTONE_TEXT_DURATION / 2:
                alpha = int(
                    255 * (self.milestone_text_timer / (MILESTONE_TEXT_DURATION / 2))
                )
            text = self.title_font.render(
                str(self.current_milestone),
                True,
                (*self.get_shimmer_color(self.animation_timer), alpha),
            )
            scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2)
            scaled_text = pygame.transform.scale(
                text, (int(text.get_width() * scale), int(text.get_height() * scale))
            )
            self.virtual_screen.blit(
                scaled_text,
                (
                    self.virtual_width // 2 - scaled_text.get_width() // 2 + shake_x,
                    self.virtual_height // 2 - scaled_text.get_height() // 2 + shake_y,
                ),
            )
            self.milestone_text_timer -= 1

    def trigger_difficulty_increase(self):
        self.difficulty_text_timer = DIFFICULTY_TEXT_DURATION
        self.current_difficulty_level = self.score // DIFFICULTY_THRESHOLD
        for _ in range(20):
            x = random.randint(0, self.virtual_width)
            y = random.randint(0, self.virtual_height)
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            lifetime = random.randint(30, 60)
            color = (255, 100, 100)
            self.buff_particles.append([x, y, vx, vy, lifetime, color])

    def draw_difficulty_text(self, shake_x, shake_y):
        if self.difficulty_text_timer > 0:
            alpha = int(
                255
                * min(self.difficulty_text_timer / (DIFFICULTY_TEXT_DURATION / 2), 1.0)
            )
            if self.difficulty_text_timer < DIFFICULTY_TEXT_DURATION / 2:
                alpha = int(
                    255 * (self.difficulty_text_timer / (DIFFICULTY_TEXT_DURATION / 2))
                )
            text = self.title_font.render(
                f"Уровень сложности {self.current_difficulty_level}",
                True,
                (*self.get_shimmer_color(self.animation_timer), alpha),
            )
            scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2)
            scaled_text = pygame.transform.scale(
                text, (int(text.get_width() * scale), int(text.get_height() * scale))
            )
            self.virtual_screen.blit(
                scaled_text,
                (
                    self.virtual_width // 2 - scaled_text.get_width() // 2 + shake_x,
                    self.virtual_height // 2 + 50 + shake_y,
                ),
            )
            self.difficulty_text_timer -= 1

    def trigger_screamer(self):
        self.screamer_flash = SCREAMER_DURATION
        if self.screamer_sound:
            self.screamer_sound.play()
        self.screamer_timer = 0

    def draw_screamer(self, shake_x, shake_y):
        if self.screamer_flash > 0:
            if self.screamer_image:
                alpha = int(
                    255 * min(self.screamer_flash / (SCREAMER_DURATION / 2), 1.0)
                )
                if self.screamer_flash < SCREAMER_DURATION / 2:
                    alpha = int(255 * (self.screamer_flash / (SCREAMER_DURATION / 2)))
                scaled_image = pygame.transform.scale(
                    self.screamer_image,
                    (
                        int(
                            self.virtual_width
                            // 2
                            * (1 + 0.2 * math.sin(self.animation_timer * 0.3))
                        ),
                        int(
                            self.virtual_height
                            // 2
                            * (1 + 0.2 * math.sin(self.animation_timer * 0.3))
                        ),
                    ),
                )
                self.virtual_screen.blit(
                    scaled_image,
                    (
                        self.virtual_width // 2
                        - scaled_image.get_width() // 2
                        + shake_x,
                        self.virtual_height // 2
                        - scaled_image.get_height() // 2
                        + shake_y,
                    ),
                )
            else:
                flash_alpha = int(
                    255 * min(self.screamer_flash / (SCREAMER_DURATION / 2), 1.0)
                )
                if self.screamer_flash < SCREAMER_DURATION / 2:
                    flash_alpha = int(
                        255 * (self.screamer_flash / (SCREAMER_DURATION / 2))
                    )
                flash_surface = pygame.Surface(
                    (self.virtual_width, self.virtual_height), pygame.SRCALPHA
                )
                flash_surface.fill((255, 0, 0, flash_alpha))
                self.virtual_screen.blit(flash_surface, (shake_x, shake_y))
                text = self.title_font.render(
                    "SCREAMER!", True, (255, 255, 255, flash_alpha)
                )
                scale = 1.0 + 0.2 * math.sin(self.animation_timer * 0.3)
                scaled_text = pygame.transform.scale(
                    text,
                    (int(text.get_width() * scale), int(text.get_height() * scale)),
                )
                self.virtual_screen.blit(
                    scaled_text,
                    (
                        self.virtual_width // 2
                        - scaled_text.get_width() // 2
                        + shake_x,
                        self.virtual_height // 2
                        - scaled_text.get_height() // 2
                        + shake_y,
                    ),
                )
            self.screamer_flash -= 1

    def trigger_lightning(self):
        self.lightning_flash = 30

    def draw_lightning(self, shake_x, shake_y):
        if self.lightning_flash > 0:
            flash_alpha = int(255 * (self.lightning_flash / 30))
            flash_surface = pygame.Surface(
                (self.virtual_width, self.virtual_height), pygame.SRCALPHA
            )
            flash_surface.fill((255, 255, 255, flash_alpha))
            self.virtual_screen.blit(flash_surface, (shake_x, shake_y))
            self.lightning_flash -= 1

    def draw_stars(self, slowdown_factor, shake_x, shake_y):
        for star in self.stars:
            brightness = int(200 * (star[2] / 3))
            pygame.draw.circle(
                self.virtual_screen,
                (brightness, brightness, brightness),
                (int(star[0] + shake_x), int(star[1] + shake_y)),
                star[2],
            )
            star[0] += star[2] * 0.05 * slowdown_factor
            if star[0] > self.virtual_width:
                star[0] = 0
                star[1] = random.randint(0, self.virtual_height)

    def draw_sun_and_rays(self, shake_x, shake_y):
        if self.score < SUN_THRESHOLD:
            sun_radius = 50
            sun_x, sun_y = self.virtual_width - 100 + shake_x, 100 + shake_y
            pygame.draw.circle(
                self.virtual_screen, (255, 255, 100), (sun_x, sun_y), sun_radius
            )
            for i in range(12):
                angle = math.radians(i * 30 + self.animation_timer * 1)
                ray_length = 80 + 10 * math.sin(self.animation_timer * 0.05)
                end_x = sun_x + math.cos(angle) * ray_length
                end_y = sun_y + math.sin(angle) * ray_length
                pygame.draw.line(
                    self.virtual_screen,
                    (255, 255, 100),
                    (sun_x, sun_y),
                    (end_x, end_y),
                    3,
                )

    def draw_halo(self, x, y, shake_x, shake_y):
        halo_radius = 30
        halo_alpha = int(127 + 127 * math.sin(self.animation_timer * 0.1))
        halo_surface = pygame.Surface(
            (halo_radius * 2, halo_radius * 2), pygame.SRCALPHA
        )
        pygame.draw.circle(
            halo_surface,
            (255, 255, 200, halo_alpha),
            (halo_radius, halo_radius),
            halo_radius,
            2,
        )
        self.virtual_screen.blit(
            halo_surface,
            (
                x - halo_radius + PLAYER_SIZE // 2 + shake_x,
                y - halo_radius - 20 + shake_y,
            ),
        )

    def draw_wings(self, x, y, shake_x, shake_y):
        if self.is_angel:
            wing_angle = 30 * math.sin(self.wing_flap_timer * WING_FLAP_SPEED)
            wing_scale = 1.0 + 0.1 * math.sin(self.wing_flap_timer * WING_FLAP_SPEED)
            if self.wing_image:
                left_wing = pygame.transform.scale(
                    self.wing_image,
                    (int(PLAYER_SIZE * wing_scale), int(PLAYER_SIZE * wing_scale)),
                )
                left_wing = pygame.transform.rotate(left_wing, wing_angle)
                self.virtual_screen.blit(
                    left_wing,
                    (x - PLAYER_SIZE // 2 + shake_x, y - PLAYER_SIZE // 4 + shake_y),
                )
                right_wing = pygame.transform.scale(
                    self.wing_image,
                    (int(PLAYER_SIZE * wing_scale), int(PLAYER_SIZE * wing_scale)),
                )
                right_wing = pygame.transform.flip(right_wing, True, False)
                right_wing = pygame.transform.rotate(right_wing, -wing_angle)
                self.virtual_screen.blit(
                    right_wing,
                    (x + PLAYER_SIZE // 2 + shake_x, y - PLAYER_SIZE // 4 + shake_y),
                )

    def draw_marihuana_mini(self, x, y, shake_x, shake_y):
        if self.marihuana_active:
            frame = self.get_animated_frame(
                self.marihuana_frames, self.marihuana_anim_timer, MARIHUANA_ANIM_FPS
            )
            if frame:
                mini_size = 30
                scaled_mini = pygame.transform.scale(frame, (mini_size, mini_size))
                self.virtual_screen.blit(
                    scaled_mini,
                    (x + PLAYER_SIZE // 2 - mini_size // 2 + shake_x, y - 40 + shake_y),
                )

    def draw_lives(self, shake_x, shake_y):
        heart_size = 50
        # Player 1
        for i in range(self.player1_lives):
            x = 10 + i * (heart_size + 10) + shake_x
            y = 70 + shake_y
            scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2 + i)
            scaled_size = int(heart_size * scale)
            scaled_x = x - (scaled_size - heart_size) // 2
            scaled_y = y - (scaled_size - heart_size) // 2
            if self.heart_image:
                scaled_heart = pygame.transform.scale(
                    self.heart_image, (scaled_size, scaled_size)
                )
                self.virtual_screen.blit(scaled_heart, (scaled_x, scaled_y))
            else:
                points = [
                    (scaled_x + scaled_size // 2, scaled_y + scaled_size // 4),
                    (scaled_x, scaled_y + scaled_size // 2),
                    (scaled_x + scaled_size // 4, scaled_y + scaled_size),
                    (scaled_x + scaled_size // 2, scaled_y + scaled_size // 2),
                    (scaled_x + 3 * scaled_size // 4, scaled_y + scaled_size),
                    (scaled_x + scaled_size, scaled_y + scaled_size // 2),
                    (scaled_x + scaled_size // 2, scaled_y + scaled_size // 4),
                ]
                pygame.draw.polygon(self.virtual_screen, (255, 0, 0), points)
        # Player 2
        if self.coop_mode:
            for i in range(self.player2_lives):
                x = self.virtual_width - 10 - (i + 1) * (heart_size + 10) + shake_x
                y = 70 + shake_y
                scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2 + i + 10)
                scaled_size = int(heart_size * scale)
                scaled_x = x - (scaled_size - heart_size) // 2
                scaled_y = y - (scaled_size - heart_size) // 2
                if self.heart_image:
                    scaled_heart = pygame.transform.scale(
                        self.heart_image, (scaled_size, scaled_size)
                    )
                    self.virtual_screen.blit(scaled_heart, (scaled_x, scaled_y))
                else:
                    points = [
                        (scaled_x + scaled_size // 2, scaled_y + scaled_size // 4),
                        (scaled_x, scaled_y + scaled_size // 2),
                        (scaled_x + scaled_size // 4, scaled_y + scaled_size),
                        (scaled_x + scaled_size // 2, scaled_y + scaled_size // 2),
                        (scaled_x + 3 * scaled_size // 4, scaled_y + scaled_size),
                        (scaled_x + scaled_size, scaled_y + scaled_size // 2),
                        (scaled_x + scaled_size // 2, scaled_y + scaled_size // 4),
                    ]
                    pygame.draw.polygon(self.virtual_screen, (255, 0, 0), points)

    def draw_bonus_indicator(self, shake_x, shake_y):
        y_offset = 10 + shake_y
        if self.bonus_timer > 0:
            remaining_time = self.bonus_timer / FPS
            text = ""
            color = (255, 255, 255)
            if self.double_points:
                text = f"Двойные очки: {remaining_time:.1f}с"
                color = (255, 215, 0)
            elif self.slow_down:
                text = f"Подмост: {remaining_time:.1f}с"
                color = (0, 191, 255)
            elif self.laser_active:
                text = f"Бримстоун: {remaining_time:.1f}с"
                color = (255, 0, 0)
            elif self.score_multiplier > 1:
                text = (
                    f"Множитель очков: x{self.score_multiplier} ({remaining_time:.1f}с)"
                )
                color = (255, 255, 0)
            if text:
                bonus_text = self.font.render(text, True, color)
                self.virtual_screen.blit(
                    bonus_text,
                    (
                        self.virtual_width - bonus_text.get_width() - 10 + shake_x,
                        y_offset,
                    ),
                )
                y_offset += 40
        # Shields
        if self.player1_shield_active and self.player1_shield_timer > 0:
            remaining_time = self.player1_shield_timer / FPS
            text = f"Щит P1: {remaining_time:.1f}с"
            color = (128, 128, 255)
            bonus_text = self.font.render(text, True, color)
            self.virtual_screen.blit(
                bonus_text,
                (self.virtual_width - bonus_text.get_width() - 10 + shake_x, y_offset),
            )
            y_offset += 40
        if (
            self.coop_mode
            and self.player2_shield_active
            and self.player2_shield_timer > 0
        ):
            remaining_time = self.player2_shield_timer / FPS
            text = f"Щит P2: {remaining_time:.1f}с"
            color = (128, 128, 255)
            bonus_text = self.font.render(text, True, color)
            self.virtual_screen.blit(
                bonus_text,
                (self.virtual_width - bonus_text.get_width() - 10 + shake_x, y_offset),
            )
            y_offset += 40
        if self.fire_active and self.fire_timer > 0:
            remaining_time = self.fire_timer / FPS
            text = f"Огонь: {remaining_time:.1f}с"
            color = (255, 69, 0)
            bonus_text = self.font.render(text, True, color)
            self.virtual_screen.blit(
                bonus_text,
                (self.virtual_width - bonus_text.get_width() - 10 + shake_x, y_offset),
            )
            y_offset += 40
        if self.dvd_active and self.dvd_timer > 0:
            remaining_time = self.dvd_timer / FPS
            text = f"DVD: {remaining_time:.1f}с"
            color = (255, 0, 255)
            bonus_text = self.font.render(text, True, color)
            self.virtual_screen.blit(
                bonus_text,
                (self.virtual_width - bonus_text.get_width() - 10 + shake_x, y_offset),
            )
            y_offset += 40
        if self.marihuana_active and self.marihuana_timer > 0:
            remaining_time = self.marihuana_timer / FPS
            text = f"Marihuana: {remaining_time:.1f}с"
            color = (0, 255, 0)
            bonus_text = self.font.render(text, True, color)
            self.virtual_screen.blit(
                bonus_text,
                (self.virtual_width - bonus_text.get_width() - 10 + shake_x, y_offset),
            )

    def draw_bonus_notification(self, shake_x, shake_y):
        if self.bonus_notification and self.bonus_notification_timer > 0:
            alpha = int(
                255
                * min(
                    self.bonus_notification_timer / (BONUS_NOTIFICATION_DURATION / 2),
                    1.0,
                )
            )
            if self.bonus_notification_timer < BONUS_NOTIFICATION_DURATION / 2:
                alpha = int(
                    255
                    * (
                        self.bonus_notification_timer
                        / (BONUS_NOTIFICATION_DURATION / 2)
                    )
                )
            text = self.font.render(
                self.bonus_notification, True, (255, 255, 255, alpha)
            )
            scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2)
            scaled_text = pygame.transform.scale(
                text, (int(text.get_width() * scale), int(text.get_height() * scale))
            )
            self.virtual_screen.blit(
                scaled_text,
                (
                    self.virtual_width // 2 - scaled_text.get_width() // 2 + shake_x,
                    self.virtual_height // 4 + shake_y,
                ),
            )
            self.bonus_notification_timer -= 1

    def draw_button(
        self,
        text,
        x,
        y,
        w,
        h,
        color,
        hover_color,
        text_color,
        clicked=False,
        hover_scale=1.0,
    ):
        mouse_pos = self.get_scaled_mouse_pos()
        button_rect = pygame.Rect(x, y, w, h)
        is_hovered = button_rect.collidepoint(mouse_pos)
        current_color = list(color)
        target_color = list(hover_color) if is_hovered else list(color)
        for i in range(3):
            current_color[i] = (
                current_color[i] + (target_color[i] - current_color[i]) * 0.3
            )
        scale = 0.92 if clicked else (1.05 if is_hovered else 1.0) * hover_scale
        scaled_w, scaled_h = int(w * scale), int(h * scale)
        scaled_x, scaled_y = x + (w - scaled_w) // 2, y + (h - scaled_h) // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_w, scaled_h)
        shadow_color = (50, 50, 50, 150)
        shadow_rect = pygame.Rect(scaled_x + 5, scaled_y + 5, scaled_w, scaled_h)
        pygame.draw.rect(
            self.virtual_screen, shadow_color, shadow_rect, border_radius=15
        )
        gradient_surface = pygame.Surface((scaled_w, scaled_h))
        for i in range(scaled_h):
            t = i / scaled_h
            r = int(current_color[0] * (1 - t) + hover_color[0] * t)
            g = int(current_color[1] * (1 - t) + hover_color[1] * t)
            b = int(current_color[2] * (1 - t) + hover_color[2] * t)
            pygame.draw.line(gradient_surface, (r, g, b), (0, i), (scaled_w, i))
        gradient_surface.set_alpha(200)
        self.virtual_screen.blit(gradient_surface, (scaled_x, scaled_y))
        pygame.draw.rect(
            self.virtual_screen, (255, 255, 255), scaled_rect, 2, border_radius=15
        )
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=scaled_rect.center)
        self.virtual_screen.blit(text_surf, text_rect)
        return button_rect

    def draw_volume_controls(self, x, y):
        volume_text = self.font.render(
            f"Громкость: {int(self.volume * 100)}%", True, (255, 255, 255)
        )
        self.virtual_screen.blit(volume_text, (x - volume_text.get_width() - 10, y))
        vol_up_button = self.draw_button(
            "+",
            x - 110,
            y + 30,
            50,
            40,
            (100, 255, 100),
            (150, 255, 150),
            (255, 255, 255),
        )
        vol_down_button = self.draw_button(
            "-",
            x - 50,
            y + 30,
            50,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
        )
        if self.volume_icon:
            self.virtual_screen.blit(self.volume_icon, (x - 80, y + 80))
        return vol_up_button, vol_down_button

    def update_background_transition(
        self,
        current_index,
        next_index,
        timer,
        switch_interval,
        transition_timer,
        transition_alpha,
        backgrounds,
    ):
        timer += 1
        if timer >= switch_interval:
            next_index = (current_index + 1) % len(backgrounds)
            transition_timer = TRANSITION_DURATION
            transition_alpha = 0
            timer = 0
        if transition_timer > 0:
            transition_alpha = int(255 * (1 - (transition_timer / TRANSITION_DURATION)))
            transition_timer -= 1
            if transition_timer <= 0:
                current_index = next_index
                transition_alpha = 0
        return current_index, next_index, timer, transition_timer, transition_alpha

    def draw_background_transition(
        self, backgrounds, current_index, next_index, transition_alpha
    ):
        current_bg = backgrounds[current_index]
        if current_bg:
            self.virtual_screen.blit(current_bg, (0, 0))
        if transition_alpha > 0:
            next_bg = backgrounds[next_index]
            if next_bg:
                transition_surface = pygame.Surface(
                    (self.virtual_width, self.virtual_height), pygame.SRCALPHA
                )
                transition_surface.blit(next_bg, (0, 0))
                transition_surface.set_alpha(transition_alpha)
                self.virtual_screen.blit(transition_surface, (0, 0))

    def draw_welcome(self):
        self.play_music("rr.mp3")
        self.virtual_screen.fill((0, 0, 0))
        frame = self.get_animated_frame(
            self.welcome_frames, self.welcome_frame_timer, self.welcome_fps
        )
        if frame:
            self.virtual_screen.blit(frame, (0, 0))
            self.welcome_frame_timer += 1
        elif self.welcome_image:
            self.virtual_screen.blit(self.welcome_image, (0, 0))
        self.draw_stars(1.0, 0, 0)
        self.draw_button(
            "Начать игру",
            self.virtual_width // 2 - 100,
            self.virtual_height - 60,
            200,
            50,
            (100, 255, 100),
            (150, 255, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 - 50,
            self.virtual_height - 10,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        return pygame.Rect(
            self.virtual_width // 2 - 100, self.virtual_height - 60, 200, 50
        ), pygame.Rect(self.virtual_width // 2 - 50, self.virtual_height - 10, 100, 40)

    def draw_character_select(self):
        self.play_music("rr.mp3")
        (
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.char_transition_timer,
            self.char_transition_alpha,
        ) = self.update_background_transition(
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.CHAR_BACKGROUND_SWITCH_INTERVAL,
            self.char_transition_timer,
            self.char_transition_alpha,
            self.char_backgrounds,
        )
        self.draw_background_transition(
            self.char_backgrounds,
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)
        title = self.title_font.render(
            "Выберите персонажа", True, self.get_shimmer_color(self.animation_timer)
        )
        title_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * title_scale),
                int(title.get_height() * title_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_title,
            (
                self.virtual_width // 2 - scaled_title.get_width() // 2,
                50 - scaled_title.get_height() // 2,
            ),
        )
        char_rects = []
        num_chars = len(self.CHARACTERS)
        for i in range(3):
            x, y = 300 + i * 250, 200
            scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05 + i)
            scaled_w, scaled_h = int(150 * scale), int(150 * scale)
            scaled_x, scaled_y = x + (150 - scaled_w) // 2, y + (150 - scaled_h) // 2
            if i < num_chars:
                char = self.CHARACTERS[i]
                if "image" in char:
                    scaled_image = pygame.transform.scale(
                        char["image"], (scaled_w, scaled_h)
                    )
                    self.virtual_screen.blit(scaled_image, (scaled_x, scaled_y))
                elif char.get("style") == "filled":
                    pygame.draw.rect(
                        self.virtual_screen,
                        char["color"],
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                    )
                elif char.get("style") == "outlined":
                    pygame.draw.rect(
                        self.virtual_screen,
                        char["color"],
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                        5,
                    )
                name = self.font.render(char["name"], True, (255, 255, 255))
                self.virtual_screen.blit(name, (x, y + 170))
                char_rects.append(pygame.Rect(x - 25, y - 25, 200, 200))
            else:
                if self.load_custom_icon:
                    scaled_image = pygame.transform.scale(
                        self.load_custom_icon, (scaled_w, scaled_h)
                    )
                    self.virtual_screen.blit(scaled_image, (scaled_x, scaled_y))
                else:
                    pygame.draw.rect(
                        self.virtual_screen,
                        (100, 100, 100),
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                    )
                name = self.font.render("Custom", True, (255, 255, 255))
                self.virtual_screen.blit(name, (x, y + 170))
                char_rects.append(pygame.Rect(x - 25, y - 25, 200, 200))
        load_custom_button = self.draw_button(
            "Загрузить",
            self.virtual_width // 2 - 100,
            450,
            200,
            50,
            (100, 150, 255),
            (150, 200, 255),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        controls_button = self.draw_button(
            "Управление",
            self.virtual_width // 2 - 100,
            510,
            200,
            50,
            (100, 150, 255),
            (150, 200, 255),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        vol_up, vol_down = self.draw_volume_controls(self.virtual_width, 10)
        if self.help_icon:
            self.virtual_screen.blit(
                self.help_icon,
                (10, self.virtual_height - self.help_icon.get_height() - 10),
            )
        self.animation_timer += 1
        return (
            char_rects,
            load_custom_button,
            controls_button,
            exit_button,
            vol_up,
            vol_down,
        )

    def draw_controls(self):
        self.play_music("rr.mp3")
        (
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.char_transition_timer,
            self.char_transition_alpha,
        ) = self.update_background_transition(
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.CHAR_BACKGROUND_SWITCH_INTERVAL,
            self.char_transition_timer,
            self.char_transition_alpha,
            self.char_backgrounds,
        )
        self.draw_background_transition(
            self.char_backgrounds,
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)
        title = self.title_font.render(
            "Настройки управления", True, self.get_shimmer_color(self.animation_timer)
        )
        title_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * title_scale),
                int(title.get_height() * title_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_title,
            (
                self.virtual_width // 2 - scaled_title.get_width() // 2,
                50 - scaled_title.get_height() // 2 + self.controls_scroll_offset,
            ),
        )
        y = 120 + self.controls_scroll_offset
        actions = ["left", "right", "jump", "crouch"]
        action_names = {
            "left": "Влево",
            "right": "Вправо",
            "jump": "Прыжок",
            "crouch": "Присесть",
        }
        # Player 1
        p1_header = self.font.render("Игрок 1 (WASD)", True, (255, 100, 100))
        self.virtual_screen.blit(
            p1_header, (self.virtual_width // 2 - p1_header.get_width() // 2, y)
        )
        y += 50
        p1_rects = {}
        for action in actions:
            action_bg_rect = pygame.Rect(self.virtual_width // 2 - 250, y, 500, 50)
            pygame.draw.rect(
                self.virtual_screen, (50, 50, 50, 100), action_bg_rect, border_radius=10
            )
            action_text = self.small_font.render(
                action_names[action], True, (255, 255, 255)
            )
            key_text = self.font.render(
                pygame.key.name(self.keys_p1[action]),
                True,
                self.get_shimmer_color(self.animation_timer),
            )
            self.virtual_screen.blit(
                action_text, (self.virtual_width // 2 - 200, y + 10)
            )
            self.virtual_screen.blit(key_text, (self.virtual_width // 2 + 50, y + 5))
            remap_rect = self.draw_button(
                "Изменить",
                self.virtual_width // 2 + 150,
                y,
                150,
                40,
                (100, 150, 255),
                (150, 200, 255),
                (255, 255, 255),
                hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
            )
            p1_rects[action] = remap_rect
            y += 60
        # Player 2
        y += 20
        p2_header = self.font.render("Игрок 2 (Co-op, стрелки)", True, (100, 100, 255))
        self.virtual_screen.blit(
            p2_header, (self.virtual_width // 2 - p2_header.get_width() // 2, y)
        )
        y += 50
        p2_rects = {}
        for action in actions:
            action_bg_rect = pygame.Rect(self.virtual_width // 2 - 250, y, 500, 50)
            pygame.draw.rect(
                self.virtual_screen, (50, 50, 50, 100), action_bg_rect, border_radius=10
            )
            action_text = self.small_font.render(
                action_names[action], True, (255, 255, 255)
            )
            key_text = self.font.render(
                pygame.key.name(self.keys_p2[action]),
                True,
                self.get_shimmer_color(self.animation_timer),
            )
            self.virtual_screen.blit(
                action_text, (self.virtual_width // 2 - 200, y + 10)
            )
            self.virtual_screen.blit(key_text, (self.virtual_width // 2 + 50, y + 5))
            remap_rect = self.draw_button(
                "Изменить",
                self.virtual_width // 2 + 150,
                y,
                150,
                40,
                (100, 150, 255),
                (150, 200, 255),
                (255, 255, 255),
                hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
            )
            p2_rects[action] = remap_rect
            y += 60
        # Global
        y += 20
        global_header = self.font.render("Глобальные", True, (255, 255, 100))
        self.virtual_screen.blit(
            global_header, (self.virtual_width // 2 - global_header.get_width() // 2, y)
        )
        y += 50
        global_text = self.small_font.render(
            "P / Escape: Пауза | F11: Полный экран", True, (200, 200, 200)
        )
        self.virtual_screen.blit(
            global_text, (self.virtual_width // 2 - global_text.get_width() // 2, y)
        )
        y += 100  # Extra space for total height
        total_content_height = y + 100
        max_scroll_offset = max(0, -(total_content_height - self.virtual_height))
        self.controls_scroll_offset = min(
            0, max(self.controls_scroll_offset, -max_scroll_offset)
        )
        back_button = self.draw_button(
            "Назад",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        self.animation_timer += 1
        return p1_rects, p2_rects, back_button

    def draw_select_character2(self):
        self.play_music("rr.mp3")
        (
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.char_transition_timer,
            self.char_transition_alpha,
        ) = self.update_background_transition(
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.CHAR_BACKGROUND_SWITCH_INTERVAL,
            self.char_transition_timer,
            self.char_transition_alpha,
            self.char_backgrounds,
        )
        self.draw_background_transition(
            self.char_backgrounds,
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)
        title = self.title_font.render(
            "Выберите персонажа для Игрока 2",
            True,
            self.get_shimmer_color(self.animation_timer),
        )
        title_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * title_scale),
                int(title.get_height() * title_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_title,
            (
                self.virtual_width // 2 - scaled_title.get_width() // 2,
                50 - scaled_title.get_height() // 2,
            ),
        )
        char_rects = []
        num_chars = len(self.CHARACTERS)
        for i in range(3):
            x, y = 300 + i * 250, 200
            scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05 + i)
            scaled_w, scaled_h = int(150 * scale), int(150 * scale)
            scaled_x, scaled_y = x + (150 - scaled_w) // 2, y + (150 - scaled_h) // 2
            if i < num_chars:
                char = self.CHARACTERS[i]
                if "image" in char:
                    scaled_image = pygame.transform.scale(
                        char["image"], (scaled_w, scaled_h)
                    )
                    self.virtual_screen.blit(scaled_image, (scaled_x, scaled_y))
                elif char.get("style") == "filled":
                    pygame.draw.rect(
                        self.virtual_screen,
                        char["color"],
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                    )
                elif char.get("style") == "outlined":
                    pygame.draw.rect(
                        self.virtual_screen,
                        char["color"],
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                        5,
                    )
                name = self.font.render(char["name"], True, (255, 255, 255))
                self.virtual_screen.blit(name, (x, y + 170))
                char_rects.append(pygame.Rect(x - 25, y - 25, 200, 200))
            else:
                if self.load_custom_icon:
                    scaled_image = pygame.transform.scale(
                        self.load_custom_icon, (scaled_w, scaled_h)
                    )
                    self.virtual_screen.blit(scaled_image, (scaled_x, scaled_y))
                else:
                    pygame.draw.rect(
                        self.virtual_screen,
                        (100, 100, 100),
                        (scaled_x, scaled_y, scaled_w, scaled_h),
                    )
                name = self.font.render("Custom", True, (255, 255, 255))
                self.virtual_screen.blit(name, (x, y + 170))
                char_rects.append(pygame.Rect(x - 25, y - 25, 200, 200))
        load_custom_button = self.draw_button(
            "Загрузить",
            self.virtual_width // 2 - 100,
            450,
            200,
            50,
            (100, 150, 255),
            (150, 200, 255),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        back_button = self.draw_button(
            "Назад",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        vol_up, vol_down = self.draw_volume_controls(self.virtual_width, 10)
        if self.help_icon:
            self.virtual_screen.blit(
                self.help_icon,
                (10, self.virtual_height - self.help_icon.get_height() - 10),
            )
        self.animation_timer += 1
        return char_rects, load_custom_button, back_button, vol_up, vol_down

    def draw_select_mode(self):
        self.play_music("rr.mp3")
        (
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_background_timer,
            self.mode_transition_timer,
            self.mode_transition_alpha,
        ) = self.update_background_transition(
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_background_timer,
            self.MODE_BACKGROUND_SWITCH_INTERVAL,
            self.mode_transition_timer,
            self.mode_transition_alpha,
            self.mode_backgrounds,
        )
        self.draw_background_transition(
            self.mode_backgrounds,
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)
        high_text = self.font.render(
            f"Рекорд: {self.high_score}",
            True,
            self.get_shimmer_color(self.animation_timer),
        )
        high_text_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_high_text = pygame.transform.scale(
            high_text,
            (
                int(high_text.get_width() * high_text_scale),
                int(high_text.get_height() * high_text_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_high_text,
            (
                self.virtual_width // 2 - scaled_high_text.get_width() // 2,
                100 - scaled_high_text.get_height() // 2,
            ),
        )
        title = self.title_font.render(
            "Выберите режим игры", True, self.get_shimmer_color(self.animation_timer)
        )
        title_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * title_scale),
                int(title.get_height() * title_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_title,
            (
                self.virtual_width // 2 - scaled_title.get_width() // 2,
                50 - scaled_title.get_height() // 2,
            ),
        )
        mode_rects = []
        for i, mode in enumerate(self.MODES):
            x, y = 300 + i * 250, 200
            hover_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05 + i)
            button = self.draw_button(
                mode["name"],
                x,
                y,
                200,
                100,
                (100, 150, 255),
                (150, 200, 255),
                (255, 255, 255),
                hover_scale=hover_scale,
            )
            mode_rects.append(button)
        coop_button = self.draw_button(
            "Кооператив",
            self.virtual_width // 2 - 100,
            320,
            200,
            100,
            (255, 215, 0),
            (255, 255, 100),
            (0, 0, 0),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.05 + 3),
        )
        mode_rects.append(coop_button)
        controls_button = self.draw_button(
            "Управление",
            self.virtual_width // 2 - 100,
            470,
            200,
            50,
            (100, 150, 255),
            (150, 200, 255),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        self.animation_timer += 1
        return mode_rects, controls_button, exit_button

    def draw_skateboard_select(self):
        """Меню выбора скейтборда после выбора персонажа"""
        self.play_music("rr.mp3")
        (
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.char_transition_timer,
            self.char_transition_alpha,
        ) = self.update_background_transition(
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_background_timer,
            self.CHAR_BACKGROUND_SWITCH_INTERVAL,
            self.char_transition_timer,
            self.char_transition_alpha,
            self.char_backgrounds,
        )
        self.draw_background_transition(
            self.char_backgrounds,
            self.char_current_background_index,
            self.char_next_background_index,
            self.char_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)

        title = self.title_font.render(
            "Выберите скейтборд", True, self.get_shimmer_color(self.animation_timer)
        )
        title_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_title = pygame.transform.scale(
            title,
            (
                int(title.get_width() * title_scale),
                int(title.get_height() * title_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_title,
            (
                self.virtual_width // 2 - scaled_title.get_width() // 2,
                50 - scaled_title.get_height() // 2,
            ),
        )

        skateboard_rects = []
        num_skateboards = len(self.skateboard_skins)

        for i in range(min(5, num_skateboards)):  # Максимум 5 скейтбордов в ряду
            x = 150 + i * 200
            y = 250
            scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05 + i)
            scaled_w, scaled_h = int(SKATEBOARD_WIDTH * scale * 2), int(
                SKATEBOARD_HEIGHT * scale * 2
            )
            scaled_x = x + (SKATEBOARD_WIDTH * 2 - scaled_w) // 2
            scaled_y = y + (SKATEBOARD_HEIGHT * 2 - scaled_h) // 2

            skateboard = self.skateboard_skins[i]

            # Отрисовка скейтборда
            if skateboard.get("image"):
                scaled_image = pygame.transform.scale(
                    skateboard["image"], (scaled_w, scaled_h)
                )
                self.virtual_screen.blit(scaled_image, (scaled_x, scaled_y))
            else:
                pygame.draw.rect(
                    self.virtual_screen,
                    skateboard.get("color", (100, 100, 100)),
                    (scaled_x, scaled_y, scaled_w, scaled_h),
                )
                pygame.draw.rect(
                    self.virtual_screen,
                    (255, 255, 255),
                    (scaled_x, scaled_y, scaled_w, scaled_h),
                    3,
                )

            name = self.font.render(skateboard["name"], True, (255, 255, 255))
            self.virtual_screen.blit(name, (x, y + 100))

            # Подсвечивание выбранного
            if i == self.selected_skateboard:
                pygame.draw.rect(
                    self.virtual_screen,
                    (255, 255, 0),
                    (scaled_x - 5, scaled_y - 5, scaled_w + 10, scaled_h + 10),
                    4,
                )

            skateboard_rects.append(pygame.Rect(x - 50, y - 50, 200, 200))

        load_custom_button = self.draw_button(
            "Загрузить",
            self.virtual_width // 2 - 100,
            450,
            200,
            50,
            (100, 150, 255),
            (150, 200, 255),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )

        next_button = self.draw_button(
            "Далее",
            self.virtual_width // 2 - 100,
            510,
            200,
            50,
            (100, 255, 100),
            (150, 255, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )

        back_button = self.draw_button(
            "Назад",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )

        vol_up, vol_down = self.draw_volume_controls(self.virtual_width, 10)
        self.animation_timer += 1

        return (
            skateboard_rects,
            load_custom_button,
            next_button,
            back_button,
            vol_up,
            vol_down,
        )

    def start_skateboard_trick(self, is_p1=True):
        """Случайный выбор трюка при прыжке"""
        trick_name = random.choice(list(SKATEBOARD_TRICKS.keys()))
        trick_data = SKATEBOARD_TRICKS[trick_name]

        if is_p1:
            self.player1_current_trick = trick_name
            self.player1_trick_timer = trick_data["duration"]
            self.player1_skateboard_rotation = 0
        else:
            self.player2_current_trick = trick_name
            self.player2_trick_timer = trick_data["duration"]
            self.player2_skateboard_rotation = 0

    def update_skateboard_trick(self, is_p1=True):
        """Обновляй состояние трюка"""
        if is_p1:
            if self.player1_trick_timer > 0:
                trick_name = self.player1_current_trick
                trick_data = SKATEBOARD_TRICKS[trick_name]

                progress = 1 - (self.player1_trick_timer / trick_data["duration"])
                self.player1_skateboard_rotation = trick_data["rotation"] * progress
                self.player1_trick_timer -= 1

                if self.player1_trick_timer <= 0:
                    self.player1_current_trick = None
                    self.player1_skateboard_rotation = 0
        else:
            if self.player2_trick_timer > 0:
                trick_name = self.player2_current_trick
                trick_data = SKATEBOARD_TRICKS[trick_name]

                progress = 1 - (self.player2_trick_timer / trick_data["duration"])
                self.player2_skateboard_rotation = trick_data["rotation"] * progress
                self.player2_trick_timer -= 1

                if self.player2_trick_timer <= 0:
                    self.player2_current_trick = None
                    self.player2_skateboard_rotation = 0

    def draw_skateboard(
        self,
        x,
        y,
        shake_x,
        shake_y,
        is_crouching,
        trick_timer,
        skateboard_rotation,
        current_trick,
        is_p1=True,
    ):
        """Рисуй скейтборд под персонажем"""
        if is_crouching:
            return
        if not self.skateboard_skins or self.selected_skateboard >= len(
            self.skateboard_skins
        ):
            self.selected_skateboard = 0
        if not self.skateboard_skins:
            return

        skateboard_index = (
            self.selected_skateboard if is_p1 else self.selected_skateboard
        )
        skateboard = self.skateboard_skins[skateboard_index]

        # Позиция скейтборда
        board_x = x + (PLAYER_SIZE - SKATEBOARD_WIDTH) // 2
        board_y = y + PLAYER_SIZE - 10

        # Отрисовка скейтборда
        if skateboard.get("image"):
            board_image = skateboard["image"]
        else:
            board_image = None

        # Применяй ротацию если идет трюк
        if trick_timer > 0:
            if board_image:
                rotated_board = pygame.transform.rotate(
                    board_image, skateboard_rotation
                )
                rotated_rect = rotated_board.get_rect(
                    center=(
                        int(board_x + SKATEBOARD_WIDTH // 3 + shake_x),
                        int(board_y + SKATEBOARD_HEIGHT // 3 + shake_y),
                    )
                )
                self.virtual_screen.blit(rotated_board, rotated_rect.topleft)
            else:
                rotated_surface = pygame.Surface(
                    (SKATEBOARD_WIDTH, SKATEBOARD_HEIGHT), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    rotated_surface,
                    skateboard.get("color", (100, 100, 100)),
                    (0, 0, SKATEBOARD_WIDTH, SKATEBOARD_HEIGHT),
                )
                pygame.draw.rect(
                    rotated_surface,
                    (255, 255, 255),
                    (0, 0, SKATEBOARD_WIDTH, SKATEBOARD_HEIGHT),
                    2,
                )
                rotated_board = pygame.transform.rotate(
                    rotated_surface, skateboard_rotation
                )
                rotated_rect = rotated_board.get_rect(
                    center=(
                        int(board_x + SKATEBOARD_WIDTH // 2 + shake_x),
                        int(board_y + SKATEBOARD_HEIGHT // 2 + shake_y),
                    )
                )
                self.virtual_screen.blit(rotated_board, rotated_rect.topleft)
        else:
            # Нормальное состояние скейтборда
            if board_image:
                self.virtual_screen.blit(
                    board_image,
                    (int(board_x + shake_x), int(board_y + shake_y)),
                )
            else:
                pygame.draw.rect(
                    self.virtual_screen,
                    skateboard.get("color", (100, 100, 100)),
                    (
                        int(board_x + shake_x),
                        int(board_y + shake_y),
                        SKATEBOARD_WIDTH,
                        SKATEBOARD_HEIGHT,
                    ),
                )
                pygame.draw.rect(
                    self.virtual_screen,
                    (255, 255, 255),
                    (
                        int(board_x + shake_x),
                        int(board_y + shake_y),
                        SKATEBOARD_WIDTH,
                        SKATEBOARD_HEIGHT,
                    ),
                    2,
                )

        # Название трюка
        if current_trick:
            trick_text = self.font.render(
                current_trick.upper(),
                True,
                (255, 255, 0),
            )
            self.virtual_screen.blit(
                trick_text,
                (int(board_x - 50 + shake_x), int(board_y - 50 + shake_y)),
            )

    def draw_player(
        self,
        x,
        y,
        crouching,
        shake_x,
        shake_y,
        character,
        is_dead,
        death_animation_timer,
        is_jumping,
        jump_animation_timer,
        invincibility,
        invincibility_timer,
        shield_active,
        shield_timer,
        double_jump_available,
    ):
        if is_dead and death_animation_timer <= 0:
            return
        size_y = PLAYER_SIZE // 2 if crouching else PLAYER_SIZE
        base_scale = 1.0 + 0.02 * math.sin(self.animation_timer * 0.1)
        if is_jumping and jump_animation_timer > 0:
            stretch_y = 1.1 + 0.1 * math.sin(
                jump_animation_timer / JUMP_ANIMATION_DURATION * math.pi
            )
            stretch_x = 0.9
            rotation = 10 * math.sin(
                jump_animation_timer / JUMP_ANIMATION_DURATION * math.pi
            )
        else:
            stretch_y = 1.0
            stretch_x = 1.0
            rotation = 0
        if is_dead and death_animation_timer > 0:
            if self.current_mode["name"] == "Уклонение":
                squash_progress = 1 - (death_animation_timer / DEATH_ANIMATION_DURATION)
                stretch_y = max(0.2, 1 - squash_progress * 0.8)
                stretch_x = min(1.8, 1 + squash_progress * 0.8)
                rotation = 0
            else:
                rotation = 360 * (1 - death_animation_timer / DEATH_ANIMATION_DURATION)
            alpha = int(255 * (death_animation_timer / DEATH_ANIMATION_DURATION))
        else:
            alpha = 255
        scaled_w = int(PLAYER_SIZE * base_scale * stretch_x)
        scaled_h = int(size_y * base_scale * stretch_y)
        scaled_x = x + (PLAYER_SIZE - scaled_w) // 2 + shake_x
        scaled_y = y + (size_y - scaled_h) // 2 + shake_y
        if RAIN_THRESHOLD <= self.score < 700 and not is_dead:
            glow_alpha = int(127 + 127 * math.sin(self.animation_timer * 0.1))
            glow_color = (255, 255, 100, glow_alpha)
            glow_radius = int(
                PLAYER_SIZE * 0.7 * (1.0 + 0.1 * math.sin(self.animation_timer * 0.15))
            )
            glow_surface = pygame.Surface(
                (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                glow_surface, glow_color, (glow_radius, glow_radius), glow_radius
            )
            self.virtual_screen.blit(
                glow_surface,
                (scaled_x - glow_radius + scaled_w // 2, scaled_y - glow_radius // 2),
            )
        if self.is_angel and not is_dead:
            self.draw_halo(scaled_x - shake_x, scaled_y - shake_y, shake_x, shake_y)
            self.draw_wings(scaled_x - shake_x, scaled_y - shake_y, shake_x, shake_y)
        self.draw_marihuana_mini(
            scaled_x - shake_x, scaled_y - shake_y, shake_x, shake_y
        )
        if shield_active and not is_dead:
            if self.shield_image:
                shield_scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.15)
                scaled_shield = pygame.transform.scale(
                    self.shield_image,
                    (
                        int(PLAYER_SIZE * 2 * shield_scale),
                        int(PLAYER_SIZE * 2 * shield_scale),
                    ),
                )
                self.virtual_screen.blit(
                    scaled_shield,
                    (
                        scaled_x + (scaled_w - scaled_shield.get_width()) // 2,
                        scaled_y + (scaled_h - scaled_shield.get_height()) // 2,
                    ),
                )
            else:
                shield_radius = int(PLAYER_SIZE * 0.8)
                shield_alpha = int(127 + 127 * math.sin(self.animation_timer * 0.15))
                shield_surface = pygame.Surface(
                    (shield_radius * 2, shield_radius * 2), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    shield_surface,
                    (128, 128, 255, shield_alpha),
                    (shield_radius, shield_radius),
                    shield_radius,
                    3,
                )
                self.virtual_screen.blit(
                    shield_surface,
                    (
                        scaled_x - shield_radius + scaled_w // 2,
                        scaled_y - shield_radius + scaled_h // 2,
                    ),
                )
        if self.laser_active and not is_dead:
            if self.tron_image:
                tron_scale = 2.4
                tron_w = int(PLAYER_SIZE * tron_scale * stretch_x * base_scale)
                tron_h = int(PLAYER_SIZE * tron_scale * stretch_y * base_scale)
                tron_x = scaled_x - (tron_w - scaled_w) // 2
                tron_y = scaled_y - (tron_h - scaled_h) // 2
                scaled_tron = pygame.transform.scale(self.tron_image, (tron_w, tron_h))
                rotated_tron = pygame.transform.rotate(scaled_tron, rotation)
                rotated_tron_rect = rotated_tron.get_rect(
                    center=(scaled_x + scaled_w // 2, scaled_y + scaled_h // 2)
                )
                self.virtual_screen.blit(rotated_tron, rotated_tron_rect.topleft)
            else:
                glow_radius = int(PLAYER_SIZE * 1.2)
                glow_alpha = int(127 + 127 * math.sin(self.animation_timer * 0.15))
                glow_surface = pygame.Surface(
                    (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    glow_surface,
                    (0, 0, 255, glow_alpha),
                    (glow_radius, glow_radius),
                    glow_radius,
                )
                self.virtual_screen.blit(
                    glow_surface,
                    (
                        scaled_x - glow_radius + scaled_w // 2,
                        scaled_y - glow_radius + scaled_h // 2,
                    ),
                )
        player_surface = pygame.Surface((scaled_w, scaled_h), pygame.SRCALPHA)
        player_surface.set_alpha(alpha)
        if invincibility and invincibility_timer > 0 and not is_dead:
            frame = self.get_animated_frame(
                self.crest_frames, self.crest_anim_timer, self.crest_anim_fps
            )
            if frame:
                scaled_image = pygame.transform.scale(frame, (scaled_w, scaled_h))
                player_surface.blit(scaled_image, (0, 0))
            elif self.crest_image:
                scaled_image = pygame.transform.scale(
                    self.crest_image, (scaled_w, scaled_h)
                )
                player_surface.blit(scaled_image, (0, 0))
        elif self.slow_down and self.csk_image and not is_dead:
            scaled_image = pygame.transform.scale(self.csk_image, (scaled_w, scaled_h))
            player_surface.blit(scaled_image, (0, 0))
        else:
            if "image" in character:
                image = pygame.transform.scale(character["image"], (scaled_w, scaled_h))
                player_surface.blit(image, (0, 0))
            elif character.get("style") == "filled":
                pygame.draw.rect(
                    player_surface, character["color"], (0, 0, scaled_w, scaled_h)
                )
            elif character.get("style") == "outlined":
                pygame.draw.rect(
                    player_surface, character["color"], (0, 0, scaled_w, scaled_h), 5
                )
            elif character.get("style") == "checkered":
                for i in range(int(12 * base_scale)):
                    for j in range(
                        int(12 * base_scale if crouching else 12 * base_scale)
                    ):
                        if (i + j) % 2 == 0:
                            pygame.draw.rect(
                                player_surface,
                                character["color"],
                                (i * 10, j * 10, 10, 10),
                            )
        rotated_surface = pygame.transform.rotate(player_surface, rotation)
        rotated_rect = rotated_surface.get_rect(
            center=(scaled_x + scaled_w // 2, scaled_y + scaled_h // 2)
        )
        self.virtual_screen.blit(rotated_surface, rotated_rect.topleft)
        if is_dead and self.explosion_particles:
            for p in self.explosion_particles:
                alpha = max(0, min(255, int(255 * (p[4] / 60))))
                size = max(2, 8 * (1 - p[4] / 60))
                pygame.draw.circle(
                    self.virtual_screen,
                    (*p[5], alpha),
                    (int(p[0] + shake_x), int(p[1] + shake_y)),
                    int(size),
                )
        if self.laser_active and not is_dead:
            color = character.get("color", (255, 255, 255))
            self.trail_particles.append(
                [
                    scaled_x + scaled_w // 2,
                    scaled_y + scaled_h // 2,
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    40,
                    color,
                ]
            )
        for p in self.trail_particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            alpha = int(255 * (p[4] / 40))
            if p[4] <= 0:
                self.trail_particles.remove(p)
        # Limit trail particles
        if len(self.trail_particles) > 100:
            self.trail_particles = self.trail_particles[-100:]

    def update_explosion_particles(self, slowdown_factor):
        for p in self.explosion_particles[:]:
            p[0] += p[2] * slowdown_factor
            p[1] += p[3] * slowdown_factor
            p[4] -= 1
            if p[4] <= 0:
                self.explosion_particles.remove(p)
        # Limit particles
        if len(self.explosion_particles) > 200:
            self.explosion_particles = self.explosion_particles[-200:]

    def spawn_explosion(self, x, y):
        self.explosion_particles.clear()
        if self.explosion_sound:
            self.explosion_sound.play()
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.randint(40, 80)
            color = (
                random.randint(150, 255),
                random.randint(50, 150),
                random.randint(0, 100),
            )
            self.explosion_particles.append([x, y, vx, vy, lifetime, color])

    def update_player(
        self,
        x,
        y,
        vel_x,
        vel_y,
        is_jumping,
        is_crouching,
        was_on_ground,
        jump_timer,
        jump_animation_timer,
        death_animation_timer,
        is_dead,
        lives,
        invincibility,
        invincibility_timer,
        shield_active,
        shield_timer,
        double_jump_available,
        keys,
        key_map,
        slowdown_factor=1.0,
        is_p2=False,
    ):
        if is_dead:
            if death_animation_timer > 0:
                death_animation_timer -= 1
            return (
                x,
                y,
                vel_x,
                vel_y,
                is_jumping,
                is_crouching,
                was_on_ground,
                jump_timer,
                jump_animation_timer,
                death_animation_timer,
                is_dead,
                lives,
                invincibility,
                invincibility_timer,
                shield_active,
                shield_timer,
                double_jump_available,
            )
        # Movement
        if keys[key_map["left"]]:
            vel_x -= PLAYER_ACCEL * slowdown_factor
        if keys[key_map["right"]]:
            vel_x += PLAYER_ACCEL * slowdown_factor
        vel_x *= PLAYER_FRICTION
        if abs(vel_x) < 0.1:
            vel_x = 0
        max_speed = MAX_SPEED * (0.3 if self.slow_down else 1.0)
        if abs(vel_x) > max_speed:
            vel_x = max_speed if vel_x > 0 else -max_speed
        x += vel_x * slowdown_factor
        x = max(0, min(x, self.virtual_width - PLAYER_SIZE))
        # Gravity and jump
        gravity = self.current_mode["gravity"]
        vel_y += gravity * slowdown_factor
        vel_y = min(vel_y, TERMINAL_VELOCITY)
        if is_jumping and jump_timer < MAX_JUMP_TIME:
            vel_y += self.current_mode["jump_hold"] * slowdown_factor
            jump_timer += 1
        y += vel_y * slowdown_factor
        player_hitbox_w = PLAYER_SIZE * PLAYER_HITBOX_SCALE
        player_hitbox_h = (
            PLAYER_SIZE * (0.5 if is_crouching else 1.0) * PLAYER_HITBOX_SCALE
        )
        crouch_offset = PLAYER_SIZE * 0.5 if is_crouching else 0
        player_hitbox_x = x + (PLAYER_SIZE - player_hitbox_w) // 2
        player_hitbox_y = (
            y
            + ((PLAYER_SIZE // 2 if is_crouching else PLAYER_SIZE) - player_hitbox_h)
            // 2
            + crouch_offset
        )
        player_rect = pygame.Rect(
            player_hitbox_x, player_hitbox_y, player_hitbox_w, player_hitbox_h
        )
        if is_crouching:
            y = self.virtual_height - PLAYER_SIZE // 2 - 10
            was_on_ground = True
        else:
            ground_y = self.virtual_height - PLAYER_SIZE - 10
            if y >= ground_y:
                y = ground_y
                vel_y = 0
                jump_animation_timer = 0
                double_jump_available = self.is_angel
                if not was_on_ground and RAIN_THRESHOLD <= self.score < 200:
                    self.spawn_splash(x + PLAYER_SIZE // 2, y + PLAYER_SIZE)
            if y < 0:
                y = 0
                vel_y = 0
            was_on_ground = y >= ground_y
        if jump_animation_timer > 0:
            jump_animation_timer -= 1
        # Timers
        if invincibility_timer > 0:
            invincibility_timer -= 1
            if invincibility_timer <= 0:
                invincibility = False
        if shield_active and shield_timer > 0:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False
        return (
            x,
            y,
            vel_x,
            vel_y,
            is_jumping,
            is_crouching,
            was_on_ground,
            jump_timer,
            jump_animation_timer,
            death_animation_timer,
            is_dead,
            lives,
            invincibility,
            invincibility_timer,
            shield_active,
            shield_timer,
            double_jump_available,
        )

    def handle_bonus_pickup(
        self,
        bonus,
        player_rect,
        player_lives,
        player_invincibility,
        player_invincibility_timer,
        player_shield_active,
        player_shield_timer,
        is_p1,
    ):
        self.bonuses.remove(bonus)
        self.score += 5 * self.score_multiplier
        self.spawn_buff_particles(
            bonus[0] + BONUS_SIZE // 2, bonus[1] + BONUS_SIZE // 2, bonus[2]
        )
        if self.bonus_sound:
            self.bonus_sound.play()
        bonus_type = bonus[2]
        if bonus_type == "laser":
            self.laser_active = True
            self.bonus_timer = 8 * FPS
            self.bonus_notification = "Бримстоун активирован!"
        elif bonus_type == "points":
            # Reset conflicting buffs only for points
            self.score_multiplier = 1
            self.double_points = True
            self.bonus_timer = 10 * FPS
            self.bonus_notification = "Двойные очки активированы!"
        elif bonus_type == "slow":
            # No reset needed, or reset if conflicting
            self.slow_down = True
            self.bonus_timer = 10 * FPS
            self.bonus_notification = "Подмост"
        elif bonus_type == "invincibility":
            player_invincibility = True
            player_invincibility_timer = 10 * FPS
            self.bonus_notification = "Спаси и сохрани меня грешного"
        elif bonus_type == "score_boost":
            # Reset double_points if active
            if self.double_points:
                self.double_points = False
            self.score_multiplier = 2
            self.bonus_timer = 10 * FPS
            self.bonus_notification = "Множитель очков x2!"
        elif bonus_type == "life":
            player_lives += 1
            self.bonus_notification = "Дополнительная жизнь!"
        elif bonus_type == "shield":
            player_shield_active = True
            player_shield_timer = SHIELD_DURATION
            self.bonus_notification = "Щит активирован!"
        elif bonus_type == "fire":
            self.fire_active = True
            self.fire_timer = FIRE_DURATION
            self.bonus_notification = "Огонь активирован!"
        elif bonus_type == "dvd":
            self.dvd_active = True
            self.dvd_timer = DVD_DURATION
            self.bonus_notification = "DVD режим активирован!"
            if DVD_CLEAR_OBSTACLES:
                self.obstacles.clear()
                self.boss_projectiles.clear()
                self.score += 50 * self.score_multiplier
        elif bonus_type == "marihuana":
            self.marihuana_active = True
            self.marihuana_timer = MARIHUANA_DURATION
            self.bonus_notification = "ВОТ ДЕРЬМО"
        self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
        return (
            player_lives,
            player_invincibility,
            player_invincibility_timer,
            player_shield_active,
            player_shield_timer,
        )

    def draw_game(self):
        slowdown_factor = (
            0.5
            if self.boss_defeat_timer > 0
            or self.slowdown_timer > 0
            or self.slowdown_timer2 > 0
            else 1.0
        )
        offset = int(math.sin(self.animation_timer * 0.025) * 10)
        shake_x = (
            random.randint(-MARIHUANA_SHAKE_INTENSITY, MARIHUANA_SHAKE_INTENSITY)
            if self.marihuana_active
            else 0
        )
        shake_y = (
            random.randint(-MARIHUANA_SHAKE_INTENSITY, MARIHUANA_SHAKE_INTENSITY)
            if self.marihuana_active
            else 0
        )
        npc_bg = None
        if self.score >= NPC_THRESHOLD:
            milestone = ((self.score - NPC_THRESHOLD) // NPC_INTERVAL) % len(
                self.npc_backgrounds
            )
            self.current_npc_index = milestone
            npc_bg = self.npc_backgrounds[self.current_npc_index]
        if npc_bg:
            self.virtual_screen.blit(npc_bg, (offset + shake_x, 0 + shake_y))
        elif self.score >= 800:
            if self.sf_background:
                self.virtual_screen.blit(
                    self.sf_background, (offset + shake_x, 0 + shake_y)
                )
            else:
                self.virtual_screen.fill((0, 0, 0))
        elif self.score >= BOSS_THRESHOLD_END and self.blood_background:
            self.virtual_screen.blit(
                self.blood_background, (offset + shake_x, 0 + shake_y)
            )
        elif self.score >= 150 and self.score < 250:
            # ddd backgrounds for score 150-249
            if hasattr(self, 'ddd_backgrounds') and self.ddd_backgrounds:
                idx = (self.score // 150) % len(self.ddd_backgrounds)
                self.virtual_screen.blit(self.ddd_backgrounds[idx], (offset + shake_x, 0 + shake_y))
            elif self.game_background:
                self.virtual_screen.blit(self.game_background, (offset + shake_x, 0 + shake_y))
        elif self.score >= 250 and self.score < 400 and self.toy_background:
            self.virtual_screen.blit(self.toy_background, (offset + shake_x, 0 + shake_y))
        elif self.score < 150:
            # anu backgrounds for score 0-149
            if self.current_anu_bg:
                self.virtual_screen.blit(self.current_anu_bg, (offset + shake_x, 0 + shake_y))
            elif self.initial_game_background:
                self.virtual_screen.blit(self.initial_game_background, (offset + shake_x, 0 + shake_y))
        if self.score < SUN_THRESHOLD:
            self.draw_sun_and_rays(shake_x, shake_y)
        bonus_scale = 1 + 0.1 * math.sin(self.animation_timer * 0.2)
        bonus_scaled_size = int(BONUS_SIZE * bonus_scale)
        monster_frame = self.get_animated_frame(
            self.monster_frames, self.monster_anim_timer, self.monster_anim_fps
        )
        marihuana_frame = self.get_animated_frame(
            self.marihuana_frames, self.marihuana_anim_timer, MARIHUANA_ANIM_FPS
        )
        crest_frame = (
            self.get_animated_frame(
                self.crest_frames, self.crest_anim_timer, self.crest_anim_fps
            )
            if BOSS_THRESHOLD_START <= self.score < BOSS_THRESHOLD_END
            else self.crest_image
        )
        obs_scale = 1 + 0.05 * math.sin(self.animation_timer * 0.05)
        self.draw_obstacles(self.obstacles, shake_x, shake_y, obs_scale, None)
        self.draw_obstacles(self.boss_projectiles, shake_x, shake_y, obs_scale, None)
        self.draw_skateboard(
            self.player1_x,
            self.player1_y,
            shake_x,
            shake_y,
            self.player1_is_crouching,
            self.player1_trick_timer,
            self.player1_skateboard_rotation,
            self.player1_current_trick,
            True,
        )
        if self.coop_mode:
            self.draw_skateboard(
                self.player2_x,
                self.player2_y,
                shake_x,
                shake_y,
                self.player2_is_crouching,
                self.player2_trick_timer,
                self.player2_skateboard_rotation,
                self.player2_current_trick,
                False,
            )
        self.draw_player(
            self.player1_x,
            self.player1_y,
            self.player1_is_crouching,
            shake_x,
            shake_y,
            self.selected_character,
            self.player1_is_dead,
            self.player1_death_animation_timer,
            self.player1_is_jumping,
            self.player1_jump_animation_timer,
            self.player1_invincibility,
            self.player1_invincibility_timer,
            self.player1_shield_active,
            self.player1_shield_timer,
            self.player1_double_jump_available,
        )
        if self.coop_mode:
            self.draw_player(
                self.player2_x,
                self.player2_y,
                self.player2_is_crouching,
                shake_x,
                shake_y,
                self.selected_character2,
                self.player2_is_dead,
                self.player2_death_animation_timer,
                self.player2_is_jumping,
                self.player2_jump_animation_timer,
                self.player2_invincibility,
                self.player2_invincibility_timer,
                self.player2_shield_active,
                self.player2_shield_timer,
                self.player2_double_jump_available,
            )
        self.draw_bonuses(
            self.bonuses,
            shake_x,
            shake_y,
            bonus_scaled_size,
            monster_frame,
            marihuana_frame,
        )
        for laser in self.lasers[:]:
            pygame.draw.line(
                self.virtual_screen,
                (255, 0, 0),
                (laser[0] + shake_x, laser[1] + shake_y),
                (laser[2] + shake_x, laser[3] + shake_y),
                LASER_THICKNESS,
            )
            laser[4] -= 1
            if laser[4] <= 0:
                self.lasers.remove(laser)
        self.draw_fire_animations(shake_x, shake_y)
        self.draw_boss(shake_x, shake_y)
        if RAIN_THRESHOLD <= self.score < 200:
            self.draw_rain(shake_x, shake_y)
        if self.score >= THUNDER_THRESHOLD:
            self.draw_lightning(shake_x, shake_y)
        if self.score >= SCREAMER_THRESHOLD:
            self.draw_screamer(shake_x, shake_y)
        self.draw_buff_particles(shake_x, shake_y)
        self.draw_milestone_flash(shake_x, shake_y)
        self.draw_difficulty_text(shake_x, shake_y)
        self.draw_lives(shake_x, shake_y)
        self.draw_bonus_indicator(shake_x, shake_y)
        self.draw_bonus_notification(shake_x, shake_y)
        score_text = self.font.render(
            f"Счёт: {self.score} x{self.score_multiplier}",
            True,
            self.get_shimmer_color(self.animation_timer),
        )
        mode_text = self.font.render(
            f"Режим: {self.current_mode['name']}",
            True,
            self.get_shimmer_color(self.animation_timer),
        )
        self.virtual_screen.blit(score_text, (10 + shake_x, 10 + shake_y))
        self.virtual_screen.blit(mode_text, (10 + shake_x, 130 + shake_y))
        if self.boss_defeat_timer > 0:
            if self.hoppe_image:
                self.virtual_screen.blit(self.hoppe_image, (shake_x, shake_y))
            text = self.title_font.render(
                "Благословение", True, self.get_shimmer_color(self.animation_timer)
            )
            scale = 1.0 + 0.1 * math.sin(self.animation_timer * 0.2)
            scaled_text = pygame.transform.scale(
                text, (int(text.get_width() * scale), int(text.get_height() * scale))
            )
            self.virtual_screen.blit(
                scaled_text,
                (
                    self.virtual_width // 2 - scaled_text.get_width() // 2 + shake_x,
                    self.virtual_height // 2 - scaled_text.get_height() // 2 + shake_y,
                ),
            )
        if self.slowdown_timer > 0 and self.sasha_image:
            self.virtual_screen.blit(self.sasha_image, (shake_x, shake_y))

    def draw_obstacles(self, obstacles, shake_x, shake_y, obs_scale, crest_frame=None):
        for obs in obstacles:
            visual_w = int(obs[2] * OBSTACLE_VISUAL_SCALE * obs_scale)
            visual_h = int(obs[3] * OBSTACLE_VISUAL_SCALE * obs_scale)
            visual_x = obs[0] - (visual_w - obs[2]) // 2 + shake_x
            visual_y = obs[1] - (visual_h - obs[3]) // 2 + shake_y
            obs_type = obs[4]

            if obs_type == "trap":
                scale = 1.0 + 0.2 * math.sin(self.animation_timer * 0.3)
                visual_w = int(visual_w * scale)
                visual_h = int(visual_h * scale)
                visual_x = obs[0] - (visual_w - obs[2]) // 2 + shake_x
                visual_y = obs[1] - (visual_h - obs[3]) // 2 + shake_y
                if self.trap_image:
                    scaled_texture = pygame.transform.scale(
                        self.trap_image, (visual_w, visual_h)
                    )
                    self.virtual_screen.blit(
                        scaled_texture, (int(visual_x), int(visual_y))
                    )
                else:
                    pygame.draw.rect(
                        self.virtual_screen,
                        (255, 0, 0),
                        (int(visual_x), int(visual_y), visual_w, visual_h),
                    )
                    pygame.draw.rect(
                        self.virtual_screen,
                        (255, 255, 255),
                        (int(visual_x), int(visual_y), visual_w, visual_h),
                        3,
                    )

            elif obs_type == "spike":
                if self.spike_texture:
                    scaled_texture = pygame.transform.scale(
                        self.spike_texture, (visual_w, visual_h)
                    )
                    self.virtual_screen.blit(
                        scaled_texture, (int(visual_x), int(visual_y))
                    )
                else:
                    points = [
                        (visual_x, visual_y + visual_h),
                        (visual_x + visual_w // 2, visual_y),
                        (visual_x + visual_w, visual_y + visual_h),
                    ]
                    pygame.draw.polygon(self.virtual_screen, (255, 0, 0), points)

            elif obs_type == "zvb":
                if self.zvb_image:
                    scaled_texture = pygame.transform.scale(
                        self.zvb_image, (visual_w, visual_h)
                    )
                    self.virtual_screen.blit(
                        scaled_texture, (int(visual_x), int(visual_y))
                    )
                else:
                    pygame.draw.rect(
                        self.virtual_screen,
                        (128, 0, 128),
                        (int(visual_x), int(visual_y), visual_w, visual_h),
                    )

            elif obs_type == "told":
                image = obs[7] if len(obs) > 7 and obs[7] else None
                if image:
                    try:
                        scaled_texture = pygame.transform.scale(
                            image, (visual_w, visual_h)
                        )
                        self.virtual_screen.blit(
                            scaled_texture, (int(visual_x), int(visual_y))
                        )
                    except:
                        pygame.draw.rect(
                            self.virtual_screen,
                            (139, 69, 19),
                            (int(visual_x), int(visual_y), visual_w, visual_h),
                        )
                else:
                    pygame.draw.rect(
                        self.virtual_screen,
                        (139, 69, 19),
                        (int(visual_x), int(visual_y), visual_w, visual_h),
                    )

            elif len(obs) > 7 and obs[7] is not None:
                try:
                    scaled_texture = pygame.transform.scale(
                        obs[7], (visual_w, visual_h)
                    )
                    self.virtual_screen.blit(
                        scaled_texture, (int(visual_x), int(visual_y))
                    )
                except:
                    if self.dadep_image:
                        scaled_texture = pygame.transform.scale(
                            self.dadep_image, (visual_w, visual_h)
                        )
                        self.virtual_screen.blit(
                            scaled_texture, (int(visual_x), int(visual_y))
                        )
                    else:
                        color = (100, 100, 100)
                        pygame.draw.rect(
                            self.virtual_screen,
                            color,
                            (int(visual_x), int(visual_y), visual_w, visual_h),
                        )

            elif self.obstacle_texture:
                scaled_texture = pygame.transform.scale(
                    self.obstacle_texture, (visual_w, visual_h)
                )
                self.virtual_screen.blit(scaled_texture, (int(visual_x), int(visual_y)))

            else:
                if self.ricc_image:
                    scaled_texture = pygame.transform.scale(
                        self.ricc_image, (visual_w, visual_h)
                    )
                    self.virtual_screen.blit(
                        scaled_texture, (int(visual_x), int(visual_y))
                    )
                else:
                    color = (100, 100, 100)
                    pygame.draw.rect(
                        self.virtual_screen,
                        color,
                        (int(visual_x), int(visual_y), visual_w, visual_h),
                    )

    def draw_bonuses(
        self,
        bonuses,
        shake_x,
        shake_y,
        bonus_scaled_size,
        monster_frame,
        marihuana_frame,
    ):
        for bonus in bonuses:
            bonus_x = bonus[0] - (bonus_scaled_size - BONUS_SIZE) // 2 + shake_x
            bonus_y = bonus[1] - (bonus_scaled_size - BONUS_SIZE) // 2 + shake_y
            self.draw_buff_glow(bonus_x - shake_x, bonus_y - shake_y, bonus_scaled_size)
            bonus_type = bonus[2]
            if bonus_type == "laser":
                if self.laser_image:
                    scaled_image = pygame.transform.scale(
                        self.laser_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (255, 0, 0),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "points":
                if self.points_image:
                    scaled_image = pygame.transform.scale(
                        self.points_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (255, 215, 0),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "slow":
                if self.slow_image:
                    scaled_image = pygame.transform.scale(
                        self.slow_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (0, 191, 255),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "invincibility":
                if self.invincibility_image:
                    scaled_image = pygame.transform.scale(
                        self.invincibility_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (255, 0, 255),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "score_boost":
                if monster_frame:
                    monster_scaled = pygame.transform.scale(
                        monster_frame, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(
                        monster_scaled, (int(bonus_x), int(bonus_y))
                    )
                elif self.score_boost_image:
                    scaled_image = pygame.transform.scale(
                        self.score_boost_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (0, 255, 128),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "life":
                if self.heart_image:
                    scaled_heart = pygame.transform.scale(
                        self.heart_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_heart, (int(bonus_x), int(bonus_y)))
                else:
                    points = [
                        (
                            bonus_x + bonus_scaled_size // 2,
                            bonus_y + bonus_scaled_size // 4,
                        ),
                        (bonus_x, bonus_y + bonus_scaled_size // 2),
                        (bonus_x + bonus_scaled_size // 4, bonus_y + bonus_scaled_size),
                        (
                            bonus_x + bonus_scaled_size // 2,
                            bonus_y + bonus_scaled_size // 2,
                        ),
                        (
                            bonus_x + 3 * bonus_scaled_size // 4,
                            bonus_y + bonus_scaled_size,
                        ),
                        (bonus_x + bonus_scaled_size, bonus_y + bonus_scaled_size // 2),
                        (
                            bonus_x + bonus_scaled_size // 2,
                            bonus_y + bonus_scaled_size // 4,
                        ),
                    ]
                    pygame.draw.polygon(self.virtual_screen, (255, 0, 0), points)
            elif bonus_type == "shield":
                if self.shield_image:
                    scaled_shield = pygame.transform.scale(
                        self.shield_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(
                        scaled_shield, (int(bonus_x), int(bonus_y))
                    )
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (128, 128, 255),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "fire":
                if self.fire_buff_image:
                    scaled_image = pygame.transform.scale(
                        self.fire_buff_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (255, 69, 0),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "dvd":
                if self.dvd_image:
                    scaled_image = pygame.transform.scale(
                        self.dvd_image, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(scaled_image, (int(bonus_x), int(bonus_y)))
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (255, 0, 255),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )
            elif bonus_type == "marihuana":
                if marihuana_frame:
                    marihuana_scaled = pygame.transform.scale(
                        marihuana_frame, (bonus_scaled_size, bonus_scaled_size)
                    )
                    self.virtual_screen.blit(
                        marihuana_scaled, (int(bonus_x), int(bonus_y))
                    )
                else:
                    pygame.draw.circle(
                        self.virtual_screen,
                        (0, 255, 0),
                        (
                            int(bonus_x + bonus_scaled_size // 2),
                            int(bonus_y + bonus_scaled_size // 2),
                        ),
                        bonus_scaled_size // 2,
                    )

    def draw_fire_animations(self, shake_x, shake_y):
        for fa in self.fire_animations[:]:
            if self.fire_animation_image:
                progress = fa[2] / FIRE_ANIMATION_DURATION
                scale = 1.0 + 0.5 * (1 - progress)
                alpha = int(255 * progress)
                scaled_fire = pygame.transform.scale(
                    self.fire_animation_image, (int(100 * scale), int(100 * scale))
                )
                surf = scaled_fire.copy()
                surf.set_alpha(alpha)
                self.virtual_screen.blit(
                    surf,
                    (
                        int(fa[0] - (100 * scale - 100) // 2 + shake_x),
                        int(fa[1] - (100 * scale - 100) // 2 + shake_y),
                    ),
                )
            fa[2] -= 1
            if fa[2] <= 0:
                self.fire_animations.remove(fa)
        # Limit fire animations
        if len(self.fire_animations) > 50:
            self.fire_animations = self.fire_animations[-50:]

    def draw_boss(self, shake_x, shake_y):
        if self.boss_active or self.boss_fade_timer > 0:
            if self.boss_image:
                boss_surf = self.boss_image.copy()
                boss_surf.set_alpha(self.boss_alpha)
                self.virtual_screen.blit(
                    boss_surf, (int(self.boss_x + shake_x), int(self.boss_y + shake_y))
                )
            else:
                pygame.draw.rect(
                    self.virtual_screen,
                    (255, 0, 0, self.boss_alpha),
                    (
                        int(self.boss_x + shake_x),
                        int(self.boss_y + shake_y),
                        BOSS_SIZE,
                        BOSS_SIZE,
                    ),
                )
            if self.boss_active:
                health_bar_w = 200
                health_bar_h = 20
                fill_w = (self.boss_health / BOSS_MAX_HEALTH) * health_bar_w
                pygame.draw.rect(
                    self.virtual_screen,
                    (255, 0, 0),
                    (
                        int(self.boss_x + BOSS_SIZE // 2 - health_bar_w // 2 + shake_x),
                        int(self.boss_y - 30 + shake_y),
                        health_bar_w,
                        health_bar_h,
                    ),
                )
                pygame.draw.rect(
                    self.virtual_screen,
                    (0, 255, 0),
                    (
                        int(self.boss_x + BOSS_SIZE // 2 - health_bar_w // 2 + shake_x),
                        int(self.boss_y - 30 + shake_y),
                        int(fill_w),
                        health_bar_h,
                    ),
                )

    def draw_help_screen(self):
        if self.help_background:
            self.virtual_screen.blit(self.help_background, (0, 0))
        else:
            self.virtual_screen.fill((0, 0, 0))
        title = self.title_font.render("Баффы и Дебаффы", True, (255, 255, 255))
        self.virtual_screen.blit(
            title,
            (
                self.virtual_width // 2 - title.get_width() // 2,
                50 + self.help_scroll_offset,
            ),
        )
        buffs = [
            ("Двойные Очки", self.points_image, "Удваивает заработанные очки на время"),
            ("Подмост", self.slow_image, "Замедляет препятствия на время"),
            (
                "Спаси и сохрани меня грешного",
                self.invincibility_image,
                "Неуязвимость на время",
            ),
            (
                "Увеличение Очков",
                self.score_boost_image,
                "Умножает получаемые очки на 2",
            ),
            ("Жизнь", self.heart_image, "Добавляет дополнительную жизнь"),
            ("Щит", self.shield_image, "Защищает от одного столкновения"),
            ("Бримстоун", self.laser_image, "Уничтожает препятствия лазером в радиусе"),
            ("Огонь", self.fire_buff_image, "Сжигает ближайшие препятствия"),
            (
                "DVD",
                self.dvd_image,
                "Очищает экран от препятствий и пауза спавна на время",
            ),
            (
                "Дерьмо",
                (
                    self.marihuana_frames[0]
                    if self.marihuana_frames and len(self.marihuana_frames) > 0
                    else None
                ),
                "fuck",
            ),
        ]
        debuffs = [
            ("Орешки БигБоб", self.trap_image, "Быстрое препятствие, наносящее урон"),
            (
                "Мяу",
                self.spike_texture,
                "Стационарное препятствие на земле или потолке",
            ),
        ]
        y = 100 + self.help_scroll_offset
        for name, image, desc in buffs:
            text = self.font.render(f"{name}: {desc}", True, (255, 255, 255))
            self.virtual_screen.blit(text, (100, y))
            if image:
                scaled_image = pygame.transform.scale(image, (50, 50))
                self.virtual_screen.blit(scaled_image, (50, y))
            y += 60
        y += 50
        debuff_title = self.font.render("Дебаффы:", True, (255, 255, 255))
        self.virtual_screen.blit(debuff_title, (50, y))
        y += 40
        for name, image, desc in debuffs:
            text = self.font.render(f"{name}: {desc}", True, (255, 255, 255))
            self.virtual_screen.blit(text, (100, y))
            if image:
                scaled_image = pygame.transform.scale(image, (50, 50))
                self.virtual_screen.blit(scaled_image, (50, y))
            y += 60
        y += 50
        total_content_height = y + 100
        max_scroll_offset = max(0, -(total_content_height - self.virtual_height))
        self.help_scroll_offset = min(
            0, max(self.help_scroll_offset, -max_scroll_offset)
        )
        if self.secret_image and self.help_scroll_offset <= -max_scroll_offset:
            secret_y = y + 300 + self.help_scroll_offset
            self.virtual_screen.blit(
                self.secret_image,
                (
                    self.virtual_width // 2 - self.secret_image.get_width() // 2,
                    int(secret_y),
                ),
            )
            ggl_text = self.font.render("ggl", True, (255, 255, 255))
            self.virtual_screen.blit(
                ggl_text,
                (
                    self.virtual_width // 2 - ggl_text.get_width() // 2,
                    int(secret_y + self.secret_image.get_height() + 20),
                ),
            )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 - 50,
            self.virtual_height - 60,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            hover_scale=1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        self.animation_timer += 1
        return exit_button

    def draw_pause_screen(self):
        overlay = pygame.Surface(
            (self.virtual_width, self.virtual_height), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 150))
        self.virtual_screen.blit(overlay, (0, 0))
        pause_text = self.title_font.render(
            "Пауза", True, self.get_shimmer_color(self.animation_timer)
        )
        pause_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
        scaled_pause = pygame.transform.scale(
            pause_text,
            (
                int(pause_text.get_width() * pause_scale),
                int(pause_text.get_height() * pause_scale),
            ),
        )
        self.virtual_screen.blit(
            scaled_pause,
            (
                self.virtual_width // 2 - scaled_pause.get_width() // 2,
                self.virtual_height // 2 - 60 - scaled_pause.get_height() // 2,
            ),
        )
        mouse_pressed = pygame.mouse.get_pressed()[0]
        resume_button = self.draw_button(
            "Продолжить",
            self.virtual_width // 2 - 110,
            self.virtual_height // 2 + 20,
            100,
            40,
            (100, 100, 255),
            (150, 150, 255),
            (255, 255, 255),
            mouse_pressed,
            1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 + 10,
            self.virtual_height // 2 + 20,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            mouse_pressed,
            1.0 + 0.05 * math.sin(self.animation_timer * 0.075 + 1),
        )
        vol_up, vol_down = self.draw_volume_controls(
            self.virtual_width // 2, self.virtual_height // 2 + 100
        )
        return resume_button, exit_button, vol_up, vol_down

    def draw_game_over(self):
        (
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_background_timer,
            self.mode_transition_timer,
            self.mode_transition_alpha,
        ) = self.update_background_transition(
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_background_timer,
            self.MODE_BACKGROUND_SWITCH_INTERVAL,
            self.mode_transition_timer,
            self.mode_transition_alpha,
            self.mode_backgrounds,
        )
        self.draw_background_transition(
            self.mode_backgrounds,
            self.mode_current_background_index,
            self.mode_next_background_index,
            self.mode_transition_alpha,
        )
        self.draw_stars(1.0, 0, 0)
        if self.game_over_timer < GAME_OVER_ANIMATION_DURATION:
            progress = self.game_over_timer / GAME_OVER_ANIMATION_DURATION
            min_scale = 0.1
            scale = min_scale + (1 - min_scale) * progress
            scaled_width = int(self.virtual_width * scale)
            scaled_height = int(self.virtual_height * scale)
            if self.game_over_image:
                scaled_image = pygame.transform.scale(
                    self.game_over_image, (scaled_width, scaled_height)
                )
                self.virtual_screen.blit(
                    scaled_image,
                    (
                        self.virtual_width // 2 - scaled_width // 2,
                        self.virtual_height // 2 - scaled_height // 2,
                    ),
                )
            self.game_over_timer += 1
        else:
            if self.game_over_image:
                scaled_image = pygame.transform.scale(
                    self.game_over_image, (self.virtual_width, self.virtual_height)
                )
                self.virtual_screen.blit(scaled_image, (0, 0))
            game_over_text = self.title_font.render(
                f"Игра окончена! Счёт: {self.score}",
                True,
                self.get_shimmer_color(self.animation_timer),
            )
            game_over_scale = 1.0 + 0.05 * math.sin(self.animation_timer * 0.05)
            scaled_game_over = pygame.transform.scale(
                game_over_text,
                (
                    int(game_over_text.get_width() * game_over_scale),
                    int(game_over_text.get_height() * game_over_scale),
                ),
            )
            self.virtual_screen.blit(
                scaled_game_over,
                (
                    self.virtual_width // 2 - scaled_game_over.get_width() // 2,
                    self.virtual_height // 2 - 60 - scaled_game_over.get_height() // 2,
                ),
            )
        mouse_pressed = pygame.mouse.get_pressed()[0]
        retry_button = self.draw_button(
            "Повторить",
            self.virtual_width // 2 - 110,
            self.virtual_height // 2 + 20,
            100,
            40,
            (100, 100, 255),
            (150, 150, 255),
            (255, 255, 255),
            mouse_pressed,
            1.0 + 0.05 * math.sin(self.animation_timer * 0.075),
        )
        exit_button = self.draw_button(
            "Выход",
            self.virtual_width // 2 + 10,
            self.virtual_height // 2 + 20,
            100,
            40,
            (255, 100, 100),
            (255, 150, 150),
            (255, 255, 255),
            mouse_pressed,
            1.0 + 0.05 * math.sin(self.animation_timer * 0.075 + 1),
        )
        self.animation_timer += 1
        return retry_button, exit_button

    def spawn_obstacle(self):
        difficulty_level = self.score // DIFFICULTY_THRESHOLD
        speed_multiplier = (
            1.0 + 0.07 * difficulty_level + 0.05 * math.sin(self.animation_timer * 0.01)
        )
        w = random.randint(60, 120)
        h = random.randint(60, 180)
        image = None
        if self.score >= 400:
            image = (
                random.choice([self.wau_image, self.zxc_image])
                if self.wau_image and self.zxc_image
                else None
            )
        if self.score >= NPC_THRESHOLD and random.random() < TOLD_SPAWN_CHANCE:
            y = random.randint(100, self.virtual_height - 100)
            told_image = random.choice(self.told_images) if self.told_images else None
            return [
                self.virtual_width,
                y,
                w,
                h,
                "told",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                told_image,
            ]
        if self.score >= 800:
            image = (
                random.choice([self.sf1_image, self.sf2_image])
                if self.sf1_image and self.sf2_image
                else None
            )
            y = random.randint(100, self.virtual_height - 100)
            return [
                self.virtual_width,
                y,
                w,
                h,
                "flying",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
                (255, 0, 0),
            ]
        if random.random() < 0.1 and self.score >= 150:
            y = random.randint(
                self.virtual_height // 2 - h, self.virtual_height - h - 30
            )
            return [
                self.virtual_width,
                y,
                w,
                h,
                "zvb",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                self.zvb_image,
            ]
        elif random.random() < SPIKE_CHANCE:
            w = random.randint(100, 200)
            h = random.randint(100, 300)
            y = self.virtual_height - h - 20 if random.random() < 0.5 else 15
            return [
                self.virtual_width,
                y,
                w,
                h,
                "spike",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
            ]
        elif random.random() < TRAP_CHANCE and self.score >= 50:
            return [
                self.virtual_width,
                self.virtual_height - h - 10,
                w,
                h,
                "trap",
                self.current_mode["obstacle_speed"] * speed_multiplier * 1.2,
                False,
                image,
            ]
        elif self.current_mode["name"] == "Уклонение":
            x = random.randint(0, self.virtual_width - w)
            return [
                x,
                -h,
                w,
                h,
                "falling",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
            ]
        elif self.score >= ANGEL_THRESHOLD and random.random() < 0.3:
            return [
                self.virtual_width,
                0,
                w,
                h,
                "ceiling",
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
            ]
        elif random.random() < self.current_mode["high_prob"]:
            obs_type = "high"
            return [
                self.virtual_width,
                self.virtual_height - h - 300,
                w,
                h,
                obs_type,
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
            ]
        else:
            obs_type = "low"
            return [
                self.virtual_width,
                self.virtual_height - h - 30,
                w,
                h,
                obs_type,
                self.current_mode["obstacle_speed"] * speed_multiplier,
                False,
                image,
            ]

    def spawn_bonus(self):
        if random.random() < LIFE_BONUS_CHANCE:
            bonus_type = "life"
        elif random.random() < SHIELD_BONUS_CHANCE:
            bonus_type = "shield"
        else:
            bonus_types = [
                "laser",
                "points",
                "slow",
                "invincibility",
                "score_boost",
                "fire",
                "marihuana",
            ]
            if self.score >= NPC_THRESHOLD and random.random() < 0.2:
                bonus_types.append("dvd")
            bonus_type = random.choice(bonus_types)
        tries = 0
        while tries < 10:
            y = random.randint(100, self.virtual_height - 100)
            bonus_rect = pygame.Rect(self.virtual_width, y, BONUS_SIZE, BONUS_SIZE)
            overlaps = any(
                bonus_rect.colliderect(pygame.Rect(obs[0], obs[1], obs[2], obs[3]))
                for obs in self.obstacles
            )
            if not overlaps:
                return [self.virtual_width, y, bonus_type]
            tries += 1
        return None

    def spawn_boss_projectile(self):
        if self.coop_mode:
            if not self.player1_is_dead and not self.player2_is_dead:
                target_x, target_y = self.player1_x, self.player1_y
            elif not self.player1_is_dead:
                target_x, target_y = self.player1_x, self.player1_y
            elif not self.player2_is_dead:
                target_x, target_y = self.player2_x, self.player2_y
            else:
                target_x = random.randint(0, self.virtual_width)
                target_y = random.randint(0, self.virtual_height)
        else:
            if not self.player1_is_dead:
                target_x = self.player1_x
                target_y = self.player1_y
            else:
                target_x = random.randint(0, self.virtual_width)
                target_y = random.randint(0, self.virtual_height)
        w = random.randint(60, 150)
        h = random.randint(60, 180)
        proj_x = self.boss_x
        proj_y = self.boss_y + BOSS_SIZE // 2
        dx = target_x - proj_x
        dy = target_y - proj_y
        dist = math.hypot(dx, dy)
        deviation = random.uniform(-0.3, 0.3)  # От -0.3 до 0.3 радиан
        angle = math.atan2(dy, dx) + deviation
        if dist > 0:
            vel_x = (dx / dist) * BOSS_PROJECTILE_SPEED
            vel_y = (dy / dist) * BOSS_PROJECTILE_SPEED
        else:
            vel_x = -BOSS_PROJECTILE_SPEED
            vel_y = 0
        image = (
            random.choice([self.dadep_image, self.hop_image, self.ricc_image])
            if self.dadep_image and self.hop_image and self.ricc_image
            else None
        )
        return [proj_x, proj_y, w, h, "boss_proj", vel_x, vel_y, image]

    def reset_game(self):
        # Pick new random anu background
        if hasattr(self, 'anu_backgrounds') and self.anu_backgrounds:
            self.current_anu_bg = random.choice(self.anu_backgrounds)
        selected_initial = random.choice(self.initial_background_files)
        self.initial_game_background = self.load_image(selected_initial)
        if self.initial_game_background:
            self.initial_game_background = pygame.transform.scale(
                self.initial_game_background, (self.virtual_width, self.virtual_height)
            )
        selected_game_bg = random.choice(self.game_background_files)
        self.game_background = self.load_image(selected_game_bg)
        if self.game_background:
            self.game_background = pygame.transform.scale(
                self.game_background, (self.virtual_width, self.virtual_height)
            )
        # Reset players
        self.player1_x = 150
        self.player1_y = self.virtual_height - PLAYER_SIZE - 10
        self.player1_vel_x = 0
        self.player1_vel_y = 0
        self.player1_is_jumping = False
        self.player1_is_crouching = False
        self.player1_was_on_ground = True
        self.player1_jump_timer = 0
        self.player1_jump_animation_timer = 0
        self.player1_death_animation_timer = 0
        self.player1_is_dead = False
        self.player1_lives = self.starting_lives
        self.player1_invincibility = False
        self.player1_invincibility_timer = 0
        self.player1_shield_active = False
        self.player1_shield_timer = 0
        self.player1_double_jump_available = False
        if self.coop_mode:
            self.player2_x = 250
            self.player2_y = self.virtual_height - PLAYER_SIZE - 10
            self.player2_vel_x = 0
            self.player2_vel_y = 0
            self.player2_is_jumping = False
            self.player2_is_crouching = False
            self.player2_was_on_ground = True
            self.player2_jump_timer = 0
            self.player2_jump_animation_timer = 0
            self.player2_death_animation_timer = 0
            self.player2_is_dead = False
            self.player2_lives = self.starting_lives
            self.player2_invincibility = False
            self.player2_invincibility_timer = 0
            self.player2_shield_active = False
            self.player2_shield_timer = 0
            self.player2_double_jump_available = False
        self.obstacles = []
        self.bonuses = []
        self.rain_particles.clear()
        self.splash_particles.clear()
        self.stars = [
            [
                random.randint(0, self.virtual_width),
                random.randint(0, self.virtual_height),
                random.randint(1, 3),
            ]
            for _ in range(STARFIELD_DENSITY)
        ]
        self.trail_particles.clear()
        self.buff_particles.clear()
        self.explosion_particles.clear()
        self.lasers.clear()
        self.fire_animations.clear()
        self.boss_active = False
        self.boss_x = self.virtual_width
        self.boss_y = self.virtual_height // 2 - BOSS_SIZE // 2
        self.boss_health = BOSS_MAX_HEALTH
        self.boss_alpha = 255
        self.boss_fade_timer = 0
        self.boss_spawn_timer = 0
        self.boss_projectiles = []
        self.boss_defeat_timer = 0
        self.bonus_notification = None
        self.bonus_notification_timer = 0
        self.milestone_flash = 0
        self.last_milestone = 0
        self.milestone_text_timer = 0
        self.current_milestone = 0
        self.difficulty_text_timer = 0
        self.current_difficulty_level = 0
        self.screamer_timer = SCREAMER_INTERVAL
        self.screamer_flash = 0
        self.score = 0
        self.high_score = 0
        self.spawn_timer = 0
        self.next_spawn_interval = 0
        self.double_points = False
        self.slow_down = False
        self.laser_active = False
        self.fire_active = False
        self.fire_timer = 0
        self.player_fire_spawn_timer = 0
        self.marihuana_active = False
        self.marihuana_timer = 0
        self.marihuana_anim_timer = 0
        self.score_multiplier = 1
        self.bonus_timer = 0
        self.game_over_timer = 0
        self.lightning_timer = 0
        self.lightning_flash = 0
        self.paused = False
        self.is_angel = False
        self.wing_flap_timer = 0
        self.music_stage = 0
        self.game_background = None
        self.initial_game_background = None
        self.toy_background = None
        self.blood_background = None
        self.game_over_image = None
        self.obstacle_texture = None
        self.screamer_image = None
        self.death_sound = None
        self.screamer_sound = None
        self.wing_image = None
        self.heart_image = None
        self.shield_image = None
        self.bonus_sound = None
        self.spike_texture = None
        self.points_image = None
        self.slow_image = None
        self.invincibility_image = None
        self.score_boost_image = None
        self.laser_image = None
        self.fire_buff_image = None
        self.fire_animation_image = None
        self.boss_image = None
        self.crest_image = None
        self.crest_frames = []
        self.crest_anim_timer = 0
        self.crest_anim_fps = 8
        self.monster_frames = []
        self.monster_anim_timer = 0
        self.monster_anim_fps = 8
        self.marihuana_frames = []
        self.hop_image = None
        self.wau_image = None
        self.zxc_image = None
        self.csk_image = None
        self.ricc_image = None
        self.dadep_image = None
        self.hoppe_image = None
        self.zvb_image = None
        self.volume_icon = None
        self.load_custom_icon = None
        self.help_icon = None
        self.help_background = None
        self.trap_image = None
        self.secret_image = None
        self.buff_particle_timer = 0
        self.score_timer = 0
        self.explosion_sound = None
        self.dr_sound = None
        self.laser_boss_timer = 0
        self.volume = 1.0
        self.slowdown_triggered = False
        self.slowdown_triggered2 = False
        self.slowdown_timer2 = 0
        self.q_sound = None
        self.q1_sound = None
        self.CHARACTERS = []
        self.char_bg_files = ["foog.jpg", "foog1.jpg", "foog2.jpg"]
        self.mode_bg_files = ["fff.png", "t.png", "tt.png", "ttt.png"]
        self.char_backgrounds = []
        self.mode_backgrounds = []
        self.char_current_background_index = 0
        self.char_next_background_index = 0
        self.char_background_timer = 0
        self.char_transition_timer = 0
        self.char_transition_alpha = 0
        self.mode_current_background_index = 0
        self.mode_next_background_index = 0
        self.mode_background_timer = 0
        self.mode_transition_alpha = 0
        self.mode_transition_timer = 0
        self.CHAR_BACKGROUND_SWITCH_INTERVAL = 7 * FPS
        self.MODE_BACKGROUND_SWITCH_INTERVAL = 5 * FPS
        self.MODES = [
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
        self.help_scroll_offset = 0
        self.help_scroll_speed = 20
        self.controls_scroll_offset = 0
        self.controls_scroll_speed = 20
        self.npc_backgrounds = []
        self.current_npc_index = 0
        self.told_images = []
        self.dvd_image = None
        self.dvd_active = False
        self.dvd_timer = 0
        self.ops_musics = ["ops.mp3", "ops1.mp3", "ops2.mp3", "ops3.mp3", "ops4.mp3"]
        self.current_ops_index = 0
        self.custom_loaded = False
        self.death_music_played = False
        self.keys_p1 = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "crouch": pygame.K_s,
        }
        self.keys_p2 = {
            "left": pygame.K_j,
            "right": pygame.K_l,
            "jump": pygame.K_i,
            "crouch": pygame.K_k,
        }
        self.remapping_active = False
        self.remapping_player = None
        self.remapping_action = None
        self.controls_state = "menu"
        self.load_high_score()
        self.load_controls()
        self.load_characters()
        self.load_music()
        self.set_all_volumes()
        self.sf_background = None
        self.sf1_image = None
        self.sf2_image = None
        self.tron_image = None
        self.sasha_image = None
        self.assets_loaded = False
        self.welcome_image = None
        self.welcome_frames = []
        self.welcome_frame_timer = 0
        self.welcome_fps = 10
        self.slowdown_timer = 0
        self.animation_timer = 0
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)
        # Skateboard selection
        self.selected_skateboard = 0  # индекс выбранного скейтборда
        self.skateboard_skins = []
        self.skateboard_images = []
        self.skateboard_default_colors = [
            (255, 0, 0),  # Red
            (0, 0, 255),  # Blue
            (0, 255, 0),  # Green
            (255, 255, 0),  # Yellow
            (255, 165, 0),  # Orange
        ]
        # Player skateboard states
        self.player1_trick_timer = 0
        self.player1_current_trick = None
        self.player1_skateboard_rotation = 0
        if self.coop_mode:
            self.player2_trick_timer = 0
            self.player2_current_trick = None
            self.player2_skateboard_rotation = 0
        self.skateboard_particle_timer = 0

    def quit_game(self):
        self.save_controls()
        pygame.quit()
        import sys

        sys.exit()

    def return_to_main_menu(self):
        self.state = "select_character"
        self.paused = False
        self.player1_is_dead = False
        self.player2_is_dead = False
        self.stop_music()
        self.play_music("rr.mp3")
        self.reset_game()
        self.coop_mode = False

    def trigger_death_music(self):
        if not self.death_music_played and (
            not self.coop_mode or (self.player1_is_dead and self.player2_is_dead)
        ):
            self.death_music_played = True
            if self.game_over_image:
                self.game_over_image.set_alpha(255)
            pygame.mixer.music.stop()
            self.play_music("dead.mp3")

    def update_game(self):
        slowdown_factor = (
            0.5
            if self.boss_defeat_timer > 0
            or self.slowdown_timer > 0
            or self.slowdown_timer2 > 0
            else 1.0
        )
        if not self.paused and (
            not self.player1_is_dead or (self.coop_mode and not self.player2_is_dead)
        ):
            if self.slowdown_timer > 0:
                self.slowdown_timer -= 1
            if self.boss_defeat_timer > 0:
                self.boss_defeat_timer -= 1
            if self.slowdown_timer2 > 0:
                self.slowdown_timer2 -= 1
            dvd_factor = 0.5 if self.dvd_active else 1.0
            effective_slowdown = slowdown_factor * dvd_factor
            if self.score >= 800 and not self.slowdown_triggered:
                self.slowdown_triggered = True
                self.slowdown_timer = 2 * FPS
                if self.q1_sound:
                    self.q1_sound.play()
            if self.score >= 1000 and not self.slowdown_triggered2:
                self.slowdown_triggered2 = True
                self.slowdown_timer2 = FPS
                if self.q1_sound:
                    self.q1_sound.play()
            if self.score >= ANGEL_THRESHOLD and not self.is_angel:
                self.is_angel = True
            if self.score // MILESTONE_INTERVAL > self.last_milestone:
                self.last_milestone = self.score // MILESTONE_INTERVAL
                self.trigger_milestone_effect()
                self.bonus_notification = "Бонусный щит активирован!"
                self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
                self.spawn_buff_particles(
                    self.player1_x + PLAYER_SIZE // 2,
                    self.player1_y + PLAYER_SIZE // 2,
                    "shield",
                )
            if self.score // DIFFICULTY_THRESHOLD > self.current_difficulty_level:
                self.trigger_difficulty_increase()
            if (
                self.score >= NPC_THRESHOLD
                and self.music_stage < 7
                and not self.death_music_played
            ):
                self.music_stage = 7
                self.current_ops_index = 0
                self.play_music(self.ops_musics[0])
            if self.score >= NPC_THRESHOLD and not self.death_music_played:
                ops_index = ((self.score - NPC_THRESHOLD) // NPC_INTERVAL) % len(
                    self.ops_musics
                )
                if ops_index != self.current_ops_index:
                    self.current_ops_index = ops_index
                    self.play_music(self.ops_musics[ops_index])
            elif (
                self.score >= 800
                and self.music_stage < 6
                and not self.death_music_played
            ):
                self.play_music("fos.mp3")
                self.music_stage = 6
            elif (
                self.score >= 400
                and self.music_stage < 5
                and not self.death_music_played
            ):
                self.play_music("dr.mp3")
                self.music_stage = 5
            elif (
                self.score >= 250
                and self.music_stage < 4
                and not self.death_music_played
            ):
                self.play_music("fon.mp3")
                self.music_stage = 4
            elif (
self.score >= 150
                and self.music_stage < 3
                and not self.death_music_played
            ):
                self.play_music("rrr.mp3")
                self.music_stage = 3
            if self.dvd_active:
                self.dvd_timer -= 1
                if self.dvd_timer <= 0:
                    self.dvd_active = False
            if self.marihuana_active:
                self.marihuana_timer -= 1
                if self.marihuana_timer <= 0:
                    self.marihuana_active = False
            # Timers managed only here now, removed from update_player
            self.player1_invincibility_timer -= (
                1 if self.player1_invincibility_timer > 0 else 0
            )
            if self.player1_invincibility_timer <= 0:
                self.player1_invincibility = False
            self.player2_invincibility_timer -= (
                1 if self.player2_invincibility_timer > 0 else 0
            )
            if self.player2_invincibility_timer <= 0:
                self.player2_invincibility = False
            self.player1_shield_timer -= 1 if self.player1_shield_timer > 0 else 0
            if self.player1_shield_timer <= 0:
                self.player1_shield_active = False
            self.player2_shield_timer -= 1 if self.player2_shield_timer > 0 else 0
            if self.player2_shield_timer <= 0:
                self.player2_shield_active = False
            if (
                BOSS_THRESHOLD_START <= self.score < BOSS_THRESHOLD_END
                and not self.boss_active
            ):
                self.obstacles.clear()
                self.boss_active = True
                self.boss_health = BOSS_MAX_HEALTH
                self.boss_x = self.virtual_width - BOSS_SIZE
                self.boss_alpha = 255
                self.boss_fade_timer = 0
                self.boss_spawn_timer = 0
            if self.score >= BOSS_THRESHOLD_END and self.boss_active:
                self.boss_fade_timer = BOSS_FADE_DURATION
                self.boss_active = False
                if self.boss_health > 0:
                    self.boss_defeated_effect_triggered = True
                    self.boss_defeat_timer = 5 * FPS
                    if self.q_sound:
                        self.q_sound.play()
                    self.bonus_notification = "Благословение!"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if self.boss_fade_timer > 0:
                self.boss_alpha = int(255 * (self.boss_fade_timer / BOSS_FADE_DURATION))
                self.boss_fade_timer -= 1
            if self.boss_active:
                self.boss_y += (
                    math.sin(self.animation_timer * BOSS_MOVEMENT_SPEED)
                    * 2
                    * slowdown_factor
                )
                self.boss_y = max(0, min(self.boss_y, self.virtual_height - BOSS_SIZE))
                self.boss_spawn_timer += slowdown_factor
                if self.boss_spawn_timer >= BOSS_SPAWN_INTERVAL:
                    self.boss_projectiles.append(self.spawn_boss_projectile())
                    self.boss_spawn_timer = 0
                    if int(self.animation_timer) % 400 == 0:
                        proj = self.spawn_boss_projectile()
                        proj[5] = proj[5] * 0.1  # Скорость в 10 раз медленнее
                        proj[6] = proj[6] * 0.1
                        proj[7] = self.ricc_image  # Используй ricc.png
                        self.boss_projectiles.append(proj)
            keys = pygame.key.get_pressed()
            # Update players
            (
                self.player1_x,
                self.player1_y,
                self.player1_vel_x,
                self.player1_vel_y,
                self.player1_is_jumping,
                self.player1_is_crouching,
                self.player1_was_on_ground,
                self.player1_jump_timer,
                self.player1_jump_animation_timer,
                self.player1_death_animation_timer,
                self.player1_is_dead,
                self.player1_lives,
                self.player1_invincibility,
                self.player1_invincibility_timer,
                self.player1_shield_active,
                self.player1_shield_timer,
                self.player1_double_jump_available,
            ) = self.update_player(
                self.player1_x,
                self.player1_y,
                self.player1_vel_x,
                self.player1_vel_y,
                self.player1_is_jumping,
                self.player1_is_crouching,
                self.player1_was_on_ground,
                self.player1_jump_timer,
                self.player1_jump_animation_timer,
                self.player1_death_animation_timer,
                self.player1_is_dead,
                self.player1_lives,
                self.player1_invincibility,
                self.player1_invincibility_timer,
                self.player1_shield_active,
                self.player1_shield_timer,
                self.player1_double_jump_available,
                keys,
                self.keys_p1,
                effective_slowdown,
            )
            if self.coop_mode:
                (
                    self.player2_x,
                    self.player2_y,
                    self.player2_vel_x,
                    self.player2_vel_y,
                    self.player2_is_jumping,
                    self.player2_is_crouching,
                    self.player2_was_on_ground,
                    self.player2_jump_timer,
                    self.player2_jump_animation_timer,
                    self.player2_death_animation_timer,
                    self.player2_is_dead,
                    self.player2_lives,
                    self.player2_invincibility,
                    self.player2_invincibility_timer,
                    self.player2_shield_active,
                    self.player2_shield_timer,
                    self.player2_double_jump_available,
                ) = self.update_player(
                    self.player2_x,
                    self.player2_y,
                    self.player2_vel_x,
                    self.player2_vel_y,
                    self.player2_is_jumping,
                    self.player2_is_crouching,
                    self.player2_was_on_ground,
                    self.player2_jump_timer,
                    self.player2_jump_animation_timer,
                    self.player2_death_animation_timer,
                    self.player2_is_dead,
                    self.player2_lives,
                    self.player2_invincibility,
                    self.player2_invincibility_timer,
                    self.player2_shield_active,
                    self.player2_shield_timer,
                    self.player2_double_jump_available,
                    keys,
                    self.keys_p2,
                    effective_slowdown,
                    True,
                )
            difficulty_level = self.score // DIFFICULTY_THRESHOLD
            spawn_interval_min = max(
                40, self.current_mode["spawn_interval"][0] - 10 * difficulty_level
            )
            spawn_interval_max = max(
                80, self.current_mode["spawn_interval"][1] - 20 * difficulty_level
            )
            self.spawn_timer += slowdown_factor
            should_spawn = self.spawn_timer >= self.next_spawn_interval and not (
                self.dvd_active and DVD_NO_SPAWN
            )
            if should_spawn:
                if not self.boss_active:
                    self.obstacles.append(self.spawn_obstacle())
                    if random.random() <= self.current_mode["bonus_chance"]:
                        bonus = self.spawn_bonus()
                        if bonus:
                            self.bonuses.append(bonus)
                self.spawn_timer = 0
                self.next_spawn_interval = random.randint(
                    spawn_interval_min, spawn_interval_max
                )
            current_obstacle_speed = self.current_mode["obstacle_speed"] * (
                0.3 if self.slow_down else 1.0
            )
            if self.current_mode["name"] != "Быстрый":
                current_obstacle_speed += self.score // 10 * 0.04
            self.update_obstacles(
                self.obstacles, current_obstacle_speed, slowdown_factor
            )
            self.update_obstacles(
                self.boss_projectiles, current_obstacle_speed, slowdown_factor
            )
            self.update_bonuses(self.bonuses, current_obstacle_speed, slowdown_factor)
            self.bonus_timer -= 1 if self.bonus_timer > 0 else 0
            if self.bonus_timer <= 0:
                self.double_points = False
                self.slow_down = False
                self.laser_active = False
                self.score_multiplier = 1
            self.fire_timer -= 1 if self.fire_active and self.fire_timer > 0 else 0
            if self.fire_timer <= 0:
                self.fire_active = False
            self.handle_fire_effect(effective_slowdown)
            self.buff_particle_timer += slowdown_factor
            if self.buff_particle_timer >= BUFF_PARTICLE_SPAWN_INTERVAL:
                self.buff_particle_timer = 0
                player_center_x = self.player1_x + PLAYER_SIZE // 2
                player_center_y = self.player1_y + PLAYER_SIZE // 2
                if self.double_points:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "double_points", 5
                    )
                if self.laser_active:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "laser", 5
                    )
                if self.score_multiplier > 1:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "score_boost", 5
                    )
                if self.player1_shield_active:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "shield", 5
                    )
                if self.fire_active:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "fire", 5
                    )
                if self.dvd_active:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "dvd", 5
                    )
                if self.marihuana_active:
                    self.spawn_buff_particles(
                        player_center_x, player_center_y, "marihuana", 5
                    )
            self.handle_laser_effect()
            self.update_boss_projectiles(slowdown_factor)
            self.handle_collisions()
            self.update_skateboard_trick(True)
            if self.coop_mode:
                self.update_skateboard_trick(False)
        self.boss_defeat_timer -= 1 if self.boss_defeat_timer > 0 else 0
        self.slowdown_timer -= 1 if self.slowdown_timer > 0 else 0
        self.slowdown_timer2 -= 1 if self.slowdown_timer2 > 0 else 0
        self.player1_death_animation_timer -= (
            1 if self.player1_death_animation_timer > 0 else 0
        )
        if self.coop_mode:
            self.player2_death_animation_timer -= (
                1 if self.player2_death_animation_timer > 0 else 0
            )
        if (
            self.player1_is_dead
            and self.player1_death_animation_timer <= 0
            and self.player1_lives <= 0
            and (
                not self.coop_mode
                or (
                    self.player2_is_dead
                    and self.player2_death_animation_timer <= 0
                    and self.player2_lives <= 0
                )
            )
        ):
            self.state = "game_over"
        if self.state == "playing" and not self.paused:
            self.score_timer += slowdown_factor
            if self.score_timer >= FPS:
                self.score += 1 * self.score_multiplier
                if self.double_points:
                    self.score += 1 * self.score_multiplier
                self.score_timer = 0
            if RAIN_THRESHOLD <= self.score < 200:
                self.spawn_rain()
        if self.state == "playing" and self.score >= SCREAMER_THRESHOLD:
            self.screamer_timer += slowdown_factor
            if self.screamer_timer >= SCREAMER_INTERVAL and random.random() < 0.001:
                self.trigger_screamer()
        self.animation_timer += slowdown_factor
        self.crest_anim_timer += 1
        self.monster_anim_timer += 1
        self.marihuana_anim_timer += 1
        self.update_rain(slowdown_factor)
        self.update_splash(slowdown_factor)
        self.update_buff_particles(slowdown_factor)
        self.update_explosion_particles(slowdown_factor)
        self.lightning_timer += slowdown_factor
        self.screamer_timer += slowdown_factor
        self.boss_spawn_timer += slowdown_factor
        self.wing_flap_timer += slowdown_factor

    def update_obstacles(self, obstacles, current_obstacle_speed, slowdown_factor):
        for obs in obstacles[:]:
            obs_type = obs[4]
            if obs_type == "spike":
                obs[0] -= current_obstacle_speed * slowdown_factor
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
            elif obs_type in ("falling", "ceiling"):
                delta = (obs[5] if obs_type == "falling" else -obs[5]) * slowdown_factor
                obs[1] += delta
                if obs[1] > self.virtual_height or obs[1] < -obs[3]:
                    obstacles.remove(obs)
                    points = (
                        2 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            elif obs_type == "trap":
                obs[0] -= obs[5] * slowdown_factor
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
                    points = (
                        3 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            elif obs_type == "zvb":
                obs[0] -= current_obstacle_speed * slowdown_factor
                obs[1] += math.sin(self.animation_timer * 0.1) * 2 * slowdown_factor
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
                    points = (
                        2 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            elif obs_type == "told":
                obs[0] -= obs[5] * slowdown_factor
                obs[1] += math.sin(obs[0] * 0.05) * 3 * slowdown_factor
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
                    points = (
                        3 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            elif obs_type == "flying":
                obs[0] -= obs[5] * slowdown_factor
                obs[1] += math.sin(obs[0] * 0.05) * 2 * slowdown_factor
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
                    points = (
                        2 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            else:
                obs[0] -= current_obstacle_speed * slowdown_factor
                if obs[0] < self.player1_x and not obs[6] and not obs[1] + obs[3]:
                    obs[6] = True
                    points = (
                        1 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
                if obs[0] < -obs[2]:
                    obstacles.remove(obs)
                    points = (
                        2 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
        # Limit obstacles
        if len(obstacles) > 50:
            obstacles[:] = obstacles[-50:]

    def update_bonuses(self, bonuses, current_obstacle_speed, slowdown_factor):
        for bonus in bonuses[:]:
            bonus[0] -= current_obstacle_speed * slowdown_factor
            if bonus[0] < -BONUS_SIZE:
                bonuses.remove(bonus)
            bonus_rect = pygame.Rect(bonus[0], bonus[1], BONUS_SIZE, BONUS_SIZE)
            player1_hitbox_w = PLAYER_SIZE * PLAYER_HITBOX_SCALE
            player1_hitbox_h = (
                PLAYER_SIZE
                * (0.5 if self.player1_is_crouching else 1.0)
                * PLAYER_HITBOX_SCALE
            )
            crouch_offset_p1 = PLAYER_SIZE * 0.5 if self.player1_is_crouching else 0
            player1_hitbox_x = self.player1_x + (PLAYER_SIZE - player1_hitbox_w) // 2
            player1_hitbox_y = (
                self.player1_y
                + (
                    (PLAYER_SIZE // 2 if self.player1_is_crouching else PLAYER_SIZE)
                    - player1_hitbox_h
                )
                // 2
                + crouch_offset_p1
            )
            player1_rect = pygame.Rect(
                player1_hitbox_x, player1_hitbox_y, player1_hitbox_w, player1_hitbox_h
            )
            if not self.player1_is_dead and player1_rect.colliderect(bonus_rect):
                (
                    self.player1_lives,
                    self.player1_invincibility,
                    self.player1_invincibility_timer,
                    self.player1_shield_active,
                    self.player1_shield_timer,
                ) = self.handle_bonus_pickup(
                    bonus,
                    player1_rect,
                    self.player1_lives,
                    self.player1_invincibility,
                    self.player1_invincibility_timer,
                    self.player1_shield_active,
                    self.player1_shield_timer,
                    True,
                )
            if self.coop_mode:
                player2_hitbox_w = PLAYER_SIZE * PLAYER_HITBOX_SCALE
                player2_hitbox_h = (
                    PLAYER_SIZE
                    * (0.5 if self.player2_is_crouching else 1.0)
                    * PLAYER_HITBOX_SCALE
                )
                player2_hitbox_x = (
                    self.player2_x + (PLAYER_SIZE - player2_hitbox_w) // 2
                )
                crouch_offset_p2 = PLAYER_SIZE * 0.5 if self.player2_is_crouching else 0
                player2_hitbox_y = (
                    self.player2_y
                    + (
                        (PLAYER_SIZE // 2 if self.player2_is_crouching else PLAYER_SIZE)
                        - player2_hitbox_h
                    )
                    // 2
                    + crouch_offset_p2
                )
                player2_rect = pygame.Rect(
                    player2_hitbox_x,
                    player2_hitbox_y,
                    player2_hitbox_w,
                    player2_hitbox_h,
                )
                if not self.player2_is_dead and player2_rect.colliderect(bonus_rect):
                    (
                        self.player2_lives,
                        self.player2_invincibility,
                        self.player2_invincibility_timer,
                        self.player2_shield_active,
                        self.player2_shield_timer,
                    ) = self.handle_bonus_pickup(
                        bonus,
                        player2_rect,
                        self.player2_lives,
                        self.player2_invincibility,
                        self.player2_invincibility_timer,
                        self.player2_shield_active,
                        self.player2_shield_timer,
                        False,
                    )
        # Limit bonuses
        if len(bonuses) > 20:
            bonuses[:] = bonuses[-20:]

    def handle_fire_effect(self, effective_slowdown=1.0):
        if self.fire_active:
            player_center = (
                self.player1_x + PLAYER_SIZE // 2,
                self.player1_y + PLAYER_SIZE // 2,
            )
            self.player_fire_spawn_timer += 1
            if (
                self.player_fire_spawn_timer
                % int(1 / PLAYER_FIRE_SPAWN_CHANCE * effective_slowdown)
                == 0
            ):
                for _ in range(3):
                    angle = random.uniform(0, 2 * math.pi)
                    offset_x = math.cos(angle) * PLAYER_SIZE / 2
                    offset_y = math.sin(angle) * PLAYER_SIZE / 2
                    self.fire_animations.append(
                        [
                            player_center[0] + offset_x - 25,
                            player_center[1] + offset_y - 25,
                            FIRE_ANIMATION_DURATION,
                        ]
                    )
            effective_fire_range = FIRE_RANGE * 2 if self.boss_active else FIRE_RANGE
            for obs in self.obstacles[:]:
                obs_center = (obs[0] + obs[2] // 2, obs[1] + obs[3] // 2)
                dist = math.hypot(
                    player_center[0] - obs_center[0], player_center[1] - obs_center[1]
                )
                if dist < effective_fire_range and random.random() < FIRE_BURN_CHANCE:
                    self.fire_animations.append(
                        [
                            obs_center[0] - 50,
                            obs_center[1] - 50,
                            FIRE_ANIMATION_DURATION,
                        ]
                    )
                    self.spawn_buff_particles(obs_center[0], obs_center[1], "fire")
                    self.obstacles.remove(obs)
                    self.score += (
                        self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
            if self.boss_active:
                boss_center = (
                    self.boss_x + BOSS_SIZE // 2,
                    self.boss_y + BOSS_SIZE // 2,
                )
                dist = math.hypot(
                    player_center[0] - boss_center[0], player_center[1] - boss_center[1]
                )
                if dist < effective_fire_range and random.random() < FIRE_BURN_CHANCE:
                    self.fire_animations.append(
                        [
                            boss_center[0] - 50,
                            boss_center[1] - 50,
                            FIRE_ANIMATION_DURATION,
                        ]
                    )
                    self.spawn_buff_particles(boss_center[0], boss_center[1], "fire")
                    self.boss_health -= BOSS_DAMAGE_FIRE
                    if self.boss_health <= 0:
                        self.boss_active = False
                        self.score += 100
                        self.boss_fade_timer = BOSS_FADE_DURATION
                        self.boss_defeat_timer = 5 * FPS
                        if self.q_sound:
                            self.q_sound.play()
                        self.bonus_notification = "Благословение!"
                        self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION

    def handle_laser_effect(self):
        if self.laser_active:
            player_center = (
                self.player1_x + PLAYER_SIZE // 2,
                self.player1_y
                + (PLAYER_SIZE // 2 if self.player1_is_crouching else PLAYER_SIZE // 2),
            )
            effective_laser_range = LASER_RANGE * 2 if self.boss_active else LASER_RANGE
            for obs in self.obstacles[:]:
                obs_center = (obs[0] + obs[2] // 2, obs[1] + obs[3] // 2)
                distance = math.hypot(
                    player_center[0] - obs_center[0], player_center[1] - obs_center[1]
                )
                if distance <= effective_laser_range:
                    self.lasers.append(
                        [
                            player_center[0],
                            player_center[1],
                            obs_center[0],
                            obs_center[1],
                            5,
                        ]
                    )
                    self.obstacles.remove(obs)
                    self.spawn_buff_particles(obs_center[0], obs_center[1], "laser")
                    points = (
                        1 * self.score_multiplier
                        if self.double_points
                        else self.score_multiplier
                    )
                    self.score += points
            if self.boss_active:
                boss_center = (
                    self.boss_x + BOSS_SIZE // 2,
                    self.boss_y + BOSS_SIZE // 2,
                )
                distance = math.hypot(
                    player_center[0] - boss_center[0], player_center[1] - boss_center[1]
                )
                if distance <= effective_laser_range and self.laser_boss_timer <= 0:
                    self.lasers.append(
                        [
                            player_center[0],
                            player_center[1],
                            boss_center[0],
                            boss_center[1],
                            5,
                        ]
                    )
                    self.boss_health -= BOSS_DAMAGE_LASER
                    self.spawn_buff_particles(boss_center[0], boss_center[1], "laser")
                    self.laser_boss_timer = LASER_BOSS_COOLDOWN
                    if self.boss_health <= 0:
                        self.boss_active = False
                        self.score += 100
                        self.boss_fade_timer = BOSS_FADE_DURATION
                        self.boss_defeat_timer = 5 * FPS
                        if self.q_sound:
                            self.q_sound.play()
                        self.bonus_notification = "Благословение!"
                        self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if self.laser_boss_timer > 0:
                self.laser_boss_timer -= 1
        # Limit lasers
        if len(self.lasers) > 20:
            self.lasers[:] = self.lasers[-20:]

    def update_boss_projectiles(self, slowdown_factor):
        for proj in self.boss_projectiles[:]:
            if self.coop_mode:
                if not self.player1_is_dead and not self.player2_is_dead:
                    target_x, target_y = self.player1_x, self.player1_y
                elif not self.player1_is_dead:
                    target_x, target_y = self.player1_x, self.player1_y
                elif not self.player2_is_dead:
                    target_x, target_y = self.player2_x, self.player2_y
                else:
                    target_x = random.randint(0, self.virtual_width)
                    target_y = random.randint(0, self.virtual_height)
            else:
                if not self.player1_is_dead:
                    target_x = self.player1_x
                    target_y = self.player1_y
                else:
                    target_x = random.randint(0, self.virtual_width)
                    target_y = random.randint(0, self.virtual_height)
            proj_x = proj[0]
            proj_y = proj[1]
            dx = target_x - proj_x
            dy = target_y - proj_y
            dist = math.hypot(dx, dy)
            if dist > 0:
                proj[5] = (dx / dist) * BOSS_PROJECTILE_SPEED
                proj[6] = (dy / dist) * BOSS_PROJECTILE_SPEED
            proj[0] += proj[5] * slowdown_factor
            proj[1] += proj[6] * slowdown_factor
            if proj[0] < -proj[2]:
                self.boss_projectiles.remove(proj)
        # Limit boss projectiles
        if len(self.boss_projectiles) > 20:
            self.boss_projectiles[:] = self.boss_projectiles[-20:]

    def handle_collisions(self):
        player1_hitbox_w = PLAYER_SIZE * PLAYER_HITBOX_SCALE
        player1_hitbox_h = (
            PLAYER_SIZE
            * (0.5 if self.player1_is_crouching else 1.0)
            * PLAYER_HITBOX_SCALE
        )
        crouch_offset_p1 = PLAYER_SIZE * 0.5 if self.player1_is_crouching else 0
        player1_hitbox_x = self.player1_x + (PLAYER_SIZE - player1_hitbox_w) // 2
        player1_hitbox_y = (
            self.player1_y
            + (
                (PLAYER_SIZE // 2 if self.player1_is_crouching else PLAYER_SIZE)
                - player1_hitbox_h
            )
            // 2
            + crouch_offset_p1
        )
        player1_rect = pygame.Rect(
            player1_hitbox_x, player1_hitbox_y, player1_hitbox_w, player1_hitbox_h
        )
        if self.coop_mode:
            player2_hitbox_w = PLAYER_SIZE * PLAYER_HITBOX_SCALE
            player2_hitbox_h = (
                PLAYER_SIZE
                * (0.5 if self.player2_is_crouching else 1.0)
                * PLAYER_HITBOX_SCALE
            )
            crouch_offset_p2 = PLAYER_SIZE * 0.5 if self.player2_is_crouching else 0
            player2_hitbox_x = self.player2_x + (PLAYER_SIZE - player2_hitbox_w) // 2
            player2_hitbox_y = (
                self.player2_y
                + (
                    (PLAYER_SIZE // 2 if self.player2_is_crouching else PLAYER_SIZE)
                    - player2_hitbox_h
                )
                // 2
                + crouch_offset_p2
            )
            player2_rect = pygame.Rect(
                player2_hitbox_x, player2_hitbox_y, player2_hitbox_w, player2_hitbox_h
            )
        # Single loop for boss projectiles to avoid duplication
        for proj in self.boss_projectiles[:]:
            proj_rect = pygame.Rect(
                proj[0] + (proj[2] - proj[2] * OBSTACLE_HITBOX_SCALE) // 2,
                proj[1] + (proj[3] - proj[3] * OBSTACLE_HITBOX_SCALE) // 2,
                proj[2] * OBSTACLE_HITBOX_SCALE,
                proj[3] * OBSTACLE_HITBOX_SCALE,
            )
            collided = False
            if not self.player1_is_dead and player1_rect.colliderect(proj_rect):
                collided = True
                if not (self.player1_invincibility or self.player1_shield_active):
                    if self.player1_lives > 1:
                        self.player1_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player1_lives = 0
                        self.player1_is_dead = True
                        self.player1_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if not self.coop_mode or self.player2_is_dead:
                            self.trigger_death_music()
                else:
                    self.player1_shield_active = False
                    self.player1_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player1_x + PLAYER_SIZE // 2,
                        self.player1_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Щит сломан!"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if (
                self.coop_mode
                and not self.player2_is_dead
                and player2_rect.colliderect(proj_rect)
            ):
                collided = True
                if not (self.player2_invincibility or self.player2_shield_active):
                    if self.player2_lives > 1:
                        self.player2_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player2_lives = 0
                        self.player2_is_dead = True
                        self.player2_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if self.player1_is_dead:
                            self.trigger_death_music()
                else:
                    self.player2_shield_active = False
                    self.player2_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player2_x + PLAYER_SIZE // 2,
                        self.player2_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Щит сломан!"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if collided:
                self.boss_projectiles.remove(proj)
        # Single loop for obstacles
        for obs in self.obstacles[:]:
            obs_rect = pygame.Rect(
                obs[0] + (obs[2] - obs[2] * OBSTACLE_HITBOX_SCALE) // 2,
                obs[1] + (obs[3] - obs[3] * OBSTACLE_HITBOX_SCALE) // 2,
                obs[2] * OBSTACLE_HITBOX_SCALE,
                obs[3] * OBSTACLE_HITBOX_SCALE,
            )
            collided = False
            if not self.player1_is_dead and player1_rect.colliderect(obs_rect):
                collided = True
                if not (self.player1_invincibility or self.player1_shield_active):
                    if self.player1_lives > 1:
                        self.player1_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player1_lives = 0
                        self.player1_is_dead = True
                        self.player1_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if not self.coop_mode or self.player2_is_dead:
                            self.trigger_death_music()
                else:
                    self.player1_shield_active = False
                    self.player1_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player1_x + PLAYER_SIZE // 2,
                        self.player1_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Щит сломан!"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if (
                self.coop_mode
                and not self.player2_is_dead
                and player2_rect.colliderect(obs_rect)
            ):
                collided = True
                if not (self.player2_invincibility or self.player2_shield_active):
                    if self.player2_lives > 1:
                        self.player2_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player2_lives = 0
                        self.player2_is_dead = True
                        self.player2_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if self.player1_is_dead:
                            self.trigger_death_music()
                else:
                    self.player2_shield_active = False
                    self.player2_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player2_x + PLAYER_SIZE // 2,
                        self.player2_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Щит сломан!"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if collided:
                self.obstacles.remove(obs)
        # Boss body
        if self.boss_active:
            boss_rect = pygame.Rect(self.boss_x, self.boss_y, BOSS_SIZE, BOSS_SIZE)
            collided = False
            if not self.player1_is_dead and player1_rect.colliderect(boss_rect):
                collided = True
                if not (self.player1_invincibility or self.player1_shield_active):
                    if self.player1_lives > 1:
                        self.player1_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player1_lives = 0
                        self.player1_is_dead = True
                        self.player1_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player1_x + PLAYER_SIZE // 2,
                            self.player1_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if not self.coop_mode or self.player2_is_dead:
                            self.trigger_death_music()
                else:
                    self.player1_shield_active = False
                    self.player1_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player1_x + PLAYER_SIZE // 2,
                        self.player1_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Бля"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION
            if (
                self.coop_mode
                and not self.player2_is_dead
                and player2_rect.colliderect(boss_rect)
            ):
                collided = True
                if not (self.player2_invincibility or self.player2_shield_active):
                    if self.player2_lives > 1:
                        self.player2_lives -= 1
                        if self.death_sound:
                            self.death_sound.play()
                        self.spawn_buff_particles(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                            "life",
                        )
                    else:
                        self.player2_lives = 0
                        self.player2_is_dead = True
                        self.player2_death_animation_timer = DEATH_ANIMATION_DURATION
                        self.spawn_explosion(
                            self.player2_x + PLAYER_SIZE // 2,
                            self.player2_y + PLAYER_SIZE // 2,
                        )
                        if self.death_sound:
                            self.death_sound.play()
                        if self.player1_is_dead:
                            self.trigger_death_music()
                else:
                    self.player2_shield_active = False
                    self.player2_shield_timer = 0
                    self.spawn_buff_particles(
                        self.player2_x + PLAYER_SIZE // 2,
                        self.player2_y + PLAYER_SIZE // 2,
                        "shield",
                    )
                    self.bonus_notification = "Бля"
                    self.bonus_notification_timer = BONUS_NOTIFICATION_DURATION

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.virtual_width, self.virtual_height)
            )
        # Preserve aspect ratio in fullscreen by adding black bars if needed
        # Note: This is a basic fix; for full letterboxing, adjust blit offset

    def get_scaled_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        screen_w, screen_h = self.screen.get_size()
        return (
            mouse_pos[0] * self.virtual_width / screen_w,
            mouse_pos[1] * self.virtual_height / screen_h,
        )

    def main(self):
        frame_count = 0
        while True:
            if not self.assets_loaded:
                self.load_assets()
                self.assets_loaded = True
            scaled_pos = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if (
                        self.state == "playing"
                        and event.key == self.keys_p1["jump"]
                        and not self.player1_is_crouching
                        and not self.player1_is_dead
                    ):
                        if self.player1_was_on_ground or (
                            self.player1_double_jump_available and self.is_angel
                        ):
                            self.player1_vel_y = self.current_mode["jump_force"]
                            self.player1_is_jumping = True
                            self.player1_jump_timer = 0
                            self.player1_jump_animation_timer = JUMP_ANIMATION_DURATION
                            self.start_skateboard_trick(True)  # ДОБАВЬ ЭТОТ СТРОКА
                            if not self.player1_was_on_ground:
                                self.player1_double_jump_available = False
                    elif (
                        self.coop_mode
                        and self.state == "playing"
                        and event.key == self.keys_p2["jump"]
                        and not self.player2_is_crouching
                        and not self.player2_is_dead
                    ):
                        if self.player2_was_on_ground or (
                            self.player2_double_jump_available and self.is_angel
                        ):
                            self.player2_vel_y = self.current_mode["jump_force"]
                            self.player2_is_jumping = True
                            self.player2_jump_timer = 0
                            self.player2_jump_animation_timer = JUMP_ANIMATION_DURATION
                            self.start_skateboard_trick(False)  # ДОБАВЬ ЭТОТ СТРОКА
                            if not self.player2_was_on_ground:
                                self.player2_double_jump_available = False
                    elif (
                        self.state == "playing"
                        and event.key == self.keys_p1["crouch"]
                        and self.player1_was_on_ground
                        and not self.player1_is_dead
                    ):
                        self.player1_is_crouching = True
                    elif (
                        self.coop_mode
                        and self.state == "playing"
                        and event.key == self.keys_p2["crouch"]
                        and self.player2_was_on_ground
                        and not self.player2_is_dead
                    ):
                        self.player2_is_crouching = True
                    elif (
                        event.key == pygame.K_p
                        and self.state == "playing"
                        and not self.player1_is_dead
                    ):

                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif (
                        event.key == pygame.K_ESCAPE
                        and self.state == "playing"
                        and not self.player1_is_dead
                    ):
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_ESCAPE and self.state == "help":
                        self.state = "select_character"
                        self.help_scroll_offset = 0
                    elif event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    if self.state == "welcome":
                        if event.key == pygame.K_RETURN:
                            self.state = "select_character"
                    if self.state == "controls" and self.remapping_active:
                        if self.remapping_player == "p1":
                            self.keys_p1[self.remapping_action] = event.key
                        else:
                            self.keys_p2[self.remapping_action] = event.key
                        self.remapping_active = False
                        self.remapping_player = None
                        self.remapping_action = None
                        self.save_controls()
                    if self.state == "help":
                        if event.key == pygame.K_UP:
                            self.help_scroll_offset += self.help_scroll_speed
                        elif event.key == pygame.K_DOWN:
                            self.help_scroll_offset -= self.help_scroll_speed
                        total_content_height = (
                            1300  # Adjusted for better scrolling range
                        )
                        max_scroll_offset = max(
                            0, -(total_content_height - self.virtual_height)
                        )
                        self.help_scroll_offset = min(
                            0, max(self.help_scroll_offset, -max_scroll_offset)
                        )
                    if self.state == "controls":
                        if event.key == pygame.K_UP:
                            self.controls_scroll_offset += self.controls_scroll_speed
                        elif event.key == pygame.K_DOWN:
                            self.controls_scroll_offset -= self.controls_scroll_speed
                        total_content_height = 1000  # Adjusted for controls content
                        max_scroll_offset = max(
                            0, -(total_content_height - self.virtual_height)
                        )
                        self.controls_scroll_offset = min(
                            0, max(self.controls_scroll_offset, -max_scroll_offset)
                        )
                elif event.type == pygame.KEYUP:
                    if (
                        self.state == "playing"
                        and event.key == self.keys_p1["jump"]
                        and not self.player1_is_dead
                    ):
                        self.player1_is_jumping = False
                    elif (
                        self.coop_mode
                        and self.state == "playing"
                        and event.key == self.keys_p2["jump"]
                        and not self.player2_is_dead
                    ):
                        self.player2_is_jumping = False
                    elif (
                        self.state == "playing"
                        and event.key == self.keys_p1["crouch"]
                        and not self.player1_is_dead
                    ):
                        self.player1_is_crouching = False
                    elif (
                        self.coop_mode
                        and self.state == "playing"
                        and event.key == self.keys_p2["crouch"]
                        and not self.player2_is_dead
                    ):
                        self.player2_is_crouching = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    scaled_pos = self.get_scaled_mouse_pos()
                    if self.state == "welcome":
                        play_rect, exit_rect = self.draw_welcome()
                        if play_rect.collidepoint(scaled_pos):
                            self.state = "select_character"
                        elif exit_rect.collidepoint(scaled_pos):
                            self.quit_game()
                    elif self.state == "select_character":
                        (
                            char_rects,
                            load_custom_rect,
                            controls_rect,
                            exit_rect,
                            vol_up_rect,
                            vol_down_rect,
                        ) = self.draw_character_select()
                        for i, rect in enumerate(char_rects):
                            if rect.collidepoint(scaled_pos):
                                if i < 2:
                                    self.selected_character = self.CHARACTERS[i]
                                    self.state = "select_mode"
                                elif i == 2:
                                    if self.custom_loaded and any(
                                        c.get("name") == "Custom"
                                        for c in self.CHARACTERS
                                    ):
                                        self.selected_character = next(
                                            c
                                            for c in self.CHARACTERS
                                            if c.get("name") == "Custom"
                                        )
                                        self.state = "select_mode"
                                    else:
                                        self.load_custom_image()
                        if load_custom_rect.collidepoint(scaled_pos):
                            self.load_custom_image()
                        if controls_rect.collidepoint(scaled_pos):
                            self.state = "controls"
                        if exit_rect.collidepoint(scaled_pos):
                            self.quit_game()
                        if vol_up_rect.collidepoint(scaled_pos):
                            self.adjust_volume(0.1)
                        elif vol_down_rect.collidepoint(scaled_pos):
                            self.adjust_volume(-0.1)
                        if self.help_icon:
                            help_rect = pygame.Rect(
                                10,
                                self.virtual_height - self.help_icon.get_height() - 10,
                                self.help_icon.get_width(),
                                self.help_icon.get_height(),
                            )
                            if help_rect.collidepoint(scaled_pos):
                                self.state = "help"

                    elif self.state == "controls":
                        p1_rects, p2_rects, back_rect = self.draw_controls()
                        if back_rect.collidepoint(scaled_pos):
                            self.state = "select_character"
                        for action, rect in p1_rects.items():
                            if rect.collidepoint(scaled_pos):
                                self.remapping_active = True
                                self.remapping_player = "p1"
                                self.remapping_action = action
                                break
                        for action, rect in p2_rects.items():
                            if rect.collidepoint(scaled_pos):
                                self.remapping_active = True
                                self.remapping_player = "p2"
                                self.remapping_action = action
                                break
                    elif self.state == "select_character2":
                        (
                            char_rects,
                            load_custom_rect,
                            back_rect,
                            vol_up_rect,
                            vol_down_rect,
                        ) = self.draw_select_character2()
                        for i, rect in enumerate(char_rects):
                            if rect.collidepoint(scaled_pos):
                                if i < 2:
                                    self.selected_character2 = self.CHARACTERS[i]
                                    self.current_mode = self.MODES[0]
                                    self.state = "playing"
                                    self.reset_game()
                                    self.play_music("r.mp3")
                                elif i == 2:
                                    if self.custom_loaded and any(
                                        c.get("name") == "Custom"
                                        for c in self.CHARACTERS
                                    ):
                                        self.selected_character2 = next(
                                            c
                                            for c in self.CHARACTERS
                                            if c.get("name") == "Custom"
                                        )
                                        self.current_mode = self.MODES[0]
                                        self.state = "playing"
                                        self.reset_game()
                                        self.play_music("r.mp3")
                                    else:
                                        self.load_custom_image()
                        if load_custom_rect.collidepoint(scaled_pos):
                            self.load_custom_image()
                        if back_rect.collidepoint(scaled_pos):
                            self.state = "select_mode"
                        if vol_up_rect.collidepoint(scaled_pos):
                            self.adjust_volume(0.1)
                        elif vol_down_rect.collidepoint(scaled_pos):
                            self.adjust_volume(-0.1)
                        if self.help_icon:
                            help_rect = pygame.Rect(
                                10,
                                self.virtual_height - self.help_icon.get_height() - 10,
                                self.help_icon.get_width(),
                                self.help_icon.get_height(),
                            )
                            if help_rect.collidepoint(scaled_pos):
                                self.state = "help"
                    elif self.state == "select_mode":
                        mode_rects, controls_rect, exit_rect = self.draw_select_mode()
                        for i, rect in enumerate(mode_rects):
                            if rect.collidepoint(scaled_pos):
                                if i < len(self.MODES):
                                    self.current_mode = self.MODES[i]
                                    self.coop_mode = False
                                    self.state = "playing"
                                    self.reset_game()
                                    self.play_music("r.mp3")
                                elif i == len(self.MODES):
                                    if not self.selected_character:
                                        self.selected_character = self.CHARACTERS[0]
                                    self.coop_mode = True
                                    self.current_mode = self.MODES[0]
                                    self.state = "select_character2"
                        if controls_rect.collidepoint(scaled_pos):
                            self.state = "controls"
                        if exit_rect.collidepoint(scaled_pos):
                            self.quit_game()
                    elif self.state == "playing" and self.paused:
                        resume_rect, exit_rect, vol_up_rect, vol_down_rect = (
                            self.draw_pause_screen()
                        )
                        if resume_rect.collidepoint(scaled_pos):
                            self.paused = False
                            pygame.mixer.music.unpause()
                        elif exit_rect.collidepoint(scaled_pos):
                            self.return_to_main_menu()
                        elif vol_up_rect.collidepoint(scaled_pos):
                            self.adjust_volume(0.1)
                        elif vol_down_rect.collidepoint(scaled_pos):
                            self.adjust_volume(-0.1)
                    elif self.state == "help":
                        exit_rect = self.draw_help_screen()
                        if exit_rect.collidepoint(scaled_pos):
                            self.state = "select_character"
                            self.help_scroll_offset = 0
                    elif self.state == "game_over":
                        retry_rect, exit_rect = self.draw_game_over()
                        if retry_rect.collidepoint(scaled_pos):
                            self.reset_game()
                            self.state = "playing"
                            self.play_music("r.mp3")
                        elif exit_rect.collidepoint(scaled_pos):
                            self.return_to_main_menu()
                    elif self.state == "select_mode":
                        (
                            skateboard_rects,
                            load_custom_rect,
                            next_rect,
                            back_rect,
                            vol_up_rect,
                            vol_down_rect,
                        ) = self.draw_skateboard_select()
                        for i, rect in enumerate(skateboard_rects):
                            if rect.collidepoint(scaled_pos):
                                self.selected_skateboard = i
                        if load_custom_rect.collidepoint(scaled_pos):
                            self.load_custom_skateboard()
                        if next_rect.collidepoint(scaled_pos):
                            self.state = "select_mode"
                        if back_rect.collidepoint(scaled_pos):
                            self.state = "select_character"
                        if vol_up_rect.collidepoint(scaled_pos):
                            self.adjust_volume(0.1)
                        elif vol_down_rect.collidepoint(scaled_pos):
                            self.adjust_volume(-0.1)
                elif event.type == pygame.MOUSEWHEEL:
                    if self.state == "help":
                        self.help_scroll_offset += event.y * self.help_scroll_speed
                        total_content_height = 1300
                        max_scroll_offset = max(
                            0, -(total_content_height - self.virtual_height)
                        )
                        self.help_scroll_offset = min(
                            0, max(self.help_scroll_offset, -max_scroll_offset)
                        )
                    elif self.state == "controls":
                        self.controls_scroll_offset += (
                            event.y * self.controls_scroll_speed
                        )
                        total_content_height = 1000
                        max_scroll_offset = max(
                            0, -(total_content_height - self.virtual_height)
                        )
                        self.controls_scroll_offset = min(
                            0, max(self.controls_scroll_offset, -max_scroll_offset)
                        )
            if frame_count % (FPS // 8) == 0:
                pygame.event.post(
                    pygame.event.Event(
                        pygame.MOUSEMOTION,
                        {"pos": (self.virtual_width // 2, self.virtual_height // 2)},
                    )
                )

            frame_count += 1
            if self.state == "welcome":
                self.draw_welcome()
            elif self.state == "select_character":
                self.draw_character_select()
            elif self.state == "controls":
                self.draw_controls()
            elif self.state == "select_character2":
                self.draw_select_character2()
            elif self.state == "select_mode":
                self.draw_select_mode()
            elif self.state == "playing":
                self.update_game()
                self.draw_game()
                if self.paused:
                    self.draw_pause_screen()
            elif self.state == "help":
                self.draw_help_screen()

            elif self.state == "select_mode":
                self.draw_skateboard_select()
            elif self.state == "select_mode":
                self.draw_select_mode()
            elif self.state == "game_over":
                self.save_high_score()
                self.draw_game_over()
            # Scale with aspect ratio preservation
            screen_w, screen_h = self.screen.get_size()
            if screen_w / screen_h > self.virtual_width / self.virtual_height:
                # Black bars on sides
                scale_w = screen_h * self.virtual_width / self.virtual_height
                scale_h = screen_h
                offset_x = (screen_w - scale_w) // 2
                scaled = pygame.transform.scale(
                    self.virtual_screen, (int(scale_w), int(scale_h))
                )
                self.screen.blit(scaled, (offset_x, 0))
                self.screen.fill((0, 0, 0), (0, 0, offset_x, screen_h))
                self.screen.fill(
                    (0, 0, 0),
                    (offset_x + scale_w, 0, screen_w - offset_x - scale_w, screen_h),
                )
            else:
                # Black bars top/bottom
                scale_h = screen_w * self.virtual_height / self.virtual_width
                scale_w = screen_w
                offset_y = (screen_h - scale_h) // 2
                scaled = pygame.transform.scale(
                    self.virtual_screen, (int(scale_w), int(scale_h))
                )
                self.screen.blit(scaled, (0, offset_y))
                self.screen.fill((0, 0, 0), (0, 0, screen_w, offset_y))
                self.screen.fill(
                    (0, 0, 0),
                    (0, offset_y + scale_h, screen_w, screen_h - offset_y - scale_h),
                )
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    print("=" * 30)
    print(" BISMILAH - Press ENTER to start!")
    print("=" * 30)
    try:
        input("Press ENTER to start...")
    except:
        pass  # If running without TTY
    game = Game()
    game.main()
