import os
import sys
import string
from itertools import combinations
from multiprocessing import Pool
from scipy.stats import mannwhitneyu


input_file = '../Indiv.C23.txt'#Indiv.C23.dvd.syn.txt'##Indiv.C22_dvd_syn.txt'#Indiv.PLP.005_syn.txt'#ndiv.C22.dvd.txt'
output_file = 'Indiv.C23.HL.txt'#Indiv.PLP.005_syn.g1set.txt'

selected_genes=[]
with open('../HL_known.txt','r') as fp:
	for line in fp:
		line_temp=line[:-1].split('\t')
		selected_genes.append(line_temp[0])
def combinations_(a_list):
    result = []
    if len(a_list) <= 6:
        len_list = len(a_list)
    else:
        len_list = 6

    for i in range(2, len_list + 1):
        combi = combinations(a_list, i)
        combi_list = list(combi)
        for j in combi_list:
            result.append(j)
    return result

def process_line(input_file,dic1,dic2,selected_genes):
    with open(input_file,'r') as fp:
        for line in fp:
            line_temp = line[:-1].split('\t')
            if not line_temp[2] in dic1.keys():
                dic1[line_temp[2]] = []

            if line_temp[0] in selected_genes and not line_temp[1] == '0':
                if not (line_temp[0] in dic1[line_temp[2]]):
                    dic1[line_temp[2]].append(line_temp[0])

            if not line_temp[2] in dic2.keys():
                dic2[line_temp[2]] = line_temp[-1]

    return dic1,dic2

def process_group(k,dic1,dic2):
    if len(dic1[k]) >= 2:
        combi = combinations_(dic1[k])
        return (k, dic2[k], str(len(dic1[k])), ';'.join(map(str, combi)))
    else:
        return (k, dic2[k], str(0), '.')

if __name__ == '__main__':
    dic1,dic2={},{}
    dic1_,dic2_ = process_line(input_file,dic1,dic2,selected_genes)  #
    print("Dic 1: ",len(dic1_.keys()))
    print("Dic 2: ",len(dic2_.keys()))
    with open(output_file,'w') as output:
        pool = Pool()  # Create a new pool for processing groups
        results = [pool.apply(process_group, args=(k, dic1_, dic2_)) for k in dic2_.keys()]  # Process groups in parallel
        pool.close()
        pool.join()
        case,control=[],[]
        for result in results:
            output.write('\t'.join(map(str,result)) + '\n')
            if result[1] == 'case':
                case.append(int(result[2]))
            else:
                control.append(int(result[2]))
        statistic, p_value = mannwhitneyu(case, control, alternative='greater')
        print(statistic, p_value)
