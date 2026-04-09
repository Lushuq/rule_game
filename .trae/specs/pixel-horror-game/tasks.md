# 诡则像素：泰安医院 - 实现计划

## [x] Task 1: 游戏基础架构搭建
- **Priority**: P0
- **Depends On**: None
- **Description**:
  - 创建HTML5 Canvas游戏画布
  - 设置游戏主循环和帧率控制
  - 实现基本的游戏状态管理
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7
- **Test Requirements**:
  - `programmatic` TR-1.1: 游戏画布正确创建，尺寸合适
  - `programmatic` TR-1.2: 游戏主循环运行流畅，帧率稳定
- **Notes**: 搭建核心游戏架构，为后续功能提供基础

## [x] Task 2: 玩家移动与碰撞系统
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 实现WASD键控制玩家移动
  - 添加碰撞检测逻辑
  - 优化移动平滑度和响应速度
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-2.1: 玩家能通过WASD键控制角色移动
  - `programmatic` TR-2.2: 玩家遇到墙壁时停止移动
  - `programmatic` TR-2.3: 移动操作响应迅速，无明显延迟
- **Notes**: 确保移动系统手感良好，碰撞检测准确

## [x] Task 3: 房间系统实现
- **Priority**: P0
- **Depends On**: Task 2
- **Description**:
  - 创建至少2个房间的布局
  - 实现房间之间的切换逻辑
  - 添加门和过渡效果
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-3.1: 玩家能从一个房间移动到另一个房间
  - `programmatic` TR-3.2: 房间切换时有适当的过渡效果
  - `programmatic` TR-3.3: 每个房间有独立的布局和碰撞边界
- **Notes**: 设计合理的房间布局，确保房间切换流畅

## [x] Task 4: 规则系统设计
- **Priority**: P0
- **Depends On**: Task 1
- **Description**:
  - 设计3-5条相互矛盾/可进化的怪谈规则
  - 实现规则生成和管理系统
  - 添加规则违反检测机制
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-4.1: 游戏开始时生成3-5条规则
  - `programmatic` TR-4.2: 规则之间存在矛盾或进化关系
  - `programmatic` TR-4.3: 系统能检测规则违反情况
- **Notes**: 设计有趣且烧脑的规则，确保规则之间存在逻辑悖论

## [x] Task 5: 线索与交互系统
- **Priority**: P1
- **Depends On**: Task 3, Task 4
- **Description**:
  - 实现E键交互功能
  - 创建线索物品（便条、电视等）
  - 添加线索收集和显示逻辑
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: 玩家能接近线索物品并按下E键收集
  - `programmatic` TR-5.2: 收集线索时显示线索内容
  - `programmatic` TR-5.3: 已收集的线索可在笔记本中查看
- **Notes**: 设计多样化的线索呈现方式，增加游戏趣味性

## [x] Task 6: 笔记本系统
- **Priority**: P1
- **Depends On**: Task 5
- **Description**:
  - 实现Tab键打开笔记本功能
  - 创建笔记本界面
  - 添加线索和规则记录功能
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 玩家按下Tab键能打开笔记本
  - `programmatic` TR-6.2: 笔记本显示已收集的线索
  - `programmatic` TR-6.3: 玩家能在笔记本中记录规则推理
- **Notes**: 设计简洁直观的笔记本界面，方便玩家记录和查看信息

## [x] Task 7: Sanity值与恐怖效果
- **Priority**: P1
- **Depends On**: Task 4
- **Description**:
  - 实现Sanity值系统
  - 添加违反规则时的Sanity值下降逻辑
  - 实现屏幕抖动和颜色偏移等轻恐怖效果
- **Acceptance Criteria Addressed**: AC-6
- **Test Requirements**:
  - `programmatic` TR-7.1: 违反规则时Sanity值正确下降
  - `programmatic` TR-7.2: Sanity值下降时出现屏幕抖动效果
  - `programmatic` TR-7.3: Sanity值下降时出现颜色偏移效果
- **Notes**: 调整恐怖效果的强度，确保达到轻恐怖的效果

## [x] Task 8: 胜利/失败条件
- **Priority**: P1
- **Depends On**: Task 7
- **Description**:
  - 实现第一夜时间限制
  - 添加胜利/失败判断逻辑
  - 创建胜利/失败界面
- **Acceptance Criteria Addressed**: AC-7
- **Test Requirements**:
  - `programmatic` TR-8.1: 达到时间限制时显示胜利界面
  - `programmatic` TR-8.2: Sanity值降为0时显示失败界面
  - `programmatic` TR-8.3: 胜利/失败后能重新开始游戏
- **Notes**: 设定合理的第一夜时间长度，确保游戏体验平衡

## [x] Task 9: 游戏内容填充与测试
- **Priority**: P2
- **Depends On**: All previous tasks
- **Description**:
  - 填充游戏场景细节
  - 添加更多线索和交互点
  - 进行游戏测试和bug修复
- **Acceptance Criteria Addressed**: All
- **Test Requirements**:
  - `programmatic` TR-9.1: 游戏运行无明显bug
  - `human-judgment` TR-9.2: 游戏体验流畅，恐怖效果适中
  - `human-judgment` TR-9.3: 规则推理烧脑但合理
- **Notes**: 确保游戏内容丰富，玩法体验良好