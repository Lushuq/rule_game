class_name RuleManager
extends Node

signal player_position_updated(position: Vector2, action: String)

singleton

func _ready() -> void:
	# 确保这是一个单例
	if not is_singleton():
		push_error("RuleManager should be an autoload singleton")

func report_player_state(position: Vector2, action: String) -> void:
	player_position_updated.emit(position, action)
	# 这里可以添加规则检查逻辑
	# print("Player at: %s, action: %s" % [position, action])
