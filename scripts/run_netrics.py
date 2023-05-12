#!/usr/bin/env python3
from gcp_upload import upload_blob, get_bucket
import argparse
import subprocess
from socket import gethostname
from datetime import datetime, timedelta, time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
import logging
import os
import sys



def get_args():
    parser = argparse.ArgumentParser(description='Run Ookla and NDT7 given a crontab')
    parser.add_argument('--service_account', type=str, help='service account file json', required=True)
    parser.add_argument('--bucket', type=str, help='bucket name to upload to', required=True)
    parser.add_argument('--crontab', type=str, help='standard crontab expression for scheduling', required=False, default= '0 * * * *')
    parser.add_argument('--logs', type=str, help='directory for logs', required=True)
    parser.add_argument('--tz', type=str, help='Timezone string, see pytz module', required=False, default='US/Pacific')

    return parser.parse_args()


def run_test(test_name, test_arg, args):

    with open(test_name+'.tmp', 'w') as f:
        subprocess.run(['netrics', test_arg], stdout=f)

    fname = '{0}-{1}-{2}.txt'.format(test_name, gethostname(), datetime.now(timezone(args.tz)).isoformat())

    upload_blob(args.bucket, test_name+'.tmp', fname, args.service_account)
    logging.info('uploaded {0}'.format(fname))

    subprocess.run(['rm', test_name+'.tmp'])


def all_tests(args):
    run_test('ookla', '-k', args)
    run_test('ndt7', '-a', args)


def run_crontab(args, path):

    tz = timezone(args.tz)
    now = datetime.now(tz)

    logging.basicConfig(filename=path+(now.isoformat())+'.log', encoding='utf-8', level=logging.INFO)
    logging.info('Command: ' + ' '.join(sys.argv))

    try:
        crontab = CronTrigger.from_crontab(args.crontab, timezone=tz)
    except:
        raise ValueError('Improper crontab expression. See https://en.wikipedia.org/wiki/Cron')

    all_tests(args)

    sched = BlockingScheduler()

    sched.add_job(all_tests, crontab, args=[args])

    sched.start()


if __name__ == '__main__':
    args = get_args()

    #check for valid key and bucket
    try:
        bucket = get_bucket(args.service_account, args.bucket)
    except:
        raise ValueError('Invalid key or bucket does not exist')

    path = args.logs
    if not path[-1] == '/':
        path = path + '/'

    if not os.path.exists(path):
        #print('logging files to ' + path)
        raise ValueError('invalid path for logging')

    run_crontab(args, path)




