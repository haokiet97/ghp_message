# Ghp_message project

## Requirement

- Python 3.6
- sqlite 3 or Mysql 5.7

## Install

### Python 3.6

```shell script
sudo apt-get update
sudo apt-get install -y software-properties-common curl
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get install -y add-apt-repository ppa:deadsnakes/ppa
# cái nào lỗi thì thôi
sudo apt-get update
sudo apt-get install -y python3.6 python3.6-venv
sudo apt-get install python3.6-dev libmysqlclient-dev
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```
### Sqlite3
search google nha
```shell script
sudo apt update
sudo apt-get install sqlite3
```
### Mysql
"Không cần thiết"

```shell script
sudo apt-get install mysql-server
```

and config mysql:

```shell script
sudo mysql_secure_installation
```

enter your user and password of mysql

check server mysql is work:
```shell script
systemctl status mysql.service
```

### Redis
cái này để làm gì chưa biết. cứ cài đã nhá

```shell script
sudo apt-get install redis-server
sudo systemctl enable redis-server.service
```

### Project config

### Project dependent

In your project, enter command below:

```shell script
virtualenv --python=python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Hoăc có thể dùng daphne:
```shell script
virtualenv --python=python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt update
sudo apt install daphne
#Trong thư mục project
source venv/bin/activate
#run server với daphne
daphne ghp_message.asgi:application --port <port tùy thích, mặc định 8000>
```

### Chú ý:
Mỗi lần sử dụng thêm thư viện gì thì nhớ update lại file requirements.txt

```shell script
pip freeze > requirements.txt
```
