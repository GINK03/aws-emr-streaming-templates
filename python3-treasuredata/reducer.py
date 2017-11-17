#!/usr/bin/python3
import sys
import re
import json

def main(argv):
  scaning = 'init' 
  buff = {}
  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    val = json.loads(val)
    timestamp = list(val.keys()).pop()
    meta = list(val.values()).pop()
    if scaning == key:
      buff[timestamp] = meta
    if scaning != key:
      if buff != {}:
        print(scaning + '\t' + json.dumps(buff, ensure_ascii=False) )
      # update scaning to new key
      scaning = key
      buff = val
if __name__ == "__main__":
    main(sys.argv)
