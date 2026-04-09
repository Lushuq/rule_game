"""
《诡则像素：泰安医院》玩家模块
Player类：移动、碰撞检测、像素绘制
"""

import pygame
import math
import random
from constants import (
    PLAYER_SPEED, PLAYER_WIDTH, PLAYER_HEIGHT, TILE_SIZE,
    COLORS, VIRTUAL_WIDTH, VIRTUAL_HEIGHT
)


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.facing = 'down'
        self.anim_frame = 0
        self.anim_timer = 0
        self.is_moving = False
        self.flashlight_on = True
        self.interaction_range = 20
        
    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )
    
    def get_feet_rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y),
            self.width,
            self.height // 2
        )
    
    def move(self, dx, dy, walls, game_time):
        if dx == 0 and dy == 0:
            self.is_moving = False
            return
        
        self.is_moving = True
        
        if abs(dx) > abs(dy):
            self.facing = 'right' if dx > 0 else 'left'
        else:
            self.facing = 'down' if dy > 0 else 'up'
        
        new_x = self.x + dx * PLAYER_SPEED
        new_y = self.y + dy * PLAYER_SPEED
        
        test_rect = pygame.Rect(
            int(new_x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )
        
        can_move_x = True
        for wall in walls:
            if test_rect.colliderect(wall):
                can_move_x = False
                break
        
        if can_move_x:
            self.x = new_x
        
        test_rect = pygame.Rect(
            int(self.x - self.width // 2),
            int(new_y - self.height // 2),
            self.width,
            self.height
        )
        
        can_move_y = True
        for wall in walls:
            if test_rect.colliderect(wall):
                can_move_y = False
                break
        
        if can_move_y:
            self.y = new_y
        
        self.x = max(self.width // 2, min(VIRTUAL_WIDTH - self.width // 2, self.x))
        self.y = max(self.height // 2, min(VIRTUAL_HEIGHT - self.height // 2, self.y))
        
        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % 4
    
    def draw(self, surface, camera_x=0, camera_y=0, sanity=100, time_offset=0):
        draw_x = int(self.x - self.width // 2)
        draw_y = int(self.y - self.height // 2)
        
        bob_offset = 0
        if self.is_moving:
            bob_offset = int(math.sin(self.anim_frame * math.pi / 2) * 1)
        
        body_color = COLORS['skin']
        hair_color = (40, 30, 25)
        shirt_color = (60, 70, 90)
        pants_color = (45, 45, 55)
        
        if sanity < 50:
            desat = sanity / 50
            body_color = self._desaturate(body_color, desat)
            hair_color = self._desaturate(hair_color, desat)
            shirt_color = self._desaturate(shirt_color, desat)
            pants_color = self._desaturate(pants_color, desat)
        
        for py in range(-1, 15):
            for px in range(-1, 13):
                pixel_color = self._get_pixel_color(px, py, body_color, hair_color, shirt_color, pants_color, bob_offset)
                if pixel_color:
                    surface.set_at((draw_x + px, draw_y + py + bob_offset), pixel_color)
        
        if self.flashlight_on:
            self._draw_flashlight_glow(surface, draw_x, draw_y, bob_offset, time_offset)
    
    def _get_pixel_color(self, px, py, body_color, hair_color, shirt_color, pants_color, bob_offset):
        hair_pattern = [
            (4, -1), (5, -1), (6, -1), (7, -1),
            (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),
            (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
        ]
        
        face_pattern = [
            (4, 2), (5, 2), (6, 2), (7, 2),
            (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
            (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
            (4, 5), (5, 5), (6, 5), (7, 5),
        ]
        
        eyes_pattern = [(5, 3), (6, 3)]
        mouth_pattern = [(5, 5), (6, 5)]
        
        body_pattern = [
            (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
            (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7),
            (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8),
            (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9),
        ]
        
        legs_pattern = [
            (4, 10), (5, 10), (6, 10), (7, 10),
            (4, 11), (5, 11), (6, 11), (7, 11),
            (4, 12), (5, 12), (7, 12), (8, 12),
            (4, 13), (5, 13), (7, 13), (8, 13),
        ]
        
        shoes_pattern = [
            (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14),
        ]
        
        if (px, py) in hair_pattern:
            return hair_color
        elif (px, py) in face_pattern:
            return body_color
        elif (px, py) in eyes_pattern:
            return (20, 20, 30)
        elif (px, py) in mouth_pattern:
            return (150, 100, 100)
        elif (px, py) in body_pattern:
            return shirt_color
        elif (px, py) in legs_pattern:
            return pants_color
        elif (px, py) in shoes_pattern:
            return (30, 30, 35)
        
        return None
    
    def _desaturate(self, color, factor):
        r, g, b = color
        gray = (r + g + b) // 3
        return (
            int(r * factor + gray * (1 - factor)),
            int(g * factor + gray * (1 - factor)),
            int(b * factor + gray * (1 - factor))
        )
    
    def _draw_flashlight_glow(self, surface, draw_x, draw_y, bob_offset, time_offset):
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        center_x = draw_x + 6
        center_y = draw_y + 6 + bob_offset
        
        pulse = math.sin(time_offset * 0.1) * 0.1 + 1.0
        
        for radius in range(60, 0, -2):
            alpha = int(15 * (1 - radius / 60) * pulse)
            color = (*COLORS['glow_warm'][:3], min(alpha, 255))
            pygame.draw.circle(glow_surface, color, (center_x, center_y), radius)
        
        surface.blit(glow_surface, (0, 0))
    
    def get_interaction_rect(self):
        if self.facing == 'up':
            return pygame.Rect(self.x - 10, self.y - 25, 20, 15)
        elif self.facing == 'down':
            return pygame.Rect(self.x - 10, self.y + 5, 20, 15)
        elif self.facing == 'left':
            return pygame.Rect(self.x - 25, self.y - 10, 15, 20)
        else:
            return pygame.Rect(self.x + 5, self.y - 10, 15, 20)
