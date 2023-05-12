#!/bin/bash

#install netrics dependency (amd64 only)
echo "downloading and installing netrics"
#wget https://github.com/chicago-cdac/nm-exp-active-netrics/releases/download/v1.0.0-2023/nm-exp-active-netrics-v1.0.0-amd64.deb

#sudo DEBIAN_FRONTEND=noninteractive apt install ./nm-exp-active-netrics-v1.0.0-amd64.deb 

#add PASSWD all line after netrics install

#echo "deleting download"
#rm -f nm-exp-active-netrics-v1.0.0-amd64.deb

#echo "installing python modules"
#sudo pip install -r requirements.txt


sudo mkdir /etc/netrics_gcp/
sudo mkdir /home/dellemc2/logs
sudo mkdir /etc/netrics_gcp/config/

sudo cp scripts/*.py /etc/netrics_gcp/
sudo cp startup/startup_netrics.sh /etc/netrics_gcp/
sudo cp startup/startup_netrics.service /etc/systemd/system/
sudo cp service-account-keyfile.json /etc/netrics_gcp/config

sudo chmod +x /etc/netrics_gcp/run_netrics.py
sudo chmod +x /etc/netrics_gcp/startup_netrics.sh
sudo chmod 755 /home/dellemc2/logs

sudo systemctl enable startup_netrics.service
sudo systemctl is-enabled startup_netrics.service
#manually start and stop this with
#sudo systemctl start/stop/restart/status startup_netrics.service




