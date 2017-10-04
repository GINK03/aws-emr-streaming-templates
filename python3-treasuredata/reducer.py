#!/usr/bin/python3
import sys
import re
import json

def main(argv):
  key_vals = {}

  for line in sys.stdin:
    line = line.strip()
    key, val = line.split('\t')
    val = json.loads(val)
    if key_vals.get(key) is None:
      key_vals[key] = {}
    for timestamp, array in val.items():
      key_vals[key][timestamp] = array
  for key, vals in key_vals.items():
    print(key + '\t' + json.dumps(vals) )
if __name__ == "__main__":
    main(sys.argv)
