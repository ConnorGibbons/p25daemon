import time
import datetime
import logging
import gc
from logging.handlers import TimedRotatingFileHandler
import torch
import whisper
import config
from src.p25daemon import move_and_transcribe


def seconds_until_next_run(hour=0, minute=1):
    now = datetime.datetime.now()
    next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if next_run <= now:
        next_run += datetime.timedelta(days=1)
    return (next_run - now).total_seconds()

def sleep_until_next_run():
    sleep_time = seconds_until_next_run(hour=0, minute=1)
    logging.info(f"Sleeping for {sleep_time/3600:.2f} seconds until next run.")
    time.sleep(sleep_time)


def main():
    log_handler = TimedRotatingFileHandler("logs/p25daemon.log", when="midnight", interval=1, backupCount=7)
    log_handler.suffix = "%m.%d.%Y"
    logging.basicConfig(level=logging.INFO, 
                        handlers=[log_handler, logging.StreamHandler()],
                        format='%(asctime)s - %(levelname)s - %(message)s'
                        )
    sleep_until_next_run()
    while True:
        try:
            model = whisper.load_model(config.WHISPER_MODEL, device=config.WHISPER_DEVICE, in_memory=True)
            move_and_transcribe(model)
        except Exception as e:
            logging.error(f"Error in move_and_transcribe: {e}")
        del model
        gc.collect()
        torch.cuda.empty_cache()
        sleep_until_next_run()
        

if __name__ == "__main__":
    main()