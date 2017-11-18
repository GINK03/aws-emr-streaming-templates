#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
import hashlib
import codecs
import pickle
from datetime import datetime


now = datetime.now()
year_month1 = '%02d-%02d'%(now.year, now.month)
if now.month != 1:
  year_month2 = '%02d-%02d'%(now.year, now.month-1) 
else:
  year_month2 = '%02d-%02d'%(now.year-1, 12) 
#print(year_month)
#sys.exit()
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
        # もし、処理の該当年月でないならスキップ
        if year_month1 not in time and year_month2 not in time:
          continue
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
      for key, keyword_freq in key_keyword_freq.items():
        print('{doi}_{key}'.format(doi=doi, key=key) + '\t' + json.dumps(keyword_freq, ensure_ascii=False) )


if __name__ == "__main__":
    main()
