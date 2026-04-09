class_name Player
extends CharacterBody2D

signal started_moving(direction: int)
signal stopped_moving

@export var speed: float = 200.0
@onready var sprite: Sprite2D = $Sprite2D

var is_moving: bool = false
var last_direction: int = 0

func _physics_process(delta: float) -> void:
	var direction: int = 0
	
	if Input.is_action_pressed("move_left"):
		direction = -1
	elif Input.is_action_pressed("move_right"):
		direction = 1
	
	velocity.x = direction * speed
	move_and_slide()
	
	if direction != 0:
		sprite.flip_h = direction < 0
		if not is_moving:
			is_moving = true
			last_direction = direction
			started_moving.emit(direction)
	else:
		if is_moving:
			is_moving = false
			stopped_moving.emit()
