extends Control

signal closed()

@onready var background: ColorRect = $Background
@onready var title_label: Label = $TitleLabel
@onready var clue_container: VBoxContainer = $ScrollContainer/ClueContainer
@onready var close_button: Button = $CloseButton

var clues: Array[String] = []
var is_open: bool = false

func _ready() -> void:
	close_button.pressed.connect(toggle)
	visible = false

func toggle() -> void:
	is_open = !is_open
	visible = is_open
	get_tree().paused = is_open
	if not is_open:
		closed.emit()

func add_clue(clue_text: String) -> void:
	if not clues.has(clue_text):
		clues.append(clue_text)
		_update_clue_list()

func _update_clue_list() -> void:
	for child in clue_container.get_children():
		child.queue_free()
	
	for clue in clues:
		var label = Label.new()
		label.text = "- " + clue
		label.autowrap_mode = TextServer.AUTOWRAP_WORD
		label.custom_minimum_size.x = 500
		label.add_theme_color_override("font_color", Color(0.2, 0.2, 0.2))
		clue_container.add_child(label)
