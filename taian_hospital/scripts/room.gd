extends Node2D

signal room_entered(room_name: String)
signal room_exited(room_name: String)

@export var room_name: String = "Room"
@export var is_start_room: bool = false

@onready var lights: Node2D = $Lights
@onready var doors: Node2D = $Doors
@onready var interactables: Node2D = $Interactables

var is_active: bool = false

func _ready() -> void:
	if is_start_room:
		activate()
	else:
		deactivate()

func activate() -> void:
	is_active = true
	visible = true
	lights.visible = true
	process_mode = Node.PROCESS_MODE_INHERIT
	room_entered.emit(room_name)

func deactivate() -> void:
	is_active = false
	visible = false
	lights.visible = false
	process_mode = Node.PROCESS_MODE_DISABLED
	room_exited.emit(room_name)
