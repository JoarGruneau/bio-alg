from suffix_tree import Suffix_tree
import matplotlib.pyplot as plt
import numpy as np
import pylab
from multiprocessing import Pool

adapter_seq = 'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'
counter = 0

def longest_suffix(x):
    suffix_tree = Suffix_tree(line + "$")
    return suffix_tree.longest_suffix(adapter_seq)

def imperfect_longest_suffix(x):
    suffix_tree = Suffix_tree(x + "$")
    return suffix_tree.imperfect_longest_suffix(0.25, adapter_seq)


def task_1():
    adapter_seq = 'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'
    file = open('../s_3_sequence_1M.txt', "r")
    output = open('task_1_out.txt', 'w')
    count = 0
    lines = file.read().splitlines()
    # lines = lines[1:100]
    print(str(len(lines)) + " to process")
    result = [0]*(len(lines[0]) + 1)
    total_matches = 0
    for line in lines:
        count += 1
        if count%1000 == 0:
            print("processed " + str(count) +" lines")
        suffix_tree = Suffix_tree(line + "$")
        match = suffix_tree.longest_suffix(adapter_seq)
        output.write("match = " + str(match) + " " + line + " " + adapter_seq +'\n')
        result[match] += 1
        if match > 0:
            total_matches +=1

    file.close()
    output.close()
    save_r = open('task_1_resutlts.txt', 'w')
    save_r.write(str(result) +'\n')
    for i in range(len(result)):
        result[i] = float(result[i])/len(lines)

    width = 1/1.5
    print(range(len(result) -1,-1,-1))
    plt.bar(range(len(result) - 1,-1,-1), result, width, align='center', color="blue")
    plt.xticks(np.arange(0, 51, 2))

    save_r.write(str(result) +'\n')
    save_r.write('total matches' + str(total_matches) +'\n')
    save_r.close()

    pylab.xlabel('Remaining length')
    pylab.ylabel('Percentage of  elements in |S| with remaining length')
    pylab.show()

def task_2():
    adapter_seq = 'TGGAATTCTCGGGTGCCAAGGAACTCCAGTCACACAGTGATCTCGTATGCCGTCTTCTGCTTG'
    file = open('../s_3_sequence_1M.txt', "r")
    output = open('task_2_out.txt', 'w')
    count = 0
    lines = file.read().splitlines()
    print(str(len(lines)) + " to process")
    result = [0]*(len(lines[0]) + 1)
    total_matches = 0


    with Pool(4) as p:
        matches = p.map(imperfect_longest_suffix, lines)

        for match in matches:
            result[match] += 1
            if match > 0:
                total_matches +=1
            output.write("match = " + str(match) + " " + lines[match] + " " + adapter_seq +'\n')

    file.close()
    output.close()

    save_r = open('task_2_resutlts.txt', 'w')
    save_r.write(str(result) +'\n')
    for i in range(len(result)):
        result[i] = float(result[i])/len(lines)

    width = 1/1.5
    plt.bar(range(len(result) - 1,-1,-1), result, width, align='center', color="blue")
    plt.xticks(np.arange(0, 51, 2))

    save_r.write(str(result) +'\n')
    save_r.write('total matches' + str(total_matches) +'\n')
    save_r.close()

    pylab.xlabel('Remaining length')
    pylab.ylabel('Remaining length distrubutuion')
    pylab.show()




if __name__ == '__main__':
    task_2()