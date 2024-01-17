import argparse
import os
import requests
from jinja2 import Environment, FileSystemLoader


def ensure_valid_directory(directory):

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        except Exception as error:
            print(f"Error creating directory '{directory}': {error}")
            return False

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory path.")
        return False

    return True


def get_spell_details(spell_url):
    full_url = f"https://www.dnd5eapi.co{spell_url}"
    response = requests.get(full_url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching spell details for {spell_url}. Status code: {response.status_code}")
        return None


def save_spell_md_file(spell_details, spell_template, save_directory):
    spell_name = spell_details['name']
    # Replace '/' with another character (curse you antipathy/sympathy, blindness/deafness) in the spell name
    sanitized_spell_name = spell_name.replace('/', '_').title()
    file_path = os.path.join(save_directory, f'{sanitized_spell_name}.md')
    content = spell_template.render(spell_data=spell_details)

    if os.path.exists(file_path):
        user_response = input(f'The file {file_path} already exists. Do you want to overwrite it? (y/n): ')
        if user_response.lower() != 'y':
            print(f'Skipping {file_path}.')
            return # File was not saved

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'Created file: {file_path}')
    print("MD file created successfully.")


def main():
    parser = argparse.ArgumentParser(description='Generate Markdown files for D&D 5e spells.')
    parser.add_argument('--path', help='Directory path to save the files', default=os.path.curdir)
    parser.add_argument('--spell', help='Specific spell to generate the MD file for')

    args = parser.parse_args()

    save_directory = args.path

    # Ensure that the save directory exists
    if not ensure_valid_directory(save_directory):
        return

    spell_name_to_generate = args.spell

    url = "https://www.dnd5eapi.co/api/spells"
    response = requests.get(url)

    if response.status_code == 200:
        spell_data = response.json()
        spells = spell_data['results']

        # jinja2 template from file
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        template_loader = FileSystemLoader(searchpath=template_dir)
        template_env = Environment(loader=template_loader)
        spell_template = template_env.get_template('spell_template.md')

        if spell_name_to_generate:
            matching_spells = [spell for spell in spells if spell_name_to_generate.lower() in spell['name'].lower()]
            if not matching_spells:
                print(f'No spells found with the name "{spell_name_to_generate}" in the API.')
            elif len(matching_spells) == 1:
                spell_details = get_spell_details(matching_spells[0]['url'])
                save_spell_md_file(spell_details, spell_template, save_directory)
            else:
                print(f'Multiple spells found with the name "{spell_name_to_generate}":')
                for i, spell in enumerate(matching_spells, 1):
                    print(f"{i}. {spell['name']}")
                spell_choice = input("Enter the number of the spell you want to generate an MD file for (or type 'back' to return to the main menu): ")
                if spell_choice.lower() == 'back':
                    return  # returns to the main menu
                try:
                    spell_index = int(spell_choice) - 1
                    selected_spell = matching_spells[spell_index]
                    spell_details = get_spell_details(selected_spell['url'])
                    save_spell_md_file(spell_details, spell_template, save_directory)
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a valid number.")
        else:
            for all_spells in spells:
                spell_details = get_spell_details(all_spells['url'])

                save_spell_md_file(spell_details, spell_template, save_directory)
    else:
        print("Error", response.status_code)

if __name__ == "__main__":
    main()
