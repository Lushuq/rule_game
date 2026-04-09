"""
《诡则像素：泰安医院》笔记本模块
Notebook类：规则记录、线索整理界面
"""

import pygame
import math
from constants import (
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT, COLORS
)


class Rule:
    def __init__(self, rule_id, text, is_true=True, discovered=False, evolved_text=None):
        self.rule_id = rule_id
        self.text = text
        self.is_true = is_true
        self.discovered = discovered
        self.evolved_text = evolved_text
        self.evolution_discovered = False
    
    def get_display_text(self):
        if self.evolution_discovered and self.evolved_text:
            return self.evolved_text
        return self.text


class Notebook:
    def __init__(self):
        self.rules = {}
        self.clues = []
        self.items = []
        self.current_page = 0
        self.scroll_offset = 0
        self._init_rules()
    
    def _init_rules(self):
        self.rules = {
            'rule1': Rule(
                'rule1',
                'Rule 1: Be careful what you see.',
                is_true=True
            ),
            'rule2': Rule(
                'rule2', 
                'Rule 2: Lights are safe.',
                is_true=True
            ),
            'rule3': Rule(
                'rule3',
                'Rule 3: When the bell rings, stay still.',
                is_true=False,
                evolved_text='Rule 3 (false): When the bell rings, MOVE!'
            ),
        }
    
    def discover_rule(self, rule_id):
        if rule_id in self.rules:
            self.rules[rule_id].discovered = True
    
    def evolve_rule(self, rule_id):
        if rule_id in self.rules and self.rules[rule_id].evolved_text:
            self.rules[rule_id].evolution_discovered = True
    
    def add_clue(self, text, source):
        clue = {'text': text, 'source': source, 'time': pygame.time.get_ticks()}
        if not any(c['text'] == text for c in self.clues):
            self.clues.append(clue)
    
    def add_item(self, item_name, description):
        item = {'name': item_name, 'desc': description}
        if not any(i['name'] == item_name for i in self.items):
            self.items.append(item)
    
    def draw(self, surface, time_offset):
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLORS['black'][:3], 200))
        surface.blit(overlay, (0, 0))
        
        self._draw_notebook_bg(surface, time_offset)
        self._draw_title(surface)
        self._draw_rules(surface, time_offset)
        self._draw_clues(surface)
        self._draw_hints(surface)
    
    def _draw_notebook_bg(self, surface, time_offset):
        margin = 10
        rect = pygame.Rect(margin, margin, VIRTUAL_WIDTH - margin * 2, VIRTUAL_HEIGHT - margin * 2)
        
        for y in range(rect.top, rect.bottom):
            for x in range(rect.left, rect.right):
                rel_y = y - rect.top
                
                base = COLORS['notebook_bg']
                line_effect = 0
                if rel_y % 8 == 0:
                    line_effect = 3
                
                flicker = int((math.sin(time_offset * 0.02 + x * 0.01) + 1) * 2)
                
                color = (
                    min(255, base[0] + line_effect + flicker),
                    min(255, base[1] + line_effect + flicker),
                    min(255, base[2] + line_effect + flicker)
                )
                surface.set_at((x, y), color)
        
        border_color = COLORS['notebook_border']
        pygame.draw.rect(surface, border_color, rect, 2)
    
    def _draw_title(self, surface):
        title = "NOTEBOOK"
        self._draw_text(surface, title, VIRTUAL_WIDTH // 2, 22, COLORS['text_highlight'], center=True)
        
        pygame.draw.line(surface, COLORS['notebook_border'],
                        (25, 32), (VIRTUAL_WIDTH - 25, 32), 1)
    
    def _draw_rules(self, surface, time_offset):
        y = 42
        self._draw_text(surface, "Rules:", 20, y, COLORS['text_rule'])
        y += 12
        
        displayed_rules = [r for r in self.rules.values() if r.discovered]
        
        for rule in displayed_rules:
            text = rule.get_display_text()
            
            if rule.evolution_discovered:
                color = COLORS['text_danger']
            elif not rule.is_true:
                color = COLORS['text_dim']
            else:
                color = COLORS['text_normal']
            
            lines = self._wrap_text(text, 38)
            for line in lines:
                self._draw_text(surface, line, 20, y, color)
                y += 8
        
        if not displayed_rules:
            self._draw_text(surface, "  (No rules discovered yet)", 20, y, COLORS['text_dim'])
    
    def _draw_clues(self, surface):
        y = VIRTUAL_HEIGHT - 85
        pygame.draw.line(surface, COLORS['notebook_border'],
                        (25, y - 5), (VIRTUAL_WIDTH - 25, y - 5), 1)
        
        self._draw_text(surface, "Clues:", 20, y, COLORS['text_clue'])
        y += 10
        
        recent_clues = self.clues[-3:]
        for clue in recent_clues:
            text = clue['text'][:35] + "..." if len(clue['text']) > 35 else clue['text']
            self._draw_text(surface, "- " + text, 20, y, COLORS['text_dim'])
            y += 8
    
    def _draw_hints(self, surface):
        hint_text = "[Tab] Close  [W/S] Scroll"
        self._draw_text(surface, hint_text, VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT - 15,
                       COLORS['text_dim'], center=True)
    
    def _draw_text(self, surface, text, x, y, color, center=False):
        char_width = 6
        char_height = 8
        
        if center:
            x = x - (len(text) * char_width) // 2
        
        for i, char in enumerate(text):
            char_x = x + i * char_width
            self._draw_char(surface, char, char_x, y, color)
    
    def _draw_char(self, surface, char, x, y, color):
        patterns = self._get_char_patterns()
        pattern = patterns.get(char, [[2],[2],[2],[2],[2]])
        
        for row_idx, row in enumerate(pattern):
            for col in row:
                px = x + col
                py = y + row_idx
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
    
    def get_discovered_rules_count(self):
        return sum(1 for r in self.rules.values() if r.discovered)
    
    def get_evolved_rules_count(self):
        return sum(1 for r in self.rules.values() if r.evolution_discovered)
