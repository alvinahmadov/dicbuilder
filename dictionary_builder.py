from database_wrapper import DatabaseWrapper
from raw_parser import RawDictParser

WORD_CLASS_NO_EN = {
    'acronym': 'fork', 'adjective': 'adj', 'adverb': 'adv', 'common_gender': 'm/f', 'common_noun': 'appell', 'comparative': 'komp',
    'conjunction': 'konj', 'definite': 'be', 'feminine': 'fem', 'imperative': 'imp', 'infinitive': 'inf', 'indefinite': 'ub',
    'masculine': 'mask', 'neuter_gender': 'nøyt', 'noun': 'subst', 'ordinal': 'ordenstall', 'past_tense': 'pret', 'passive': 'pass',
    'perfect_participle': 'perf-part', 'plural': 'fl', 'positive': 'pos', 'proper_noun': 'prop', 'present_tense': 'pres', 'prefix': 'pref',
    'superlative': 'sup', 'singular': 'ent', 'verb': 'verb'}


class DictionaryBuilder:
    def __init__(self, *args, **kwargs):
        self.__parser = RawDictParser(filename = kwargs.get('filepath'), sep = kwargs.get('sep'))
        self.__wbbuilder = DatabaseWrapper(kwargs.pop('db_uri'))

    def build(self, table_name: str, columns: list, drop = True):
        self.__wbbuilder.create_table(table_name, columns, drop)
        parsed = self.__parser.parse_lines()
        for words, paradigmes in zip(parsed[0].values(), parsed[1].values()):
            for word, paradigme in zip(words, paradigmes):
                row_values = {'word': word}
                self._variable_row_values(row_values, paradigme, columns, 2)
                self.__wbbuilder.insert_values(table_name, row_values)
        print("Database build finished.")

    def _variable_row_values(self, rows: dict, row_values: str, columns: list, start_index: int) -> None:
        translated_values = self._translate(WORD_CLASS_NO_EN, row_values)
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
