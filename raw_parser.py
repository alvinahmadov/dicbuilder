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

    def extract_words(self, key_index = 0, word_index = 2, start = 0, end = 0):
        word_map = defaultdict(list)
        self.extract(word_map, key_index, word_index, start, end)
        return word_map

    def extract_paradigms(self, key_index = 0, paradigm_index = 3, start = 0, end = 0):
        morph_map = defaultdict(list)
        self.extract(morph_map, key_index, paradigm_index, start, end)
        return morph_map

    def parse_lines(self, start = 0, end = 0, word_index = 2, paradigm_index = 3, key_index = 0) -> list:
        word_proc = ParseThread(target = self.extract_words, args = (key_index, word_index, start, end))
        paradigm_proc = ParseThread(target = self.extract_paradigms, args = (key_index, paradigm_index, start, end))
        word_proc.start()
        paradigm_proc.start()
        word_proc.join(0.001)
        paradigm_proc.join(0.001)
        self._dictionary.insert(0, word_proc.run())
        self._dictionary.insert(1, paradigm_proc.run())
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

    def extract(self, data_map, key_index, value_index, start = 0, end = 0):
        for i in range(end if start + end < self.line_count else self.line_count - start):
            data_list = self.parse_line(i + start).split(self._separator)
            if self.keyword not in data_list:
                self.keyword = data_list[key_index]
            # if data_list[value_index] not in data_map[self.keyword]:
            data_map[self.keyword].append(data_list.pop(value_index))
