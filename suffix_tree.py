import math
tree_depth = -1

class Node(object):
    def __init__(self, leaf_node):
        self.leaf_node = leaf_node
        self.parent = None
        self.children = {}
        self.string_pointers = []
        self.start =None
        self.end = None
        self.suffix_link = None

    def length(self):
        if(self.start == -1):
            return 0
        else:
            return self.end - self.start +1

    def depth(self):
        length = self.length()
        node = self
        print("pp" + str(node.parent))
        while node.parent != None:
            print("legtha com " + str(length))
            print("edge " + node.get_edge('TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGC$'))
            node = node.parent
            length += node.length()
            print("legtha com " + str(node.length()))
            print("pp" + str(node.parent))
        return length

    def __getattribute__(self, name):
        # print(name)
        if name == 'end':
            if self.leaf_node:
                return tree_depth
        return super(Node, self).__getattribute__(name)

class Suffix_tree:
    def __init__(self, string):
        self.string = string
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.last_created_node = None
        self.root = None

        self.build_tree()

    def reset():
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.last_created_node = None

    def get_edge(self, node):
        return string_list[node.string_pointers[0]][node.start: node.end + 1]

    def create_node(self, start, end=None, parent = None, leaf_node = False):
        node = Node(leaf_node = leaf_node)
        node.start = start
        node.end = end
        node.parent = parent
        node.suffix_link = self.root
        return node

    def new_node(self, start, end=None, leaf=False):
        """For root node, suffix_link will be set to NULL
        For internal nodes, suffix_link will be set to root
        by default in  current extension and may change in
        next extension"""
        node = Node(leaf)
        node.suffix_link = self.root
        node.start = start
        node.end = end
        """suffixIndex will be set to -1 by default and
           actual suffix index will be set later for leaves
           at the end of all phases"""
        return node

    def build_tree(self):
        size = len(self.string)
        self.root = self.create_node(start = -1, end = -1)
        self.active_node = self.root
        for i in range(size):
            self.extend_tree(i)

    def walk_down(self, current_node):
        """Walk down from current node.

        activePoint change for walk down (APCFWD) using
        Skip/Count Trick  (Trick 1). If active_length is greater
        than current edge length, set next  internal node as
        active_node and adjust active_edge and active_length
        accordingly to represent same activePoint.
        """
        length = current_node.length()
        if (self.active_length >= length):
            self.active_edge += length
            self.active_length -= length
            self.active_node = current_node
            return True
        return False


    def extend_tree(self, index):
        global tree_depth
        tree_depth = index

        self.remainder += 1
        self.last_created_node = None

        while (self.remainder > 0):
            if (self.active_length == 0):
                self.active_edge = index

            if (self.active_node.children.get(self.string[self.active_edge]) is None):
                self.active_node.children[self.string[self.active_edge]] = self.create_node(index, parent = self.active_node, leaf_node=True)
                if (self.last_created_node is not None):
                    self.last_created_node.suffix_link = self.active_node
                    self.last_created_node = None
            else:
                child = self.active_node.children.get(self.string[self.active_edge])

                length = child.length()
                if (self.active_length >= length):
                    self.active_edge += length
                    self.active_length -= length
                    self.active_node = child
                    continue

                if (self.string[child.start + self.active_length] == self.string[index]):
                    if((self.last_created_node is not None) and (self.active_node != self.root)):
                        self.last_created_node.suffix_link = self.active_node
                        self.last_created_node  = None

                    self.active_length += 1
                    break

                split_end = child.start + self.active_length - 1
                split = self.create_node(start = child.start, end =split_end, parent = self.active_node)
                self.active_node.children[self.string[self.active_edge]] = split

                split.children[self.string[index]] = self.create_node(start = index, parent = split, leaf_node=True)
                child.start += self.active_length
                split.children[self.string[child.start]] = child

                if (self.last_created_node is not None):
                    self.last_created_node.suffix_link = split

                self.last_created_node = split

            self.remainder -= 1
            if ((self.active_node == self.root) and (self.active_length > 0)):
                self.active_length -= 1
                self.active_edge = index - self.remainder + 1
            elif (self.active_node != self.root):
                self.active_node = self.active_node.suffix_link

    def print_clear(self, spacer, node):
        print(spacer + "node = " + self.string[node.start: node.end + 1])
        spacer = spacer + "  |  "
        for _, child in node.children.items():
            self.print_clear(spacer, child)

    def edge_matching(self, node, index, prefix):
        end = False
        length = 0
        for char in self.string[node.start:node.end + 1]:
            if char == "$":
                end =True
                break
            elif char == prefix[index + length]:
                length += 1
            else:
                break
        return end, length

    def imperfect_edge_matching(self, node, index, prefix):
        end = False
        miss_matches = 0
        length = 0
        for char in self.string[node.start:node.end + 1]:
            if char == "$":
                end =True
                break
            elif char != prefix[index + length]:
                miss_matches += 1
            length += 1
        return end, length, miss_matches


    def go_back(self, node):
        while (node.children.get("$") == None):
            node = node.parent
        node = node.children.get('$')
        return node


    def longest_suffix(self, prefix):
        size = len(prefix)
        node = self.root
        length = 0
        index = 0
        while index < size:
            if node.children.get('$') != None:
                length = index
            child = node.children.get(prefix[index])
            # print("looking for" + prefix[index])
            # print(node.children.items())
            if child != None:
                # print("")
                # print("node = " + self.string[child.start: child.end + 1])
                # print("len = " + str(child.length()))
                # print("pre =" +prefix[index:index + child.length()])
                # print("depth = " + str(child.depth()))
                # print("")
                end, match_length = self.edge_matching(child, index, prefix)

                if end:
                    length = index + match_length
                    break

                elif match_length == child.length():
                    node = child
                    index += match_length
                else:
                    break
            else:
                break

        return length

    def imperfect_longest_suffix(self, missmatch_percentage, prefix):
        self.longest_match = 0

        def imperfect(node, miss_matches, index):
            end, length, node_miss_matches = self.imperfect_edge_matching(node, index, prefix)
            total_miss_matches = miss_matches + node_miss_matches
            index += length


            if (float(total_miss_matches)/tree_depth <= missmatch_percentage):
                if ((index != 0) and (float(total_miss_matches)/index <= missmatch_percentage)):
                   if ((end or  node.children.get('$') != None) and self.longest_match < index):
                        self.longest_match = index

                for key, child in node.children.items():
                    if(key != '$'):
                        imperfect(child, total_miss_matches, index)

        imperfect(self.root, 0, 0)
        return self.longest_match






if __name__ =="__main__":
    suf = Suffix_tree('XXX$')
    suf.print_clear("", suf.root)
    print(suf.imperfect_longest_suffix(1, "TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"))
    # print(suf.longest_suffix("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"))




