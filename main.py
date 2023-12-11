import requests
import os
from tkinter import Tk, filedialog

def choose_directory():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title='Select Directory')
    return directory

def create_spell_markdown(spell_data, save_directory):
    #variables
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
    #tables with dmg at lvl slots
    #damage_at_slot_level = spell_data.get('damage',{}).get('damage_type'),{}).get('name','')
    damage_at_slot_level = spell_data.get('damage', {}).get('damage_at_slot_level', {}).get('name', '')
    damage_table = ('\n| Slot Level | Damage |\n|------------|--------|\n|'
                    + '\n'.join([f'| {level} | {damage} |' for level, damage in damage_at_slot_level.items()])
    )
    # Schools, Classes, Subclasses with backlinks
    school = spell_data.get('school',{}).get('name','')
    classes = '  '.join([f'[[{c["name"]}]]' for c in spell_data.get('classes',[])])
    subclasses = '  '.join([f'[[{sub_c["name"]}]]' for sub_c in spell_data.get('subclasses',[])])
    #description+++ = content+++
    content = f'# {spell_name}\n\n'
    content += f'{spell_desc}\n\n'  # Description as the main content
    content += f'## Higher Level\n{higher_level}\n\n'
    content += f'## Details\n'
    content += f'- Range: {range_val}\n'
    content += f'- Components: {components}\n'
    content += f'- Material: {material}\n'
    content += f'- Ritual: {ritual}\n'
    content += f'- Duration: {duration}\n'
    content += f'- Concentration: {concentration}\n'
    content += f'- Casting Time: {casting_time}\n'
    content += f'- Attack Type: {attack_type}\n'
    content += f'- Damage Type: {damage_type}\n'
    content += damage_table
    #backlinks
    content += f'\n- School: [[{school}]]\n'
    content += f'- Classes: {classes}\n'
    content += f'- Subclasses: {subclasses}\n'
    return content

url = "https://www.dnd5eapi.co/api/spells"
response = requests.get(url)

if response.status_code == 200:
    spell_data = response.json()
    spells = spell_data['results']
    save_directory = choose_directory()

    if not save_directory:
        print("User canceled. Exiting.")
    else:
        for spell in spells:
            spell_url = f"https://www.dnd5eapi.co{spell['url']}"
            # spell_name = spell['name']
            spell_response = requests.get(spell_url)
            spell_details = spell_response.json()
            #content = f'# {spell_name}\n\n{spell_details}'
            content = create_spell_markdown(spell_details)

            file_path = os.path.join(save_directory, f'{spell_details["name"]}.md')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Created file: {file_path}')
else:
    print("Error", response.status_code)