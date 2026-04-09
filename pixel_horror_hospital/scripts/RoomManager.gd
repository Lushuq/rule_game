class_name RoomManager
extends Node

# 信号
signal room_changed(room_name: String)

# 单例
static var singleton: RoomManager = null

# 房间数据
var current_room: String = ""
var rooms: Dictionary = {
	"ward": preload("res://scenes/rooms/Ward.tscn"),
	"corridor": preload("res://scenes/rooms/Corridor.tscn")
}

# 玩家引用
var player: Player = null

func _ready() -> void:
	if singleton != null:
		singleton.queue_free()
	singleton = self

	# 延迟加载初始房间
	call_deferred("load_room", "ward")

func load_room(room_name: String) -> void:
	if not rooms.has(room_name):
		push_error("Room not found: %s" % room_name)
		return

	# 移除当前房间
	var current_scene = get_tree().current_scene
	if current_scene:
		current_scene.queue_free()

	# 加载新房间
	var room_scene = rooms[room_name].instantiate()
	# 先添加到场景树
	get_tree().root.add_child(room_scene)
	# 延迟设置当前场景，确保场景树操作完成
	call_deferred("_set_current_scene", room_scene)

	# 更新当前房间
	current_room = room_name
	room_changed.emit(room_name)

	# 更新玩家房间信息
	if player:
		player.set_current_room(room_name)

func set_player(p: Player) -> void:
	player = p

func get_current_room() -> String:
	return current_room

func _set_current_scene(scene: Node) -> void:
	# 延迟设置当前场景
	get_tree().current_scene = scene