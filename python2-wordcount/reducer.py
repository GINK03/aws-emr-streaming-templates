#!/usr/bin/python3
import sys
import re

def main(argv):
  term_freq = {}

  for line in sys.stdin:
    line = line.strip()
    ents = line.split('\t')
    term, freq = ents
    freq = int(freq)
   
    try:
      if term_freq.get(term) == None:
        term_freq[term] = 0
      term_freq[term] += 1
    except Exception as e:
      print(e)
  for term, freq in term_freq.items():
    print( term, freq )

if __name__ == "__main__":
    main(sys.argv)
