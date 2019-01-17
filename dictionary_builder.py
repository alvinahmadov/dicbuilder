from database_wrapper import DatabaseWrapper
from raw_parser import SDParser
from morphtypes import load_tag
from sqlalchemy import Column, Integer, String


class DictionaryBuilder:
    def __init__(self, **kwargs):
        self.__source_parser = SDParser(filename = kwargs.pop('filepath'), sep = kwargs.pop('sep'))
        self.__wordbase_builder = DatabaseWrapper(kwargs.pop('db_uri'))

    def __delete__(self, instance):
        pass

    def build(self, table_name: str, columns: list, language: str, drop = True):
        print("Creating table")
        self.__wordbase_builder.create_table(table_name, columns, drop)
        parsed = self.__source_parser.parse_lines()
        for words, paradigms in zip(parsed[0].values(), parsed[1].values()):
            for word, paradigme in zip(words, paradigms):
                row_values = {'word': word}
                self._variable_row_values(language, row_values, paradigme, columns, 2)
                self.__wordbase_builder.insert_values(table_name, row_values)
        print("Database build finished.")

    def _variable_row_values(self, language, rows: dict, row_values: str, columns: list, start_index: int) -> None:
        translated_values = self._translate(load_tag(language), row_values)
        index = start_index
        for value in translated_values:
            rows[columns[index].name] = value
            index += 1

    @staticmethod
    def _translate(dictionary: dict, row: str):
        values = row.split(' ')
        translated_values = list()
        for value in values:
            for key, cmp_value in zip(dictionary.keys(), dictionary.values()):
                if value == cmp_value:
                    translated_values.append(key)

        return translated_values

    @staticmethod
    def generate_columns(column_infos: dict, primarykey_index):
        """ Generate database columns
        :param column_infos dictionary of column name as key and column type with additional size info
        :type column_infos dict
        :param primarykey_index index of column which is primary key
        :type primarykey_index int
         """
        columns = list()
        index = 0
        print("Generating column")
        for (col_name, col_type) in column_infos.items():
            if index == primarykey_index:
                columns.append(Column(col_name, col_type, primary_key = True))
            else:
                columns.append(Column(col_name, col_type))
            index += 1
        return columns
