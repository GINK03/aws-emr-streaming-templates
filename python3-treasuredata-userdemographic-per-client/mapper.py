#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
import hashlib
import codecs
import pickle


doi_key_keyword_freq = {}
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
      try:
        key, val = line.split('\t')
      except ValueError as e:
        continue
      obj  = json.loads( val )
      #print( obj )

      for time, data in obj.items():
        keyword = data[0]
        data_owner_id = data[-3]
        gender_age = data[-2]
        income = data[-1]
        key = '{}_{}'.format(gender_age, income)
        #print(time, keyword, data_owner_id, gender_age, income)
        if doi_key_keyword_freq.get(data_owner_id) is None:
          doi_key_keyword_freq[data_owner_id] = {}
        if doi_key_keyword_freq[data_owner_id].get(key) is None:
          doi_key_keyword_freq[data_owner_id][key] = {}
        if doi_key_keyword_freq[data_owner_id][key].get( keyword ) is None:
          doi_key_keyword_freq[data_owner_id][key][keyword] = 0
        doi_key_keyword_freq[data_owner_id][key][keyword] += 1
    for doi, key_keyword_freq in doi_key_keyword_freq.items():
      print(str(doi) + '\t' + json.dumps(key_keyword_freq, ensure_ascii=False) )


if __name__ == "__main__":
    main()
