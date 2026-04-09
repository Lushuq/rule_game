class_name PlayerMove
extends State

@export var player: Player

func enter(_msg: Dictionary = {}) -> void:
	if player.sprite:
		# 这里可以播放移动动画
		pass

func physics_update(_delta: float) -> void:
	var direction: int = 0
	
	if Input.is_action_pressed("move_left"):
		direction = -1
	elif Input.is_action_pressed("move_right"):
		direction = 1
	
	player.velocity.x = direction * player.speed
	player.move_and_slide()
	
	if direction != 0:
		player.sprite.flip_h = direction < 0
		# 向 RuleManager 报告位置和动作
		RuleManager.report_player_state(player.global_position, "moving")
	else:
		# 停止移动，切换回 idle 状态
		state_machine.transition_to("Idle")
