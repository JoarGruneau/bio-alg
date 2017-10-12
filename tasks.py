from suffix_tree import Suffix_tree

def build_tree(file):
    file = open(file, "r")
    lines = file.read().splitlines()
    lines = lines[0:69]
    print(str(len(lines)) + " to process")
    suffix_tree = Suffix_tree(lines)
    return suffix_tree, lines, len(lines)

def calc_length_count(max_length, result):
    length_count = [0]*(max_length + 1)
    n_lines = len(result)
    for element in result:
        length_count[element] += 1
    return length_count

def calc_length_ratio(length_count, n_lines):
    length_ratio = [None]*len(length_count)
    for i in range(len(length_ratio)):
        length_ratio[i] = float(length_count[i])/n_lines
    return length_count




def task_1(suffix_tree, adapter_seq, lines, n_lines):
    longest_suffix = suffix_tree.longest_suffix(adapter_seq)
    length_count = calc_length_count(50, longest_suffix)
    length_ratio = calc_length_ratio(length_count, n_lines)

    output = open('task_1_out.txt', 'w')
    for i in range(len(longest_suffix)):
        output.write("match = " + str(longest_suffix[i]) + " " + lines[i] + " " + adapter_seq +'\n')

    print(longest_suffix)
    # print(length_count)
    # print(sum(length_count[1:]))
    # print(length_ratio)
    # suffix_tree.print_clear("", suffix_tree.root)
    output.close()

if __name__ == '__main__':
    suffix_tree, lines, n_lines = build_tree('../s_3_sequence_1M.txt')
    adapter_seq = 'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'
    task_1(suffix_tree, adapter_seq, lines, n_lines)