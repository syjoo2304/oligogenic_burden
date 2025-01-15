import os,sys,string

##List control samples
with open('CTRL.Count23.243.vcf','r') as control:
	hd=control.readline()
	hd_tmp=hd[:-1].split('\t')
	ctrl_lis=hd_tmp[9:]

##List Hearing Loss Genes
Ref=open('/home/syjoo/REF/HL_KNOWN/YUHL200_final_genelist_re.txt','r')
Gen_Total=[]

for lin in Ref:
	lin_tmp=lin[:-1].split('\t')
	Gen_Total.append(lin_tmp[0])

print(len(Gen_Total))
#Calculate the number of variants per gene for Additive model
def tabulator(file_name):
	YUHL=open(file_name,'r')
	Dom_model = {}  #'Gene:[cnt1, cnt2, ...]'
	for line in YUHL:
		line_temp=line[:-1].split('\t')
		if line.startswith('#CHROM'):
			Sample_lis=line_temp[9:]
		else:
			INFO=line_temp[7].split(';')
			for inf in INFO:
				name = inf.split('=')
				if name[0] == 'Gene.refGene':				
					Gene=name[1]
					break
			if not Gene in Dom_model.keys():
				Dom_model[Gene]=[0 for i in range(len(Sample_lis))]	
			GT=line_temp[9:]
			Sample_size = len(GT)
			for i in range(0,len(GT)):
				if '0/1' in GT[i]:
					Dom_model[Gene][i] += 1
				elif '1/1' in GT[i]:
					Dom_model[Gene][i] += 2


	return  Dom_model, Sample_size, Sample_lis

YUHL_dom,YUHL_size,YUHL_lis = tabulator('F4_hf2_miss20.Count23.vcf')

import numpy as np

co,cnt =0,0

indiv=open('Indiv.C23.txt','w')

for k,v in YUHL_dom.items():#k = the name of gene
	#k: the name of gene, v:sample_name:YUHL_size[v]
	for j in range(0,len(v)):
		if not YUHL_lis[j] in ctrl_lis:
			indiv.write(k+'\t'+str(v[j])+'\t'+YUHL_lis[j]+'\t'+'case'+'\n')
		else:
			indiv.write(k+'\t'+str(v[j])+'\t'+YUHL_lis[j]+'\t'+'control'+'\n')	
indiv.close()
'''
	if co==0:
		YUHL_count_np = YUHL_dom[k]
		co+=1
	else:
		YUHL_count_np = np.vstack((YUHL_count_np,YUHL_dom[k]))

for k in CTRL_dom.keys():
	if cnt==0:
		CTRL_count_np = CTRL_dom[k]
		cnt+=1
	else:
		CTRL_count_np = np.vstack((CTRL_count_np, CTRL_dom[k]))

print YUHL_count_np

YUHL_count_arr = YUHL_count_np.sum(axis=0)
CTRL_count_arr = CTRL_count_np.sum(axis=0)

YUHL_count,CTRL_count = YUHL_count_arr.tolist(), CTRL_count_arr.tolist()

TOTAL_Indiv = YUHL_count + CTRL_count
TOTAL_lis = YUHL_lis + CTRL_lis

if len(TOTAL_Indiv) == len(TOTAL_lis):
	indiv=open('Indiv_PostOnly.C23.txt','w')
	for i in range(0,len(YUHL_count)):
		indiv.write('case'+'\t'+str(YUHL_lis[i])+'\t'+str(YUHL_count[i])+'\n')
	for i in range(0,len(CTRL_count)):
		indiv.write('control'+'\t'+str(CTRL_lis[i])+'\t'+str(CTRL_count[i])+'\n')

	indiv.close()
'''
