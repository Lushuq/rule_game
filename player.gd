class_name Player
extends CharacterBody2D

@export var speed: float = 200.0
@onready var sprite: Sprite2D = $Sprite2D
@onready var state_machine: StateMachine = $StateMachine

