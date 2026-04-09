"""
《诡则像素：泰安医院》笔记本模块
Notebook类：界面显示、规则记录、线索整理
"""

import pygame
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
        self.font = None
        self.small_font = None
        self._init_rules()
    
    def _init_rules(self):
        self.rules = {
            'rule1': Rule(
                'rule1',
                '规则一：午夜后不要看镜子，除非你带着红色的东西。',
                is_true=True
            ),
            'rule2': Rule(
                'rule2', 
                '规则二：灯光下是安全的，但不要让"它们"看到你。',
                is_true=True
            ),
            'rule3': Rule(
                'rule3',
                '规则三：当钟声响起，必须静止不动。',
                is_true=False,
                evolved_text='规则三（已证伪）：钟声响起时，必须移动！静止会引来它们！'
            ),
            'rule4': Rule(
                'rule4',
                '规则四：午夜时分，所有灯光都会熄灭。那时不要呼吸。',
                is_true=True
            ),
            'rule5': Rule(
                'rule5',
                '规则五：红色保护你，但也会引来它们。',
                is_true=True
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
        if clue not in self.clues:
            self.clues.append(clue)
    
    def add_item(self, item_name, description):
        item = {'name': item_name, 'desc': description}
        if item not in self.items:
            self.items.append(item)
    
    def draw(self, surface, time_offset):
        overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((*COLORS['black'][:3], 200))
        surface.blit(overlay, (0, 0))
        
        self._draw_notebook_bg(surface, time_offset)
        self._draw_title(surface)
        self._draw_rules(surface, time_offset)
        self._draw_clues(surface)
        self._draw_items(surface)
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
        
        for i in range(3):
            inner_rect = pygame.Rect(rect.left + i + 1, rect.top + i + 1,
                                    rect.width - (i + 1) * 2, rect.height - (i + 1) * 2)
            alpha_color = (
                border_color[0] - i * 15,
                border_color[1] - i * 15,
                border_color[2] - i * 15
            )
            pygame.draw.rect(surface, alpha_color, inner_rect, 1)
    
    def _draw_title(self, surface):
        title = "【 怪谈规则记录 】"
        self._draw_text(surface, title, VIRTUAL_WIDTH // 2, 22, COLORS['text_highlight'], center=True)
        
        pygame.draw.line(surface, COLORS['notebook_border'],
                        (25, 32), (VIRTUAL_WIDTH - 25, 32), 1)
    
    def _draw_rules(self, surface, time_offset):
        y = 42
        self._draw_text(surface, "已发现的规则:", 20, y, COLORS['text_rule'])
        y += 12
        
        displayed_rules = [r for r in self.rules.values() if r.discovered]
        
        for rule in displayed_rules:
            text = rule.get_display_text()
            
            if rule.evolution_discovered:
                color = COLORS['text_danger']
                prefix = "⚠ "
            elif not rule.is_true:
                color = COLORS['text_dim']
                prefix = "? "
            else:
                color = COLORS['text_normal']
                prefix = "• "
            
            lines = self._wrap_text(prefix + text, 38)
            for line in lines:
                self._draw_text(surface, line, 20, y, color)
                y += 8
        
        if not displayed_rules:
            self._draw_text(surface, "  (尚未发现任何规则)", 20, y, COLORS['text_dim'])
    
    def _draw_clues(self, surface):
        y = VIRTUAL_HEIGHT - 85
        pygame.draw.line(surface, COLORS['notebook_border'],
                        (25, y - 5), (VIRTUAL_WIDTH - 25, y - 5), 1)
        
        self._draw_text(surface, "线索:", 20, y, COLORS['text_clue'])
        y += 10
        
        recent_clues = self.clues[-3:]
        for clue in recent_clues:
            text = clue['text'][:35] + "..." if len(clue['text']) > 35 else clue['text']
            self._draw_text(surface, "• " + text, 20, y, COLORS['text_dim'])
            y += 8
    
    def _draw_items(self, surface):
        if not self.items:
            return
        
        y = VIRTUAL_HEIGHT - 45
        self._draw_text(surface, "持有物品:", 20, y, COLORS['bright_yellow'])
        y += 10
        
        for item in self.items[:3]:
            self._draw_text(surface, "• " + item['name'], 25, y, COLORS['text_normal'])
            y += 8
    
    def _draw_hints(self, surface):
        hint_text = "[Tab] 关闭笔记本  [W/S] 滚动"
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
        char_patterns = {
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
            '9': [[1,2,3],[0,4],[1,2,3,4],[4],[1,2,3]],
            ' ': [],
            '.': [[],[],[],[],[2]],
            ',': [[],[],[],[1],[0]],
            ':': [[],[2],[],[2],[]],
            ';': [[],[2],[],[1],[0]],
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
            '@': [[1,2,3],[0,3],[0,2,3],[0,3],[1,2]],
            '#': [[0,2,4],[1,2,3],[0,2,4],[1,2,3],[0,2,4]],
            '$': [[1,2,3],[0,2],[1,2,3],[2,4],[1,2,3]],
            '%': [[0,4],[3],[2],[1],[0,4]],
            '&': [[1,3],[0,4],[1,3],[0,4],[0,3]],
            '*': [[1,3],[2],[0,1,2,3,4],[2],[1,3]],
            '~': [[],[1,3],[0,2,4],[],[]],
            '【': [[0,1,2,3,4],[0],[0],[0],[0,1,2,3,4]],
            '】': [[0,1,2,3,4],[4],[4],[4],[0,1,2,3,4]],
            '：': [[],[2],[],[2],[]],
            '。': [[],[],[],[],[1,2]],
            '、': [[],[],[],[0],[1]],
            '一': [[],[1,2,3],[],[],[]],
            '二': [[0,1,2,3,4],[],[0,1,2,3,4],[],[0,1,2,3,4]],
            '三': [[0,1,2,3,4],[],[0,1,2,3,4],[],[0,1,2,3,4]],
            '四': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '五': [[0,1,2,3,4],[0],[0,1,2,3],[4],[0,1,2,3,4]],
            '中': [[2],[0,1,2,3,4],[2],[2],[2]],
            '文': [[0,4],[0,4],[1,2,3],[0,4],[0,4]],
            '规': [[0,1,2,3,4],[0,2,4],[0,2,4],[0,2,4],[0,1,2,3,4]],
            '则': [[0,1,2,3,4],[4],[0,1,2,3],[0],[0,1,2,3,4]],
            '记': [[0,1,2,3,4],[0],[0,1,2,3],[0,4],[0,4]],
            '录': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '已': [[0,1,2,3,4],[2],[1,2,3],[2],[1]],
            '发': [[0,4],[0,4],[1,2,3],[0,4],[0,4]],
            '现': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '的': [[0,1,2,3,4],[4],[0,1,2,3],[0],[0,1,2,3,4]],
            '线': [[0,4],[0,4],[1,2,3],[0,4],[0,4]],
            '索': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '持': [[0,1,2,3,4],[0],[0,1,2,3],[0,4],[0,4]],
            '有': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '物': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '品': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '尚': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '未': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '任': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '何': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '关': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '闭': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '笔': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '本': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '滚': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
            '动': [[0,4],[0,4],[0,1,2,3,4],[0,4],[0,4]],
        }
        
        pattern = char_patterns.get(char, [[2],[2],[2],[2],[2]])
        
        for row_idx, row in enumerate(pattern):
            for col in row:
                px = x + col
                py = y + row_idx
                if 0 <= px < VIRTUAL_WIDTH and 0 <= py < VIRTUAL_HEIGHT:
                    surface.set_at((px, py), color)
    
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


import math
