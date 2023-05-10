#!/bin/bash

#install netrics dependency (amd64 only)
echo "downloading and installing netrics"
wget https://github.com/chicago-cdac/nm-exp-active-netrics/releases/download/v1.0.0-2023/nm-exp-active-netrics-v1.0.0-amd64.deb

sudo DEBIAN_FRONTEND=noninteractive apt install ./nm-exp-active-netrics-v1.0.0-amd64.deb 

echo "deleting download"
rm -f nm-exp-active-netrics-v1.0.0-amd64.deb

echo "installing python modules"
pip install -r requirements.txt

mkdir logs
echo "created logs directory"

