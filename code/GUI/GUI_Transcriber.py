import os
import json
import vosk
import wave
from silero import silero_te
from PyQt5.QtCore import QThread, pyqtSignal


class TranscriptionWorker(QThread):
    result_ready = pyqtSignal(list)  # Define the signal for sending results

    def __init__(self, audio_files, vosk_model):
        super().__init__()
        self.audio_files = audio_files
        self.vosk_model = vosk_model
        self.results = []

    def run(self):
        try:
            for audio_file in self.audio_files:
                result = self.post_processing(self.transcribe_audio_vosk(audio_file, self.vosk_model))
                self.results.append((os.path.basename(audio_file), result))
        except Exception as e:
            self.results.append(("Error", f"Error: {str(e)}"))

        self.result_ready.emit(self.results)  # Emit the results when done

    def transcribe_audio_vosk(self, audio_file, vosk_model):
        wf = wave.open(audio_file, 'rb')  # Open the audio file using wave module
        sample_rate = wf.getframerate()  # Get the sample rate of the audio file
        chunk_size = int(sample_rate * 0.1)  # Read 100 ms of audio data at a time
        rec = vosk.KaldiRecognizer(vosk_model, sample_rate)
        results = []

        while True:
            data = wf.readframes(chunk_size)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                results.append(json.loads(result))

        result = rec.FinalResult()
        if result:
            results.append(json.loads(result))

        wf.close()  # Close the audio file after processing
        return ' '.join([res['text'] for res in results])

    def post_processing(self, text):
        # Applying siler model for capital letters
        _, _, _, _, apply_te_func = silero_te()
        return apply_te_func(text=text, lan='de')

    def get_results(self):
        return self.results
