class_name Player
extends CharacterBody2D

@export var speed: float = 200.0
@export var max_health: int = 100

@onready var animation: AnimationPlayer = $AnimationPlayer
@onready var state_machine: StateMachine = $StateMachine

var current_health: int:
	set(value):
		current_health = clampi(value, 0, max_health)

func _ready() -> void:
	current_health = max_health

func handle_idle_input(event: InputEvent) -> void:
	pass

func handle_move_input(event: InputEvent) -> void:
	pass

func take_damage(amount: int) -> void:
	current_health -= amount
	
	if current_health <= 0:
		EventBus.violation_triggered.emit("玩家生命值耗尽")

func heal(amount: int) -> void:
	current_health = minf(current_health + amount, max_health)
