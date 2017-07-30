#!/usr/bin/python3
import sys
import re
 
def main(argv):
  for line in sys.stdin:
    line = line.strip()
    for term in line.split():
      print('{}\t1'.format(term) )
if __name__ == "__main__":
    main(sys.argv)
