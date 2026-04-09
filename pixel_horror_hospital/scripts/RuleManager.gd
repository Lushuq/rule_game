class_name RuleManager
extends Node

# 信号
signal rule_discovered(rule: Dictionary)
signal rule_evolved(rule: Dictionary, old_rule: Dictionary)
signal rule_broken(rule: Dictionary)

# 单例
static var singleton: RuleManager = null

# 规则数据
var rules: Array[Dictionary] = []
var discovered_rules: Array[Dictionary] = []
var active_rules: Array[Dictionary] = []

# 第一夜规则池
var rule_pool: Array[Dictionary] = [
	{
		"id": "rule_1",
		"text": "不要在走廊里停留超过30秒",
		"clue": "墙上的便条：'走廊不安全，速进速出'",
		"consequence": "SAN值缓慢下降",
		"evolution": "规则1进化：不要在任何房间停留超过30秒"
	},
	{
		"id": "rule_2",
		"text": "不要相信镜子中的自己",
		"clue": "病历文件：'患者报告看到镜中自己的异常行为'",
		"consequence": "视觉幻觉",
		"evolution": "规则2进化：镜子是通往另一个世界的入口"
	},
	{
		"id": "rule_3",
		"text": "听到低语声时保持沉默",
		"clue": "鬼魂低语：'保持安静...否则他们会找到你'",
		"consequence": "吸引更多鬼魂",
		"evolution": "规则3进化：听到低语声时必须念出特定咒语"
	},
	{
		"id": "rule_4",
		"text": "不要打开任何关闭的门",
		"clue": "闪烁的电视：'门后有不该存在的东西'",
		"consequence": "遭遇恐怖事件",
		"evolution": "规则4进化：必须打开所有关闭的门"
	},
	{
		"id": "rule_5",
		"text": "只相信穿白大褂的人",
		"clue": "墙上的涂鸦：'白大褂是唯一的安全标志'",
		"consequence": "被误导",
		"evolution": "规则5进化：白大褂的人也不可信"
	}
]

# 玩家行为跟踪
var player_behavior: Dictionary = {
	"time_in_corridor": 0.0,
	"looked_in_mirror": false,
	"spoke_when_whispering": false,
	"opened_closed_door": false,
	"trusted_white_coat": false
}

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

	# 生成第一夜规则
	_generate_night_rules()

func _generate_night_rules() -> void:
	# 随机选择3-5条规则
	var rule_count = randi_range(3, 5)
	var shuffled_pool = rule_pool.duplicate()
	shuffled_pool.shuffle()

	rules.clear()
	for i in range(rule_count):
		rules.append(shuffled_pool[i])

	active_rules = rules.duplicate()

func _process(delta: float) -> void:
	# 跟踪玩家在走廊的时间
	if RoomManager and RoomManager.singleton:
		if RoomManager.singleton.get_current_room() == "corridor":
			player_behavior.time_in_corridor += delta
			# 检查规则1
			_check_rule_1()

func _check_rule_1() -> void:
	var rule = _find_rule_by_id("rule_1")
	if rule and player_behavior.time_in_corridor > 30:
		_break_rule(rule)

func _find_rule_by_id(rule_id: String) -> Dictionary?:
	for rule in rules:
		if rule.id == rule_id:
			return rule
	return null

func discover_rule(rule_id: String) -> void:
	var rule = _find_rule_by_id(rule_id)
	if rule and not _is_rule_discovered(rule_id):
		discovered_rules.append(rule)
		rule_discovered.emit(rule)

func _is_rule_discovered(rule_id: String) -> bool:
	for rule in discovered_rules:
		if rule.id == rule_id:
			return true
	return false

func _break_rule(rule: Dictionary) -> void:
	rule_broken.emit(rule)
	# 触发后果
	_trigger_consequence(rule)

func _trigger_consequence(rule: Dictionary) -> void:
	match rule.id:
		"rule_1":
			if SanityManager and SanityManager.singleton:
				SanityManager.singleton.decrease_sanity(5)
		"rule_2":
			# 触发视觉幻觉
			if VisualEffects and VisualEffects.singleton:
				VisualEffects.singleton.trigger_hallucination()
		"rule_3":
			# 吸引更多鬼魂
			# 实现鬼魂生成逻辑
			pass
		"rule_4":
			# 遭遇恐怖事件
			if VisualEffects and VisualEffects.singleton:
				VisualEffects.singleton.trigger_horror_event()
		"rule_5":
			# 被误导
			if SanityManager and SanityManager.singleton:
				SanityManager.singleton.decrease_sanity(10)

func evolve_rule(rule_id: String) -> void:
	var rule = _find_rule_by_id(rule_id)
	if rule:
		var old_rule = rule.duplicate()
		rule.text = rule.evolution
		rule_evolved.emit(rule, old_rule)

func track_player_behavior(behavior: String, value: Variant = true) -> void:
	if player_behavior.has(behavior):
		player_behavior[behavior] = value

func get_active_rules() -> Array[Dictionary]:
	return active_rules

func get_discovered_rules() -> Array[Dictionary]:
	return discovered_rules