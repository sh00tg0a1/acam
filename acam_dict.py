# coding: utf-8
from __future__ import absolute_import
from collections import deque
from wordlist import *

get_word_list = get_word_list
Pattern = Pattern
WordList = WordList


class ACAMExp(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

    def __repr__(self):
        return "ACAMExp: %s" % super(ACAMExp, self).__repr__()


class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = dict()
        self.par = None
        self.tag = None
        self.fail = None
        self.weight = 1

    def set_par(self, par):
        self.par = par

    def add_child(self, child):
        if not isinstance(child, Node):
            return

        self.children[child.value] = child
        child.set_par(self)

    def get_par(self):
        return self.par

    def set_tag(self, tag):
        self.tag = tag

    def set_fail(self, node):
        self.fail = node


class WordTree(object):
    def __init__(self):
        self.root = Node(0)
        self.len = 0

    @staticmethod
    def __dftraverse(node, func=None):
        if not isinstance(node, Node):
            return

        if func:
            func(node)

        for c in node.children:
            WordTree.__dftraverse(c)

    def dftraverse(self, func=None):
        """
        深度优先变量树
        :param func: 遍历时执行的操作
        :return:
        """

        def print_v(node):
            if node is self.root:
                print('Root->')
            else:
                print(node.value)

        WordTree.__dftraverse(self.root, print_v if not func else func)

    @staticmethod
    def __bftraverse(traverse_queue, func):
        while len(traverse_queue):
            node = traverse_queue.popleft()

            if not isinstance(node, Node):
                return

            if func:
                func(node)

            for child in node.children.values():
                # next_queue.append(child)
                traverse_queue.append(child)

    def bftraverse(self, func=None):
        """
        广度优先变量树
        :param func: 遍历时需要进行的操作，默认传入参数 Node 类型的变量
        :return:
        """
        def print_v(node):
            if node.par is None:
                print('Root->')
            else:
                print(node.value)

        queue = deque()
        queue.append(self.root)
        WordTree.__bftraverse(queue, print_v if not func else func)

    def __add_word(self, word, tag):
        # if not isinstance(word, str):
        #     raise ACAMExp("Word type not allowed!")

        # 　从 root 节点开始搜索
        cur = self.root
        for c in word:
            if not cur.children:
                new = Node(c)
                cur.add_child(new)
                cur = new
            else:
                found = False

                node = cur.children.get(c)

                if node:
                    cur = node
                    continue
                else:
                    new = Node(c)
                    cur.add_child(new)
                    cur = new

        # 设置一个 tag
        if tag is not None:
            cur.tag = tag

        self.len += 1

    def build(self, wlist):
        """
        增量方式添加词语
        :param wlist: 待添加的词
        :return:
        """
        # 首先构建
        for i in range(len(wlist)):
            if isinstance(wlist[i], list):
                word = wlist[i][0]
            else:
                word = wlist[i]

            self.__add_word(word, i)

        # 构建 AC 自动机
        def find_failure(node):
            # 1. 根节点，不做处理
            if node is self.root:
                return

            # 2. 第二层节点，全部指向 root
            if node.par is self.root:
                node.fail = self.root
                return

            # 3. 其他节点，搜索
            node_to_search = node.par.fail
            while True:
                fail = node_to_search.children.get(node.value)
                if fail:
                    node.fail = fail
                    break
                else:
                    if node_to_search == self.root:
                        node.fail = self.root
                        break
                    else:
                        node_to_search = node_to_search.fail

        WordTree.bftraverse(self, find_failure)

    def search_one(self, word):
        """
        查询一个关键词
        :param word: 关键词
        :return: 关键词在 word_list 中的位置
        """
        cur = self.root
        failed = False
        for c in word:
            next = cur.children.get(c)
            if next is None:
                failed = True
                break
            else:
                cur = next

        if not failed and cur.tag:
            return cur.tag

        return -1

    def search_multi(self, text):
        """
        查找多个匹配的模式
        :param text: 待处理字符串
        :return:
        """
        cur = self.root
        result = dict()
        for i in range(len(text)):
            step_failed = True
            while True:
                node = cur.children.get(text[i])
                if node:
                    cur = node
                    step_failed = False

                if not step_failed:
                    if cur.tag is not None:
                        if cur.tag in result:
                            result[cur.tag].append(i)
                        else:
                            # 记录出现位置
                            result[cur.tag] = [i]
                    break
                else:
                    if cur.fail:
                        cur = cur.fail
                    else:
                        break

        return result
