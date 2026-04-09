class_name MoveState
extends State

@export var player: Player

func enter(_msg: Dictionary = {}) -> void:
	if player.animation:
		player.animation.play("move")

func physics_update(delta: float) -> void:
	var direction := Input.get_vector("left", "right", "up", "down")
	
	if direction == Vector2.ZERO:
		state_machine.transition_to("Idle")
		return
	
	player.velocity = direction * player.speed
	player.move_and_slide()
	
	if RuleManager:
		RuleManager.report_player_action(
			player.global_position,
			"moving",
			player.velocity
		)

func handle_input(event: InputEvent) -> void:
	if player:
		player.handle_move_input(event)
