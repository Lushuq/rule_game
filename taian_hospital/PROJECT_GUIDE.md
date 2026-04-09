# 《诡则像素：泰安医院》项目指南

## 项目概述

这是一个创意烧脑的2D像素规则怪谈轻恐怖游戏，采用Godot 4.x引擎开发。

## 项目设置说明

### 分辨率与渲染配置

在 `project.godot` 中已配置以下关键设置：

```ini
[display]
window/size/viewport_width=640
window/size/viewport_height=360
window/size/mode=2
window/stretch/mode="canvas_items"
window/stretch/aspect="keep"

[rendering]
textures/canvas_textures/default_texture_filter=0
```

**关键配置说明：**
- **分辨率**：640×360（16:9 比例，适合像素风格）
- **拉伸模式**：`canvas_items` 确保像素保持锐利
- **纹理过滤**：`0`（Nearest）禁用模糊，确保像素干净锐利

## 文件夹结构

```
taian_hospital/
├── project.godot          # Godot项目配置
├── icon.svg               # 项目图标
├── scenes/                # 场景文件
│   ├── main.tscn          # 主场景
│   ├── player.tscn        # 玩家角色场景
│   ├── patient_room.tscn  # 病房场景
│   ├── corridor.tscn      # 走廊场景
│   └── notebook_ui.tscn   # 笔记本UI场景
├── scripts/               # GDScript脚本
│   ├── game.gd            # 主游戏控制器
│   ├── player.gd          # 玩家脚本
│   ├── room.gd            # 房间基类
│   ├── door.gd            # 门脚本
│   ├── interactable.gd    # 可交互物体脚本
│   ├── rule_manager.gd    # 规则管理器
│   ├── sanity_manager.gd  # SAN值管理器
│   ├── effects_manager.gd # 特效管理器
│   └── notebook_ui.gd     # 笔记本UI脚本
└── assets/                # 资源文件夹
    ├── images/
    ├── sprites/
    ├── tilesets/
    ├── fonts/
    └── audio/
```

## 核心玩法

### 操作说明
- **A/D 键**：左右移动
- **空格键**：跳跃
- **E 键**：交互（检查物体、收集线索）
- **Tab/I 键**：打开/关闭笔记本

### 游戏目标
收集5条线索，成功存活第一夜！

## 如何在Godot中运行项目

1. **下载并安装Godot 4.x**（推荐4.2或更高版本）
2. **打开Godot引擎**
3. **导入项目**：
   - 点击"导入"
   - 选择 `taian_hospital` 文件夹
   - 点击"导入并编辑"
4. **运行项目**：
   - 按 F5 键或点击右上角的"运行项目"按钮

## 替换像素艺术素材

当前版本使用简单的ColorRect作为占位符。以下是替换为精致像素素材的步骤：

### 1. 生成像素艺术素材

使用 `byted-seedream-image-generate` 技能生成素材，示例提示词：

**病房内部：**
```
sharp retro pixel art, abandoned hospital patient room interior, dark horror atmosphere, flickering lights, subtle neon glow, clean pixel details, Animal Well style, 32x32 tiles
```

**玩家角色：**
```
detailed pixel art player character, side view, hospital gown, standing pose, retro pixel style, sharp edges
```

**鬼魂：**
```
floating ghost pixel art, semi-transparent, purple glow, dark corridor background, horror pixel art
```

**门：**
```
old wooden hospital door pixel art, dark atmosphere, rusty handle, 32x64 pixels
```

### 2. 导入素材到Godot

1. 将生成的图片放入 `assets/sprites/` 文件夹
2. 在Godot中右键点击图片文件 → "导入"
3. **重要设置**：
   - **Texture Filter**：选择 `Nearest`（禁用模糊）
   - **Texture Repeat**：选择 `Disable`
   - **Import As**：选择 `Texture2D`

### 3. 替换占位素材

#### 替换玩家角色
1. 打开 `scenes/player.tscn`
2. 选中 `Sprite2D` 节点
3. 在 Inspector 中，将 `ColorRect` 替换为 `Sprite2D`
4. 拖拽导入的玩家精灵纹理到 `Texture` 属性

#### 替换房间背景
1. 打开病房或走廊场景
2. 选中 `Background` 节点
3. 将 `ColorRect` 替换为 `Sprite2D` 或 `TileMap`
4. 应用对应的像素纹理

#### 替换可交互物体
类似地，替换各个可交互物体（便条、电视、鬼魂等）的 `ColorRect` 为 `Sprite2D`

## 代码架构说明

### 主要系统

1. **Game** ([game.gd](file:///workspace/taian_hospital/scripts/game.gd))
   - 主游戏控制器
   - 管理所有子系统
   - 处理游戏流程

2. **Player** ([player.gd](file:///workspace/taian_hospital/scripts/player.gd))
   - 角色移动、跳跃
   - 碰撞检测
   - 交互检测

3. **RuleManager** ([rule_manager.gd](file:///workspace/taian_hospital/scripts/rule_manager.gd))
   - 管理怪谈规则
   - 规则发现和进化
   - 违规检测

4. **SanityManager** ([sanity_manager.gd](file:///workspace/taian_hospital/scripts/sanity_manager.gd))
   - SAN值管理
   - SAN值变化通知

5. **EffectsManager** ([effects_manager.gd](file:///workspace/taian_hospital/scripts/effects_manager.gd))
   - 屏幕抖动
   - 颜色偏移
   - 恐怖特效

### 信号系统

游戏使用Godot的信号系统实现模块间通信：
- `player.interacted` → 玩家交互
- `rule_manager.rule_discovered` → 发现规则线索
- `rule_manager.rule_violated` → 违反规则
- `sanity_manager.sanity_changed` → SAN值变化

## 第一夜Demo内容

### 可探索区域
- **病房**：起始房间，包含2条线索
- **走廊**：连接区域，包含3条线索

### 线索分布
1. 墙上便条：灯光规则线索
2. 病历文件：黑暗规则线索
3. 旧电视：回头规则线索
4. 鬼魂低语：前方规则线索
5. 门上便条：关门规则线索
6. 墙上血字：安静规则线索

### 胜利/失败条件
- **胜利**：收集5条线索
- **失败**：SAN值降至0

## 扩展开发建议

### 添加新房间
1. 继承 `room.gd` 创建新房间脚本
2. 设计房间布局和可交互物体
3. 在 `main.tscn` 的 `RoomManager` 中添加新房间实例
4. 连接门的 `door_used` 信号

### 添加新规则
1. 在 `rule_manager.gd` 的 `initialize_rules()` 中添加新规则
2. 为规则创建线索和可交互物体
3. 在 `check_rule_violation()` 中实现违规检测逻辑

### 增强视觉效果
- 添加粒子系统（灰尘、雾气）
- 实现动态光影动画
- 添加更多恐怖特效（视觉扭曲、残影等）

## 技术注意事项

1. **像素完美**：始终确保 `Texture Filter` 设置为 `Nearest`
2. **性能优化**：对于大地图，考虑使用可见性剔除
3. **代码风格**：遵循Godot 4最佳实践，使用 `@onready`、信号等
4. **版本控制**：推荐使用Git管理项目版本

## 常见问题

**Q: 为什么像素看起来模糊？**
A: 检查纹理导入设置，确保 `Texture Filter` 设为 `Nearest`。

**Q: 如何添加更多房间？**
A: 参考现有房间场景的结构，创建新场景并添加到 `RoomManager`。

**Q: 游戏怎么保存进度？**
A: 当前Demo版本不包含存档功能，可以使用Godot的 `ConfigFile` 或 `ResourceSaver` 实现。
