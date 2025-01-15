import os,sys,string

def cal_p(file_name,p_value_of_hl):
	with open(file_name,'r') as fp:
	co=0
	for line in fp:
		line_temp=line[:-1].split(',')
		p=line_temp[1]
		if float(p) <= float(p_value_of_hl):
			co+=1
	return co, co/10000

	
		
