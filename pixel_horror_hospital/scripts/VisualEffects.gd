class_name VisualEffects
extends CanvasLayer

# 单例
static var singleton: VisualEffects = null

# 内部变量
var _shake_timer: Timer = null
var _shake_duration: float = 0.0
var _shake_intensity: float = 0.0
var _shake_offset: Vector2 = Vector2.ZERO

var _color_timer: Timer = null
var _color_duration: float = 0.0
var _original_color: Color = Color(1, 1, 1)
var _target_color: Color = Color(1, 1, 1)

# 节点引用
@onready var canvas_modulate: CanvasModulate = $CanvasModulate

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

	# 创建定时器
	_shake_timer = Timer.new()
	_shake_timer.wait_time = 0.016
	_shake_timer.autostart = false
	_shake_timer.timeout.connect(_on_shake_timeout)
	add_child(_shake_timer)

	_color_timer = Timer.new()
	_color_timer.wait_time = 0.016
	_color_timer.autostart = false
	_color_timer.timeout.connect(_on_color_timeout)
	add_child(_color_timer)

	# 初始化CanvasModulate
	if not canvas_modulate:
		canvas_modulate = CanvasModulate.new()
		canvas_modulate.color = Color(1, 1, 1)
		add_child(canvas_modulate)

func _process(delta: float) -> void:
	# 应用屏幕抖动
	if _shake_timer.is_stopped():
		_shake_offset = Vector2.ZERO
		position = Vector2.ZERO
	else:
		position = _shake_offset

func trigger_shake(duration: float = 0.5, intensity: float = 5.0) -> void:
	_shake_duration = duration
	_shake_intensity = intensity
	_shake_timer.start()

func _on_shake_timeout() -> void:
	_shake_duration -= _shake_timer.wait_time
	if _shake_duration <= 0:
		_shake_timer.stop()
		_shake_offset = Vector2.ZERO
		position = Vector2.ZERO
	else:
		_shake_offset = Vector2(
			random_range(-_shake_intensity, _shake_intensity),
			random_range(-_shake_intensity, _shake_intensity)
		)

func trigger_color_shift(duration: float = 1.0, target_color: Color = Color(1, 0.8, 0.8)) -> void:
	_original_color = canvas_modulate.color
	_target_color = target_color
	_color_duration = duration
	_color_timer.start()

func _on_color_timeout() -> void:
	_color_duration -= _color_timer.wait_time
	if _color_duration <= 0:
		_color_timer.stop()
		canvas_modulate.color = _original_color
	else:
		var t = 1.0 - (_color_duration / 1.0)
		canvas_modulate.color = _original_color.lerp(_target_color, t)

func trigger_hallucination() -> void:
	# 触发幻觉效果
	trigger_shake(0.8, 8.0)
	trigger_color_shift(2.0, Color(0.8, 0.2, 0.8))

func trigger_horror_event() -> void:
	# 触发恐怖事件效果
	trigger_shake(1.0, 10.0)
	trigger_color_shift(3.0, Color(0.2, 0.0, 0.0))