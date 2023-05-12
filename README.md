Scripts to execute Netrics speed tests and upload to GCP buckets.

Preconditions: See [here](https://github.com/broadband-testing-capstone/.github/blob/main/OS_install_guide.md) for OS installation. Cloud storage buckets are setup on Google Cloud Platform and a service account key is downloaded to device. 

Download the repository to your device. Edit startup/startup_netrics.sh and change the location of the logs directory to /home/<username>. Change the bucket argument to the name of your bucket. Run this for details on arguments,
  ```
  python3 scripts/run_netrics.py -h 
  ```
Edit setup.sh similarly so /home/<username> is correct. 
To finish setup, run,
  ```
  bash setup.sh
  ```
This downloads Netrics and other dependencies, and initializes the daemon. The default command in startup/startup_netrics.sh runs 32 tests between the hours of 7-11pm. This can be changed by modifying the crontab argument in startup/startup_netrics.sh. See [this](https://www.ibm.com/docs/en/db2/11.5?topic=task-unix-cron-format) for details on the cron format. 

To manage the daemon, the following commands are useful
  ```
  sudo systemctl start/stop/restart/status startup_netrics.service
  ```

