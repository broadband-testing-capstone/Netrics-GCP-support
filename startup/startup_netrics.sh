#!/bin/sh
#run 32 tests between 7-11pm daily
#change logs argument and bucket argument
python3 /etc/netrics_gcp/run_netrics.py --service_account /etc/netrics_gcp/config/service-account-keyfile.json --logs /home/dellemc2/logs --bucket netrics_tests --crontab "*/8 19-23 * * *" 

