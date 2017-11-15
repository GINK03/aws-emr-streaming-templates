#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
import hashlib
def main(argv):
  try:
    for line in sys.stdin:
      line = line.strip()
      obj  = json.loads( line )
      data_owner_id = obj['data_owner_id']
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
      domain = None
      if src is not None:
        src = src.group(1)
      if ref is not None:
        ref = ref.group(1)
      date_time = obj['date_time']
      key = '{}'.format(tuuid) 
      tosave = (date_time, ref, src)
      print(key + '\t' + json.dumps(tosave, ensure_ascii=False) )

  except Exception as e:
    print('SOME DEEP error occured!', e, file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv)
