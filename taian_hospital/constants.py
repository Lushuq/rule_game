"""
《诡则像素：泰安医院》常量定义模块
定义分辨率、颜色、缩放等核心常量
"""

VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 240
WINDOW_SCALE = 2
WINDOW_WIDTH = VIRTUAL_WIDTH * WINDOW_SCALE
WINDOW_HEIGHT = VIRTUAL_HEIGHT * WINDOW_SCALE

TILE_SIZE = 16

FPS = 60

COLORS = {
    'black': (0, 0, 0),
    'dark_bg': (8, 12, 18),
    'wall_dark': (25, 30, 40),
    'wall_light': (45, 50, 65),
    'floor_dark': (15, 18, 25),
    'floor_light': (22, 26, 35),
    'white': (255, 255, 255),
    'gray': (128, 128, 128),
    'dark_gray': (64, 64, 64),
    'red': (180, 40, 40),
    'bright_red': (255, 60, 60),
    'green': (40, 180, 80),
    'bright_green': (80, 255, 120),
    'blue': (40, 80, 180),
    'bright_blue': (80, 140, 255),
    'cyan': (60, 200, 220),
    'bright_cyan': (100, 255, 255),
    'yellow': (220, 200, 60),
    'bright_yellow': (255, 240, 100),
    'purple': (140, 60, 180),
    'bright_purple': (200, 100, 255),
    'orange': (220, 140, 40),
    'skin': (220, 180, 160),
    'blood': (120, 20, 20),
    'glow_white': (200, 220, 255),
    'glow_warm': (255, 200, 120),
    'glow_cold': (120, 180, 255),
    'glow_green': (120, 255, 150),
    'glow_red': (255, 100, 100),
    'sanity_high': (100, 255, 150),
    'sanity_mid': (255, 200, 80),
    'sanity_low': (255, 80, 80),
    'notebook_bg': (40, 35, 50),
    'notebook_border': (80, 70, 100),
    'text_normal': (200, 200, 210),
    'text_dim': (120, 120, 140),
    'text_highlight': (255, 255, 200),
    'text_rule': (255, 220, 150),
    'text_danger': (255, 100, 100),
    'text_clue': (150, 220, 255),
    'door': (60, 50, 40),
    'door_frame': (90, 75, 60),
    'bed_frame': (70, 60, 55),
    'bed_sheet': (180, 175, 170),
    'desk': (55, 45, 40),
    'tv_off': (30, 30, 35),
    'tv_static': (100, 100, 110),
    'note_paper': (230, 225, 210),
    'shadow': (5, 8, 12),
}

PLAYER_SPEED = 1.2
PLAYER_WIDTH = 12
PLAYER_HEIGHT = 14

MAX_SANITY = 100
SANITY_DECAY_RATE = 0.015
SANITY_VIOLATION_PENALTY = 15

GAME_STATE_TITLE = 0
GAME_STATE_PLAYING = 1
GAME_STATE_NOTEBOOK = 2
GAME_STATE_GAMEOVER = 3
GAME_STATE_VICTORY = 4

NIGHT_DURATION = 180
