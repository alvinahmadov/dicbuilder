from database_wrapper import DatabaseWrapper
from raw_parser import SDParser
from morphtypes import load_tag
from collections import defaultdict


class DictionaryBuilder:
    def __init__(self, **kwargs):
        self._source_parser = SDParser(filename = kwargs.pop('filepath'), sep = kwargs.pop('sep'))
        self._wordbase_builder = DatabaseWrapper(kwargs.pop('db_uri'))
        self.primary_col_index = -1

    def __delete__(self, instance):
        del self._source_parser
        del self._wordbase_builder
        pass

    def build(self, table_name: str, column_infos: dict, language: str, drop = True):
        columns = self._wordbase_builder.generate_columns(column_infos, self.primary_col_index)
        self._wordbase_builder.create_table(table_name, columns, drop)
        parsed = self._source_parser.parse_lines()
        for words, paradigms in zip(parsed[0].values(), parsed[1].values()):
            for word, paradigm in zip(words, paradigms):
                row_values = {'word': word}
                self._variable_row_values(language, row_values, paradigm, columns, 2)
                self._wordbase_builder.insert_values(table_name, row_values)
        print("Database build finished.")

    def read(self, table_name, column):
        pass

    def _variable_row_values(self, language, rows: dict, row_values: str, columns: list, start_index: int) -> None:
        translated_values = self.translate_tag(load_tag(language), row_values)
        index = start_index
        for value in translated_values:
            rows[columns[index].name] = value
            index += 1

    @staticmethod
    def translate_tag(dictionary: dict, row: str):
        values = row.split(' ')
        translated_values = list()
        for value in values:
            for key, cmp_value in zip(dictionary.keys(), dictionary.values()):
                if cmp_value in value:
                    translated_values.append(key)
        return translated_values
