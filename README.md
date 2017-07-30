# AWS Elastic Map Reduce Hadoop Examples

## Python2でのワードカウント
各種インターネット上の文献では、Python2でワードカウントしていることが多い。  
AWSの解説サイトで紹介されていた方法で、集計する  
Reducerを特別な予約関数を割り当てることができるが、ボトムアップ的に学ぶには、実装してしまった方が良いだろうという判断である  


## Python3でのワードカウント
Python3をインストールするため、Hadoopのクラスタにログインする必要がある  

AWSのデフォルトのセキュリティグループについては、sshでログインできないので、セキュリティグループを解放する  
```console
$ ssh -i {$KEY} hadoop@{$IPADDR}
```

Python35のインストール(必要に応じでバージョンを切り替えてください)
```cosnole
$ sudo yum install python35
$ sudo yum install python35-devel
$ sudo yum install python35-pip
```

### mapper
```python
#!/usr/bin/python3
import sys
import re
 
def main(argv):
  for line in sys.stdin:
    line = line.strip()
    for term in line.split():
      print('{}\t1'.format(term) )
if __name__ == "__main__":
    main(sys.argv)
```

### reducer
```python
#!/usr/bin/python3
import sys
import re

def main(argv):
  term_freq = {}
  for line in sys.stdin:
    line = line.strip()
    ents = line.split('\t')
    term, freq = ents
    freq = int(freq)
    try:
      if term_freq.get(term) == None:
        term_freq[term] = 0
      term_freq[term] += 1
    except Exception as e:
      print(e)
  for term, freq in term_freq.items():
    print( term, freq )

if __name__ == "__main__":
    main(sys.argv)
```

## Rubyでのワードカウント

