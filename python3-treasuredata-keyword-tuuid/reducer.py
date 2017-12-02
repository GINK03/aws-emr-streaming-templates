#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs
def main(argv):
  scaning = 'init' 
  buff = set()
  for line in sys.stdin:
    line = line.strip()
    try:
      key, val = line.split('\t')
    except Exception as ex:
      continue
    val = json.loads(val)['tuuid']
    if scaning == key:
      buff.add(val)
    # 最大の要素数を定義
    if scaning != key or len(buff) >= 100000:
      if buff != set():
        print(scaning + '\t' + json.dumps(list(buff), ensure_ascii=False) )
        buff = set()
      # update scaning to new key
      scaning = key
      buff.add(val)
if __name__ == "__main__":
    main(sys.argv)
