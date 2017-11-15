#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
import hashlib
import codecs
import pickle
def main(argv):
  try:
    for line in sys.stdin:
      line = line.strip()
      obj  = json.loads( line )
      data_owner_id = obj['data_owner_id']
      '''skip suumo(6517)'''
      if data_owner_id == 6517:
        continue
      gender_age = obj['gender_age']
      tuuid = obj['tuuid']
      if tuuid == None or tuuid == 'null' or tuuid == 'opt-out':
        ''' if there is no tuuid, fill tuuid filed as ip-addr + browser '''
        tuuid =  'sha256_' + hashlib.sha256( bytes(obj['ip'] + obj['useragent'],'utf8') ).hexdigest()
      request_uri = obj['request_uri']
      dec         = urllib.parse.unquote( urllib.parse.unquote(request_uri) )
      #print(dec)
      src = re.search(r'src=(.*?)&', dec)
      ref = re.search(r'ref=(.*?)&', dec)
      if src is None or ref is None:
        continue
      domain = None
      if src is not None:
        src = src.group(1)
      if ref is not None:
        ref = ref.group(1)
      if src is None or ref is None:
        continue
      date_time = obj['date_time']
      key = '{}'.format(tuuid) 
      tosave = (date_time, data_owner_id, ref, src)
      print(key + '\t' + codecs.encode(pickle.dumps(tosave),'base64').decode().replace('\n', '') )

  except Exception as e:
    print('SOME DEEP error occured!\t' + str(e))
    ...

if __name__ == "__main__":
    main(sys.argv)
