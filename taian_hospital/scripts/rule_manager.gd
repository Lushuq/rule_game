extends Node

signal rule_discovered(rule_id: String, clue: String)
signal rule_violated(rule_id: String, severity: int)
signal sanity_lost(amount: float)

class Rule:
	var id: String
	var description: String
	var is_active: bool = true
	var discovered: bool = false
	var clues: Array[String] = []
	var evolution_stage: int = 0
	var max_evolution: int = 2

var rules: Dictionary = {}
var player_actions: Array = []
var max_rules: int = 5
var min_rules: int = 3

func _ready() -> void:
	initialize_rules()

func initialize_rules() -> void:
	rules.clear()
	
	var rule1 = Rule.new()
	rule1.id = "rule_no_lights"
	rule1.description = "午夜后，不要在黑暗中停留超过10秒"
	rule1.clues = ["墙上的便条写着：'灯光是你的朋友'", "病历上有奇怪的备注：'黑暗中有人'"]
	rules[rule1.id] = rule1
	
	var rule2 = Rule.new()
	rule2.id = "rule_no_look_back"
	rule2.description = "听到脚步声时，不要回头"
	rule2.clues = ["旧电视闪烁着：'别回头'", "鬼魂低语：'看着前方'"]
	rules[rule2.id] = rule2
	
	var rule3 = Rule.new()
	rule3.id = "rule_doors"
	rule3.description = "离开房间前，必须关上门"
	rule3.clues = ["门上的便条：'随手关门'"]
	rules[rule3.id] = rule3
	
	var rule4 = Rule.new()
	rule4.id = "rule_mirror"
	rule4.description = "不要长时间盯着镜子"
	rule4.clues = ["镜子上有雾气写的字：'别看'"]
	rules[rule4.id] = rule4
	
	var rule5 = Rule.new()
	rule5.id = "rule_silence"
	rule5.description = "保持安静，它们能听到你的呼吸"
	rule5.clues = ["墙上的血字：'嘘...'"]
	rules[rule5.id] = rule5

func get_active_rules() -> Array:
	var result = []
	for rule in rules.values():
		if rule.is_active:
			result.append(rule)
	return result

func discover_clue(rule_id: String, clue_index: int) -> void:
	if not rules.has(rule_id):
		return
	
	var rule = rules[rule_id]
	if clue_index < rule.clues.size() and not rule.discovered:
		rule_discovered.emit(rule_id, rule.clues[clue_index])
		if clue_index >= rule.clues.size() - 1:
			rule.discovered = true

func check_rule_violation(action: String, context: Dictionary) -> void:
	player_actions.append(action)
	
	for rule in rules.values():
		if not rule.is_active:
			continue
		
		var violated = false
		var severity = 1
		
		match rule.id:
			"rule_no_lights":
				if context.has("in_dark") and context["in_dark"] > 10:
					violated = true
					severity = 2
			"rule_no_look_back":
				if action == "look_back" and context.has("hearing_steps") and context["hearing_steps"]:
					violated = true
					severity = 3
			"rule_doors":
				if action == "leave_room" and context.has("door_open") and context["door_open"]:
					violated = true
			"rule_mirror":
				if context.has("looking_mirror") and context["looking_mirror"] > 5:
					violated = true
					severity = 2
			"rule_silence":
				if action == "make_noise":
					violated = true
		
		if violated:
			rule_violated.emit(rule.id, severity)
			sanity_lost.emit(severity * 5.0)
			evolve_rule(rule.id)

func evolve_rule(rule_id: String) -> void:
	if not rules.has(rule_id):
		return
	
	var rule = rules[rule_id]
	if rule.evolution_stage < rule.max_evolution:
		rule.evolution_stage += 1
		match rule.id:
			"rule_no_lights":
				rule.description = "午夜后，任何光线都可能引来它们..."
			"rule_no_look_back":
				rule.description = "脚步声越来越近，即使不回头也不安全了..."
