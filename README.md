# P25Daemon

This python script is intended to be run in the background on a windows machine, allowing the user to receive automatic transcriptions of decoded DSDPlus audio.

It does the following, in order:
- Moves DSDPlus.wav to a directory of your choice; names it MM.DD.YY.wav
- Truncates DSDPlus.wav to 0 bytes (gives DSDPlus a blank slate) --- This step will restart DSDPlus if necessary to allow truncation.
- Transcribes the audio using OpenAI's Whisper model.
- Saves the transcription to directory of your choice, named MM.DD.YY.txt
- Sleeps until the next day, at a chosen time.

## Requirements
- DSDPlus (I have only tested this on the free version -- I do not know if it works with Fast Lane!)
- You'll need a python environment with torch & whisper.
- A CUDA-capable GPU is preferable, otherwise the transcription will be very slow.
- Model information & VRAM Requirements: [Whisper GitHub Repository](https://github.com/openai/whisper)
- Modify config.py to suit your setup.

## Notes
This script is **very** minimally tested so far. I cannot guarantee it'll work with your setup without some adaptation.
If you have any issues or questions, feel free to email me at connor@ccgibbons.com