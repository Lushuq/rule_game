class_name Interactable
extends Area2D

@export var dialogue_data: DialogueData

func _ready() -> void:
	input_event.connect(_on_input_event)

func _on_input_event(viewport: Node, event: InputEvent, shape_idx: int) -> void:
	if event is InputEventMouseButton and event.is_pressed() and event.button_index == MOUSE_BUTTON_LEFT:
		if dialogue_data:
			EventBus.object_clicked.emit(dialogue_data.object_name, dialogue_data.dialogue)
