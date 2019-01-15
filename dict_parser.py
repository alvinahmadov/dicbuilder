from collections import ChainMap, defaultdict, deque


class DictionaryReader:
    def __init__(self, filename, separator):
        self.__file_name = filename
        self.__separator = separator
        self.__freader = None
        self.__line_count = 0
        self.__dictionary = ChainMap()
        self._lines_count()
        self._keyword = ""

    def __delete__(self, instance):
        self.__freader.close()
        self.__dictionary.clear()
        del instance
        pass

    def extract_words(self, key_index = 1, word_index = 2):
        word_map = defaultdict(list)
        self._extract(word_map, key_index, word_index)
        return word_map
        pass

    def extract_mophems(self, key_index = 1, morphem_index = 3):
        morph_map = defaultdict(list)
        self._extract(morph_map, key_index, morphem_index)
        return morph_map
        pass

    def parse_lines(self):
        self.__dictionary["words"] = self.extract_words()
        self.__dictionary["morphems"] = self.extract_mophems()
        return self.__dictionary
        pass

    def lines_count(self) -> int:
        return self.__line_count

    def _lines_count(self):
        self.__freader = open(self.__file_name, 'r')
        with self.__freader as f:
            for line in f:
                self.__line_count += 1
                pass
        pass

    def _parse_line(self, line_index):
        index = 0
        self.__freader = open(self.__file_name, 'r')
        with self.__freader as file:
            for line in file:
                if line_index == index:
                    return line
                index += 1
        pass

    def _extract(self, data_map, key_index, value_index):
        for i in range(self.__line_count):
            data_list = self._parse_line(i).split(self.__separator)
            if self._keyword not in data_list:
                self._keyword = data_list[key_index]
                data_map[self._keyword].append(data_list[value_index])
            else:
                data_map[self._keyword].append(data_list[value_index])
