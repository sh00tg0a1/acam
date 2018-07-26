# coding: utf-8

from acam import WordTree, get_word_list, WordList, Pattern
import time
import os


def test_acam():
    word_list = ['he', 'she', 'his', 'hers', 'her']

    tree = WordTree()
    tree.build(word_list)

    # tree.bftraverse()

    print tree.search_multi('ahoiuqweuryioqweyasdf')


def test_search():
    cur = time.time()
    # word_list = WordList(os.path.join(os.path.dirname(__file__), 'for_word_tree/chinese_words.txt'))
    word_list = WordList(os.path.join(os.path.dirname(__file__), 'for_word_tree/非法关键字.txt'), Pattern(3, '\t', True))
    # word_list = WordList(os.path.join(os.path.dirname(__file__), 'for_word_tree/敏感词库/敏感词/敏感词库大全.txt'), Pattern(3, '\t', True))

    print time.time() - cur

    # 构建一个次数
    tree = WordTree()
    tree.build(word_list)

    print time.time() - cur

    # 搜索单个
    # index = tree.search_multi('时光')
    # if index != -1:
    #     print index, word_list[index]
    # else:
    #     print "Not found!"

    # 搜索长文本
    # text = """由于大连现场赛的一道 AC自动机+ DP的题目(zoj3545 Rescue the Rabbit)被小媛同学推荐看 AC自动机。经过一段时间的努力，终于把 shǎ崽神牛的 AC自动机专辑题目 AK(其实还差那个高中题。。囧。。不让做)。
    # """

    with open(os.path.join(os.path.dirname(__file__), 'for_query/test1.txt')) as f:
        text = f.read()

    result = tree.search_multi(text)
    print result

    for k in result:
        print "%s, %s, %s" % (word_list[k][0], word_list[k][1], word_list[k][2]) \
            if isinstance(word_list[k], list) else word_list[k], result[k]

    print time.time() - cur


if __name__ == "__main__":
    # test_acam()
    test_search()

