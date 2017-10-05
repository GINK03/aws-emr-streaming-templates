#!/usr/bin/python3
import sys
import re
import json

def main(argv):
  key_vals = {} 
  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    val = json.loads(val)
    if key_vals.get( key ) is None:
      key_vals[key] = {}
    
    for timestamp, meta in val.items():  
      key_vals[key][timestamp] = meta
  for key, vals in key_vals.items():
    print(key + '\t' + json.dumps(vals, ensure_ascii=False) )
if __name__ == "__main__":
    main(sys.argv)
