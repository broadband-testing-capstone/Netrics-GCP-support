from gcp_upload import upload_blob, list_buckets
import argparse
import subprocess
from socket import gethostname
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz


TZ_STR='US/Pacific'


def get_args():
    parser = argparse.ArgumentParser(description='Run Ookla and NDT7 tests N times given a starting time and date')
    parser.add_argument('--service_account', help='service account file json', required=True)
    parser.add_argument('--bucket_name', help='bucket name to upload to', required=True)
    parser.add_argument('--start', help='starting date in PST TZ and ISO 8601 format (yyyy-mm-ddTHH:MM:SS)', required=True)
    parser.add_argument('--interval', type=int, help='interval in minutes', required=False, default=5)
    parser.add_argument('--n', type=int, help='number of tests, do not exceed 40 in 24hrs', required=False, default=10)    

    return parser.parse_args()


def run_test(test_name, test_arg, args):
    
    with open(test_name+'.tmp', 'w') as f:
        subprocess.run(['netrics', test_arg], stdout=f)
    
    fname = '{0}-{1}-{2}.txt'.format(test_name, gethostname(), datetime.now(tz=pytz.timezone(TZ_STR)).isoformat())
    print(fname)
 
    upload_blob(args.bucket_name, test_name+'.tmp', fname, args.service_account)
    print('uploaded {0}'.format(fname))
    
    subprocess.run(['rm', test_name+'.tmp'])


def all_tests(args):
    
    run_test('ookla', '-k', args)
    run_test('ndt7', '-a', args)
    
    print('ran test')

if __name__ == '__main__':
    print('running netrics')
    args = get_args()    
    
    
    #Timezone naive solution
    run_date = datetime.fromisoformat(args.start)
    #-8:00 hours offset for PST from UTC
    now = datetime.now() - timedelta(hours=8)
    
    #check that start is in the future
    if not run_date > now:
        raise ValueError('entered start time already past.')
    
    inc = timedelta(minutes=args.interval)
    
    sched = BlockingScheduler()

    for n in range(args.n):
        sched.add_job(all_tests, 'date', run_date=run_date, timezone=TZ_STR, args=[args])
        #increment start time by inc
        run_date += inc
    
    sched.print_jobs()    
    sched.start()



