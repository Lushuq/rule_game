class_name PlayerIdle
extends State

@export var player: Player

func enter(_msg: Dictionary = {}) -> void:
	if player.sprite:
		# 这里可以播放 idle 动画
		pass

func physics_update(_delta: float) -> void:
	var direction: int = 0
	
	if Input.is_action_pressed("move_left"):
		direction = -1
	elif Input.is_action_pressed("move_right"):
		direction = 1
	
	if direction != 0:
		state_machine.transition_to("Move")
