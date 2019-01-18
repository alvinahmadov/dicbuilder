from sqlalchemy import Integer, String
from dictionary_builder import DictionaryBuilder as Builder
from utils import create_uri, join_str
from morphtypes import load_tagname
import os

LANG = load_tagname(0)
FILENAME = 'AOA'
EXT = 'dix'
DATA_DIR = 'data'
ABS_DATA_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], DATA_DIR)
DICTIONARY_FILE = join_str(ABS_DATA_DIR, LANG, join_str(FILENAME, EXT, sep = '.'), sep = '/')

if __name__ == '__main__':
    cols = {'word_id': Integer, 'word': String(35),
            'category_1': String(20), 'category_2': String(20), 'category_3': String(20),
            'category_4': String(20), 'category_5': String(20), 'category_6': String(20), 'category_7': String(20)}

    builder = Builder(filepath = DICTIONARY_FILE, sep = '\t', db_uri = create_uri())
    builder.build(FILENAME, cols, language = LANG, drop = False)

    del builder
