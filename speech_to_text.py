from groq import Groq

from dotenv import load_dotenv
import os


class SpeechToText:
    def __init__(self, language="fr"):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.model = "whisper-large-v3-turbo"
        self.language = language


    def transcribe(self, audio_file):
        transcription = self.groq_client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.getvalue()),
            model=self.model,
            language=self.language,
        )
        return transcription.text.strip()