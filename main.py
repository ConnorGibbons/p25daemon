import time
import datetime
import logging
import traceback
import gc
from logging.handlers import TimedRotatingFileHandler
import config
from src.p25daemon import move_and_transcribe
import os


def seconds_until_next_run(hour = 0, minute = 1):
    now = datetime.datetime.now()
    next_run = now.replace(hour = hour, minute = minute, second = 0, microsecond = 0)
    if next_run <= now:
        next_run += datetime.timedelta(days = 1)
    logging.info(f"Now: {now.isoformat()}")
    logging.info(f"Next Run: {next_run.isoformat()}")
    return (next_run - now).total_seconds()

def sleep_until_next_run(next_run_hour = config.RUN_TIME_HOUR, next_run_minute = config.RUN_TIME_MINUTE):
    sleep_time = seconds_until_next_run(hour = next_run_hour, minute = next_run_minute)
    logging.info(f"Sleeping for {sleep_time/3600:.2f} hours until next run.")
    time.sleep(sleep_time)

def main():
    try:
        os.makedirs("logs", exist_ok = True)
        
        log_handler = TimedRotatingFileHandler(
            "logs/p25daemon",  
            when = "midnight", 
            interval = 1,
            backupCount = 7,
            encoding = "utf-8"
        )
        log_handler.suffix = "%m.%d.%Y"
        log_handler.extMatch = None
        
        logging.basicConfig(level = logging.INFO, 
                        handlers = [log_handler, logging.StreamHandler()],
                        format = '%(asctime)s - %(levelname)s - %(message)s'
                        )
        logging.info(f"Starting p25daemon, using model {config.WHISPER_MODEL} on {config.WHISPER_DEVICE}")
        
        if not config.RUN_IMMEDIATELY:
            sleep_until_next_run()

        while True:
            datetime_today = datetime.date.today()
            try:
                move_and_transcribe(datetime_today)
            except Exception as e:
                logging.error(f"Error in move_and_transcribe: {e}")
            finally:
                gc.collect()
            sleep_until_next_run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())
    finally:
        gc.collect()
    

if __name__ == "__main__":
    main()