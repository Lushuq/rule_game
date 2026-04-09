extends StaticBody2D

signal clue_discovered(clue: String)

@export var clue_text: String = ""
@export var rule_id: String = ""
@export var clue_index: int = 0
@export var interact_message: String = "按E键检查"

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var area: Area2D = $Area2D
@onready var light: PointLight2D = $PointLight2D
@onready var message_label: Label = $MessageLabel

var is_nearby: bool = false
var has_been_interacted: bool = false

func _ready() -> void:
	area.body_entered.connect(_on_area_body_entered)
	area.body_exited.connect(_on_area_body_exited)
	message_label.visible = false

func on_interact() -> void:
	if has_been_interacted:
		return
	
	has_been_interacted = true
	if clue_text != "":
		clue_discovered.emit(clue_text)
	light.energy = 2.0
	message_label.text = "已收集线索！"
	await get_tree().create_timer(2.0).timeout
	message_label.visible = false

func _on_area_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		is_nearby = true
		if not has_been_interacted:
			message_label.text = interact_message
			message_label.visible = true
		light.energy = 1.5

func _on_area_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		is_nearby = false
		message_label.visible = false
		light.energy = 1.0
