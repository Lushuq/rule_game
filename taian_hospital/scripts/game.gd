extends Node

signal game_won()
signal game_lost()

@onready var player: CharacterBody2D = $Player
@onready var room_manager: Node = $RoomManager
@onready var rule_manager: Node = $RuleManager
@onready var sanity_manager: Node = $SanityManager
@onready var effects_manager: Node = $EffectsManager
@onready var notebook_ui: Control = $NotebookUI
@onready var sanity_bar: ProgressBar = $HUD/SanityBar
@onready var clue_count_label: Label = $HUD/ClueCountLabel
@onready var time_label: Label = $HUD/TimeLabel
@onready var global_light: DirectionalLight2D = $GlobalLight

var current_room: Node2D = null
var rooms: Dictionary = {}
var clues_collected: int = 0
var required_clues: int = 5
var game_time: float = 0.0
var game_over: bool = false

func _ready() -> void:
	setup_input_map()
	setup_connections()
	initialize_rooms()
	sanity_bar.max_value = sanity_manager.max_sanity
	sanity_bar.value = sanity_manager.current_sanity

func setup_input_map() -> void:
	if not InputMap.has_action("move_left"):
		InputMap.add_action("move_left")
		var event = InputEventKey.new()
		event.keycode = KEY_A
		InputMap.action_add_event("move_left", event)
	
	if not InputMap.has_action("move_right"):
		InputMap.add_action("move_right")
		var event = InputEventKey.new()
		event.keycode = KEY_D
		InputMap.action_add_event("move_right", event)
	
	if not InputMap.has_action("jump"):
		InputMap.add_action("jump")
		var event = InputEventKey.new()
		event.keycode = KEY_SPACE
		InputMap.action_add_event("jump", event)
	
	if not InputMap.has_action("interact"):
		InputMap.add_action("interact")
		var event = InputEventKey.new()
		event.keycode = KEY_E
		InputMap.action_add_event("interact", event)
	
	if not InputMap.has_action("toggle_notebook"):
		InputMap.add_action("toggle_notebook")
		var event1 = InputEventKey.new()
		event1.keycode = KEY_TAB
		InputMap.action_add_event("toggle_notebook", event1)
		var event2 = InputEventKey.new()
		event2.keycode = KEY_I
		InputMap.action_add_event("toggle_notebook", event2)

func setup_connections() -> void:
	player.interacted.connect(_on_player_interacted)
	player.notebook_toggled.connect(_on_notebook_toggled)
	
	rule_manager.rule_discovered.connect(_on_rule_discovered)
	rule_manager.rule_violated.connect(_on_rule_violated)
	rule_manager.sanity_lost.connect(_on_sanity_lost)
	
	sanity_manager.sanity_changed.connect(_on_sanity_changed)
	sanity_manager.sanity_depleted.connect(_on_sanity_depleted)

func initialize_rooms() -> void:
	for child in room_manager.get_children():
		if child is Node2D and child.has_method("activate"):
			rooms[child.room_name] = child
			if child.is_start_room:
				current_room = child
				player.global_position = Vector2(320, 200)
			
			if child.has_node("Doors"):
				for door in child.get_node("Doors").get_children():
					if door.has_method("door_used"):
						door.door_used.connect(_on_door_used)
			
			if child.has_node("Interactables"):
				for item in child.get_node("Interactables").get_children():
					if item.has_method("clue_discovered"):
						item.clue_discovered.connect(_on_interactable_clue_discovered)

func _process(delta: float) -> void:
	if game_over:
		return
	
	game_time += delta
	var minutes = int(game_time / 60)
	var seconds = int(game_time) % 60
	time_label.text = "时间: %02d:%02d" % [minutes, seconds]
	
	if clues_collected >= required_clues:
		win_game()

func _on_player_interacted(interactable: Node) -> void:
	if interactable.has_method("on_interact"):
		interactable.on_interact()
	
	if interactable.has_method("door_used"):
		pass

func _on_notebook_toggled() -> void:
	notebook_ui.toggle()

func _on_rule_discovered(rule_id: String, clue: String) -> void:
	notebook_ui.add_clue(clue)
	clues_collected += 1
	clue_count_label.text = "线索: %d/%d" % [clues_collected, required_clues]

func _on_rule_violated(rule_id: String, severity: int) -> void:
	effects_manager.trigger_horror_effects(severity)

func _on_sanity_lost(amount: float) -> void:
	sanity_manager.lose_sanity(amount)

func _on_sanity_changed(new_value: float) -> void:
	sanity_bar.value = new_value

func _on_sanity_depleted() -> void:
	lose_game()

func _on_door_used(target_room: String) -> void:
	for child in room_manager.get_children():
		if child.room_name == target_room:
			switch_room(target_room, child.get_node("Doors").get_child(0).spawn_position)
			break

func _on_interactable_clue_discovered(clue: String) -> void:
	_on_rule_discovered("", clue)

func switch_room(room_name: String, spawn_pos: Vector2) -> void:
	if not rooms.has(room_name):
		return
	
	if current_room:
		current_room.deactivate()
	
	current_room = rooms[room_name]
	current_room.activate()
	player.global_position = spawn_pos

func win_game() -> void:
	game_over = true
	get_tree().paused = true
	print("恭喜！你收集了足够的线索，第一夜存活成功！")

func lose_game() -> void:
	game_over = true
	get_tree().paused = true
	print("SAN值耗尽...你被黑暗吞噬了。")
