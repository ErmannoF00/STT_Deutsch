import os
import wave
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
import sounddevice as sd

class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.recording = False
        self.audio_file = 'temp_audio.wav'
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_waveform)

    def init_ui(self):
        self.setWindowTitle("Audio Recorder")
        self.setGeometry(400, 400, 400, 200)
        self.setStyleSheet("background-color: white;")

        self.recording_label = QLabel('Recording audio...', self)
        self.recording_label.setGeometry(50, 50, 200, 30)

        self.stop_button = QPushButton('Stop Recording', self)
        self.stop_button.setGeometry(50, 100, 120, 40)
        self.stop_button.clicked.connect(self.stop_recording)

    def start_recording(self):
        self.recording = True
        self.timer.start(50)  # Update waveform every 50ms
        self.recording_label.setText('Recording audio...')

        duration = 10  # Record for 10 seconds (example)
        fs = 16000  # Sample rate
        self.recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        with wave.open(self.audio_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(self.recording.tobytes())

        self.recording_label.setText('Audio recorded.')

    def stop_recording(self):
        self.timer.stop()
        self.recording_label.setText('Audio recording stopped.')

    def update_waveform(self):
        # Placeholder for updating waveform visualization
        pass
