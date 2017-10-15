# coding: utf-8

from acam import WordTree, get_word_list
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
    word_list = get_word_list(os.path.join(os.path.dirname(__file__), 'chinese_words.txt'))
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
    text = """由于大连现场赛的一道 AC自动机+ DP的题目(zoj3545 Rescue the Rabbit)被小媛同学推荐看 AC自动机。经过一段时间的努力，终于把 shǎ崽神牛的 AC自动机专辑题目 AK(其实还差那个高中题。。囧。。不让做)。
    """
    result = tree.search_multi(text)
    print result

    for k in result:
        print word_list[k], result[k]

    print time.time() - cur

    index = tree.search_one('大连')
    if index != -1:
        print index, word_list[index]


if __name__ == "__main__":
    # test_acam()
    test_search()

