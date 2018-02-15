#!/usr/bin/env python
import sys

current_key=None
code_dict={}
for line in sys.stdin:
    line=line.strip()
    key,value=line.split("\t",1)
    if current_key==None:
        code_dict[key]=int(value)
        current_key=key
    elif current_key==key:
        code_dict[key]+=1
    else:
        code_dict[key]=int(value)
        current_key=key

        
for f,v in code_dict.items():
    print ('%s\t%s' % (int(f),v))
    
    
    