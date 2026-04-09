# 诡则像素：泰安医院

一个创意烧脑的2D像素规则怪谈轻恐怖游戏，采用复古精致像素风格，参考《Animal Well》的视觉效果。

## 项目结构

```
pixel_horror_hospital/
├── scenes/
│   ├── Main.tscn          # 主场景
│   ├── VisualEffects.tscn # 视觉效果场景
│   ├── NotebookUI.tscn    # 笔记本UI场景
│   └── rooms/
│       ├── Ward.tscn      # 病房场景
│       └── Corridor.tscn  # 走廊场景
├── scripts/
│   ├── Player.gd          # 玩家脚本
│   ├── RoomManager.gd     # 房间管理脚本
│   ├── Door.gd            # 门脚本
│   ├── Clue.gd            # 线索脚本
│   ├── RuleManager.gd     # 规则管理脚本
│   ├── NotebookUI.gd      # 笔记本UI脚本
│   ├── SanityManager.gd   # SAN值管理脚本
│   ├── VisualEffects.gd   # 视觉效果脚本
│   └── GameManager.gd     # 游戏管理脚本
├── assets/
│   ├── textures/          # 纹理素材
│   ├── sounds/            # 音效素材
│   └── fonts/             # 字体素材
├── resources/             # 资源文件
├── project.godot          # 项目配置文件
└── README.md              # 项目说明
```

## 项目设置

### 1. 分辨率和窗口设置

在 `project.godot` 文件中已经配置了以下设置：

- 基础分辨率：640×360
- 窗口缩放：2倍（实际显示1280×720）
- 拉伸模式：2D
- 宽高比：保持

### 2. 渲染设置

为了实现清晰锐利的像素效果，需要在Godot编辑器中进行以下设置：

1. **全局纹理过滤**：
   - 打开 `Project Settings` → `Rendering` → `Textures`
   - 将 `Default Texture Filter` 设置为 `Nearest`

2. **Sprite2D 和 TileMap 设置**：
   - 对于每个 Sprite2D 和 TileMap 节点，确保其 `Texture Filter` 属性设置为 `Nearest`

3. **光照设置**：
   - 使用 `PointLight2D` 和 `DirectionalLight2D` 实现动态光照
   - 配合 `CanvasModulate` 实现全局压暗效果

### 3. 输入设置

已配置以下输入键位：

- A / D 键：左右移动
- 空格键：跳跃
- E 键：交互（检查物体、收集线索）
- Tab / I 键：打开/关闭笔记本界面

## 素材替换指南

### 1. 生成像素艺术素材

使用 `byted-seedream-image-generate` 技能生成以下素材：

#### 场景素材
- **病房**：`sharp retro pixel art, abandoned hospital patient room interior, dark horror atmosphere, flickering lights, subtle neon glow, clean pixel details, Animal Well style, 32x32 tiles`
- **走廊**：`sharp retro pixel art, abandoned hospital corridor, dark horror atmosphere, flickering lights, subtle neon glow, clean pixel details, Animal Well style, 32x32 tiles`

#### 角色素材
- **玩家**：`detailed pixel art player character, side view, hospital gown, standing pose, retro pixel style, sharp edges`
- **鬼魂**：`floating ghost pixel art, semi-transparent, purple glow, dark corridor background, horror pixel art`

#### 物品素材
- **线索**：`pixel art note paper, blood stains, retro pixel style, sharp edges`
- **门**：`pixel art hospital door, old and rusty, retro pixel style, sharp edges`

### 2. 导入素材到Godot

1. 将生成的图片保存到 `assets/textures/` 目录
2. 在Godot编辑器中，将图片拖放到 `FileSystem` 面板中
3. 对于每个纹理，确保其 `Import` 设置中的 `Filter` 选项为 `Nearest`

### 3. 替换场景中的素材

#### 替换 TileMap 素材
1. 打开 `Ward.tscn` 和 `Corridor.tscn` 场景
2. 选择 `TileMap` 节点
3. 在 `Inspector` 面板中，点击 `TileSet` 属性，创建新的 TileSet
4. 导入生成的场景素材作为 tiles

#### 替换 Player 素材
1. 打开 `Ward.tscn` 和 `Corridor.tscn` 场景
2. 选择 `Player/Sprite2D` 节点
3. 在 `Inspector` 面板中，将 `Texture` 属性设置为生成的玩家素材

#### 替换 Clue 素材
1. 打开 `Ward.tscn` 和 `Corridor.tscn` 场景
2. 选择 `Clue/Sprite2D` 节点
3. 在 `Inspector` 面板中，将 `Texture` 属性设置为生成的线索素材

## 运行Demo

### 1. 打开项目

1. 打开 Godot 4.x 编辑器
2. 点击 `Import` 按钮，选择 `pixel_horror_hospital/project.godot` 文件
3. 等待项目加载完成

### 2. 运行游戏

1. 点击编辑器顶部的 `Play` 按钮
2. 游戏将从 `Main.tscn` 开始运行
3. 第一夜Demo目标：存活并收集至少3个线索

### 3. 游戏操作

- **移动**：A / D 键
- **跳跃**：空格键
- **交互**：E 键（收集线索、检查物体）
- **笔记本**：Tab / I 键（查看收集的线索和发现的规则）

## 游戏机制

### 核心玩法
1. **规则系统**：每晚生成3-5条相互矛盾或可进化的规则
2. **线索收集**：通过探索房间收集线索，发现规则
3. **SAN值系统**：违反规则会导致SAN值下降，SAN值耗尽则游戏失败
4. **轻恐怖效果**：违反规则时会触发屏幕抖动、颜色偏移等视觉效果
5. **规则进化**：规则会根据玩家行为进化、反转或形成逻辑悖论

### 第一夜Demo流程
1. 玩家从病房开始
2. 收集病房中的线索（墙上的便条）
3. 通过门进入走廊
4. 收集走廊中的线索（病历文件）
5. 探索过程中注意遵守规则（如不在走廊停留超过30秒）
6. 收集足够线索（至少3个）以完成第一夜
7. 或在规定时间内（60秒）生存下来

## 代码结构

### 主要脚本说明

1. **Player.gd**：处理玩家移动、跳跃、交互和笔记本操作
2. **RoomManager.gd**：管理房间切换和场景加载
3. **RuleManager.gd**：生成和管理游戏规则，处理规则违反和进化
4. **NotebookUI.gd**：显示和管理收集的线索和发现的规则
5. **SanityManager.gd**：管理玩家的SAN值
6. **VisualEffects.gd**：实现轻恐怖视觉效果
7. **GameManager.gd**：管理游戏流程、胜利条件和失败条件

### 信号系统

游戏使用 Godot 的信号系统实现组件间通信，主要信号包括：

- `player.collect_clue()`：收集线索时触发
- `RuleManager.rule_discovered`：发现规则时触发
- `RuleManager.rule_broken`：违反规则时触发
- `SanityManager.sanity_changed`：SAN值变化时触发
- `SanityManager.sanity_depleted`：SAN值耗尽时触发
- `GameManager.game_over`：游戏结束时触发

## 扩展建议

1. **增加更多房间**：添加更多不同类型的房间，如手术室、药房、太平间等
2. **增加更多规则**：扩展规则池，增加更多复杂的规则和进化路径
3. **增加敌人AI**：添加鬼魂敌人，根据规则行为
4. **增加音效**：添加环境音效和恐怖音效，增强氛围
5. **增加动画**：为玩家和鬼魂添加动画效果
6. **增加多夜流程**：实现完整的多夜游戏流程，每夜规则难度递增

## 技术要求

- Godot 4.x
- GDScript
- 像素艺术素材（使用 byted-seedream-image-generate 生成）

## 注意事项

- 确保所有纹理的 `Texture Filter` 设置为 `Nearest`，以保持像素的清晰锐利
- 使用 `CanvasModulate` 和 `PointLight2D` 营造黑暗压抑的氛围
- 调整 `GameManager.gd` 中的 `night_duration` 和 `required_clues` 参数以调整游戏难度
- 扩展 `RuleManager.gd` 中的 `rule_pool` 以增加更多规则和线索
