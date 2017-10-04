#!/usr/bin/python3
import sys
import re
import json 
import urllib
import urllib.parse
def main(argv):
  try:
    for line in sys.stdin:
      line = line.strip()
      obj  = json.loads( line )
      data_owner_id = obj['data_owner_id']
      gender_age = obj['gender_age']
      if gender_age is None:
        continue
      tuuid = obj['tuuid']
      if tuuid == None or tuuid == 'null' or tuuid == 'opt-out':
        ''' if there is no tuuid, fill tuuid filed as ip-addr + browser '''
        tuuid =  'sha256_' + hashlib.sha256( bytes(obj['ip'] + obj['useragent'],'utf8') ).hexdigest()
      request_uri = obj['request_uri']
      dec         = urllib.parse.unquote( urllib.parse.unquote(request_uri) )
      keyword     = re.search(r'ipao9702=(.*?)&', dec)
      if keyword is not None:
        keyword = keyword.group(1)
      else: 
        keyword = re.search(r'mtk=(.*?)&', dec)
        if keyword is not None:
          keyword = keyword.group(0)
      src = re.search(r'src=(.*?)&', dec)
      domain = None
      if src is not None:
        src     = src.group(1)
        try:
          domain  = src.split('/').pop(2)
        except Exception as e:
          print( 'domain parse error', e, src, file=sys.stderr )
          domain  = src
      if src is None:
        continue
      date_time = obj['date_time']
      key = '{}_{}'.format(tuuid, data_owner_id) 
      tosave = { date_time : [keyword, src, domain, data_owner_id, gender_age] }
      print(key + '\t' + json.dumps(tosave) )

  except Exception as e:
    print('SOME DEEP error occured!', e, file=sys.stderr)

if __name__ == "__main__":
    main(sys.argv)
