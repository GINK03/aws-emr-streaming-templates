#!/usr/bin/python3
import sys

buff = []
for line in sys.stdin: 
  buff.append( line.strip() )

for line in sorted( buff, key=lambda x:x.split('\t')[0] ):
  print( line )
