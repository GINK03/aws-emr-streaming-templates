#!/usr/bin/python3
import sys
import re
import json
import pickle
import codecs

def main():
  for line in sys.stdin:
    line = line.strip()
    print(line)
if __name__ == "__main__":
    main()
