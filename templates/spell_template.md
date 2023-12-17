# {{ spell_data.name }}

## Description
{% for section in spell_data.desc|default('No description') %}
{{ section }}
{% endfor %}

## Higher Level
{{ spell_data.higher_level|default('No higher level') }}

## Details

	- Range: {{ spell_data.range|default('Unknown range') }}

	- Components: {{ spell_data.components|default('None') }}

	- Ritual: {{ spell_data.ritual|default('Not a ritual spell') }}

	- Duration: {{ spell_data.duration|default('Unknown') }}

	- Concentration: {{ spell_data.concentration|default('No Concentration') }}

	- Casting Time: {{ spell_data.casting_time|default('1 action') }}

	- Level: {{ spell_data.level|default('Unknown') }}
{% if spell_data.dc %}
	- Dc: {{ spell_data.dc.dc_type.name }} (Success: {{ spell_data.dc.dc_success|default('Unknown') }})
	{% endif %}
{% if spell_data.area_of_effect %}
	- Area of Effect: {{ spell_data.area_of_effect.type }} (Size: {{ spell_data.area_of_effect.size }})
	{% endif %}

## Damage at Slot Level
| Slot Level | Damage |
{% if spell_data.damage and spell_data.damage.damage_at_slot_level %}
{% for level, damage in spell_data.damage.damage_at_slot_level.items() %}
|---- {{ level }} ----|- {{ damage }} -|
{% endfor %}
{% else %}
	('No damage description for this spell')
{% endif %}
# Backlinks
- School: [[{{ spell_data.school.name|default('Unknown School') }}]]
- Classes: {% for c in spell_data.classes %}[[{{ c.name }}]] {% endfor %}
- Subclasses: {% for sub_c in spell_data.subclasses %}[[{{ sub_c.name }}]] {% endfor %}
