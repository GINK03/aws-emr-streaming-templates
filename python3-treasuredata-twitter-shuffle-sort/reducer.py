#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs
def main(argv):
  scaning = 'init' 
  buff = list()
  for line in sys.stdin:
    line = line.strip()
    try:
      key, val = line.split('\t')
    except Exception as ex:
      continue
    val = json.loads(val)
    if scaning == key:
      buff.append(val)
    # 最大の要素数を定義はしない
    if scaning != key:
      if buff != list():
        print(scaning + '\t' + json.dumps(list(buff), ensure_ascii=False) )
        buff = list()
      # update scaning to new key
      scaning = key
      buff.append(val)
if __name__ == "__main__":
    main(sys.argv)
