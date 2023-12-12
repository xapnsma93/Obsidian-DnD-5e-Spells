import requests
import os
from tkinter import Tk, filedialog

def choose_directory():
    root = Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title='Select Directory to create md files to')
    root.destroy()
    return directory

def get_spell_details(spell_url):
    full_url = f"https://www.dnd5eapi.co{spell_url}"
    response = requests.get(full_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching spell details for {spell_url}. Status code: {response.status_code}")
        return None

def create_spell_markdown(spell_data, save_directory):
    #variables
    spell_name = spell_data.get('name', 'Unknown Spell')
    spell_desc = spell_data.get('desc', ['No description'])[0]
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
    damage_at_slot_level = spell_data.get('damage', {}).get('damage_at_slot_level', {})
    if isinstance(damage_at_slot_level, str):
        # If damage_at_slot_level is a string, create a list with a dictionary
        damage_at_slot_level = [{'level': 'N/A', 'damage': damage_at_slot_level}]
    elif not isinstance(damage_at_slot_level, list):
        # If damage_at_slot_level is neither a string nor a list, create an empty list
        damage_at_slot_level = []
    damage_table = (
            '\n| Slot Level | Damage |\n|------------|--------|\n' +
            '\n'.join([f'| {level.get("level", "N/A")} | {level.get("damage", "N/A")} |' for level in damage_at_slot_level])
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

def save_spell_md_file(spell_details, content, save_directory):
    spell_name = spell_details.get('name', 'Unknown Spell')
    file_path = os.path.join(save_directory, f'{spell_name}.md')
    if os.path.exists(file_path):
        user_response = input(f'The file {file_path} already exists. Do you want to overwrite it? (y/n): ')
        if user_response.lower() != 'y':
            print(f'Skipping {file_path}.')
            return False  # File was not saved
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f'Created file: {file_path}')
    return True  # File was saved successfully

def main():
    url = "https://www.dnd5eapi.co/api/spells"
    response = requests.get(url)

    if response.status_code == 200:
        spell_data = response.json()
        spells = spell_data['results']
        save_directory = choose_directory()

        if not save_directory:
            print("User canceled. Exiting.")
            return  # breaks if the user cancels directory selection

        while True:
            # Main menu
            print("\nMain Menu:")
            print("1) Create MD files for all spells")
            print("2) Create for a specific spell")
            print("3) Stop")

            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                for spell in spells:
                    spell_details = get_spell_details(spell['url'])
                    if spell_details is not None:
                        content = create_spell_markdown(spell_details, save_directory)
                        save_result = save_spell_md_file(spell_details, content, save_directory)
                        if save_result:
                            print(f"MD file created successfully for {spell_details['name']}.")
            elif choice == "2":
                while True:
                    spell_name_to_generate = input("Enter the name of the spell you want to generate an MD file for (or type 'back' to return to the main menu): ")

                    if spell_name_to_generate.lower() == 'back':
                        break  # returns to the main menu

                    matching_spells = [spell for spell in spells if spell_name_to_generate.lower() in spell['name'].lower()]

                    if not matching_spells:
                        print(f'No spells found with the name "{spell_name_to_generate}" in the API.')
                    elif len(matching_spells) == 1:
                        spell_details = get_spell_details(matching_spells[0]['url'])
                        if spell_details is not None:
                            content = create_spell_markdown(spell_details, save_directory)
                            save_result = save_spell_md_file(spell_details, content, save_directory)
                            if save_result:
                                print("MD file created successfully.")
                    else:
                        print(f'Multiple spells found with the name "{spell_name_to_generate}":')
                        for i, spell in enumerate(matching_spells, 1):
                            print(f"{i}. {spell['name']}")

                        spell_choice = input("Enter the number of the spell you want to generate an MD file for (or type 'back' to return to the main menu): ")
                        if spell_choice.lower() == 'back':
                            break  # returns to the main menu

                        try:
                            spell_index = int(spell_choice) - 1
                            selected_spell = matching_spells[spell_index]
                            spell_details = get_spell_details(selected_spell['url'])
                            if spell_details is not None:
                                content = create_spell_markdown(spell_details, save_directory)
                                save_result = save_spell_md_file(spell_details, content, save_directory)
                                if save_result:
                                    print("MD file created successfully.")
                        except (ValueError, IndexError):
                            print("Invalid input. Please enter a valid number.")
            elif choice == "3":
                print("Exiting the program.")
                break  # stops the program
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    else:
        print("Error", response.status_code)

if __name__ == "__main__":
    main()
