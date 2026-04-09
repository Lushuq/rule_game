class_name NotebookUI
extends CanvasLayer

# 单例
static var singleton: NotebookUI = null

# 内部变量
var clues: Array[Dictionary] = []
var discovered_rules: Array[Dictionary] = []

# 节点引用
@onready var panel: ColorRect = $Panel
@onready var clue_list: VBoxContainer = $Panel/ClueList
@onready var rule_list: VBoxContainer = $Panel/RuleList

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

	# 初始化UI
	visible = false

	# 连接信号
	RuleManager.singleton.rule_discovered.connect(_on_rule_discovered)

func set_visible(visible: bool) -> void:
	self.visible = visible

func add_clue(clue: Dictionary) -> void:
	if not _is_clue_exists(clue.id):
		clues.append(clue)
		_update_clue_list()

func _is_clue_exists(clue_id: String) -> bool:
	for clue in clues:
		if clue.id == clue_id:
			return true
	return false

func _on_rule_discovered(rule: Dictionary) -> void:
	if not _is_rule_exists(rule.id):
		discovered_rules.append(rule)
		_update_rule_list()

func _is_rule_exists(rule_id: String) -> bool:
	for rule in discovered_rules:
		if rule.id == rule_id:
			return true
	return false

func _update_clue_list() -> void:
	# 清空现有列表
	for child in clue_list.get_children():
		child.queue_free()

	# 添加线索
	for clue in clues:
		var label = Label.new()
		label.text = clue.text
		label.add_theme_color_override("font_color", Color(0.9, 0.9, 0.9))
		clue_list.add_child(label)

func _update_rule_list() -> void:
	# 清空现有列表
	for child in rule_list.get_children():
		child.queue_free()

	# 添加规则
	for rule in discovered_rules:
		var label = Label.new()
		label.text = "规则：" + rule.text
		label.add_theme_color_override("font_color", Color(0.8, 0.2, 0.2))
		rule_list.add_child(label)