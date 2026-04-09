"""
《诡则像素：泰安医院》房间模块
Room类：房间数据、碰撞检测、物体绘制、交互系统
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


class Door:
    def __init__(self, x, y, target_room, target_x, target_y, direction='horizontal'):
        self.rect = pygame.Rect(x, y, TILE_SIZE if direction == 'vertical' else TILE_SIZE * 2,
                                TILE_SIZE * 2 if direction == 'vertical' else TILE_SIZE)
        self.target_room = target_room
        self.target_x = target_x
        self.target_y = target_y
        self.direction = direction
        self.is_open = False
        self.glow_phase = random.random() * math.pi * 2


class Room:
    def __init__(self, room_id, name):
        self.room_id = room_id
        self.name = name
        self.walls = []
        self.doors = []
        self.interactables = []
        self.lights = []
        self.floor_tiles = []
        self.ambient_color = COLORS['dark_bg']
        self.has_flicker = False
        self.flicker_timer = 0
        
    def add_wall(self, rect):
        self.walls.append(rect)
    
    def add_door(self, door):
        self.doors.append(door)
    
    def add_interactable(self, interactable):
        self.interactables.append(interactable)
    
    def add_light(self, x, y, radius, color, intensity=1.0):
        self.lights.append({
            'x': x, 'y': y, 'radius': radius,
            'color': color, 'intensity': intensity,
            'phase': random.random() * math.pi * 2
        })
    
    def draw(self, surface, time_offset, sanity=100):
        self._draw_floor(surface, time_offset)
        self._draw_walls(surface, time_offset)
        self._draw_doors(surface, time_offset)
        self._draw_interactables(surface, time_offset)
        self._draw_lights(surface, time_offset)
        self._draw_ambient_overlay(surface, sanity)
    
    def _draw_floor(self, surface, time_offset):
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
                
                pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))
                
                if random.random() < 0.02:
                    stain_color = (
                        min(255, color[0] + 5),
                        min(255, color[1] + 3),
                        color[2]
                    )
                    stain_x = x + random.randint(2, TILE_SIZE - 4)
                    stain_y = y + random.randint(2, TILE_SIZE - 4)
                    surface.set_at((stain_x, stain_y), stain_color)
    
    def _draw_walls(self, surface, time_offset):
        for wall in self.walls:
            self._draw_detailed_wall(surface, wall, time_offset)
    
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
        
        for i in range(0, rect.width, 32):
            crack_x = rect.left + i + random.randint(5, 20)
            crack_y = rect.top + random.randint(5, rect.height - 5)
            if crack_x < rect.right and crack_y < rect.bottom:
                if 0 <= crack_x < VIRTUAL_WIDTH and 0 <= crack_y < VIRTUAL_HEIGHT:
                    surface.set_at((crack_x, crack_y), COLORS['shadow'])
    
    def _draw_doors(self, surface, time_offset):
        for door in self.doors:
            self._draw_detailed_door(surface, door, time_offset)
    
    def _draw_detailed_door(self, surface, door, time_offset):
        rect = door.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                is_edge = (rel_x == 0 or rel_x == rect.width - 1 or 
                          rel_y == 0 or rel_y == rect.height - 1)
                
                if is_edge:
                    color = COLORS['door_frame']
                else:
                    grain = int(math.sin(rel_y * 0.3) * 8)
                    color = (
                        max(0, min(255, COLORS['door'][0] + grain)),
                        max(0, min(255, COLORS['door'][1] + grain)),
                        max(0, min(255, COLORS['door'][2] + grain))
                    )
                
                if rel_x == rect.width - 3 and abs(rel_y - rect.height // 2) < 2:
                    color = (180, 150, 50)
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
        
        glow_intensity = (math.sin(time_offset * 0.08 + door.glow_phase) + 1) / 2
        glow_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        for radius in range(20, 0, -2):
            alpha = int(10 * glow_intensity * (1 - radius / 20))
            pygame.draw.rect(glow_surface, (*COLORS['glow_cold'][:3], alpha),
                           (rect.left - radius//2, rect.top - radius//2,
                            rect.width + radius, rect.height + radius))
        
        surface.blit(glow_surface, (0, 0))
    
    def _draw_interactables(self, surface, time_offset):
        for item in self.interactables:
            if item.item_type == 'note':
                self._draw_note(surface, item, time_offset)
            elif item.item_type == 'tv':
                self._draw_tv(surface, item, time_offset)
            elif item.item_type == 'bed':
                self._draw_bed(surface, item, time_offset)
            elif item.item_type == 'desk':
                self._draw_desk(surface, item, time_offset)
            elif item.item_type == 'ghost_whisper':
                self._draw_ghost_whisper(surface, item, time_offset)
            elif item.item_type == 'clock':
                self._draw_clock(surface, item, time_offset)
            elif item.item_type == 'cabinet':
                self._draw_cabinet(surface, item, time_offset)
    
    def _draw_note(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                color = COLORS['note_paper']
                
                if rel_y < 2 or rel_y > rect.height - 3:
                    color = (200, 195, 180)
                
                if rel_y > 3 and rel_y < rect.height - 3:
                    if rel_x > 2 and rel_x < rect.width - 2:
                        if rel_y % 3 == 0:
                            color = (150, 145, 140)
                
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
    
    def _draw_bed(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                if rel_y < 3:
                    color = COLORS['bed_frame']
                elif rel_y < 6:
                    color = (80, 70, 65)
                else:
                    wave = int(math.sin(rel_x * 0.2) * 3)
                    color = (
                        COLORS['bed_sheet'][0] + wave,
                        COLORS['bed_sheet'][1] + wave,
                        COLORS['bed_sheet'][2] + wave
                    )
                
                if rel_x < 2 or rel_x > rect.width - 3:
                    color = COLORS['bed_frame']
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
    
    def _draw_desk(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                if rel_y < 3:
                    grain = int(math.sin(rel_x * 0.5) * 5)
                    color = (
                        COLORS['desk'][0] + grain + 15,
                        COLORS['desk'][1] + grain + 12,
                        COLORS['desk'][2] + grain + 10
                    )
                else:
                    color = COLORS['desk']
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
    
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
    
    def _draw_clock(self, surface, item, time_offset):
        rect = item.rect
        center_x = rect.centerx
        center_y = rect.centery
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                if dist > rect.width // 2:
                    continue
                
                if dist > rect.width // 2 - 2:
                    color = (60, 55, 50)
                else:
                    color = (30, 28, 25)
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
        
        angle = time_offset * 0.05
        hand_len = rect.width // 3
        hand_x = int(center_x + math.cos(angle) * hand_len)
        hand_y = int(center_y + math.sin(angle) * hand_len)
        pygame.draw.line(surface, COLORS['bright_red'], 
                        (center_x, center_y), (hand_x, hand_y), 1)
    
    def _draw_cabinet(self, surface, item, time_offset):
        rect = item.rect
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_x = x - rect.left
                rel_y = y - rect.top
                
                grain = int(math.sin(rel_x * 0.3 + rel_y * 0.2) * 5)
                base = COLORS['desk']
                color = (
                    max(0, min(255, base[0] + grain)),
                    max(0, min(255, base[1] + grain)),
                    max(0, min(255, base[2] + grain))
                )
                
                if rel_y == rect.height // 2:
                    color = (40, 35, 30)
                
                if 0 <= x < VIRTUAL_WIDTH and 0 <= y < VIRTUAL_HEIGHT:
                    surface.set_at((x, y), color)
    
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
    
    def check_door_collision(self, player_rect):
        for door in self.doors:
            if player_rect.colliderect(door.rect):
                return door
        return None
    
    def check_interactable(self, interaction_rect):
        for item in self.interactables:
            if interaction_rect.colliderect(item.rect):
                return item
        return None


def create_patient_room():
    room = Room('patient_room', '病房 101')
    
    room.add_wall(pygame.Rect(0, 0, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, VIRTUAL_HEIGHT - TILE_SIZE, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    room.add_wall(pygame.Rect(VIRTUAL_WIDTH - TILE_SIZE, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    
    room.add_door(Door(
        VIRTUAL_WIDTH - TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE,
        'corridor', TILE_SIZE * 2, VIRTUAL_HEIGHT // 2,
        'vertical'
    ))
    
    room.add_interactable(Interactable(
        40, 50, 40, 24, 'bed'
    ))
    
    room.add_interactable(Interactable(
        200, 40, 20, 16, 'note',
        {'text': '便条：午夜后不要看镜子，除非你带着红色的东西...', 'rule_hint': 'mirror_rule'}
    ))
    
    room.add_interactable(Interactable(
        220, 80, 24, 20, 'cabinet',
        {'text': '柜子里有一件红色外套', 'item': 'red_coat'}
    ))
    
    room.add_interactable(Interactable(
        100, 150, 16, 16, 'ghost_whisper',
        {'text': '低语："灯光下安全...但不要让它们看到你..."', 'rule_hint': 'light_rule'}
    ))
    
    room.add_light(160, 120, 60, COLORS['glow_warm'], 0.6)
    room.add_light(60, 80, 40, COLORS['glow_warm'], 0.4)
    
    return room


def create_corridor():
    room = Room('corridor', '走廊')
    
    room.add_wall(pygame.Rect(0, 0, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, VIRTUAL_HEIGHT - TILE_SIZE, VIRTUAL_WIDTH, TILE_SIZE))
    
    room.add_wall(pygame.Rect(0, 0, TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE))
    room.add_wall(pygame.Rect(0, VIRTUAL_HEIGHT // 2 + TILE_SIZE, TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE))
    
    room.add_wall(pygame.Rect(VIRTUAL_WIDTH - TILE_SIZE, 0, TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE))
    room.add_wall(pygame.Rect(VIRTUAL_WIDTH - TILE_SIZE, VIRTUAL_HEIGHT // 2 + TILE_SIZE, TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE))
    
    room.add_door(Door(
        0, VIRTUAL_HEIGHT // 2 - TILE_SIZE,
        'patient_room', VIRTUAL_WIDTH - TILE_SIZE * 3, VIRTUAL_HEIGHT // 2,
        'vertical'
    ))
    
    room.add_door(Door(
        VIRTUAL_WIDTH - TILE_SIZE, VIRTUAL_HEIGHT // 2 - TILE_SIZE,
        'nurse_station', TILE_SIZE * 2, VIRTUAL_HEIGHT // 2,
        'vertical'
    ))
    
    room.add_interactable(Interactable(
        80, 30, 24, 20, 'tv',
        {'text': '电视闪烁着画面...隐约显示："当钟声响起，必须静止不动"', 'rule_hint': 'clock_rule'}
    ))
    
    room.add_interactable(Interactable(
        200, 35, 12, 12, 'clock',
        {'text': '时钟的指针在疯狂旋转...'}
    ))
    
    room.add_interactable(Interactable(
        150, VIRTUAL_HEIGHT - TILE_SIZE - 20, 16, 12, 'note',
        {'text': '地上的便条：有些规则是假的。相信你的直觉。', 'rule_hint': 'meta_rule'}
    ))
    
    room.add_light(80, 60, 50, COLORS['glow_cold'], 0.5)
    room.add_light(200, 60, 40, COLORS['glow_cold'], 0.4)
    room.add_light(160, VIRTUAL_HEIGHT - 40, 35, COLORS['glow_warm'], 0.3)
    
    room.has_flicker = True
    
    return room


def create_nurse_station():
    room = Room('nurse_station', '护士站')
    
    room.add_wall(pygame.Rect(0, 0, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, VIRTUAL_HEIGHT - TILE_SIZE, VIRTUAL_WIDTH, TILE_SIZE))
    room.add_wall(pygame.Rect(0, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    room.add_wall(pygame.Rect(VIRTUAL_WIDTH - TILE_SIZE, 0, TILE_SIZE, VIRTUAL_HEIGHT))
    
    room.add_door(Door(
        0, VIRTUAL_HEIGHT // 2 - TILE_SIZE,
        'corridor', VIRTUAL_WIDTH - TILE_SIZE * 3, VIRTUAL_HEIGHT // 2,
        'vertical'
    ))
    
    room.add_interactable(Interactable(
        160, 60, 48, 24, 'desk',
        {'text': '护士站的桌上有一本日志...'}
    ))
    
    room.add_interactable(Interactable(
        170, 45, 18, 14, 'note',
        {'text': '日志条目：第三条规则是谎言。记住，第三条是谎言。', 'rule_hint': 'rule3_lie'}
    ))
    
    room.add_interactable(Interactable(
        50, 80, 16, 16, 'ghost_whisper',
        {'text': '低语："红色保护你...但也会引来它们..."', 'rule_hint': 'red_paradox'}
    ))
    
    room.add_interactable(Interactable(
        250, 100, 20, 16, 'note',
        {'text': '墙上的告示：午夜时分，所有灯光都会熄灭。那时...不要呼吸。', 'rule_hint': 'midnight_rule'}
    ))
    
    room.add_light(160, 80, 70, COLORS['glow_warm'], 0.7)
    room.add_light(60, 100, 40, COLORS['glow_green'], 0.3)
    
    return room


ROOMS = {
    'patient_room': create_patient_room,
    'corridor': create_corridor,
    'nurse_station': create_nurse_station,
}


def get_room(room_id):
    if room_id in ROOMS:
        return ROOMS[room_id]()
    return None
