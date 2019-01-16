from src.database_wrapper import DatabaseWrapper
from src.raw_parser import RawDictParser

WORD_CLASS_NO_EN = {
    'acronym': 'fork', 'adjective': 'adj', 'common_gender': 'm/f', 'common_noun': 'appell', 'comparative': 'komp', 'conjunction': 'konj',
    'definite': 'be', 'feminine': 'fem', 'imperative': 'imp', 'infinitive': 'inf', 'indefinite': 'ub', 'masculine': 'mask',
    'neuter_gender': 'nøyt', 'noun': 'subst', 'ordinal': 'ordenstall', 'past_tense': 'pret', 'passive': 'pass',
    'perfect_participle': 'perf-part', 'plural': 'fl', 'positive': 'pos', 'proper_noun': 'prop', 'present_tense': 'pres',
    'superlative': 'sup', 'singular': 'ent', 'verb': 'verb'}


class DictionaryBuilder:
    def __init__(self, *args, **kwargs):
        self.__parser = RawDictParser(filename = kwargs.get('filepath'), sep = kwargs.get('sep'))
        self.__wbbuilder = DatabaseWrapper(kwargs.pop('db_uri'))
        pass

    def build(self, table_name: str, columns: list, drop=True):
        vals = {}
        print("Creating table...")
        self.__wbbuilder.create_table(table_name, columns, drop)
        print("Reading data...")
        wordm = self.__parser.extract_words()
        morphm = self.__parser.extract_mophems()
        for words, paradigmes in zip(wordm.values(), morphm.values()):
            for word, paradigme in zip(words, paradigmes):
                print("Writing data...")
                vals['word'] = word
                self._variable_row_values(vals, paradigme, columns, 2)
                self.__wbbuilder.insert_values(table_name, vals)
        print("Database build finished.")

    def _variable_row_values(self, rows: dict, row_values: str, columns: list, start_index = 1):
        values = row_values.split(' ')
        for value in values:
            eval_val = self._translator(WORD_CLASS_NO_EN, value)
            if eval_val is not None:
                if eval_val in rows:
                    break
                else:
                    rows[columns[start_index].name] = self._translator(WORD_CLASS_NO_EN, value)
                    start_index += 1
            else:
                continue

    @staticmethod
    def _translator(dictionary: dict, value: str) -> str:
        for key, cmp_value in zip(dictionary.keys(), dictionary.values()):
            if value in cmp_value:
                return key
