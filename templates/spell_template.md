# {{ spell_data['name'] }}

## Description
{{ spell_data.get('desc', ['No description'])[0] }}

## Higher Level
{{ spell_data.get('higher_level', '') }}

## Details
{% for key, value in spell_data.items() %}
	{% if key == 'damage' %}
		{% break %}
	{% endif %}
	- {{ key|capitalize }}: {{ value }}
{% endfor %}

## Damage at Slot Level
| Slot Level | Damage |
|------------|--------|
{% for level, damage in spell_data.get('damage', {}).get('damage_at_slot_level', {}).items() %}
| {{ level }} | {{ damage }} |
{% endfor %}

# Backlinks
- School: [[{{ spell_data.get('school', {}).get('name', '') }}]]
- Classes: {% for c in spell_data.get('classes', []) %}[[{{ c['name'] }}]] {% endfor %}
- Subclasses: {% for sub_c in spell_data.get('subclasses', []) %}[[{{ sub_c['name'] }}]] {% endfor %}
