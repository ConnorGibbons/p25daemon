# Configuration file

DSDPLUS_INSTALL_PATH = r""
AUDIO_ARCHIVE_PATH = r""
TRANSCRIPT_ARCHIVE_PATH = r""
AUDIO_FILENAME_FORMAT = "%m.%d.%Y.wav"
TRANSCRIPT_FILENAME_FORMAT = "%m.%d.%Y.txt"
RUN_TIME_HOUR = 23 # Be careful with this -- it should be the **same day** as the recorded audio, else the date will be off by a day.
RUN_TIME_MINUTE = 50
WHISPER_MODEL = "base" # Options are: "tiny", "base", "small", "medium", "large", "turbo"
WHISPER_DEVICE = "cpu" # Options are: "cpu", "cuda" (NVIDIA GPU), "mps" (Apple Silicon)
WHISPER_PROMPT = "Transcribe the following audio file"
TRUNCATE_DSDPLUS_FILE = True # Adjust this if testing the script, so you don't delete your DSDPlus recording.
RUN_IMMEDIATELY = False # Adjust this if testing the script, so you don't have to wait until the next run time.
DSDPLUS_LAUNCH_ARGS = "" # Add your launch arguments here -- make sure to specify your audio input device! 
FORCE_DSDPLUS_RESTART = False # Also, just for testing. If True, will kill and relaunch DSDPlus if it is already running.