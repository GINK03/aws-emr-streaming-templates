#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs

def update(buff, key_keyword_freq):
  for key, keyword_freq in key_keyword_freq.items():
    if buff.get(key) is None:
      buff[key] = {}
    for keyword, freq in keyword_freq.items():
      if buff[key].get(keyword) is None:
        buff[key][keyword] = 0
      buff[key][keyword] += freq 


def main(argv):
  scaning = 'init' 
  buff = {}
  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    key_keyword_freq = json.loads(val)
    if scaning == key:
      update(buff,key_keyword_freq)
    if scaning != key:
      if buff != {}:
        print(scaning + '\t' + json.dumps(buff, ensure_ascii=False) )
        buff = {}
      # update scaning to new key
      scaning = key
      update(buff,key_keyword_freq)
if __name__ == "__main__":
    main(sys.argv)
