from datetime import datetime

class Timer:
    def __init__(self):
        self.__start = datetime.now()
        self.__end = 0
        pass

    def elapsed(self):
        print("\nDone in %f seconds." % (datetime.now() - self.__start).total_seconds())
        pass

    pass
