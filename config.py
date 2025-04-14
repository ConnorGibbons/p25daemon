# Configuration file

DSDPLUS_INSTALL_PATH = r"C:\Users\conno\Documents\DSDPlus1p101"
AUDIO_ARCHIVE_PATH = r"\\192.168.1.187\SharedFolder\Storage\DSD\Recordings"
TRANSCRIPT_ARCHIVE_PATH = r"\\192.168.1.187\SharedFolder\Storage\DSD\Transcriptions"
AUDIO_FILENAME_FORMAT = "%m.%d.%Y.wav"
TRANSCRIPT_FILENAME_FORMAT = "%m.%d.%Y.txt"
RUN_TIME_HOUR = 23 # Be careful with this -- it should be the **same day** as the recorded audio, else the date will be off by a day.
RUN_TIME_MINUTE = 50
WHISPER_MODEL = "turbo"
WHISPER_DEVICE = "cuda" # Options are: "cpu", "cuda" (NVIDIA GPU), "mps" (Apple Silicon)
WHISPER_PROMPT = "Transcribe the following audio file containing Marlborough, MA police radio traffic."
TRUNCATE_DSDPLUS_FILE = True # Adjust this if testing the script, so you don't delete your DSDPlus recording.
RUN_IMMEDIATELY = True # Adjust this if testing the script, so you don't have to wait until the next run time.
DSDPLUS_LAUNCH_ARGS = "-i4"
FORCE_DSDPLUS_RESTART = False # Also, just for testing. If True, will kill and relaunch DSDPlus if it is already running.