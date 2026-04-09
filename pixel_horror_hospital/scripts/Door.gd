class_name Door
extends Area2D

# 导出变量
@export var target_room: String = ""
@export var spawn_position: Vector2 = Vector2.ZERO

# 信号
signal door_entered()

func _ready() -> void:
	# 连接信号
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
	if body is Player and RoomManager and RoomManager.singleton:
		# 切换房间
		RoomManager.singleton.load_room(target_room)
		# 设置玩家位置
		body.position = spawn_position
		door_entered.emit()