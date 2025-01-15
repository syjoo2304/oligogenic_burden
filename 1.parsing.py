import string,sys,os,glob
os.system('perl /home/program/annovar/table_annovar.pl Total_3_f.remov_sample.vcf /home/program/annovar/humandb/ -buildver hg19 -out F4_hf2_miss20 -remove -otherinfo -protocol refGene,cytoBand,exac03,gnomad211_exome,gnomad211_genome,cadd13,revel,dbnsfp33a,avsnp147,clinvar_20190305 -operation g,r,f,f,f,f,f,f,f,f -nastring . -vcfinput -polish')
fname='F4_hf2_miss20.hg19_multianno.vcf'
Sample=string.split(fname,'.hg19_multianno.vcf')[0]
#Extract variants in hearing loss genes
#os.system('bedtools intersect -header -a ../'+fname+' -b /home/syjoo/REF/HL_KNOWN/HL-KNOWN-GENE_v201030.bed > '+Sample+'.HL.vcf')	

PTV=['stopgain','stoploss']
Splice=['splicing']
Total=['frameshift_insertion','frameshift_deletion','stopgain','stoploss','frameshift_block_substitution','nonframeshift_insertion','nonframeshift_deletion','nonframeshift_block_substitution','nonsynonymous_SNV']
Missense=['nonsynonymous_SNV']
Syn=['synonymous_SNV']

#Extract variants with  filtering criteria and divide into non-syn, syn
#fp=open(Sample+'.HL.vcf','r')
fp=fname
fpout=open(Sample+'.Count23.vcf','w')
fpout2=open(Sample+'.Count23_syn.vcf','w')

for line in fp:
	if line.startswith('##'):continue
	elif line.startswith('#CHROM'):
		fpout.write(line)
		fpout2.write(line)
	else:
		line_temp=line[:-1].split('\t')
		Info=string.split(line_temp[7],';')
		co,cnt=0,0
		for j in Info:
			name_=string.split(j,'=')
			if name_[0] == 'Func.refGene':
				Func = name_[1]
			if name_[0] == 'ExonicFunc.refGene':
				Exonic = name_[1]
			if name_[0] == 'Gene.refGene':
				Gene = name_[1]
			if name_[0] == 'DVD':
				DVD = string.split(name_[1],'_')[0]
			if name_[0] == 'AF':
				co+=1
				if co == 1:
					AF_internal=name_[1]
				elif co == 2:	
					AF_exome = name_[1]
				elif co == 3:
					AF_genome= name_[1]
			if name_[0] == 'AF_eas':
				cnt+=1
				if cnt == 1:
					AF_eas_exome = name_[1]
				elif cnt == 2:
        			AF_eas_genome = name_[1]
			if name_[0] == 'non_neuro_AF_eas_kor':
				KOR = name_[1]
			if name_[0] == 'SIFT_pred': #set(['T', 'D', '.'])
				SIFT = name_[1]
			if name_[0] == 'Polyphen2_HVAR_pred': #set(['P', 'B', 'D', '.'])
				PP2 = name_[1]
			if name_[0] == 'REVEL':	
				REVEL_tmp = name_[1]
				if not REVEL_tmp == '.':
					REVEL=float(REVEL_tmp)
				else:
					REVEL=REVEL_tmp
			if name_[0] == 'CADD_phred':
				CADD_tmp = name_[1]
				if not CADD_tmp == '.':
					CADD = float(CADD_tmp) #score
				else:
					CADD = CADD_tmp
			if name_[0] == 'PROVEAN_pred':
				PROVEAN= name_[1] #set(['N', 'D', '.'])
		##Variant Interpret with in-silico tools
		co=0
		PRED=[SIFT,PP2,REVEL,CADD,PROVEAN]
		if '.' in PRED:
			co=3	
		elif len(PRED) == 5:
			if SIFT in ['D']:			
				co+=1
			if PP2 in ['P', 'D']:
				co+=1
			if PROVEAN in ['D']: 
				co+=1
			if float(CADD) >= 20:
				co+=1
			if float(REVEL) >= 0.8:
				co+=1

		if  (Exonic in Total or Func in Splice):
			if (AF_eas_exome == '.' or float(AF_eas_exome) < 0.01) and (KOR == '.' or float(KOR) < 0.01):
				fpout.write(line)	

		elif Exonic in Syn:
			if (AF_eas_exome == '.' or float(AF_eas_exome) < 0.01) and (KOR == '.' or float(KOR) < 0.01):
	                	fpout2.write(line)


fpout.close()
fpout2.close()
