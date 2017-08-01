# AWS EMR Hadoop Streaming Examples

GCPのDataFlowの方が、AWS EMRより個人的にはモダンな印象があるのですが、業務でAWSで非構造化データの大規模な分析が必要になる可能性があり、Hadoop Streamingの仕組みを軽くおさらいして、いくつかの言語で動かしました　　

Map Reduceの仕組み自体は古いのですが、論文にもなっており、この構成でほとんどの集計が可能みたいなことを言っており、パワーを感じます[1]  

<div align="center">
  <img width="450px" src="https://user-images.githubusercontent.com/4949982/28753294-9aee0e74-756d-11e7-9eaf-97c5906f890f.png">
</div>
<div align="center"> 図1. イメージしているところのMapReduceの構成 </div>

AWSのElastic Map Reduceを利用してHadoop Streamingで任意の言語で、ビッグデータを処理する方法を説明します  

任意の言語で処理をつなげることができるため、AWS EMR(Hadoop Streaming)の仕組みさえ理解していれば、好きな言語で処理が可能です



ここでは、以下の言語におけるもっとも簡単な集計である、全てのドキュメントになんの語が何回出現するか、カウントするプログラムを例示します
1. Python2
2. Python3
3. Ruby ( 2.4 )  
4. Go ( 1.8 )

## S3にデータをおく
S3に分析する対象の非構造化データをフォルダを作っていれておきます　　

生データか、gzで圧縮されている必要があります  

例えば、一つのバケットで処理する場合には、このようなフォルダ構成をとります  

<div align="center">
  <img width="450px" src="https://user-images.githubusercontent.com/4949982/28753094-7f3067e4-7569-11e7-8740-e13b21c9c2fd.png">
</div>

フォルダに必要なデータを適切に配置して、awscliのコンフィグレーションを通した状態で、次のコマンドでHadoop Streamingを実行します  

```console
$ aws emr add-steps --cluster-id j-{$YOUR_EMR_ID} --steps file://./WordCount_step.json --region ap-northeast-1
```

ここで、引数に指定されている　JSONファイルはこのような記述になっています  
```json
[
  {
     "Name": "WordCount",
     "Type": "STREAMING",
     "ActionOnFailure": "CONTINUE",
     "Args": [
         "-files",
         "s3://{$YOUR_S3}/wordcount-code/mapper,s3://{$YOUR_S3}/wordcount-code/reducer",
         "-mapper",
         "mapper",
         "-reducer",
         "reducer",
         "-input",
         "s3://{$YOUR_S3}/wordcount-dataset/",
         "-output",
         "s3://{$YOUR_S3}/wordcount-result"]
  }
]
```
（注：これはGoでバイナリを指定しているので、pythonやrubyの場合、適切にfilesの引数を変えてください）

## Python2でのワードカウント
各種インターネット上の文献では、Python2でワードカウントしていることが多いです  

AWSの解説サイトで紹介されていた方法で、集計する  

Reducerを特別な予約関数を割り当てることで省略できますが、ボトムアップ的に学ぶには、実装してしまった方が良いだろうという判断をしました  

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
世の中には、Rubyestが多く、PythonでなくてRubyでやりたいという人も多いです  

Rubyは悪くない選択肢でもあるので、使い方を説明します

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

好みの問題である気がしてて、好きな言語で良いと思います  

## Goでのワードカウント
私がstreamingにおいて、スクリプト言語より、速度やメモリリソースや、シングルバイナリになるという点で、良いと感じているのが、Go言語です  

Go言語はそのシンプルなシンタックスでありながら、ランタイムに依存することなく、実行可能なバイナリを出力が可能です  

つまり、AWS EMRのノードに対して、なんらかログインしてソフトウェアをインストールやセットアップをする必要がありません  

### mapper
```go
package main

import (
        "bufio"
        "fmt"
        "os"
        "strings"
)

func main() {
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
                line := scanner.Text()
                terms := strings.Split(line, " ")
                for _, term := range terms {
                        out := fmt.Sprintf("%s\t1", term)
                        fmt.Println(out)
                }
        }
}
```

### reducer
```go
package main

import (
        "bufio"
        "fmt"
        "os"
        "strings"
)

func main() {
        dic := map[string]int{}
        scanner := bufio.NewScanner(os.Stdin)
        for scanner.Scan() {
                line := scanner.Text()
                ents := strings.Split(line, "\t")
                term := ents[0]
                _ = ents[1]

                _, ok := dic[term]
                if ok == false {
                        dic[term] = 0
                }
                dic[term] += 1
        }

        for term, freq := range dic {
                out := fmt.Sprintf("%s %d", term, freq)
                fmt.Println(out)
        }
}
```
## コード
[GITHUB](https://github.com/GINK03/aws-emr-streaming-templates)

## まとめ
いくつかの言語において、実際に、AWS EMRを動かして集計しました  

PythonやRubyおける使い方は、数年前からあまり進化を感じられませんが、Go言語という選択が可能になったことで、goroutineによる効率的な並列処理や、実行可能なバイナリであるというメモリが少なく済んだりするメリットがあるので、今までの集計方では集められなかった角度のデータが取得できそうで、未来が見えました  

## 参考文献
[1] [MapReduce: Simplified Data Processing on Large Clusters](https://static.googleusercontent.com/media/research.google.com/ja//archive/mapreduce-osdi04.pdf)
