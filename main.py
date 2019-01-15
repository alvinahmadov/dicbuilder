from wordbase_builder import WordBase, Column, Integer, String
from dict_parser import DictionaryReader
from datetime import datetime as dt

DICTIONARY_FILE = "/home/alvin/PycharmProjects/DictionaryBuilder/data/dic_NO/C.dix"
DBURI = 'sqlite:///data/test.sqlite'
ECHO = True
DATA_OPS = 0


class Timer:
    def __init__(self):
        self.__start = dt.now()
        self.__end = 0
        pass

    def elapsed(self):
        print("\nDone in %f seconds." % (dt.now() - self.__start).total_seconds())
        pass

    pass


def write_data(*args, **kwargs):
    wb_builder = WordBase(DBURI)
    data = kwargs.pop('data')
    columns = [
        Column('word_id', Integer, primary_key = True),
        Column('word', String(10)),
        Column('sg_def', String(10)),
        Column('pl_def', String(10))
    ]
    wb_builder.create_table("words", columns)
    values = {'default': 'test', 'sg_def': 'singular_definite', 'pl_def': 'plural_definite'}
    wb_builder.insert_values("words", values)
    wb_builder.select_table("words")
    del wb_builder
    pass


def read_data():
    word_file = DICTIONARY_FILE
    dparser = DictionaryReader(word_file, '\t')
    dparser.parse_lines()
    pass


def main(*args, **kwargs):
    if DATA_OPS is 1:
        write_data()
    else:
        timer = Timer()
        read_data()
        timer.elapsed()
    pass


if __name__ == '__main__':
    main()
