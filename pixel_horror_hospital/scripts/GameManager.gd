class_name GameManager
extends Node

# 信号
signal game_started
signal game_over(won: bool)
signal night_ended

# 单例
static var singleton: GameManager = null

# 游戏状态
var is_playing: bool = false
var current_night: int = 1
var night_duration: float = 60.0  # 第一夜60秒
var elapsed_time: float = 0.0

# 胜利条件
var required_clues: int = 3
var collected_clues: int = 0

# 节点引用
@onready var timer: Timer = $Timer

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

	# 创建定时器
	if not timer:
		timer = Timer.new()
		timer.wait_time = 1.0
		timer.autostart = false
		timer.timeout.connect(_on_timer_timeout)
		add_child(timer)

	# 延迟连接信号并启动游戏
	call_deferred("_connect_signals_and_start")

func _connect_signals_and_start() -> void:
	if SanityManager and SanityManager.singleton:
		SanityManager.singleton.sanity_depleted.connect(_on_sanity_depleted)
	# 启动游戏
	start_game()

func start_game() -> void:
	is_playing = true
	elapsed_time = 0.0
	collected_clues = 0
	timer.start()
	game_started.emit()

func _on_timer_timeout() -> void:
	if not is_playing:
		return

	elapsed_time += 1.0

	# 检查时间是否结束
	if elapsed_time >= night_duration:
		_end_night()

	# 检查胜利条件
	if collected_clues >= required_clues:
		_win_game()

func _end_night() -> void:
	timer.stop()
	is_playing = false
	night_ended.emit()
	# 检查是否收集了足够的线索
	if collected_clues >= required_clues:
		_win_game()
	else:
		_lose_game()

func _on_sanity_depleted() -> void:
	_lose_game()

func _win_game() -> void:
	timer.stop()
	is_playing = false
	game_over.emit(true)

func _lose_game() -> void:
	timer.stop()
	is_playing = false
	game_over.emit(false)

func add_clue() -> void:
	collected_clues += 1

func get_elapsed_time() -> float:
	return elapsed_time

func get_night_duration() -> float:
	return night_duration

func get_collected_clues() -> int:
	return collected_clues

func get_required_clues() -> int:
	return required_clues