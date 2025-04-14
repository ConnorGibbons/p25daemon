import os
import datetime
import logging
import config
from src.utils import move_file, truncate_file, make_file_with_contents, log_error

def move_current_DSDPlus_recording():
    today = datetime.date.today()
    output_file_name = today.strftime(config.AUDIO_FILENAME_FORMAT)
    src = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.wav")
    dest = os.path.join(config.AUDIO_ARCHIVE_PATH, output_file_name)
    result = move_file(src, dest)

    if result[0]:
        truncate_result = truncate_file(src)
        if not truncate_result[0]:
            log_error("Error truncating DSDPlus recording", truncate_result)
        return dest
    
    log_error("Error moving DSDPlus recording", result)
    return None

def transcribe_audio_file(audio_path, model):
    prompt = "Transcribe the following audio file containing Marlborough, MA police radio traffic."
    result = model.transcribe(audio_path, initial_prompt = prompt, language="en")
    print(result.keys())
    if "segments" in result:
        transcript = "\n".join([segment["text"].strip() for segment in result["segments"]])
    else:
        transcript = result.get("text", "")
    print(len(transcript))
    return transcript

def move_and_transcribe(model):
    audio_path = move_current_DSDPlus_recording()
    
    if not audio_path:
        logging.info("No new DSDPlus recording found. Skipping transcription.")
        return

    try:
        transcription = transcribe_audio_file(audio_path, model)
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return
    if not transcription:
        logging.warning("Transcription completed but returned no text.")
        return

    output_file_name = datetime.date.today().strftime(config.TRANSCRIPT_FILENAME_FORMAT)
    dest = os.path.join(config.TRANSCRIPT_ARCHIVE_PATH, output_file_name)

    make_file_result = make_file_with_contents(dest, transcription)
    if not make_file_result[0]:
        log_error("Error creating transcription file", make_file_result)
        return

    logging.info(f"Successfully transcribed {os.path.abspath(audio_path)} to {os.path.abspath(dest)}")

