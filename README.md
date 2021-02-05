# madqtt-pi #

## install ##
```bash
sudo adduser --system --home /opt/madqtt --group madqtt
sudo adduser madqtt gpio
sudo -u madqtt bash
cd /opt/madqtt
git clone https://github.com/techolutions/madqtt-pi.git .
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt --upgrade
cp configs/config.yml.example configs/config.yml
nano configs/config.yml
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
