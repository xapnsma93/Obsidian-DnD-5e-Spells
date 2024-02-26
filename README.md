# Obsidian-DnD-5e-Spells
Trying to fetch DnD 5e spells using API, then formating the spells to md files for Obsidian in a certain location.

# Requirements:
Use 
```
pip install -r requirements.txt
```
to download requests and jinja2

# Usage:

usage: main.py [-h] [--path PATH] [--spell SPELL]

Generate Markdown files for D&D 5e spells.

options:
  -h, --help     show this help message and exit
  --path PATH    Directory path to save the files
  --spell SPELL  Specific spell to generate the MD file for

# Spell Template:
Modify the spell_template.md to create your own template.
