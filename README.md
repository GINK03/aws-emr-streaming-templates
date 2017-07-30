# AWS Elastic Map Reduce Hadoop Examples

## Python2でのワードカウント

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

## Rubyでのワードカウント

