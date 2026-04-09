"""
《诡则像素：泰安医院》主程序
主循环、简单游戏状态管理
"""

import pygame
import math
import random
import sys

from constants import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_SCALE, FPS, COLORS, TILE_SIZE,
    MAX_SANITY, SANITY_DECAY_RATE,
    GAME_STATE_TITLE, GAME_STATE_PLAYING, GAME_STATE_NOTEBOOK,
    GAME_STATE_GAMEOVER, GAME_STATE_VICTORY, NIGHT_DURATION
)
from player import Player
from room import get_room
from notebook import Notebook


class Game:
    def __init__(self):
        pygame.init()
        
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pixel Hospital - First Night")
        
        self.virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.time_offset = 0
        
        self.state = GAME_STATE_TITLE
        self.sanity = MAX_SANITY
        self.night_time = 0
        
        self.player = None
        self.current_room = None
        self.notebook = Notebook()
        
        self.screen_shake = 0
        self.color_shift = 0
        self.violation_flash = 0
        
        self.message = ""
        self.message_timer = 0
        
        self._init_game()
    
    def _init_game(self):
        self.player = Player(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 50)
        self.current_room = get_room('hospital')
        self.sanity = MAX_SANITY
        self.night_time = 0
        self.notebook = Notebook()
        self.message = ""
        self.message_timer = 0
        self.screen_shake = 0
        self.color_shift = 0
        self.violation_flash = 0
    
    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GAME_STATE_TITLE:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.state = GAME_STATE_PLAYING
                        self._init_game()
                
                elif self.state == GAME_STATE_PLAYING:
                    if event.key == pygame.K_TAB:
                        self.state = GAME_STATE_NOTEBOOK
                    
                    elif event.key == pygame.K_e:
                        self._handle_interaction()
                
                elif self.state == GAME_STATE_NOTEBOOK:
                    if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                        self.state = GAME_STATE_PLAYING
                
                elif self.state in [GAME_STATE_GAMEOVER, GAME_STATE_VICTORY]:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.state = GAME_STATE_TITLE
    
    def _handle_interaction(self):
        interaction_rect = self.player.get_interaction_rect()
        item = self.current_room.check_interactable(interaction_rect)
        
        if item and not item.interacted:
            item.interacted = True
            
            data = item.data
            text = data.get('text', 'Something interesting...')
            self._show_message(text)
            self.notebook.add_clue(text, item.item_type)
            
            if item.item_type == 'ghost_whisper':
                self.sanity -= 5
                self.screen_shake = 5
                self.color_shift = 0.5
    
    def _show_message(self, text):
        self.message = text
        self.message_timer = 180
    
    def _update(self):
        self.time_offset += 1
        
        if self.state == GAME_STATE_PLAYING:
            self._update_playing()
        
        if self.screen_shake > 0:
            self.screen_shake -= 0.5
        if self.color_shift > 0:
            self.color_shift -= 0.02
        if self.violation_flash > 0:
            self.violation_flash -= 5
    
    def _update_playing(self):
        keys = pygame.key.get_pressed()
        
        self.player.update(keys, self.current_room.platforms)
        
        self.sanity -= SANITY_DECAY_RATE
        self.sanity = max(0, self.sanity)
        
        self.night_time += 1 / FPS
        
        if self.message_timer > 0:
            self.message_timer -= 1
        
        if self.sanity <= 0:
            self.state = GAME_STATE_GAMEOVER
        
        if self.night_time >= NIGHT_DURATION:
            self.state = GAME_STATE_VICTORY
    
    def _render(self):
        self.virtual_surface.fill(COLORS['dark_bg'])
        
        if self.state == GAME_STATE_TITLE:
            self._render_title()
        elif self.state == GAME_STATE_PLAYING:
            self._render_playing()
        elif self.state == GAME_STATE_NOTEBOOK:
            self._render_playing()
            self.notebook.draw(self.virtual_surface, self.time_offset)
        elif self.state == GAME_STATE_GAMEOVER:
            self._render_gameover()
        elif self.state == GAME_STATE_VICTORY:
            self._render_victory()
        
        self._apply_horror_effects()
        
        scaled_surface = pygame.transform.scale(
            self.virtual_surface,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        
        self.window.blit(scaled_surface, (0, 0))
        pygame.display.flip()
    
    def _render_title(self):
        self._draw_gradient_bg()
        
        title = "PIXEL HOSPITAL"
        subtitle = "Taian Hospital"
        self._draw_big_text(title, VIRTUAL_WIDTH // 2, 60, COLORS['bright_red'])
        self._draw_big_text(subtitle, VIRTUAL_WIDTH // 2, 90, COLORS['text_highlight'])
        
        pygame.draw.line(self.virtual_surface, COLORS['text_dim'],
                        (60, 110), (VIRTUAL_WIDTH - 60, 110), 1)
        
        intro_lines = [
            "You wake up in a strange room...",
            "There are strange rules on the wall.",
            "Every rule has a hidden truth.",
            "Some rules are real, some are lies.",
            "Breaking rules will cost your sanity.",
            "",
            "Survive the night to escape."
        ]
        
        y = 130
        for line in intro_lines:
            self._draw_text(line, VIRTUAL_WIDTH // 2, y, COLORS['text_normal'], center=True)
            y += 12
        
        pulse = (math.sin(self.time_offset * 0.05) + 1) / 2
        color = (
            int(COLORS['text_highlight'][0] * pulse + COLORS['text_dim'][0] * (1 - pulse)),
            int(COLORS['text_highlight'][1] * pulse + COLORS['text_dim'][1] * (1 - pulse)),
            int(COLORS['text_highlight'][2] * pulse + COLORS['text_dim'][2] * (1 - pulse))
        )
        self._draw_text("[Press Enter to Start]", VIRTUAL_WIDTH // 2, 220, color, center=True)
        
        self._draw_text("A/D or Left/Right: Move  W/Up/Space: Jump  E: Interact", 
                       VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 10, COLORS['text_dim'], center=True)
    
    def _render_playing(self):
        self.current_room.draw(self.virtual_surface, self.time_offset, self.sanity)
        self.player.draw(self.virtual_surface, 0, 0, self.sanity, self.time_offset)
        
        self._draw_ui()
        
        if self.message_timer > 0:
            self._draw_message()
    
    def _draw_gradient_bg(self):
        for y in range(VIRTUAL_HEIGHT):
            ratio = y / VIRTUAL_HEIGHT
            color = (
                int(COLORS['dark_bg'][0] * (1 - ratio * 0.3)),
                int(COLORS['dark_bg'][1] * (1 - ratio * 0.3)),
                int(COLORS['dark_bg'][2] * (1 - ratio * 0.3))
            )
            pygame.draw.line(self.virtual_surface, color, (0, y), (VIRTUAL_WIDTH, y))
    
    def _draw_ui(self):
        self._draw_sanity_bar()
        self._draw_time_indicator()
        self._draw_room_name()
        self._draw_interaction_hint()
    
    def _draw_sanity_bar(self):
        bar_width = 80
        bar_height = 6
        x = 10
        y = 10
        
        pygame.draw.rect(self.virtual_surface, COLORS['dark_gray'],
                        (x - 1, y - 1, bar_width + 2, bar_height + 2))
        
        fill_width = int(bar_width * (self.sanity / MAX_SANITY))
        
        if self.sanity > 70:
            color = COLORS['sanity_high']
        elif self.sanity > 40:
            color = COLORS['sanity_mid']
        else:
            pulse = (math.sin(self.time_offset * 0.2) + 1) / 2
            color = (
                int(COLORS['sanity_low'][0] * pulse + 150 * (1 - pulse)),
                int(COLORS['sanity_low'][1] * pulse),
                int(COLORS['sanity_low'][2] * pulse)
            )
        
        pygame.draw.rect(self.virtual_surface, color, (x, y, fill_width, bar_height))
        
        self._draw_text("SAN", x + bar_width + 5, y, COLORS['text_dim'])
    
    def _draw_time_indicator(self):
        progress = min(1.0, self.night_time / NIGHT_DURATION)
        
        x = VIRTUAL_WIDTH - 50
        y = 10
        radius = 12
        
        pygame.draw.circle(self.virtual_surface, COLORS['dark_gray'], (x, y + radius), radius + 1)
        
        fill_angle = int(360 * progress)
        if fill_angle > 0:
            pygame.draw.arc(self.virtual_surface, COLORS['bright_cyan'],
                          (x - radius + 2, y + 2, radius * 2 - 4, radius * 2 - 4),
                          math.radians(-90), math.radians(-90 + fill_angle), 2)
        
        self._draw_text("TIME", x - 12, y + radius - 4, COLORS['text_dim'])
    
    def _draw_room_name(self):
        name = self.current_room.name
        self._draw_text(name, VIRTUAL_WIDTH // 2, 10, COLORS['text_dim'], center=True)
    
    def _draw_interaction_hint(self):
        interaction_rect = self.player.get_interaction_rect()
        item = self.current_room.check_interactable(interaction_rect)
        
        if item:
            hint = "[E] "
            if item.item_type == 'note':
                hint += "Read Note"
            elif item.item_type == 'tv':
                hint += "Check TV"
            elif item.item_type == 'ghost_whisper':
                hint += "Listen"
            else:
                hint += "Interact"
            
            self._draw_text(hint, VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 15,
                          COLORS['text_highlight'], center=True)
    
    def _draw_message(self):
        if not self.message:
            return
        
        lines = self._wrap_text(self.message, 35)
        box_height = len(lines) * 10 + 16
        box_y = VIRTUAL_HEIGHT - box_height - 20
        
        box_surface = pygame.Surface((VIRTUAL_WIDTH - 20, box_height), pygame.SRCALPHA)
        box_surface.fill((*COLORS['black'][:3], 180))
        
        self.virtual_surface.blit(box_surface, (10, box_y))
        
        pygame.draw.rect(self.virtual_surface, COLORS['text_dim'],
                        (10, box_y, VIRTUAL_WIDTH - 20, box_height), 1)
        
        y = box_y + 8
        for line in lines:
            self._draw_text(line, VIRTUAL_WIDTH // 2, y, COLORS['text_highlight'], center=True)
            y += 10
    
    def _render_gameover(self):
        self._draw_gradient_bg()
        
        self._draw_big_text("GAME OVER", VIRTUAL_WIDTH // 2, 80, COLORS['bright_red'])
        
        self._draw_text("The hospital consumed you...", VIRTUAL_WIDTH // 2, 120,
                       COLORS['text_dim'], center=True)
        
        pygame.draw.line(self.virtual_surface, COLORS['text_dim'],
                        (60, 140), (VIRTUAL_WIDTH - 60, 140), 1)
        
        self._draw_text("Clues found: " + str(len(self.notebook.clues)),
                       VIRTUAL_WIDTH // 2, 160, COLORS['text_normal'], center=True)
        
        pulse = (math.sin(self.time_offset * 0.05) + 1) / 2
        self._draw_text("[Press Enter to Restart]", VIRTUAL_WIDTH // 2, 210,
                       COLORS['text_dim'], center=True)
    
    def _render_victory(self):
        self._draw_gradient_bg()
        
        glow = (math.sin(self.time_offset * 0.1) + 1) / 2
        color = (
            int(COLORS['bright_yellow'][0] * glow + COLORS['bright_green'][0] * (1 - glow)),
            int(COLORS['bright_yellow'][1] * glow + COLORS['bright_green'][1] * (1 - glow)),
            int(COLORS['bright_yellow'][2] * glow + COLORS['bright_green'][2] * (1 - glow))
        )
        
        self._draw_big_text("SURVIVED!", VIRTUAL_WIDTH // 2, 60, color)
        self._draw_big_text("First Night", VIRTUAL_WIDTH // 2, 90, COLORS['text_highlight'])
        
        pygame.draw.line(self.virtual_surface, COLORS['text_dim'],
                        (60, 110), (VIRTUAL_WIDTH - 60, 110), 1)
        
        self._draw_text("You made it through the night...", VIRTUAL_WIDTH // 2, 130,
                       COLORS['text_normal'], center=True)
        
        self._draw_text("Clues found: " + str(len(self.notebook.clues)),
                       VIRTUAL_WIDTH // 2, 170, COLORS['text_normal'], center=True)
        
        self._draw_text("[Press Enter to Return]", VIRTUAL_WIDTH // 2, 210,
                       COLORS['text_dim'], center=True)
    
    def _apply_horror_effects(self):
        if self.screen_shake > 0:
            shake_x = int(random.uniform(-self.screen_shake, self.screen_shake))
            shake_y = int(random.uniform(-self.screen_shake, self.screen_shake))
            
            temp_surface = self.virtual_surface.copy()
            self.virtual_surface.fill(COLORS['black'])
            self.virtual_surface.blit(temp_surface, (shake_x, shake_y))
        
        if self.color_shift > 0:
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            alpha = int(self.color_shift * 50)
            overlay.fill((100, 0, 0, alpha))
            self.virtual_surface.blit(overlay, (0, 0))
        
        if self.violation_flash > 0:
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, self.violation_flash))
            self.virtual_surface.blit(overlay, (0, 0))
    
    def _draw_text(self, text, x, y, color, center=False):
        char_width = 6
        char_height = 8
        
        if center:
            x = x - (len(text) * char_width) // 2
        
        for i, char in enumerate(text):
            char_x = x + i * char_width
            self._draw_char(self.virtual_surface, char, char_x, y, color)
    
    def _draw_big_text(self, text, x, y, color):
        char_width = 10
        char_height = 14
        
        x = x - (len(text) * char_width) // 2
        
        for i, char in enumerate(text):
            char_x = x + i * char_width
            self._draw_large_char(self.virtual_surface, char, char_x, y, color)
    
    def _draw_char(self, surface, char, x, y, color):
        patterns = self._get_char_patterns()
        pattern = patterns.get(char, [[2],[2],[2],[2],[2]])
        
        for row_idx, row in enumerate(pattern):
            for col in row:
                px = x + col
                py = y + row_idx
                if 0 <= px < VIRTUAL_WIDTH and 0 <= py < VIRTUAL_HEIGHT:
                    surface.set_at((px, py), color)
    
    def _draw_large_char(self, surface, char, x, y, color):
        patterns = self._get_char_patterns()
        pattern = patterns.get(char, [[2],[2],[2],[2],[2]])
        
        scale = 2
        
        for row_idx, row in enumerate(pattern):
            for col in row:
                for dy in range(scale):
                    for dx in range(scale):
                        px = x + col * scale + dx
                        py = y + row_idx * scale + dy
                        if 0 <= px < VIRTUAL_WIDTH and 0 <= py < VIRTUAL_HEIGHT:
                            surface.set_at((px, py), color)
    
    def _get_char_patterns(self):
        return {
            'A': [[1,2,3],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            'B': [[0,1,2,3],[0,4],[0,1,2,3],[0,4],[0,1,2,3]],
            'C': [[1,2,3],[0],[0],[0],[1,2,3]],
            'D': [[0,1,2],[0,3],[0,3],[0,3],[0,1,2]],
            'E': [[0,1,2,3,4],[0],[0,1,2,3],[0],[0,1,2,3,4]],
            'F': [[0,1,2,3,4],[0],[0,1,2,3],[0],[0]],
            'G': [[1,2,3,4],[0],[0,3,4],[0,4],[1,2,3]],
            'H': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            'I': [[0,1,2],[1],[1],[1],[0,1,2]],
            'J': [[0,1,2,3,4],[4],[4],[0,4],[1,2,3]],
            'K': [[0,3],[0,2],[0,1],[0,2],[0,3]],
            'L': [[0],[0],[0],[0],[0,1,2,3,4]],
            'M': [[0,4],[0,1,3,4],[0,2,4],[0,4],[0,4]],
            'N': [[0,4],[0,1,4],[0,2,4],[0,3,4],[0,4]],
            'O': [[1,2,3],[0,4],[0,4],[0,4],[1,2,3]],
            'P': [[0,1,2,3],[0,4],[0,1,2,3],[0],[0]],
            'Q': [[1,2,3],[0,4],[0,4],[0,3,4],[1,2,3,4]],
            'R': [[0,1,2,3],[0,4],[0,1,2,3],[0,3],[0,4]],
            'S': [[1,2,3,4],[0],[1,2,3],[4],[0,1,2,3]],
            'T': [[0,1,2,3,4],[2],[2],[2],[2]],
            'U': [[0,4],[0,4],[0,4],[0,4],[1,2,3]],
            'V': [[0,4],[0,4],[0,4],[1,3],[2]],
            'W': [[0,4],[0,4],[0,2,4],[0,1,3,4],[0,4]],
            'X': [[0,4],[1,3],[2],[1,3],[0,4]],
            'Y': [[0,4],[1,3],[2],[2],[2]],
            'Z': [[0,1,2,3,4],[3],[2],[1],[0,1,2,3,4]],
            'a': [[],[1,2,3],[0,4],[0,1,2,3,4],[0,4]],
            'b': [[0],[0],[0,1,2,3],[0,4],[0,1,2,3]],
            'c': [[],[1,2,3],[0],[0],[1,2,3]],
            'd': [[4],[4],[1,2,3,4],[0,4],[1,2,3,4]],
            'e': [[],[1,2,3],[0,1,2,3,4],[0],[1,2,3]],
            'f': [[1,2,3],[0],[0,1,2],[0],[0]],
            'g': [[1,2,3,4],[0,4],[1,2,3],[4],[1,2,3]],
            'h': [[0],[0],[0,1,2,3],[0,4],[0,4]],
            'i': [[1],[1],[],[1],[1]],
            'j': [[2],[2],[],[2],[1]],
            'k': [[0,3],[0,2],[0,1],[0,2],[0,3]],
            'l': [[0],[0],[0],[0],[0]],
            'm': [[],[0,1,2,3,4],[0,2,4],[0,4],[0,4]],
            'n': [[],[0,1,2,3],[0,4],[0,4],[0,4]],
            'o': [[],[1,2,3],[0,4],[0,4],[1,2,3]],
            'p': [[0,1,2,3],[0,4],[0,1,2,3],[0],[0]],
            'q': [[1,2,3],[0,4],[0,4],[0,3,4],[1,2,3,4]],
            'r': [[],[0,1,2,3],[0,4],[0],[0]],
            's': [[],[1,2,3,4],[0],[4],[1,2,3]],
            't': [[0,1,2],[1],[1],[1],[1]],
            'u': [[],[0,4],[0,4],[0,4],[1,2,3,4]],
            'v': [[],[0,4],[0,4],[1,3],[2]],
            'w': [[],[0,4],[0,2,4],[0,1,3,4],[0,1,2,3,4]],
            'x': [[],[0,4],[1,3],[1,3],[0,4]],
            'y': [[0,4],[1,3],[2],[2],[2]],
            'z': [[],[0,1,2,3,4],[2],[3],[0,1,2,3,4]],
            '0': [[1,2,3],[0,3,4],[0,2,4],[0,1,4],[1,2,3]],
            '1': [[1,2],[0,2],[2],[2],[0,1,2,3,4]],
            '2': [[0,1,2,3],[4],[1,2,3],[0],[0,1,2,3,4]],
            '3': [[0,1,2,3],[4],[1,2,3],[4],[0,1,2,3]],
            '4': [[0,4],[0,4],[0,1,2,3,4],[4],[4]],
            '5': [[0,1,2,3,4],[0],[0,1,2,3],[4],[0,1,2,3]],
            '6': [[1,2,3],[0],[0,1,2,3],[0,4],[1,2,3]],
            '7': [[0,1,2,3,4],[4],[3],[2],[1]],
            '8': [[1,2,3],[0,4],[1,2,3],[0,4],[1,2,3]],
            '9': [[1,2,3],[0,4],[0,1,2,3,4],[4],[1,2,3]],
            ' ': [],
            '.': [[],[],[],[],[2]],
            ',': [[],[],[],[1],[0]],
            ':': [[],[2],[],[2],[]],
            '!': [[2],[2],[2],[],[2]],
            '?': [[0,1,2],[3],[1,2],[],[1]],
            '-': [[],[],[1,2,3],[],[]],
            '_': [[],[],[],[],[0,1,2,3,4]],
            '(': [[1,2],[0],[0],[0],[1,2]],
            ')': [[1,2],[4],[4],[4],[1,2]],
            '[': [[1,2,3],[0],[0],[0],[1,2,3]],
            ']': [[1,2,3],[3],[3],[3],[1,2,3]],
            '/': [[4],[3],[2],[1],[0]],
            '\\': [[0],[1],[2],[3],[4]],
            '"': [[0,2],[],[],[],[]],
            '\'': [[1],[],[],[],[]],
            '+': [[],[2],[1,2,3],[2],[]],
            '=': [[],[1,2,3],[],[1,2,3],[]],
            '<': [[3],[2],[1],[2],[3]],
            '>': [[1],[2],[3],[2],[1]],
        }
    
    def _wrap_text(self, text, max_chars):
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
