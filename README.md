# zalo-apps
Zalo Mini Apps DEMO for CDP

# How to run 

1. Need Python 3.10, run following commands
```
sudo apt install python-is-python3
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.10
sudo apt-get install python3.10-venv
pip install virtualenv
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
2. You need to refresh the session of login shell after install python-is-python3
3. Need to create a file .env to store environment variables
4. In the file .env, set value like this example
```
DEV_MODE=true
HOSTNAME=zalo-apps.example.com

5. Set correct DIR_PATH in start_app.sh, an example like this
```
DIR_PATH="/build/zalo-apps/"
```
6. Run ./start_app.sh for PRODUCTION or ./start_dev.sh for DEVELOPMENT
7. The zaloapp is started at the host 0.0.0.0 with port 9090