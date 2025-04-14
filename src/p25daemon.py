import os
import datetime
import logging
import config
from src.utils import truncate_file, make_file_with_contents, log_error, copy_file

def move_current_DSDPlus_recording():
    """
    Moves the current DSDPlus recording file to the archive directory and truncates the source file.
    
    Returns:
        str or None: The destination path of the moved file if successful, None if the move failed.
    """
    today = datetime.date.today()
    output_file_name = today.strftime(config.AUDIO_FILENAME_FORMAT)
    src = os.path.join(config.DSDPLUS_INSTALL_PATH, "DSDPlus.wav")
    dest = os.path.join(config.AUDIO_ARCHIVE_PATH, output_file_name)
    result = copy_file(src, dest)

    if result[0]:
        if config.TRUNCATE_DSDPLUS_FILE:
            truncate_result = truncate_file(src)
            if not truncate_result[0]:
                log_error("Error truncating DSDPlus recording", truncate_result)
        else:
            logging.warning("Skipped truncating DSDPlus recording! Check config if you're not testing.")
        return dest
    
    log_error("Error moving DSDPlus recording", result)
    return None

def transcribe_audio_file(audio_path, model):
    """
    Transcribes an audio file using the provided model.
    
    Args:
        audio_path (str): Path to the audio file to transcribe.
        model: The transcription model to use.
    
    Returns:
        str: The transcribed text from the audio file.
    """
    prompt = config.WHISPER_PROMPT
    result = model.transcribe(audio_path, initial_prompt = prompt, language="en")
    if "segments" in result:
        transcript = "\n".join([segment["text"].strip() for segment in result["segments"]])
    else:
        transcript = result.get("text", "")
    return transcript

def move_and_transcribe(model):
    """
    Moves the current DSDPlus recording and transcribes it.
    
    This function:
    1. Moves the current DSDPlus recording to the archive directory
    2. Transcribes the audio file using the provided model
    3. Saves the transcription to a file in the transcript archive directory
    
    Args:
        model: The transcription model to use. (turbo, base, small, medium, large)
    """
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

