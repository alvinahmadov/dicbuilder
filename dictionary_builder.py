from database_wrapper import DatabaseWrapper
from raw_parser import SDParser
from morphtypes import load_tag
import re as regex


class DictionaryBuilder:
    def __init__(self, **kwargs):
        self._source_parser = SDParser(filename = kwargs.pop('filepath'), sep = kwargs.pop('sep'))
        self._wordbase_builder = DatabaseWrapper(kwargs.pop('db_uri'))
        self.primary_col_index = -1

    def __delete__(self, instance):
        del self._source_parser
        del self._wordbase_builder
        pass

    def build(self, table_name: str, column_infos: dict, language: str, start = 0, end = 0):
        columns = self._wordbase_builder.generate_columns(column_infos, self.primary_col_index)
        self._wordbase_builder.create_table(table_name, columns)
        self._parse(table_name, columns, language, start, end)
        print("Database build for \"%s.%s\" finished." % (self._wordbase_builder.get_dbname(), table_name))

    def resume(self, table_name: str, column_infos: dict, language: str, primary_key = 0, end = 0):
        columns = self._wordbase_builder.generate_columns(column_infos, self.primary_col_index)
        start = self._wordbase_builder.resume_table(table_name, primary_key, columns)
        self._parse(table_name, columns, language, start, end)
        pass

    def read(self, table_name, row_num = -1, col_num = -1):
        return self._wordbase_builder.fetch_row(table_name, row_num, col_num)

    def _variable_row_values(self, language, rows: dict, row_values: str, columns: list, start_index: int) -> None:
        translated_values = self.translate_tag(load_tag(language), row_values)
        index = start_index
        for value in translated_values:
            rows[columns[index].name] = value
            index += 1

    def _parse(self, table_name, columns, language, start = 0, end = 0):
        parsed = self._source_parser.parse_lines(0, (2, 3), start = start, end = end)
        for words, paradigms in zip(parsed[0].values(), parsed[1].values()):
            for word, paradigm in zip(words, paradigms):
                row_values = {'word': word}
                self._variable_row_values(language, row_values, paradigm, columns, 2)
                self._wordbase_builder.insert_values(table_name, row_values)
        pass

    @staticmethod
    def translate_tag(dictionary: dict, row: str):
        values = row.split(' ')
        translated_values = list()
        index = 0
        for value in values:
            for key, cmp_value in zip(dictionary.keys(), dictionary.values()):
                if regex.match(r'<?' + cmp_value + r'(\d?|>?)', value, regex.I) is not None \
                        and key not in translated_values:
                    translated_values.insert(index, key)
                    index += 1
        return translated_values
