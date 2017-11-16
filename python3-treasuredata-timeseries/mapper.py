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
      '''skip suumo(6517)'''
      if data_owner_id == 6517 or data_owner_id is None:
        continue
      #gender_age = obj['gender_age']
      tuuid = obj['tuuid']
      if tuuid == None or tuuid == 'null' or tuuid == 'opt-out':
        ''' if there is no tuuid, fill tuuid filed as ip-addr + browser '''
        try:
          tuuid =  'sha256_' + hashlib.sha256( bytes(obj['ip'] + obj['useragent'],'utf8') ).hexdigest()
        except TypeError as e:
          continue
      request_uri = obj['request_uri']
      try:
        dec         = urllib.parse.unquote( urllib.parse.unquote(request_uri) )
      except Exception as e:
        continue
      #print(dec)
      src = re.search(r'src=(.*?)&', dec)
      ref = re.search(r'ref=(.*?)&', dec)
      if src is None or ref is None:
        continue
      #domain = None
      if src is not None:
        src = src.group(1)
      if ref is not None:
        ref = ref.group(1)
      if src is None or ref is None:
        continue
      date_time = obj['date_time']
      if date_time is None:
        continue
      key = '{}'.format(tuuid) 
      tosave = (date_time, data_owner_id, ref, src)
      val = json.dumps(tosave, ensure_ascii=False)
      if key == '' or val == '':
        continue
      try:
        sys.stdout.write(key + '\t' + val + '\n' )
      except Exception as e:
        continue


if __name__ == "__main__":
    main()
