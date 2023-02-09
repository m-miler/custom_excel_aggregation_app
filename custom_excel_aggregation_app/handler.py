import os
import pandas as pd
from custom_excel_aggregation_app.utils import Utils
from datetime import datetime
from pandas import DataFrame


class ExcelHandler:
    def __init__(self, settings: dict) -> None:
        self.settings = settings
        self.columns = [self.settings.get(f'COLUMN_NAME_{n}').get('NAME') for n in
                        range(1, self.settings.get('NUMBER_OF_COLUMNS')+1)]
        self.columns += ['User name', 'Creation date', 'Last update']

    def concat_data_to_data_frame(self) -> DataFrame:
        """
        Loop through all the Excel files in the indicated path. Get all data from each file and
        concat in the one data frame with already specified columns names. Create a report date column
        based on file name string.
        """
        files = Utils.get_files_name_from_folder(self.settings.get('DATABASE_PATH'))
        df = pd.DataFrame(columns=self.columns)

        for file in files:
            file_path = os.path.join(self.settings.get('DATABASE_PATH'), file)
            data = pd.read_excel(file_path, sheet_name='Content', header=3)
            data = self._custom_columns_names(data)
            data['report_date'] = datetime.strptime(file.split('_')[2][-8:], "%d%m%Y").strftime('%Y-%m-%d')
            df = pd.concat([df, data], axis=0, ignore_index=True)
        return df

    def _get_csv_full_path(self) -> str:
        """ Create a full path name to the final csv save destination."""
        csv_path = os.path.join(self.settings.get('FINAL_CSV_PATH'), self.settings.get('CSV_NAME') + '.csv')
        return csv_path

    def _custom_columns_names(self, data: DataFrame) -> DataFrame:
        data = data.rename(columns={data.columns[n]: self.columns[n] for n in range(len(data.columns)-3)})
        return data

    def _columns_custom_reindex(self, data: DataFrame) -> DataFrame:
        """ Custom reindex columns in data frame."""
        reindex_columns = ['report_date', 'ID', 'Material'] + self.columns
        data = data.reindex(reindex_columns, axis=1)
        return data

    def _merge_with_info_data(self, data: DataFrame) -> DataFrame:
        """ Add additional information to the survey data."""
        info_data = pd.read_excel(self.settings.get('INFO_PATH'))
        data = pd.merge(data, info_data, left_on='User name', right_on='Email', how='left')
        return data

    def _convert_string_choices_to_numerical(self, data: DataFrame) -> DataFrame:
        """ Covert a string survey options to the numerical representation."""
        for n, col in enumerate(self.columns[:-3], start=1):
            numerical_rep = self.settings.get(f'COLUMN_NAME_{n}').get('CHOICES')
            if numerical_rep:
                data[col] = data[col].apply(lambda x: numerical_rep[x])
        return data

    def save_data(self) -> None:
        """ Save concat data frame to the csv file in final csv path."""
        raw_data = self.concat_data_to_data_frame()
        if self.settings.get('INFO_PATH'):
            raw_data = self._merge_with_info_data(raw_data)
        raw_data = self._convert_string_choices_to_numerical(raw_data)
        data = self._columns_custom_reindex(raw_data)
        csv_path = self._get_csv_full_path()
        data.to_csv(csv_path, encoding='utf-8-sig', index=False, sep=";")


