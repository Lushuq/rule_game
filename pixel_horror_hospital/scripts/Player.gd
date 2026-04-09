class_name Player
extends CharacterBody2D

# 信号
signal interacted_with(object: Node)
signal sanity_changed(sanity: float)
signal collected_clue(clue: Dictionary)

# 导出变量
@export var speed: float = 200.0
@export var jump_velocity: float = -400.0
@export var interaction_distance: float = 50.0

# 内部变量
var _sanity: float = 100.0
var _current_room: String = ""
var _notebook_open: bool = false

# 节点引用
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D
@onready var interaction_ray: RayCast2D = $InteractionRay

func _ready() -> void:
	# 确保碰撞形状正确设置
	if not collision_shape:
		var shape := CollisionShape2D.new()
		shape.shape = RectangleShape2D.new()
		shape.shape.size = Vector2(32, 64)
		add_child(shape)
		collision_shape = shape

	# 确保交互射线正确设置
	if not interaction_ray:
		var ray := RayCast2D.new()
		ray.name = "InteractionRay"
		ray.target_position = Vector2(40, 0)
		add_child(ray)
		interaction_ray = ray

	# 连接信号
	call_deferred("_connect_sanity_signal")

func _connect_sanity_signal() -> void:
	if SanityManager and SanityManager.singleton:
		SanityManager.singleton.connect("sanity_changed", _on_sanity_changed)

func _physics_process(delta: float) -> void:
	if _notebook_open:
		return

	# 获取输入方向
	var direction := Input.get_axis("left", "right")
	var new_velocity := Vector2.ZERO

	# 水平移动
	if direction != 0:
		new_velocity.x = direction * speed
		# 翻转精灵
		if sprite:
			sprite.flip_h = direction < 0
	else:
		new_velocity.x = move_toward(velocity.x, 0, speed * 2)

	# 跳跃
	if is_on_floor() and Input.is_action_just_pressed("jump"):
		new_velocity.y = jump_velocity
	else:
		new_velocity.y = velocity.y

	# 重力
	new_velocity.y += 1000.0 * delta

	# 应用速度
	velocity = new_velocity
	move_and_slide()

	# 相机跟随
	var camera = get_viewport().get_camera_2d()
	if camera:
		camera.position = Vector2(position.x, position.y)

func _input(event: InputEvent) -> void:
	# 交互
	if event.is_action_just_pressed("interact"):
		_interact()

	# 打开/关闭笔记本
	if event.is_action_just_pressed("notebook"):
		_notebook_open = not _notebook_open
		if NotebookUI and NotebookUI.singleton:
			NotebookUI.singleton.show_notebook(_notebook_open)

func _interact() -> void:
	# 检测交互对象
	interaction_ray.cast_to = Vector2(interaction_distance if not sprite or not sprite.flip_h else -interaction_distance, 0)
	interaction_ray.force_raycast_update()

	if interaction_ray.is_colliding():
		var collider = interaction_ray.get_collider()
		if collider and collider.has_method("interact"):
			collider.interact(self)
			interacted_with.emit(collider)

func _on_sanity_changed(new_sanity: float) -> void:
	_sanity = new_sanity
	sanity_changed.emit(_sanity)

func get_sanity() -> float:
	return _sanity

func set_current_room(room: String) -> void:
	_current_room = room

func get_current_room() -> String:
	return _current_room

func collect_clue(clue: Dictionary) -> void:
	collected_clue.emit(clue)
	if NotebookUI and NotebookUI.singleton:
		NotebookUI.singleton.add_clue(clue)