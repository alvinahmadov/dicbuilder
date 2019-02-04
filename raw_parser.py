from collections import defaultdict
from threading import Thread
from multiprocessing import Process


class ParseThread(Thread):
    def __init__(self, group = None, target = None, args = ()):
        Thread.__init__(self, group = group, target = target, args = args, name = None)
        self._args = args
        self._target = target

    def run(self):
        if self._target:
            return self._target(*self._args)
        else:
            return defaultdict(list)


class ParseProcess(Process):
    def __init__(self, target = None, args = ()):
        Process.__init__(self, None, target, args = args)
        self._arguments = args
        self._process = target

    def run(self):
        return self._process(*self._arguments)


class SDParser:
    def __init__(self, *args, **kwargs):
        self._filename = kwargs.pop('filename')
        self._separator = kwargs.pop('sep')
        self._dictionary = list()
        self.line_count = 0
        self.count_lines()

    keyword = ""

    def __delete__(self, instance):
        self._dictionary.clear()
        del instance

    def parse_lines(self, key_index: int, indexes: tuple, start = 0, end = 0) -> list:
        processors = [ParseProcess(target = self.extract, args = (key_index, index, start, end)) for index in indexes]
        i = 0
        for proc in processors:
            proc.start()
            proc.join(0.001)
            self._dictionary.insert(i, proc.run())
            i += 1
        return self._dictionary

    def parse_line(self, line_index):
        index = 0
        with open(self._filename, 'r') as file:
            for line in file:
                if line_index == index:
                    return line
                index += 1

    def count_lines(self):
        with open(self._filename, 'r') as f:
            for _ in f:
                self.line_count += 1
            f.close()

    def extract(self, group: int, value_index: int, start = 0, end = 0):
        data_map = defaultdict(list)
        for i in range(end if start + end < self.line_count and end is not 0 else self.line_count - start):
            data_list = self.parse_line(i + start).split(self._separator)
            if self.keyword not in data_list:
                self.keyword = data_list[group]
            data_map[self.keyword].append(data_list[value_index])
        return data_map
