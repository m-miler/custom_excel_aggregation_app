import os
import json


class Utils:
    @staticmethod
    def get_files_name_from_folder(folder_path: str) -> list:
        """ Make a list with all files name in the folder."""
        files = [file_name for file_name in os.listdir(folder_path)]
        return files

    @staticmethod
    def save_settings_to_json_file(settings: dict) -> None:
        """ Save survey settings as json file."""
        settings_file_name = f"settings_{settings.get('SURVEY_NAME')}"
        with open(f'colostrum_code/survey_settings/{settings_file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(settings, file,  ensure_ascii=False, indent=2)
            print('Survey has been created correctly')

    @staticmethod
    def check_if_setting_file_exist(survey_name: str) -> dict | None:
        """ Check if settings for chosen survey exists. If true return survey settings."""
        settings_file_path = f"colostrum_code/survey_settings/settings_{survey_name}.json"
        if os.path.isfile(settings_file_path):
            with open(settings_file_path, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                return settings
        else:
            print("Settings for selected survey doesn't exist.")



