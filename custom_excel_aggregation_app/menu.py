from typing import Any


class Menu:
    @staticmethod
    def show() -> None:
        print("Menu:")
        print("1. Create a new survey")
        print("2. Load survey settings from file")
        print("3. Save survey data to CSV")
        print("4. Exit")

    @staticmethod
    def get_user_choice() -> str:
        user_input = input('\nPlease select number from menu to execute --> ')
        return user_input

    @staticmethod
    def get_survey_settings() -> dict[str, Any]:
        settings: dict[str, Any] = dict()
        settings['SURVEY_NAME'] = input("Please provide the survey full name: ").lower()
        settings['DATABASE_PATH'] = input("Please provide full path to the folder with Excel files: ").strip()
        settings['INFO_PATH'] = input("Please provide full path to the file with survey information: ").strip()
        settings['FINAL_CSV_PATH'] = input("Please provide the csv destination folder full path: ")
        settings['CSV_NAME'] = input("Please provide the survey csv final name: ")
        settings['NUMBER_OF_COLUMNS'] = int(input("Please provide the survey columns number: "))

        for i in range(1, settings.get('NUMBER_OF_COLUMNS')+1):
            col_index = f'COLUMN_NAME_{i}'
            col_name = input(f"Please provide the column name {i}: ").strip()
            settings[col_index] = {'NAME': col_name, 'CHOICES': {}}
            number_of_choices = int(input("Please provide the survey columns number of choices: "))

            for j in range(1, number_of_choices+1):
                str_choice = input(f"Please provide string choice representation: ").strip()
                int_choice = input(f"Please provide numerical choice representation: ").strip()
                settings[col_index]['CHOICES'][str_choice] = int_choice

        return settings

    @staticmethod
    def get_survey() -> str:
        """ Submenu to get survey name and period for handling."""
        survey = input("Please provide the survey full name: ").lower()
        return survey

    @staticmethod
    def get_settings_from_file() -> str:
        """ Get data from the previous prepared json file."""
        setting_path = input("Please provide full path to the folder with Excel files: ")
        return setting_path
