from sqlalchemy import Integer, String
from dictionary_builder import DictionaryBuilder as Builder
from utils import create_uri, concat
from morphtypes import load_tagname
import os

LANG = load_tagname(0)
FILENAME = 'C'
EXT = 'dix'
DATA_DIR = 'data'
ABS_DATA_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], DATA_DIR)
DICTIONARY_FILE = concat(ABS_DATA_DIR, LANG, concat(FILENAME, EXT, sep = '.'), sep = '/')

if __name__ == '__main__':
    cols = {'word_id': Integer, 'word': String(35),
            'category_1': String(20), 'category_2': String(20), 'category_3': String(20),
            'category_4': String(20), 'category_5': String(20), 'category_6': String(20),
            'category_7': String(20), 'category_8': String(20), 'category_9': String(20),
            'category_10': String(20), 'category_11': String(20), 'category_12': String(20)}

    builder = Builder(filepath = DICTIONARY_FILE, sep = '\t', db_uri = create_uri())
    builder.primary_col_index = 0
    builder.build('C', cols, LANG)
    # builder.resume('C', cols, LANG, 0, 4000)
    # print(builder.read('X', row_num = 150))
    del builder
