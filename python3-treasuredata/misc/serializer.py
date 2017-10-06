import os
import gzip
import glob
import sys
import math
import json
import urllib.parse
import re
import pickle
import os.path
import concurrent.futures
import itertools
import hashlib


def _bundles(name):
  urls = set([url.replace('\n', '') for url in open('conversion.urls') if url != ''])
  for en, line in enumerate(open(name)):
    line = line.strip()
    if en%500 == 0:
      print('now iter', en)
    tuuid, vraw = line.split('\t')

    obj = json.loads(vraw)
    data = []
    for time, tup in sorted( obj.items(), key=lambda x:x[0] ):
      #print( tup )
      keyword, url, domain, data_owner_id, gender_age = tup 
      # 順序に注意すること
      if url is not None and any(map(lambda x: x in url, urls)):
        data.append('CV')
      else:
        data.append(keyword)
    data = list( data )
    # CVが入っているもののみを保存する
    if 'CV' in data:
      open('flatten/{data_owner_id}_{gender_age}_{tuuid}.json'.format( data_owner_id=data_owner_id, gender_age=gender_age, tuuid=tuuid ), 'w').write( json.dumps(data) )

def bundle():
  names = [name for name in glob.glob('../../../20170825-result/part-*')]
  #_bundles( [0] ) # これはテスト,例外が生じるような際に、強制的にシングルプロセスで動作ささせると落ちるので、それを利用する
  with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
    executor.map( _bundles, names )
    
def reversed_shrink():
  keys = set()
  for name in glob.glob('flatten/*.json'):
    ents = name.split('/').pop().split('_')
    data_owner_id = ents[0]
    gender_age = ents[1]
    key = data_owner_id + '_' + gender_age
    keys.add( key )
  for key in keys:
    results = []
    for eg, name in enumerate( glob.glob('flatten/*.json') ):
      data_owner_id = ents[0]
      gender_age = ents[1]
      _key = data_owner_id + '_' + gender_age
      if eg%100 == 0:
        print( key, eg, name )
      if key != _key:
        continue
      obj  = list( filter(lambda x:x!=None, json.loads( open(name).read() ) ) )
      trim = list( map(lambda x:x.replace('&', ''), filter(lambda x:x!=None, list( itertools.takewhile(lambda x:x!='CV', obj) ) ) ) )
      trim.append( 'CV' )
      if len( trim ) == 1: # CVしかなかったらスキップ
        continue
      ts = []
      for t in list(reversed(trim)):
        if len(ts) == 0:
          ts.append( t )
        if ts[-1] != t:
          ts.append( t )
      results.append( ts )
    open('results/{key}_result.pkl'.format(key=key), 'wb').write( pickle.dumps(results) )

def make():
  for name in glob.glob('results/*.pkl'):
    result = pickle.loads(open(name, 'rb').read() )
    key_freq = {}
    for seq in result:
      print( seq )
      for i in range(1, len(seq)+1):
        key = '/'.join( seq[0:i] )
        if key_freq.get( key ) is None:
          key_freq[key] = 0
        key_freq[key] += 1
    savename = name.replace('.pkl', '.json')
    open(savename, 'w').write( json.dumps( key_freq, ensure_ascii=False, indent=2 ) )
    #print( result )
    
if __name__ == '__main__':
  if '--serialize' in sys.argv:
    serialize()
 
  if '--bundle' in sys.argv:
    bundle()

  if '--reversed_shrink' in sys.argv:
    reversed_shrink()

  if '--make' in sys.argv:
    make()
