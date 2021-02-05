# madqtt-pi #

## preconditions ##

You need a mqtt-broker, for example mosquitto:
```bash
sudo apt install mosquitto
```

## install ##

Create a service user for madqtt and grant rights for gpio usage:
```bash
sudo adduser --system --home /opt/madqtt --group madqtt
sudo adduser madqtt gpio
```

Start bash as service user and install service and requirements:
```bash
sudo -u madqtt bash
cd /opt/madqtt
git clone https://github.com/techolutions/madqtt-pi.git .
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt --upgrade
```

Copy example config and adjust settings:
```bash
cp configs/config.yml.example configs/config.yml
nano configs/config.yml
```

Try if everything works, deactivate venv, leave bash:
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

## restrict broker by user and password authentification ##
For minimal security, it's recommended to restrict broker usage by username and password.

First create a password file and add a user:
```bash
sudo touch /etc/mosquitto/passwd
sudo mosquitto_passwd -b /etc/mosquitto/passwd <user> <password>
```
Create a conf file for mosquitto:
```bash
sudo nano /etc/mosquitto/conf.d/default.conf
```
Insert the following content inside the conf file to restrict usage:
```bash
allow_anonymous false
password_file /etc/mosquitto/passwd
```
Restart mosquitto:
```bash
sudo systemctl restart mosquitto.service
```
