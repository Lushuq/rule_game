class_name Clue
extends Area2D

# 导出变量
@export var clue_data: Dictionary = {
	"id": "",
	"text": "",
	"rule_id": "",
	"room": ""
}

# 信号
signal clue_collected(clue: Dictionary)

func _ready() -> void:
	# 连接信号
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
	if body is Player:
		_collect_clue(body)

func interact(player: Player) -> void:
	_collect_clue(player)

func _collect_clue(player: Player) -> void:
	# 收集线索
	player.collect_clue(clue_data)
	clue_collected.emit(clue_data)

	# 通知GameManager
	GameManager.singleton.add_clue()

	# 如果线索关联到规则，发现规则
	if clue_data.rule_id:
		RuleManager.singleton.discover_rule(clue_data.rule_id)

	# 隐藏线索
	visible = false
	set_deferred("queue_free")