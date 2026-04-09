class_name IdleState
extends State

@export var player: Player

func enter(_msg: Dictionary = {}) -> void:
	if player.animation:
		player.animation.play("idle")

func physics_update(_delta: float) -> void:
	var direction := Input.get_vector("left", "right", "up", "down")
	
	if direction != Vector2.ZERO:
		state_machine.transition_to("Move")

func handle_input(event: InputEvent) -> void:
	if player:
		player.handle_idle_input(event)
