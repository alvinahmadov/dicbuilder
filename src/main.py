from src.database_wrapper import Column, Integer, String
from src.dictionary_builder import DictionaryBuilder as Builder
from src.timer import Timer
import sys

DATA_DIR = "data"
DICTIONARY_FILE = DATA_DIR + "/dic_NO/E.dix"


def create_uri():
    def parse_arg(ident: str):
        return sys.argv[sys.argv.index(ident) + 1]
    db_uri = '{0}://{1}:{2}@{3}/{4}'
    return db_uri.format(parse_arg('db_type'), parse_arg('db_user'), parse_arg('db_pass'),
                         parse_arg('db_host'), parse_arg('db_name'))
    pass


def main(*args, **kwargs):
    t = Timer()
    columns = [
        Column('word_id', Integer, primary_key=True),
        Column('word', String(35)),
        Column('desc1', String(20)),
        Column('desc2', String(20)),
        Column('desc3', String(20)),
        Column('desc4', String(20)),
        Column('desc5', String(20)),
        Column('desc6', String(20)),
        Column('desc7', String(20)),
        Column('desc8', String(20))
    ]

    builder = Builder(filepath = DICTIONARY_FILE, sep = '\t', db_uri = create_uri())
    builder.build('E', columns)

    t.elapsed()
    del builder
    pass


pass

if __name__ == '__main__':
    main()
