import math
tree_depth = -1

class Node(object):
    def __init__(self, leaf_node):
        self.leaf_node = leaf_node
        self.children = {}
        self.pointer = None
        self.start =None
        self.end = None
        self.suffix_link = None

    def length(self):
        if(self.start == -1):
            return 0
        else:
            return self.end - self.start +1

    def __getattribute__(self, name):
        if name == 'end':
            if self.leaf_node:
                return tree_depth
        return super(Node, self).__getattribute__(name)

class Suffix_tree:
    def __init__(self, string_list):
        self.lines = len(string_list)
        self.string_list = [None]*self.lines
        self.root = None

        for i in range(self.lines):
            self.string_list[i] = string_list[i] + '$' + (1 + len(str(self.lines)) -len(str(i)))*'0' + str(i)

        self.build_tree()

    def reset(self):
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.last_created_node = None
        self.active_node = self.root

    def get_edge(self, node):
        return self.string_list[node.string_pointer][node.start: node.end + 1]

    def create_node(self, start, string_pointer, end=None, leaf_node = False):
        node = Node(leaf_node = leaf_node)
        node.string_pointer = string_pointer
        node.start = start
        node.end = end
        # if(start != -1 and self.get_edge(node) == ""):
        #     raise ValueError('asdads')

        node.suffix_link = self.root
        return node

    def build_tree(self):
        string_list_size = len(self.string_list)
        self.root = self.create_node(start = -1, string_pointer = 0, end = -1)
        global tree_depth
        tree_depth = len(self.string_list[0]) - 1
        self.reset()
        for string_pointer in range(string_list_size):
            size = len(self.string_list[string_pointer])
            self.reset()
            for index in range(size):
                self.extend_tree(index, string_pointer)


    def extend_tree(self, index, string_pointer):

        self.remainder += 1
        self.last_created_node = None

        # print('string pointer =' + str(string_pointer))
        # print('index =' + str(index))
        # print('char' + self.string_list[string_pointer][index])
        # self.print_clear("", self.root)
        # print(self.root.children.items())
        # print(self.remainder)


        while (self.remainder > 0):
            if (self.active_length == 0):
                self.active_edge = index

            # print('len string' +  str(len(self.string_list[string_pointer])))
            # print('active' + str(self.active_edge))
            # print(self.string_list[string_pointer][self.active_edge])
            if (self.active_node.children.get(self.string_list[string_pointer][self.active_edge]) is None):
                new_node = self.create_node(index, string_pointer = string_pointer, leaf_node=True)

                print('adding at' + self.string_list[string_pointer][self.active_edge])
                self.active_node.children[self.string_list[string_pointer][self.active_edge]] = new_node
                if (self.last_created_node is not None):
                    self.last_created_node.suffix_link = self.active_node
                    self.last_created_node = None
            else:
                child = self.active_node.children.get(self.string_list[string_pointer][self.active_edge])
                print('getting ' +  self.string_list[string_pointer][self.active_edge] + ' got ' + self.get_edge(child))
                print(child)
                length = child.length()
                if (self.active_length >= length):
                    self.active_edge += length
                    self.active_length -= length
                    self.active_node = child
                    print('walking dow')
                    continue

                # print('edge =' + self.get_edge(child))
                # print('active edge'  +str(self.active_edge))
                # print('active legth'  +str(self.active_length))
                # print('index' + str(index))
                # print('active edge'  +str(self.active_edge))
                # print(self.string_list[string_pointer][child.start + self.active_length] == self.string_list[string_pointer][self.active_edge])
                # print(self.get_edge(child))
                # print(self.string_list[string_pointer][index])
                # print(len(self.string_list[child.string_pointer]))
                # print('start' + str(child.start))
                print(child.start + self.active_length)
                if (self.string_list[child.string_pointer][child.start + self.active_length] == self.string_list[string_pointer][index]):
                    if((self.last_created_node is not None) and (self.active_node != self.root)):
                        self.last_created_node.suffix_link = self.active_node
                        self.last_created_node  = None

                    self.active_length += 1
                    break

                # print(self.string_list[child.string_pointer][child.start + self.active_length])
                # print(self.string_list[string_pointer][index])
                split_end = child.start + self.active_length - 1
                # print('split end' + str(split_end))
                # print('split' + str(child.start))
                split = self.create_node(start = child.start,  string_pointer = child.string_pointer, end =split_end)
                self.active_node.children[self.string_list[string_pointer][self.active_edge]] = split

                new_node = self.create_node(start  = index, string_pointer = string_pointer, leaf_node=True)
                split.children[self.string_list[string_pointer][index]] = new_node
                child.start += self.active_length
                split.children[self.string_list[child.string_pointer][child.start]] = child

                if (self.last_created_node is not None):
                    self.last_created_node.suffix_link = split

                self.last_created_node = split

            self.remainder -= 1
            if ((self.active_node == self.root) and (self.active_length > 0)):
                # print('active length' + str(self.active_length))
                # print('active edge' + str(self.active_edge))
                # print('active rem' + str(self.remainder))
                # print('indexh' + str(index))
                self.active_length -= 1
                self.active_edge = index - self.remainder + 1
            elif (self.active_node != self.root):
                self.active_node = self.active_node.suffix_link

    def print_clear(self, spacer, node):
        print(spacer + "node = " + self.get_edge(node) + " str_pointers " + str(node.string_pointer))
        spacer = spacer + "  |  "
        for _, child in node.children.items():
            self.print_clear(spacer, child)

    def print_children(self, node):
        print('children for node ' + self.get_edge(node))
        for key, child in node.children.items():
            print('key =' + key + ' edge = ' + self.get_edge(child))

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

    def get_string_pointers(self, node):
        result = []
        for _, child in node.children.items():
            result += self.get_string_pointers(child)
        result.append(node.string_pointer)
        return result



    def longest_suffix(self, prefix):
        result = [0]*self.lines
        size = len(prefix)
        node = self.root
        length = 0
        index = 0
        while index < size:
            end_node = node.children.get('$')
            if end_node != None:
                tmp_result = self.get_string_pointers(end_node)
                for element in tmp_result:
                    result[element] = index
            # print(node.length())
            child = node.children.get(prefix[index])
            print("looking for " + prefix[index + node.length()]+".")
            print('node: ' + str(self.get_edge(node)) + 'length: ' + str(node.length()))
            print(index  + node.length())
            print(prefix)
            print(node.children.items())
            if child != None:
                print('looked up  node' + prefix[index + node.length()] + 'got node ' + self.get_edge(child))
                print("node = " + self.get_edge(child))
                print("")
                print("node = " + self.get_edge(child))
                print("len = " + str(child.length()))
                print("pre =" +prefix[index:index + child.length()])
                print("")
                end, match_length = self.edge_matching(child, index, prefix)

                if end:
                    tmp_result = self.get_string_pointers(child)
                    print(match_length)
                    for element in tmp_result:
                        result[element] = index + match_length
                        print(index + match_length)
                    break

                elif match_length == child.length():
                    node = child
                    index += match_length
                    print('match le' + str(match_length))
                else:
                    print('break 1')
                    break
            else:
                self.print_children(node)
                print('break 2')
                break

        return result

    # def imperfect_longest_suffix(self, missmatch_percentage, prefix):



A = [
# 'CACTTCATTGGTCCGTGTTTCTGAACCACATGAT',
'TTCACAGTGGCTAAGTTCTGTGGAATTCTCGGGTGCCAAGGAACTCCAGT',
    # 'TTTCTATGATGAATCAAACTAGCTCACTATGACCGACAGTGAAAATACAT',
    'GCATGGGTGGTTCAGTGGTAGAATTCTCGCCTGGAATTCTCGGGTGCCAA',
    ]
Ab = [
# 'CACTTCATTGGTCCGTGTTTCTGAACCACATGAT',
    'TG',
    # 'TTTCTATGATGAATCAAACTAGCTCACTATGACCGACAGTGAAAATACAT',
    'CT',
    ]


if __name__ =="__main__":
    suf = Suffix_tree(A)
    suf.print_children(suf.root)
    suf.print_clear("", suf.root)
    print(suf.root.children.items())
    # # print(suf.root.start)
    # # print(suf.root.end)
    # # print(suf.root.children.get('T').start)
    # # print(suf.root.children.get('T').end)
    # # print(suf.get_edge(suf.root.children.get('T')))
    print(suf.longest_suffix('TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'))
