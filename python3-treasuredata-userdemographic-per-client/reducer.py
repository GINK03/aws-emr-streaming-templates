#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs

def main():
  key_term_freq = {}
  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    val = json.loads(val)
    if key_term_freq.get(key) is None:
      key_term_freq[key] = {}
    for keyword, freq in val.items():
      if key_term_freq[key].get(keyword) is None:
        key_term_freq[key][keyword] = 0
      key_term_freq[key][keyword] += freq

    if len(key_term_freq) >= 2:
      for key, term_freq in key_term_freq.items():
        print(key + '\t' + json.dumps(term_freq, ensure_ascii=False) )
      key_term_freq = {}
if __name__ == "__main__":
    main()
