from concurrent.futures import ProcessPoolExecutor as Pool
from itertools import repeat
from multiprocessing import current_process
import time

import random
import os
from itertools import combinations
#from multiprocessing import Pool
from scipy.stats import mannwhitneyu

input_file = '../Indiv.C23.txt'
output_file = 'Unsolved243/Indiv.C23.house_keeping.p-value.txt'

# Function to select 121 random genes from the file
def select_random_genes(gene_file, num_genes):
    with open(gene_file, 'r') as fp:
        genes = [line.strip() for line in fp]
    return random.sample(genes, num_genes)

def combinations_(a_list):
    for i in range(2, len(a_list) + 1):
        for combi in combinations(a_list, i):
            yield combi

def process_line(input_file, selected_genes):
    dic1, dic2 = {}, {}
    with open(input_file, 'r') as fp:
        for line in fp:
            line_temp = line.strip().split('\t')
            gene, score, group = line_temp[0], line_temp[1], line_temp[2]
            if group not in dic1:
                dic1[group] = set()
            if gene in selected_genes and score != '0':
                dic1[group].add(gene)
            dic2[group] = line_temp[-1]
    return dic1, dic2

def process_group(args):
    k, dic1_, dic2_ = args
    if len(dic1_[k]) >= 2:
        combi = list(combinations_(dic1_[k]))
        return (k, dic2_[k], str(len(dic1_[k])), ';'.join(map(str, combi)))
    else:
        return (k, dic2_[k], str(0), '.')

def process_iteration(_):
    # Select 121 random genes for this iteration
    selected_genes = select_random_genes('housekeeping_.txt', num_genes=121) #15:g2, 17:g6
    dic1, dic2, case, control = {}, {}, [], []
    dic1_, dic2_ = process_line(input_file, selected_genes)
    print("Dic 1: ", len(dic1_.keys()))
    print("Dic 2: ", len(dic2_.keys()))
    with Pool(max_workers=40) as inner_pool:
        results = inner_pool.map(process_group, [(k, dic1_, dic2_) for k in dic2_.keys()])  # Process groups in parallel
    for result in results:
        if result[1] == 'case':
            case.append(int(result[2]))
        else:
            control.append(int(result[2]))
    statistic, p_value = mannwhitneyu(case, control, alternative='greater')
    return statistic, p_value

if __name__ == '__main__':
    # Open output file
    with open(output_file, 'w') as output:
        with Pool(max_workers=40) as outer_pool:
            results = outer_pool.map(process_iteration, range(10000))  # Process iterations in parallel
        for statistic, p_value in results:
            output.write(f"{statistic},{p_value}\n")
