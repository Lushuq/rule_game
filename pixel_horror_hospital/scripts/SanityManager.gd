class_name SanityManager
extends Node

# 信号
signal sanity_changed(sanity: float)
signal sanity_depleted()

# 单例
var singleton: SanityManager = null

# 内部变量
var _sanity: float = 100.0
var _max_sanity: float = 100.0

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

func get_sanity() -> float:
	return _sanity

func get_max_sanity() -> float:
	return _max_sanity

func increase_sanity(amount: float) -> void:
	_sanity = min(_sanity + amount, _max_sanity)
	sanity_changed.emit(_sanity)

func decrease_sanity(amount: float) -> void:
	_sanity = max(_sanity - amount, 0)
	sanity_changed.emit(_sanity)

	if _sanity <= 0:
		sanity_depleted.emit()

func set_sanity(value: float) -> void:
	_sanity = clamp(value, 0, _max_sanity)
	sanity_changed.emit(_sanity)

	if _sanity <= 0:
		sanity_depleted.emit()