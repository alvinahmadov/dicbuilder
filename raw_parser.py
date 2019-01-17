from collections import defaultdict


class SDParser:
    def __init__(self, *args, **kwargs):
        self.__filename = kwargs.pop('filename')
        self.__separator = kwargs.pop('sep')
        self.__dictionary = list()
        self.line_count = 0
        self._count_lines()
        self._keyword = ""

    def __delete__(self, instance):
        self.__dictionary.clear()
        del instance

    def extract_words(self, key_index = 0, word_index = 2):
        word_map = defaultdict(list)
        self._extract(word_map, key_index, word_index)
        return word_map

    def extract_paradigms(self, key_index = 0, morphem_index = 3):
        morph_map = defaultdict(list)
        self._extract(morph_map, key_index, morphem_index)
        return morph_map

    def parse_lines(self):
        self.__dictionary.insert(0, self.extract_words())
        self.__dictionary.insert(1, self.extract_paradigms())
        return self.__dictionary

    def parse_line(self, line_index):
        index = 0
        with open(self.__filename, 'r') as file:
            for line in file:
                if line_index == index:
                    return line
                index += 1

    def _count_lines(self):
        with open(self.__filename, 'r') as f:
            for l in f:
                self.line_count += 1
            f.close()

    def _extract(self, data_map, key_index, value_index):
        for i in range(self.line_count):
            data_list = self.parse_line(i).split(self.__separator)
            if self._keyword not in data_list:
                self._keyword = data_list[key_index]
                data_map[self._keyword].append(data_list[value_index])
            else:
                data_map[self._keyword].append(data_list[value_index])
