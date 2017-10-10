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

    def get_pointer(self):
        return self.string_pointers[0]

    def add_pointer(self, pointer):
        if len(self.string_pointers) == 0:
            self.string_pointers.append(pointer)
        else:
            if(self.string_pointers[len(self.string_pointers) - 1] != pointer):
                self.string_pointers.append(pointer)
        print(self.string_pointers)

    def __getattribute__(self, name):
        # print(name)
        if name == 'end':
            if self.leaf_node:
                return tree_depth
        return super(Node, self).__getattribute__(name)

class Suffix_tree:
    def __init__(self, string_list):
        self.string_list = string_list
        self.root = None

        self.build_tree()

    def reset(self):
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.last_created_node = None
        self.active_node = self.root
        self.force_print_out = False

    def get_edge(self, node):
        return self.string_list[node.string_pointers[0]][node.start: node.end + 1]

    def create_node(self, start, end=None, parent = None, leaf_node = False):
        node = Node(leaf_node = leaf_node)
        node.start = start
        node.end = end
        node.parent = parent
        node.suffix_link = self.root
        return node

    def build_tree(self):
        string_list_size = len(self.string_list)
        self.root = self.create_node(start = -1, end = -1)
        self.root.add_pointer(0)
        for string_pointer in range(string_list_size):
            self.reset()
            size = len(self.string_list[string_pointer])
            for index in range(size):
                self.extend_tree(index, string_pointer)



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

    # def force_print(self, index, string_pointer):
    #      while (self.remainder > 0):
    #         print(self.remainder)
    #         self.active_node.add_pointer(string_pointer)
    #         end_node = self.active_node.children.get('$')

    #         if(end_node != None):
    #             end_node.add_pointer(string_pointer)

    #         if (self.active_length == 0):
    #             self.active_edge = index

    #         self.remainder -= 1
    #         if ((self.active_node == self.root) and (self.active_length > 0)):
    #             self.active_length -= 1
    #             self.active_edge = index - self.remainder + 1
    #             self.active_node
    #         elif (self.active_node != self.root):
    #             self.active_node = self.active_node.suffix_link


    def extend_tree(self, index, string_pointer):
        global tree_depth
        tree_depth = index

        self.remainder += 1
        self.last_created_node = None
        force_printout = False
        print(self.string_list[string_pointer])

        while (self.remainder > 0):
            end_node = self.active_node.children.get('$')
            if(end_node != None):
                end_node.add_pointer(string_pointer)

            if (self.active_length == 0):
                self.active_edge = index

            if (self.active_node.children.get(self.string_list[string_pointer][self.active_edge]) is None):
                new_node = self.create_node(index, leaf_node=True)
                new_node.add_pointer(string_pointer)

                self.active_node.children[self.string_list[string_pointer][self.active_edge]] = new_node
                if (self.last_created_node is not None):
                    self.last_created_node.suffix_link = self.active_node
                    self.last_created_node = None
            else:
                child = self.active_node.children.get(self.string_list[string_pointer][self.active_edge])

                # if(self.string_list[string_pointer][index] =='$'):
                #     child.add_pointer(string_pointer)

                length = child.length()
                if (self.active_length >= length):
                    self.active_edge += length
                    self.active_length -= length
                    self.active_node = child
                    continue

                if (self.string_list[child.get_pointer()][child.start + self.active_length] == self.string_list[string_pointer][index]):
                    if((self.last_created_node is not None) and (self.active_node != self.root)):
                        self.last_created_node.suffix_link = self.active_node
                        self.last_created_node  = None

                    self.active_length += 1
                    # if self.string_list[string_pointer][index] == '$':
                    #     self.force_print(index, string_pointer)
                    break

                split_end = child.start + self.active_length - 1
                split = self.create_node(start = child.start,  end =split_end)
                split.add_pointer(child.get_pointer())
                self.active_node.children[self.string_list[child.get_pointer()][self.active_edge]] = split

                new_node = self.create_node(index, leaf_node=True)
                new_node.add_pointer(string_pointer)
                split.children[self.string_list[string_pointer][index]] = new_node
                child.start += self.active_length
                split.children[self.string_list[child.string_pointers[0]][child.start]] = child

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
        print(spacer + "node = " + self.get_edge(node) + " str_pointers " + str(node.string_pointers))
        spacer = spacer + "  |  "
        for _, child in node.children.items():
            self.print_clear(spacer, child)

    def edge_matching(self, node, index, prefix):
        end = False
        length = 0
        for char in self.get_edge(node):
            if char == "$":
                end =True
                break
            elif char == prefix[index + length]:
                length += 1
            else:
                break
        return end, length


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
                # print("node = " + self.string_list[string_pointer][child.start: child.end + 1])
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

    # def imperfect_longest_suffix(self, missmatch_percentage, prefix):






if __name__ =="__main__":
    suf = Suffix_tree(['TGGA$', 'TGGSA$'])
    suf.print_clear("", suf.root)
    # print(suf.longest_suffix("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"))




