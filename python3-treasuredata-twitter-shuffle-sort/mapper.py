#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
import hashlib
import codecs
import pickle
def main():
    #for line in sys.stdin:
    while True:
      try:
        line = sys.stdin.readline()
      except UnicodeDecodeError as e:
        continue
      if not line :
        break
      line = line.strip()
      print(line)  

if __name__ == "__main__":
    main()
