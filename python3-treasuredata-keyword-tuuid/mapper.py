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
      obj  = json.loads( line )
      data_owner_id = obj['data_owner_id']
      if data_owner_id is None:
        continue
      gender_age = obj['gender_age']
      income = obj['income']
      tuuid = obj['tuuid']
      if tuuid == 'opt-out':
        continue
      if tuuid == None or tuuid == 'null':
        ''' if there is no tuuid, fill tuuid filed as ip-addr + browser '''
        try:
          tuuid =  'sha256_' + hashlib.sha256( bytes(obj['ip'] + obj['useragent'],'utf8') ).hexdigest()
        except TypeError as e:
          continue
      request_uri = obj['request_uri']
      try:
        dec = urllib.parse.unquote( urllib.parse.unquote(request_uri) )
      except Exception as ex:
        continue
      src = re.search(r'src=(.*?)&', dec)
      ref = re.search(r'ref=(.*?)&', dec)
      if src is None or ref is None:
        continue
      if src is not None:
        src = src.group(1)
      if ref is not None:
        ref = ref.group(1)
     
      keyword  = re.search(r'ipao9702=(.*?)&', dec)
      if keyword is not None:
        keywords = [ 'SEARCH_' + keyword.group(1) ]
      else:
        keywords = [ 'META_' + m for m in re.findall(r'mtk=(.*?)&', dec) ]

      for key in keywords:
        tosave = {'tuuid':tuuid, 'data_owner_id': data_owner_id, 'income': income, 'gender_age':gender_age}
        val = json.dumps(tosave, ensure_ascii=False)
        if key == '' or val == '':
          continue
        try:
          sys.stdout.write(key + '\t' + val + '\n' )
        except Exception as ex:
          continue


if __name__ == "__main__":
    main()
