# madqtt-pi #

## install ##

create a service user for madqtt and grant rights for gpio
```bash
sudo adduser --system --home /opt/madqtt --group madqtt
sudo adduser madqtt gpio
```

start bash as service user and install service and requirements
```bash
sudo -u madqtt bash
cd /opt/madqtt
git clone https://github.com/techolutions/madqtt-pi.git .
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt --upgrade
```

copy example config and ajust settings
```bash
cp configs/config.yml.example configs/config.yml
nano configs/config.yml
```

try if everything works
```bash
python start.py
deactivate
exit
```

## systemd service file ##
```bash
[Unit]
Description=MADqtt
After=network.target

[Service]
User=madqtt
WorkingDirectory=/opt/madqtt/
ExecStart=/opt/madqtt/venv/bin/python start.py
Restart=on-abnormal

[Install]
WantedBy=multi-user.target

```
