# madqtt-pi #

## install ##
```bash
cd /opt
git clone https://github.com/techolutions/madqtt-pi.git
cd madqtt-pi
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt --upgrade
cd configs
cp config.yml.example config.yml
nano config.yml
python start.py
deactivate
```
