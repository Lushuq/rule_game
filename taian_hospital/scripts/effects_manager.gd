extends Node

@onready var canvas_modulate: CanvasModulate = $CanvasModulate
@onready var camera: Camera2D = null

var screen_shake_intensity: float = 0.0
var screen_shake_duration: float = 0.0
var color_shift_intensity: float = 0.0
var color_shift_duration: float = 0.0

var original_camera_position: Vector2 = Vector2.ZERO

func _ready() -> void:
	var player = get_tree().get_first_node_in_group("player")
	if player:
		var parent = player.get_parent()
		if parent.has_node("Camera2D"):
			camera = parent.get_node("Camera2D")
			original_camera_position = camera.position

func trigger_screen_shake(intensity: float = 5.0, duration: float = 0.3) -> void:
	screen_shake_intensity = intensity
	screen_shake_duration = duration

func trigger_color_shift(intensity: float = 0.3, duration: float = 0.5) -> void:
	color_shift_intensity = intensity
	color_shift_duration = duration

func trigger_horror_effects(severity: int = 1) -> void:
	match severity:
		1:
			trigger_screen_shake(3.0, 0.2)
			trigger_color_shift(0.1, 0.3)
		2:
			trigger_screen_shake(6.0, 0.4)
			trigger_color_shift(0.2, 0.5)
		3:
			trigger_screen_shake(10.0, 0.6)
			trigger_color_shift(0.4, 0.8)

func _process(delta: float) -> void:
	update_screen_shake(delta)
	update_color_shift(delta)

func update_screen_shake(delta: float) -> void:
	if screen_shake_duration > 0 and camera:
		screen_shake_duration -= delta
		var offset = Vector2(
			randf_range(-screen_shake_intensity, screen_shake_intensity),
			randf_range(-screen_shake_intensity, screen_shake_intensity)
		)
		camera.position = original_camera_position + offset
		
		if screen_shake_duration <= 0:
			camera.position = original_camera_position
			screen_shake_intensity = 0.0

func update_color_shift(delta: float) -> void:
	if color_shift_duration > 0:
		color_shift_duration -= delta
		var t = color_shift_duration / max(0.01, color_shift_duration + delta)
		var r = 1.0 + color_shift_intensity * (1.0 - t) * sin(OS.get_ticks_msec() / 100.0)
		var g = 1.0 - color_shift_intensity * (1.0 - t) * 0.5
		var b = 1.0 + color_shift_intensity * (1.0 - t) * cos(OS.get_ticks_msec() / 150.0)
		canvas_modulate.color = Color(r, g, b, 1.0)
	else:
		canvas_modulate.color = Color(1.0, 1.0, 1.0, 1.0)
