import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 800, 600
FPS = 60
TILE_SIZE = 32

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 游戏状态
GAME_STATE = "playing"
NIGHT = 1
SANITY = 100

# 初始化屏幕
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("诡则像素：泰安医院")
clock = pygame.time.Clock()

# 字体
font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)

# 玩家类
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 3
        self.direction = "down"
    
    def draw(self, surface):
        # 简单的像素风格玩家
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height))
    
    def move(self, dx, dy, walls, doors):
        # 检查碰撞
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 检查墙壁碰撞
        collision = False
        for wall in walls:
            if (new_x < wall[0] + wall[2] and new_x + self.width > wall[0] and
                new_y < wall[1] + wall[3] and new_y + self.height > wall[1]):
                collision = True
                break
        
        # 检查门碰撞
        for door in doors:
            if (new_x < door[0] + door[2] and new_x + self.width > door[0] and
                new_y < door[1] + door[3] and new_y + self.height > door[1]):
                # 可以通过门
                return True
        
        if not collision:
            self.x = new_x
            self.y = new_y
        
        return False

# 房间类
class Room:
    def __init__(self, name, walls, doors, interactables):
        self.name = name
        self.walls = walls  # 墙壁列表 [(x, y, width, height), ...]
        self.doors = doors  # 门列表 [(x, y, width, height, target_room), ...]
        self.interactables = interactables  # 可交互物体 [(x, y, width, height, text, rule_id), ...]
    
    def draw(self, surface):
        # 绘制墙壁
        for wall in self.walls:
            pygame.draw.rect(surface, GRAY, wall)
        
        # 绘制门
        for door in self.doors:
            pygame.draw.rect(surface, BLUE, door[:4])
        
        # 绘制可交互物体
        for item in self.interactables:
            pygame.draw.rect(surface, YELLOW, item[:4])

# 规则类
class Rule:
    def __init__(self, id, text, is_active=True):
        self.id = id
        self.text = text
        self.is_active = is_active
        self.discovered = False

# 笔记类
class Notebook:
    def __init__(self):
        self.rules = []
        self.visible = False
    
    def add_rule(self, rule):
        if not any(r.id == rule.id for r in self.rules):
            rule.discovered = True
            self.rules.append(rule)
    
    def draw(self, surface):
        if not self.visible:
            return
        
        # 绘制笔记背景
        pygame.draw.rect(surface, BLACK, (50, 50, WIDTH - 100, HEIGHT - 100))
        pygame.draw.rect(surface, WHITE, (55, 55, WIDTH - 110, HEIGHT - 110))
        
        # 绘制标题
        title = font.render("笔记本", True, BLACK)
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
        
        # 绘制规则
        y_offset = 120
        for rule in self.rules:
            rule_text = small_font.render(f"规则 {rule.id}: {rule.text}", True, BLACK)
            surface.blit(rule_text, (80, y_offset))
            y_offset += 30
            
            if y_offset > HEIGHT - 80:
                break

# 初始化游戏对象
player = Player(100, 100)

# 创建房间
room1_walls = [
    (0, 0, WIDTH, 32),          # 上
    (0, 0, 32, HEIGHT),          # 左
    (WIDTH - 32, 0, 32, HEIGHT), # 右
    (0, HEIGHT - 32, WIDTH, 32), # 下
    (200, 100, 32, 200),         # 中间墙
    (400, 200, 32, 150)          # 中间墙
]

room1_doors = [
    (300, HEIGHT - 64, 64, 32, "room2")  # 通往下一个房间的门
]

room1_interactables = [
    (150, 150, 40, 40, "墙上的便条: 夜晚不要打开任何门", 1),
    (500, 200, 40, 40, "闪烁的电视: 不要相信镜子中的自己", 2),
    (300, 150, 40, 40, "鬼魂低语: 保持灯光明亮", 3)
]

room2_walls = [
    (0, 0, WIDTH, 32),          # 上
    (0, 0, 32, HEIGHT),          # 左
    (WIDTH - 32, 0, 32, HEIGHT), # 右
    (0, HEIGHT - 32, WIDTH, 32), # 下
    (200, 150, 32, 150),         # 中间墙
    (500, 100, 32, 200)          # 中间墙
]

room2_doors = [
    (300, 0, 64, 32, "room1")  # 通往上一个房间的门
]

room2_interactables = [
    (150, 250, 40, 40, "桌上的日记: 凌晨3点前必须回到房间", 4),
    (550, 250, 40, 40, "墙上的涂鸦: 红色的东西不要碰", 5)
]

# 房间字典
rooms = {
    "room1": Room("病房", room1_walls, room1_doors, room1_interactables),
    "room2": Room("走廊", room2_walls, room2_doors, room2_interactables)
}

current_room = "room1"

# 初始化规则
rules = [
    Rule(1, "夜晚不要打开任何门"),
    Rule(2, "不要相信镜子中的自己"),
    Rule(3, "保持灯光明亮"),
    Rule(4, "凌晨3点前必须回到房间"),
    Rule(5, "红色的东西不要碰")
]

# 初始化笔记
notebook = Notebook()

# 游戏时间（模拟）
game_time = 0

# 视觉效果变量
screen_shake = 0
color_offset = 0

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                notebook.visible = not notebook.visible
            elif event.key == pygame.K_e and not notebook.visible:
                # 检查交互
                for item in rooms[current_room].interactables:
                    if (player.x < item[0] + item[2] and player.x + player.width > item[0] and
                        player.y < item[1] + item[3] and player.y + player.height > item[1]):
                        # 显示提示
                        rule_id = item[5]
                        rule = next(r for r in rules if r.id == rule_id)
                        notebook.add_rule(rule)
                        print(f"发现规则: {rule.text}")
        
    # 处理玩家输入
    keys = pygame.key.get_pressed()
    if not notebook.visible:
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy = -player.speed
            player.direction = "up"
        if keys[pygame.K_s]:
            dy = player.speed
            player.direction = "down"
        if keys[pygame.K_a]:
            dx = -player.speed
            player.direction = "left"
        if keys[pygame.K_d]:
            dx = player.speed
            player.direction = "right"
        
        # 移动玩家
        door_found = player.move(dx, dy, rooms[current_room].walls, rooms[current_room].doors)
        
        # 检查门
        if door_found:
            for door in rooms[current_room].doors:
                if (player.x < door[0] + door[2] and player.x + player.width > door[0] and
                    player.y < door[1] + door[3] and player.y + player.height > door[1]):
                    current_room = door[4]
                    # 重置玩家位置
                    if current_room == "room1":
                        player.x, player.y = 100, 100
                    else:
                        player.x, player.y = 500, 400
                    # 违反规则1：夜晚打开门
                    SANITY -= 10
                    screen_shake = 10
                    print("警告：你违反了规则1！SAN值下降！")
                    break
    
    # 更新游戏时间
    game_time += 1
    
    # 检查规则违反
    # 规则3：保持灯光明亮（模拟）
    if game_time % 60 == 0:
        if random.random() > 0.7:
            SANITY -= 5
            screen_shake = 5
            print("警告：灯光变暗了！SAN值下降！")
    
    # 检查SAN值
    if SANITY <= 0:
        GAME_STATE = "game_over"
        print("游戏结束：SAN值耗尽！")
    
    # 检查胜利条件（第一夜存活）
    if game_time > 3600:  # 60秒 * 60 = 1分钟
        GAME_STATE = "victory"
        print("胜利：你成功存活了第一夜！")
    
    # 视觉效果
    screen_shake = max(0, screen_shake - 1)
    color_offset = (color_offset + 1) % 256
    
    # 绘制
    screen.fill(BLACK)
    
    # 应用视觉效果
    if SANITY < 50:
        # 颜色偏移
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((255, color_offset % 100, 0))
        surface.set_alpha(50)
        screen.blit(surface, (0, 0))
    
    # 屏幕抖动
    if screen_shake > 0:
        offset_x = random.randint(-screen_shake, screen_shake)
        offset_y = random.randint(-screen_shake, screen_shake)
        screen_copy = screen.copy()
        screen.fill(BLACK)
        screen.blit(screen_copy, (offset_x, offset_y))
    
    # 绘制房间
    rooms[current_room].draw(screen)
    
    # 绘制玩家
    player.draw(screen)
    
    # 绘制SAN值
    sanity_text = font.render(f"SAN值: {SANITY}", True, WHITE)
    screen.blit(sanity_text, (20, 20))
    
    # 绘制时间
    time_text = font.render(f"时间: {game_time // 60}:{game_time % 60:02d}", True, WHITE)
    screen.blit(time_text, (20, 50))
    
    # 绘制笔记
    notebook.draw(screen)
    
    # 绘制游戏状态
    if GAME_STATE == "game_over":
        game_over_text = font.render("游戏结束：SAN值耗尽！", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    elif GAME_STATE == "victory":
        victory_text = font.render("胜利：你成功存活了第一夜！", True, GREEN)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2))
    
    # 刷新屏幕
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()