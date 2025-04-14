import os
import datetime
import logging
import config
from multiprocessing import Queue, Process
from src.utils import truncate_file, make_file_with_contents, log_error, copy_file, kill_DSDPlus, launch_DSDPlus

def move_current_DSDPlus_recording(datetime_today = datetime.date.today()):
    """
    Moves the current DSDPlus recording file to the archive directory and truncates the source file.
    
    Returns:
        str or None: The destination path of the moved file if successful, None if the move failed.
    """
    output_file_name = datetime_today.strftime(config.AUDIO_FILENAME_FORMAT)
    src = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.wav")
    dest = os.path.join(config.AUDIO_ARCHIVE_PATH, output_file_name)
    result = copy_file(src, dest)

    if result[0]:
        if config.TRUNCATE_DSDPLUS_FILE:
            truncate_result = truncate_file(src)
            if not truncate_result[0] or config.FORCE_DSDPLUS_RESTART:
                log_error("Error truncating DSDPlus recording", truncate_result)
                logging.info("Attempting to kill DSDPlus, truncate, and relaunch.")
                kill_result = kill_DSDPlus()
                if not kill_result[0]:
                    log_error("Error killing DSDPlus process after truncation error", kill_result)
                    return None
                logging.info("Killed DSDPlus process, truncating file.")
                truncate_result = truncate_file(src)
                if not truncate_result[0]:
                    log_error("Error truncating DSDPlus recording after kill", truncate_result)
                    return None
                logging.info("Truncation successful, relaunching DSDPlus.")
                launch_result = launch_DSDPlus()
                if not launch_result[0]:
                    log_error("Error launching DSDPlus after truncation error", launch_result)
                    return None
            logging.info("Truncated DSDPlus recording successfully.")
        else:
            logging.warning("Skipped truncating DSDPlus recording! Check config if you're not testing.")
        return dest
    
    log_error("Error moving DSDPlus recording", result)
    return None    

def transcribe_audio_file_worker(audio_path, queue):
    import whisper
    model = whisper.load_model(config.WHISPER_MODEL, device = config.WHISPER_DEVICE)
    prompt = config.WHISPER_PROMPT
    try:
        result = model.transcribe(audio_path, initial_prompt = prompt, language="en")
        if "segments" in result:
            transcript = "\n".join([segment["text"].strip() for segment in result["segments"]])
        else:
            transcript = result.get("text", "")
        queue.put(transcript)
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        queue.put(None)


def move_and_transcribe(datetime_today = datetime.date.today()):
    """
    Moves the current DSDPlus recording and transcribes it.
    
    This function:
    1. Moves the current DSDPlus recording to the archive directory
    2. Transcribes the audio file using the provided model
    3. Saves the transcription to a file in the transcript archive directory
    
    Args:
        model: The transcription model to use. (turbo, base, small, medium, large)
        datetime_today (datetime): The date to use for file naming --> Important because this operation could take significant time, causing the filename to be wrong if ran late.
    """
    audio_path = move_current_DSDPlus_recording(datetime_today = datetime_today)
    if not audio_path:
        logging.info("No new DSDPlus recording found or an error occured truncating the recording. Skipping transcription.")
        return
    logging.info(f"Saved DSDPlus recording to {os.path.abspath(audio_path)}")

    queue = Queue()
    p = Process(target=transcribe_audio_file_worker, args=(audio_path, queue))
    p.start()
    p.join()

    transcription = queue.get()
    if not transcription:
        logging.error("Transcription failed or returned empty result.")
        return

    output_file_name = datetime_today.strftime(config.TRANSCRIPT_FILENAME_FORMAT)
    dest = os.path.join(config.TRANSCRIPT_ARCHIVE_PATH, output_file_name)

    make_file_result = make_file_with_contents(dest, transcription)
    if not make_file_result[0]:
        log_error("Error creating transcription file", make_file_result)
        return

    logging.info(f"Successfully transcribed {os.path.abspath(audio_path)} to {os.path.abspath(dest)}")

