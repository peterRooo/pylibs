import whisper
import logging 

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    logging.info(result["text"])

