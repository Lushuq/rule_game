class_name EventBus
extends Node

# Interaction events
signal object_clicked(object_name: String, dialogue: String)
signal dialogue_started
signal dialogue_finished

singleton
