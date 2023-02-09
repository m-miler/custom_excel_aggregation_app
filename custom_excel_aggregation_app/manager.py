import json
import os
from typing import Callable
from custom_excel_aggregation_app.menu import Menu
from custom_excel_aggregation_app.utils import Utils
from custom_excel_aggregation_app.handler import ExcelHandler


class Manager:
    def __init__(self) -> None:
        self.__run: bool = True
        self.__options: dict[str, Callable] = {
            "1": self.__create_survey,
            "2": self._load_setting_from_fiel,
            "3": self.__save_survey_data,
            "4": self.__exit_app
        }

    def start_app(self) -> None:
        """ Start application."""
        Menu.show()
        while self.__run:
            user_input = Menu.get_user_choice()
            self.execute(user_input)

    def __exit_app(self) -> None:
        """ Exit application."""
        self.__run = False

    def execute(self, user_input) -> None:
        """ Execute options selected by user."""
        if user_input in self.__options:
            self.__options.get(user_input)()
        else:
            print("Incorrect option")

    def __create_survey(self) -> None:
        """ Create a settings dict for new survey."""
        settings = Menu.get_survey_settings()
        Utils.save_settings_to_json_file(settings)

    def _load_setting_from_fiel(self) -> None:
        """ Load a survey settings from json file."""
        setting_path = Menu.get_settings_from_file()
        if os.path.isfile(setting_path):
            with open(setting_path, 'r', encoding='utf-8') as file:
                settings = json.load(file)
                Utils.save_settings_to_json_file(settings)
        else:
            print("File doesn't exist.")

    def __save_survey_data(self) -> None:
        """ Save a selected Excel files to the csv."""
        survey = Menu.get_survey()
        settings = Utils.check_if_setting_file_exist(survey)
        if settings:
            ExcelHandler(settings=settings).save_data()



