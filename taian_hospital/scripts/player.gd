extends CharacterBody2D

signal interacted(interactable: Node)
signal notebook_toggled()

@export var move_speed: float = 200.0
@export var jump_force: float = -400.0
@export var gravity: float = 1200.0
@export var interact_range: float = 50.0

@onready var sprite: ColorRect = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var interact_area: Area2D = $InteractArea
@onready var light: PointLight2D = $PointLight2D

var is_on_ground: bool = false
var facing_right: bool = true
var current_interactable: Node = null

func _physics_process(delta: float) -> void:
	apply_gravity(delta)
	handle_movement()
	handle_jump()
	move_and_slide()
	
	update_sprite_direction()
	check_interactables()

func apply_gravity(delta: float) -> void:
	if not is_on_floor():
		velocity.y += gravity * delta

func handle_movement() -> void:
	var input_dir: float = Input.get_action_strength("move_right") - Input.get_action_strength("move_left")
	velocity.x = input_dir * move_speed

func handle_jump() -> void:
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_force

func update_sprite_direction() -> void:
	if velocity.x > 0:
		facing_right = true
	elif velocity.x < 0:
		facing_right = false

func check_interactables() -> void:
	var interactables = interact_area.get_overlapping_bodies()
	if interactables.size() > 0:
		current_interactable = interactables[0]
	else:
		current_interactable = null

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("interact") and current_interactable:
		interacted.emit(current_interactable)
	
	if Input.is_action_just_pressed("toggle_notebook"):
		notebook_toggled.emit()

func _ready() -> void:
	interact_area.body_entered.connect(_on_interact_area_body_entered)
	interact_area.body_exited.connect(_on_interact_area_body_exited)

func _on_interact_area_body_entered(body: Node) -> void:
	if body.has_method("on_interact"):
		current_interactable = body

func _on_interact_area_body_exited(body: Node) -> void:
	if body == current_interactable:
		current_interactable = null
