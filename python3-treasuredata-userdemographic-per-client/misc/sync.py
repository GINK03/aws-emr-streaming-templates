import os
import sys

if '--test' in sys.argv:
  os.system('mc mirror s3/ml-persona-reports/result-20171118 result-20171118')
