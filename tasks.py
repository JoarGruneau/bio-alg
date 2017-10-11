from suffix_tree import Suffix_tree

def task_1():
    adapter_seq = 'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'
    file = open('../s_3_sequence_1M.txt', "r")
    output = open('task_1_out.txt', 'w')
    count = 0
    lines = file.read().splitlines()
    # lines = lines[1:100]
    print(str(len(lines)) + " to process")
    suffix_tree = Suffix_tree(lines)
    match = suffix_tree.longest_suffix(adapter_seq)

    for i in range(len(match)):
        output.write("match = " + str(match[i]) + " " + lines[i] + " " + adapter_seq +'\n')

    # for line in lines:
    #     count += 1
    #     if count%1000 == 0:
    #         print("processed " + str(count) +" lines")
        # suffix_tree = Suffix_tree(line + "$")
        # match = suffix_tree.longest_suffix(adapter_seq)
        # output.write("match = " + str(match) + " " + line + " " + adapter_seq +'\n')
    file.close()
    output.close()
    suffix_tree.print_clear("", suffix_tree.root)

if __name__ == '__main__':
    task_1()