# AWS Elastic Map Reduce Hadoop Examples

AWSのElastic Map Reduceを利用してHadoop Streamingで任意の言語で、ビッグデータを処理する方法を説明する  
任意の言語で処理をつなげることができるため、AWS EMR(Hadoop Streaming)の仕組みさえ理解していれば、好きな言語で処理が可能である

ここでは、以下の言語におけるもっとも簡単な集計である、全てのドキュメントになんの語が何回出現するか、カウントするプログラムを例示する
1. Python2
2. Python3
3. Ruby ( 2.4 

)
4. Go ( 1.8 )


## Python2でのワードカウント
各種インターネット上の文献では、Python2でワードカウントしていることが多い  

AWSの解説サイトで紹介されていた方法で、集計する  

Reducerを特別な予約関数を割り当てることができるが、ボトムアップ的に学ぶには、実装してしまった方が良いだろうという判断である  

### mapper
```python
#!/usr/bin/python
import sys
import re
 
def main(argv):
  pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")
  for line in sys.stdin:
    line = line.strip()
    for word in pattern.findall(line):
      print( word.lower() + "\t" + "1" )
 
if __name__ == "__main__":
    main(sys.argv)
```

### reducer
```python
#!/usr/bin/python
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

### 実行命令
```cosnole
$ aws emr add-steps --cluster-id j-{$YOUR_CLUSTER} --steps file://./WordCount_step.json --region ap-northeast-1
```

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
世の中には、Rubiestが多く、PythonでなくてRubyでやりたいという人も多いです  
悪くない選択肢でもあるので、使い方を説明します

AWS EMRのノードにインストールされているバージョンは古く、アップデートします  

rpmは[ここのサイトから](https://github.com/feedforce/ruby-rpm/releases)ダウンロードしました
```console
$ sudo yum remove ruby
$ sudo yum install ./ruby-2.4.1-1.el6.x86_64.rpm
```

### mapper
```ruby
#!/usr/bin/ruby
STDIN.each_line { |x|
  x.split(" ").map { |x| 
    puts sprintf("%s\t1", x.downcase)
  }
}
```

### reducer
```ruby
#!/usr/bin/ruby
term_freq = {}
STDIN.each_line { |x| 
  term, freq = x.split("\t")
  if term_freq[term] == nil  then 
    term_freq[term] = 0
  end
  term_freq[term] += 1
}

term_freq.each { |term, freq| 
  puts sprintf("%s %d", term, freq)
}
```

全体的にみて、PythonよりRubyの方がスッキリかけますね  
好みの問題でありますが、好きな言語で良いと思います
