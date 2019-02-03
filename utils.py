from datetime import datetime
import sys


class Timer:
    def __init__(self):
        self.__start = datetime.now()
        self.__end = 0
        pass

    def elapsed(self):
        print("\nDone in %f seconds." % (datetime.now() - self.__start).total_seconds())
        pass

    pass


def create_uri():
    def parse_arg(ident: str):
        return sys.argv[sys.argv.index(ident) + 1]

    db_uri = 'mysql://{0}:{1}@{2}/{3}'
    return db_uri.format(parse_arg('db_user'), parse_arg('db_pass'), parse_arg('db_host'), parse_arg('db_name'))
    pass


def concat(*arguments, sep = '') -> str:
    result = ""
    for arg in arguments:
        result += arg
        if arguments.index(arg) is len(arguments) - 1:
            break
        result += sep
    return result
    pass
