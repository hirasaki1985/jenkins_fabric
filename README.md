## require
* docker
* openssh (.ssh/)の設定ファイル

## インストール & 環境構築
### プロジェクトのダウンロード
```
$ git clone https://github.com/hirasaki1985/jenkins_fabric.git
$ cd jenkins_fabric
```

### 鍵の作成 or 鍵の設置
新しく作成する場合は以下のコマンドを実行
```
$ ssh-keygen -t rsa -b 4096 -f ./.ssh/id_rsa
```

### configファイルの作成

```
vi ./.ssh/config
```

configファイルのサンプルです。
```
ServerAliveInterval 60

Host webserver01
  HostName 192.168.0.100
  User deployuser
  Port 22
  IdentityFile ~/.ssh/id_rsa

Host webserver02
  HostName 192.168.0.101
  User deployuser
  Port 22
  IdentityFile ~/.ssh/id_rsa

Host database01
  HostName 192.168.0.102
  User dbuser
  Port 22
  IdentityFile ~/.ssh/id_rsa
```

鍵とconfigファイルは、環境に合わせて修正してください。

### create docker volumes
```
$ docker volume create --name deployserver-volume
$ docker volume ls
```

### build docker image
.sshディレクトリの設定が終わったらビルドを開始。

```
$ docker build . -t deployserver
```

### create container
```
$ docker run -t -i -d \
    -v `pwd`/src:/tools \
    -v deployserver-volume:/var/jenkins_home \
    -p 8080:8080 -p 50000:50000 \
    -e MYSQL_PASSWORD=password -e MYSQL_USER=user_name -e MYSQL_DB_NAME=db_name \
    -h deployserver --name deployserver deployserver
```

### init jenkins
```
$ docker exec -it deployserver bash
(deployserver)$ cat /var/jenkins_home/secrets/initialAdminPassword
```

### access jenkins & setup
http://localhost:8080
「init jenkins」で出力されたinitialAdminPasswordを入力し、セットアップを続ける。

## ジョブの作成
「シェルの実行」の欄にそれぞれ以下のように入力

### デプロイ
```
fab -f /tools/fabfile.py -H webserver01,webserver02 webserver_deploy
```
.ssh/configに設定されたwebserver01,02に対し、fabfile.pyのwebserver_deploy()関数が実行されます。

### SQL実行
```
fab -f /tools/fabfile.py -H database01 exec_sql_sample
```
.ssh/configに設定されたdatabase01に対し、fabfile.pyのexec_sql_sample()関数が実行され、
mysql_exec()によりSQLが実行されます。

あとはジョブを実行するだけ。

## 手動でfabricを動かす場合
```
$ docker exec -it deployserver bash
(deployserver)$ fab -f /tools/fabfile.py -H webserver01,webserver02 webserver_deploy
(deployserver)$ fab -f /tools/fabfile.py -H database01 exec_sql_sample
```

## Other Commands
```
### root権限でコンテナに入る場合
$ docker exec -it -u root deployserver bash

### コンテナとイメージを削除
$ docker rm -f deployserver && docker rmi deployserver

### exitedで終了しているコンテナを一括削除
$ docker rm $(docker ps -a --filter 'status=exited' -q)
```




