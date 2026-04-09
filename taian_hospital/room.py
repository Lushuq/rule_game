"""
《诡则像素：泰安医院》房间模块
Room类：平台风格房间数据、物体绘制、交互系统
"""

import pygame
import math
import random
from constants import (
    TILE_SIZE, VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLORS
)


class Interactable:
    def __init__(self, x, y, width, height, item_type, data=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.item_type = item_type
        self.data = data or {}
        self.interacted = False
        self.glow_phase = random.random() * math.pi * 2
    
    def get_glow_intensity(self, time_offset):
        return (math.sin(time_offset * 0.05 + self.glow_phase) + 1) / 2


class Room:
    def __init__(self, room_id, name):
        self.room_id = room_id
        self.name = name
        self.walls = []
        self.platforms = []
        self.interactables = []
        self.lights = []
        self.ambient_color = COLORS['dark_bg']
        
    def add_wall(self, rect):
        self.walls.append(rect)
        self.platforms.append(rect)
    
    def add_platform(self, rect):
        self.platforms.append(rect)
    
    def add_interactable(self, interactable):
        self.interactables.append(interactable)
    
    def add_light(self, x, y, radius, color, intensity=1.0):
        self.lights.append({
            'x': x, 'y': y, 'radius': radius,
            'color': color, 'intensity': intensity,
            'phase': random.random() * math.pi * 2
        })
    
    def draw(self, surface, time_offset, sanity=100):
        self._draw_background(surface, time_offset)
        self._draw_platforms(surface, time_offset)
        self._draw_interactables(surface, time_offset)
        self._draw_lights(surface, time_offset)
        self._draw_ambient_overlay(surface, sanity)
    
    def _draw_background(self, surface, time_offset):
        for y in range(VIRTUAL_HEIGHT):
            ratio = y / VIRTUAL_HEIGHT
            color = (
                int(COLORS['dark_bg'][0] * (1 - ratio * 0.2)),
                int(COLORS['dark_bg'][1] * (1 - ratio * 0.2)),
                int(COLORS['dark_bg'][2] * (1 - ratio * 0.2))
            )
            pygame.draw.line(surface, color, (0, y), (VIRTUAL_WIDTH, y))
        
        for y in range(0, VIRTUAL_HEIGHT, TILE_SIZE):
            for x in range(0, VIRTUAL_WIDTH, TILE_SIZE):
                tile_x = x // TILE_SIZE
                tile_y = y // TILE_SIZE
                
                if (tile_x + tile_y) % 2 == 0:
                    base_color = COLORS['floor_dark']
                else:
                    base_color = COLORS['floor_light']
                
                variation = int(math.sin(x * 0.3 + y * 0.2 + time_offset * 0.01) * 3)
                color = (
                    max(0, min(255, base_color[0] + variation)),
                    max(0, min(255, base_color[1] + variation)),
                    max(0, min(255, base_color[2] + variation))
                )
                
                pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE), 1)
    
    def _draw_platforms(self, surface, time_offset):
        for wall in self.walls:
            self._draw_detailed_wall(surface, wall, time_offset)
        
        for platform in self.platforms:
            if platform not in self.walls:
                self._draw_detailed_platform(surface, platform, time_offset)
    
    def _draw_detailed_wall(self, surface, rect, time_offset):
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                base_color = COLORS['wall_dark']
                
                if rel_y < 2:
                    color = COLORS['wall_light']
                elif rel_y == 2:
                    color = (
                        COLORS['wall_dark'][0] + 10,
                        COLORS['wall_dark'][1] + 10,
                        COLORS['wall_dark'][2] + 15
                    )
                elif rel_y == rect.height - 1:
                    color = COLORS['shadow']
                else:
                    noise = int(math.sin(rel_x * 0.5 + rel_y * 0.3) * 5)
                    color = (
                        max(0, min(255, base_color[0] + noise)),
                        max(0, min(255, base_color[1] + noise)),
                        max(0, min(255, base_color[2] + noise + 5))
                    )
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
    
    def _draw_detailed_platform(self, surface, rect, time_offset):
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                base_color = COLORS['wall_dark']
                
                if rel_y < 2:
                    color = COLORS['wall_light']
                elif rel_y == 2:
                    color = (
                        COLORS['wall_dark'][0] + 8,
                        COLORS['wall_dark'][1] + 8,
                        COLORS['wall_dark'][2] + 12
                    )
                else:
                    noise = int(math.sin(rel_x * 0.5) * 3)
                    color = (
                        max(0, min(255, base_color[0] + noise)),
                        max(0, min(255, base_color[1] + noise)),
                        max(0, min(255, base_color[2] + noise + 3))
                    )
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
    
    def _draw_interactables(self, surface, time_offset):
        for item in self.interactables:
            if item.item_type == 'note':
                self._draw_note(surface, item, time_offset)
            elif item.item_type == 'tv':
                self._draw_tv(surface, item, time_offset)
            elif item.item_type == 'ghost_whisper':
                self._draw_ghost_whisper(surface, item, time_offset)
    
    def _draw_note(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                color = COLORS['note_paper']
                
                if rel_y < 1 or rel_y > rect.height - 2:
                    color = (200, 195, 180)
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
        
        glow = item.get_glow_intensity(time_offset)
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        for radius in range(15, 0, -2):
            alpha = int(20 * glow * (1 - radius / 15))
            pygame.draw.rect(glow_surface, (*COLORS['glow_white'][:3], alpha),
                           (rect.left - radius//2, rect.top - radius//2,
                            rect.width + radius, rect.height + radius))
        surface.blit(glow_surface, (0, 0))
    
    def _draw_tv(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                if rel_x < 2 or rel_x > rect.width - 3 or rel_y < 2 or rel_y > rect.height - 3:
                    color = (40, 40, 45)
                else:
                    if random.random() < 0.3:
                        color = (
                            COLORS['tv_static'][0] + random.randint(-30, 30),
                            COLORS['tv_static'][1] + random.randint(-30, 30),
                            COLORS['tv_static'][2] + random.randint(-30, 30)
                        )
                    else:
                        color = COLORS['tv_off']
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
        
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        flicker = 0.3 + random.random() * 0.7
        for radius in range(30, 0, -2):
            alpha = int(15 * flicker * (1 - radius / 30))
            pygame.draw.ellipse(glow_surface, (*COLORS['glow_cold'][:3], alpha),
                              (rect.centerx - radius, rect.centery - radius,
                               radius * 2, radius * 2))
        surface.blit(glow_surface, (0, 0))
    
    def _draw_ghost_whisper(self, surface, item, time_offset):
        if item.interacted:
            return
        
        rect = item.rect
        alpha = int((math.sin(time_offset * 0.1 + item.glow_phase) + 1) * 60)
        
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        for radius in range(20, 0, -2):
            a = int(alpha * (1 - radius / 20))
            pygame.draw.circle(glow_surface, (*COLORS['glow_green'][:3], a),
                             rect.center, radius)
        
        surface.blit(glow_surface, (0, 0))
    
    def _draw_lights(self, surface, time_offset):
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        for light in self.lights:
            pulse = (math.sin(time_offset * 0.05 + light['phase']) + 1) / 2
            intensity = light['intensity'] * (0.7 + pulse * 0.3)
            
            for radius in range(light['radius'], 0, -3):
                alpha = int(20 * intensity * (1 - radius / light['radius']))
                color = (*light['color'][:3], min(alpha, 255))
                pygame.draw.circle(glow_surface, color,
                                 (light['x'], light['y']), radius)
        
        surface.blit(glow_surface, (0, 0))
    
    def _draw_ambient_overlay(self, surface, sanity):
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        if sanity < 70:
            alpha = int((70 - sanity) * 1.5)
            overlay.fill((100, 20, 20, min(alpha, 100)))
        
        for _ in range(max(0, (100 - sanity) // 10)):
            x = random.randint(0, VIRTUAL_WIDTH - 1)
            y = random.randint(0, VIRTUAL_HEIGHT - 1)
            overlay.set_at((x, y), (50, 0, 0, 30))
        
        surface.blit(overlay, (0, 0))
    
    def check_interactable(self, interaction_rect):
        for item in self.interactables:
            if interaction_rect.colliderect(item.rect):
                return item
        return None


def create_platform_level():
    room = Room('hospital', 'Taian Hospital')
    
    room.add_wall(pygame.Rect(0, 0, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, VIRTUAL_HEIGHT - TILE_SIZE, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    room.add_wall(pygame.Rect(VIRTUAL_WIDTH - TILE_SIZE, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    
    room.add_platform(pygame.Rect(60, 180, 80, TILE_SIZE))
    room.add_platform(pygame.Rect(180, 160, 80, TILE_SIZE))
    room.add_platform(pygame.Rect(80, 130, 70, TILE_SIZE))
    room.add_platform(pygame.Rect(200, 100, 80, TILE_SIZE))
    
    room.add_interactable(Interactable(
        100, 100, 16, 14, 'note',
        {'text': 'Note: Don\'t believe everything you see.', 'rule_hint': 'note1'}
    ))
    
    room.add_interactable(Interactable(
        200, 70, 20, 16, 'tv',
        {'text': 'TV: Welcome to Taian Hospital.', 'rule_hint': 'tv1'}
    ))
    
    room.add_interactable(Interactable(
        250, 130, 12, 12, 'ghost_whisper',
        {'text': 'Whisper: Be careful here...', 'rule_hint': 'whisper1'}
    ))
    
    room.add_light(50, 50, 60, COLORS['glow_warm'], 0.5)
    room.add_light(280, 60, 50, COLORS['glow_cold'], 0.4)
    room.add_light(160, 200, 70, COLORS['glow_warm'], 0.3)
    
    return room


ROOMS = {
    'hospital': create_platform_level,
}


def get_room(room_id):
    if room_id in ROOMS:
        return ROOMS[room_id]()
    return None
