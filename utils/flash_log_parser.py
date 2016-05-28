#!/usr/bin/env python

import sys
count=0
infile=open(sys.argv[1]).readlines()
for line in infile:
	
	if line=="[FLASH] Input files:\n":
		print infile[count+1].split('/')[-1].strip()+','+infile[count+2].split('/')[-1].strip()+',',

	if line.startswith("[FLASH]     Percent combined:"):
		print line.split(': ')[1].strip()
		
	count+=1
