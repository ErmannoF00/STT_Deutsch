from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFont


class RecordingPopup(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Recording Audio')
        self.setGeometry(400, 400, 300, 150)

        layout = QVBoxLayout(self)

        self.recording_label = QLabel('00:00:00', self)
        self.recording_label.setAlignment(Qt.AlignCenter)
        self.recording_label.setFont(QFont('Arial', 15))
        layout.addWidget(self.recording_label)

        self.start_recording_button = QPushButton('Start Recording', self)
        self.start_recording_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_recording_button)

        self.stop_recording_button = QPushButton('Stop Recording', self)
        self.stop_recording_button.clicked.connect(self.stop_recording)
        self.stop_recording_button.setEnabled(False)
        layout.addWidget(self.stop_recording_button)

        self.save_button = QPushButton('Save and Close', self)
        self.save_button.clicked.connect(self.save_and_close)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.recording_time = QTime(0, 0)
        self.timer_running = False

    def start_recording(self):
        # Start recording and timer
        self.controller.start_recording()
        self.timer.start(1000)
        self.timer_running = True
        self.start_recording_button.setEnabled(False)
        self.stop_recording_button.setEnabled(True)
        self.save_button.setEnabled(False)

    def stop_recording(self):
        # Stop recording and timer
        self.controller.stop_recording()
        self.timer.stop()
        self.timer_running = False
        self.start_recording_button.setEnabled(True)
        self.stop_recording_button.setEnabled(False)
        self.save_button.setEnabled(True)

    def save_and_close(self):
        # Save recording and close the dialog
        self.controller.save_and_close_recording()
        self.close()

    def update_timer(self):
        # Update the timer label with elapsed time
        self.recording_time = self.recording_time.addSecs(1)
        self.recording_label.setText(self.recording_time.toString('hh:mm:ss'))

    def closeEvent(self, event):
        # Prevent closing the dialog if recording is still ongoing
        if self.timer_running:
            event.ignore()
        else:
            event.accept()
