from sqlalchemy import Column, Integer, String
from dictionary_builder import DictionaryBuilder as Builder
from utils import create_uri
from morphtypes import load_tag
import os

LANGUAGE = 'NO'
DATA_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
DICTIONARY_FILE = DATA_DIR + os.path.sep + LANGUAGE + os.path.sep + "AOA.dix"

if __name__ == '__main__':
    columns = [
        Column('word_id', Integer, primary_key = True),
        Column('word', String(20)),
        Column('tag1', String(20)),
        Column('tag2', String(20)),
        Column('tag3', String(20)),
        Column('tag4', String(20)),
        Column('tag5', String(20)),
        Column('tag6', String(20)),
        Column('tag7', String(20))
    ]
    builder = Builder(filepath = DICTIONARY_FILE, sep = '\t', db_uri = create_uri())
    builder.build('AOA', columns, language = LANGUAGE)

    del builder
