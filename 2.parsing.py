import os,sys,string
##Bring Sample list as variable
YUHL_lis=open('YUHL_CASE.list','r')
CTRL_lis=open('YUHL_CTRL.list','r')
CODA_lis=open('CODA.list','r')
Pre_lis=open('Pre_CASE.list','r')

YUHL_sn,CTRL_sn,Pre_sn=[],[],[]

for line in CTRL_lis:
        line_temp=line[:-1].split('\t')
        CTRL_sn.append(line_temp[0])

for line in CODA_lis:
        line_temp=line[:-1].split('\t')
        CTRL_sn.append(line_temp[0])

for line in Pre_lis:
	line_temp=line[:-1].split('\t')
        CTRL_sn.append(line_temp[0])
	Pre_sn.append(line_temp[0])
	
for line in YUHL_lis:
        line_temp=line[:-1].split('\t')
	if not line_temp[0] in Pre_sn: #post + pre_moderate 
	        YUHL_sn.append(line_temp[0])

##Divide case and control for calculating the number of samples
vcf=open('F4_hf2_miss20.Count23.vcf','r')
vcf_yuhl=open('YUHL_Post.C23.vcf','w')
vcf_ctrl=open('CTRL_Post.C23.vcf','w')

YU,CT=[],[]

for line in vcf:
	if line.startswith('##'): continue
	if line.startswith('#CHROM'):
		SN=line[:-1].split('\t')
		sn_yuhl,sn_ctrl=[],[]
		for j in SN[9:]:
			if j in YUHL_sn:
				sn_yuhl.append(j)
			elif j in CTRL_sn:
				sn_ctrl.append(j)
		print len(sn_yuhl),len(sn_ctrl)
		vcf_yuhl.write('\t'.join(SN[:9])+'\t'+'\t'.join(sn_yuhl)+'\n')
		vcf_ctrl.write('\t'.join(SN[:9])+'\t'+'\t'.join(sn_ctrl)+'\n')
	else:

	        yuhl,ctrl=[],[]
        	co,cnt=0,0
	        line_temp=line[:-1].split('\t')
	        SI=line_temp[9:]
	        for j in range(9,len(line_temp)):
        		if SN[j] in YUHL_sn:
                		yuhl.append(line_temp[j])
                        	if './.' in line_temp[j] or '0/0' in line_temp[j]:
                     	        	co+=1
			elif SN[j] in CTRL_sn:
				ctrl.append(line_temp[j])
				if './.' in line_temp[j] or '0/0' in line_temp[j]:
                        	        cnt+=1
			

	        if not co == len(YUHL_sn):
	                vcf_yuhl.write('\t'.join(line_temp[:9])+'\t'+'\t'.join(yuhl)+'\n')
	        else:
	                print 'YUHL'+'\t'.join(set(yuhl))
	        if not cnt == len(CTRL_sn):
	                vcf_ctrl.write('\t'.join(line_temp[:9])+'\t'+'\t'.join(ctrl)+'\n')
	        else:
	                print 'CTRL'+'\t'.join(set(ctrl))

print len(YUHL_sn) #213
print len(CTRL_sn) #398

vcf_yuhl.close()
vcf_ctrl.close()
	
	
