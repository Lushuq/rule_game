extends StaticBody2D

signal door_used(target_room: String)

@export var target_room: String = ""
@export var spawn_position: Vector2 = Vector2.ZERO

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var area: Area2D = $Area2D
@onready var light: PointLight2D = $PointLight2D

var is_interactable: bool = true

func _ready() -> void:
	area.body_entered.connect(_on_area_body_entered)
	area.body_exited.connect(_on_area_body_exited)

func on_interact() -> void:
	if not is_interactable:
		return
	
	door_used.emit(target_room)

func _on_area_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		light.energy = 1.5

func _on_area_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		light.energy = 1.0
