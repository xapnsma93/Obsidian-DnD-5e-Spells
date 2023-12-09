import requests
import os
from tkinter import Tk, filedialog


def choose_directory():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title='Select Directory')
    return directory


def create_spell_markdown(spell_data, save_directory):
    spell_name = spell_data['name']
    spell_desc = spell_data['desc'][0]
    higher_level = spell_data.get('higher_level', '')
    range_val = spell_data.get('range', '')
    components = ','.join(spell_data.get('components', []))
    material = spell_data.get('material', '')
    ritual = spell_data.get('ritual', 'False')
    duration = spell_data.get('duration', '')
    concentration = spell_data.get('concentration', 'False')
    casting_time = spell_data.get('casting_time', '')
    attack_type = spell_data.get('attack_type', '')
    damage_type = spell_data.get('damage', {}).get('damage_type', {}).get('name', '')


url = "https://www.dnd5eapi.co/api/spells"
response = requests.get(url)

if response.status_code == 200:
    spell_data = response.json()
    spells = spell_data['results']
    save_directory = choose_directory()

    for spell in spells:
        spell_url = f"https://www.dnd5eapi.co{spell['url']}"
        spell_name = spell['name']
        spell_response = requests.get(spell_url)
        spell_details = spell_response.json()
        content = f'# {spell_name}\n\n{spell_details}'

        file_path = os.path.join(save_directory, f'{spell_name}.md')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Created file: {file_path}')
else:
    print("Error", response.status_code)