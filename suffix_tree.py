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
    def __init__(self, string_list):
        self.string_list = string_list
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


    # def extend_tree(self, pos):
    #     global tree_depth
    #     """Extension Rule 1, this takes care of extending all
    #     leaves created so far in tree"""
    #     tree_depth = pos
    #     """Increment remainder indicating that a
    #     new suffix added to the list of suffixes yet to be
    #     added in tree"""
    #     self.remainder += 1
    #     """set lastNewNode to None while starting a new phase,
    #      indicating there is no internal node waiting for
    #      it's suffix link reset in current phase"""
    #     self.last_created_node = None
    #     # Add all suffixes (yet to be added) one by one in tree
    #     while(self.remainder > 0):
    #         if (self.active_length == 0):
    #             self.active_edge = pos  # APCFALZ
    #         #  There is no outgoing edge starting with
    #         #  active_edge from active_node
    #         if (self.active_node.children.get(self.string[self.active_edge]) is None):
    #             # Extension Rule 2 (A new leaf edge gets created)
    #             self.active_node.children[self.string[self.active_edge]] = self.new_node(pos, leaf=True)
    #             """A new leaf edge is created in above line starting
    #              from  an existng node (the current active_node), and
    #              if there is any internal node waiting for it's suffix
    #              link get reset, point the suffix link from that last
    #              internal node to current active_node. Then set lastNewNode
    #              to None indicating no more node waiting for suffix link
    #              reset."""
    #             if (self.last_created_node is not None):
    #                 self.last_created_node.suffix_link = self.active_node
    #                 self.last_created_node = None
    #         #  There is an outgoing edge starting with active_edge
    #         #  from active_node
    #         else:
    #             #  Get the next node at the end of edge starting
    #             #  with active_edge
    #             _next = self.active_node.children.get(self.string[self.active_edge])
    #             if self.walk_down(_next):  # Do walkdown
    #                 # Start from _next node (the new active_node)
    #                 continue
    #             """Extension Rule 3 (current character being processed
    #               is already on the edge)"""
    #             if (self.string[_next.start + self.active_length] == self.string[pos]):
    #                 # If a newly created node waiting for it's
    #                 # suffix link to be set, then set suffix link
    #                 # of that waiting node to curent. active node
    #                 if((self.last_created_node is not None) and (self.active_node != self.root)):
    #                     self.last_created_node.suffix_link = self.active_node
    #                     self.last_created_node = None
    #                 # APCFER3
    #                 self.active_length += 1
    #                 """STOP all further processing in this phase
    #                 and move on to _next phase"""
    #                 break
    #             """We will be here when activePoint is in middle of
    #               the edge being traversed and current character
    #               being processed is not  on the edge (we fall off
    #               the tree). In this case, we add a new internal node
    #               and a new leaf edge going out of that new node. This
    #               is Extension Rule 2, where a new leaf edge and a new
    #             internal node get created"""
    #             self.splitEnd = _next.start + self.active_length - 1
    #             # New internal node
    #             split = self.new_node(_next.start, self.splitEnd)
    #             self.active_node.children[self.string[self.active_edge]] = split
    #             # New leaf coming out of new internal node
    #             split.children[self.string[pos]] = self.new_node(pos, leaf=True)
    #             _next.start += self.active_length
    #             split.children[self.string[_next.start]] = _next
    #             """We got a new internal node here. If there is any
    #               internal node created in last extensions of same
    #               phase which is still waiting for it's suffix link
    #               reset, do it now."""
    #             if (self.last_created_node is not None):
    #                 # suffix_link of lastNewNode points to current newly
    #                 # created internal node
    #                 self.last_created_node.suffix_link = split
    #             """Make the current newly created internal node waiting
    #               for it's suffix link reset (which is pointing to self.root
    #               at present). If we come across any other internal node
    #               (existing or newly created) in next extension of same
    #               phase, when a new leaf edge gets added (i.e. when
    #               Extension Rule 2 applies is any of the next extension
    #               of same phase) at that point, suffix_link of this node
    #               will point to that internal node."""
    #             self.last_created_node = split
    #         """One suffix got added in tree, decrement the count of
    #            suffixes yet to be added."""
    #         self.remainder -= 1
    #         if ((self.active_node == self.root) and (self.active_length > 0)):  # APCFER2C1
    #             self.active_length -= 1
    #             self.active_edge = pos - self.remainder + 1
    #         elif (self.active_node != self.root):  # APCFER2C2
    #             self.active_node = self.active_node.suffix_link 

    def extend_tree(self, string_pointer, index):
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

    # def imperfect_longest_suffix(self, missmatch_percentage, prefix):






if __name__ =="__main__":
    suf = Suffix_tree('TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGC$')
    suf.print_clear("", suf.root)
    print(suf.find_longest_prefix("TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG"))




