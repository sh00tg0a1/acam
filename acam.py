# coding: utf-8

from collections import deque


def get_word_list(file_name):
    wf = open(file_name)

    words_str = wf.read()
    # 使用 Unicode 会慢很多, 差了10倍....
    # words_str = unicode(words_str, 'utf-8')

    words_str = words_str.replace('\t', ' ')
    words_str = words_str.replace('\n', ' ')

    word_list = words_str.split(' ')

    return word_list


class ACAMExp(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)

    def __repr__(self):
        return "ACAMExp: %s" % super(ACAMExp, self).__repr__()


class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = list()
        self.par = None
        self.tag = None
        self.fail = None
        self.weight = 1

    def set_par(self, par):
        self.par = par

    def add_child(self, child):
        if not isinstance(child, Node):
            return

        self.children.append(child)
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
        Traverse the whole tree
        :return:
        """

        def print_v(node):
            if node is self.root:
                print 'Root->'
            else:
                print node.value

        WordTree.__dftraverse(self.root, print_v if not func else func)

    @staticmethod
    def __bftraverse(traverse_queue, func):
        while len(traverse_queue):
            node = traverse_queue.popleft()

            if not isinstance(node, Node):
                return

            if func:
                func(node)

            for child in node.children:
                # next_queue.append(child)
                traverse_queue.append(child)

    def bftraverse(self, func=None):
        def print_v(node):
            if node.par is None:
                print 'Root->'
            else:
                print node.value

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
                for node in cur.children:
                    if c == node.value:
                        cur = node
                        found = True
                        break

                if not found:
                    # 没有找到节点，增加一个
                    new = Node(c)
                    cur.add_child(new)
                    cur = new
                else:
                    continue

        # 设置一个 tag
        if tag is not None:
            cur.tag = tag

        self.len += 1

    def build(self, wlist):
        # 首先构建
        for i in range(len(wlist)):
            self.__add_word(wlist[i], i)

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
                found = False
                for child in node_to_search.children:
                    if child.value == node.value:
                        node.fail = child
                        found = True
                        break
                # 如果父节点的 fail 没找到合适的子节点
                if found:
                    break
                else:
                    # 如果父节点的 fail 是 root，则直接复制给 root，如果不是，再找父节点的下一个 fail
                    if node_to_search == self.root:
                        node.fail = self.root
                        break
                    else:
                        node_to_search = node_to_search.fail

        WordTree.bftraverse(self, find_failure)

    def search_one(self, word):
        cur = self.root
        failed = False
        for c in word:
            step_failed = True
            for node in cur.children:
                if c == node.value:
                    cur = node
                    step_failed = False
                    break

            if step_failed:
                failed = True
                break

        if not failed and cur.tag:
            return cur.tag

        return -1

    def search_multi(self, word):
        cur = self.root
        result = dict()
        for i in range(len(word)):
            step_failed = True
            while True:
                for node in cur.children:
                    if word[i] == node.value:
                        cur = node
                        step_failed = False
                        break

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
