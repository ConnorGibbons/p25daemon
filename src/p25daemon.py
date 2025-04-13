import os
import datetime
import logging
import whisper
from src import config
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
    if "segments" in result:
        transcript = "\n".join([segment["text"].strip() for segment in result["segments"]])
    else:
        transcript = result.get("text", "")
    return transcript

def move_and_transcribe(model): 
    audio_path = move_current_DSDPlus_recording()
    if not audio_path:
        logging.error("Failed to move current DSDPlus recording, can't transcribe.")
        return
    transcription = transcribe_audio_file(audio_path, model)
    transcription_path = config.TRANSCRIPT_ARCHIVE_PATH
    if transcription:
        output_file_name = datetime.date.today().strftime(config.TRANSCRIPT_FILENAME_FORMAT)
        dest = os.path.join(transcription_path, output_file_name)
        if not make_file_with_contents(dest, transcription):
            logging.error("Failed to write transcription to file.")
    else:
        logging.error("Transcription failed or returned no text.")
    logging.info(f"Successfully transcribed file: {audio_path} as {dest}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    log_filename = datetime.date.today().strftime("logs/%Y-%m-%d.log")
    logging.basicConfig(level=logging.INFO, 
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()]
                        )
    model = whisper.load_model("turbo", device="cuda", in_memory=True)
    move_and_transcribe(model)
