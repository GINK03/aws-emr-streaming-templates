#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs
def main(argv):
  scaning = 'init' 
  buff = []
  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    val = json.loads(val)
    if scaning == key:
      buff.append(val)
    if scaning != key:
      if buff != []:
        print(scaning + '\t' + json.dumps(buff, ensure_ascii=False) )
        buff = []
      # update scaning to new key
      scaning = key
if __name__ == "__main__":
    main(sys.argv)
