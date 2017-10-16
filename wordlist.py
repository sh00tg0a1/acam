# coding: utf-8


class Pattern(object):
    def __init__(self, column_num, column_delimiter, header):
        """
        构造一个 Word list 的样式
        :param column_num: 列数
        :param column_delimiter: 列分隔符
        :param header: 是否有头
        """
        self.column_num = column_num
        self.column_delimiter = column_delimiter
        self.header = header


class WordList(object):
    def __init__(self, file_name, pattern=Pattern(1, ' ', False)):
        self.file_name = file_name
        self.pattern = pattern
        self.content = list()

        # 根据读取 list
        self.__get_word_list(pattern)

    def __getitem__(self, item):
        return self.content[item]

    def __len__(self):
        return len(self.content)

    def __get_word_list(self, pattern):
        self.content = []
        with open(self.file_name) as wf:

            first_line = True
            for line in wf:
                # 有表头的情况下跳过第一行
                line = line.strip()
                if pattern.header and first_line:
                    first_line = False
                    continue

                if pattern.column_num == 1:

                    # 如果转成 Unicode 会慢很多, 差了10倍....
                    # words_str = unicode(words_str, 'utf-8')

                    self.content += line.split(pattern.column_delimiter)
                else:
                    columns = line.split(pattern.column_delimiter)
                    columns = [c for c in columns if c]
                    self.content.append(columns)

    def get_word_list(self):
        return self.content


def get_word_list(filename):
    wl = WordList(filename)
    return wl.get_word_list()
