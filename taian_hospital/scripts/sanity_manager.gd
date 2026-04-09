extends Node

signal sanity_changed(new_value: float)
signal sanity_depleted()

@export var max_sanity: float = 100.0
@export var min_sanity: float = 0.0
@export var recovery_rate: float = 0.5

var current_sanity: float = 100.0
var is_recovering: bool = false

func _ready() -> void:
	current_sanity = max_sanity

func lose_sanity(amount: float) -> void:
	current_sanity = clamp(current_sanity - amount, min_sanity, max_sanity)
	sanity_changed.emit(current_sanity)
	is_recovering = false
	
	if current_sanity <= min_sanity:
		sanity_depleted.emit()

func recover_sanity(amount: float) -> void:
	current_sanity = clamp(current_sanity + amount, min_sanity, max_sanity)
	sanity_changed.emit(current_sanity)

func _process(delta: float) -> void:
	if is_recovering and current_sanity < max_sanity:
		recover_sanity(recovery_rate * delta)

func start_recovery() -> void:
	is_recovering = true

func stop_recovery() -> void:
	is_recovering = false
