import schedule
import time
import os
from Miyoushe import miyoushe
from Loguru import my_logger

def job():
    current_work_dir = os.path.dirname(__file__)
    my_logger.info(current_work_dir)
    with open(current_work_dir+'/cookies.txt') as f:
        lines = f.read().splitlines()
        i = 0
        for line in lines:
            mi = miyoushe(line,i)
            mi.miyoushe_sign()
            mi.miyoubi_all()
            i = i+1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        my_logger.info("start")
        schedule.every().day.at("06:01").do(job)
    except Exception as e:
        my_logger.error(e)
    while True:
        schedule.run_pending()
        time.sleep(2)
    job()


