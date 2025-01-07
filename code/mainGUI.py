import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTextEdit,
                             QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer
# ---------------------------------------------------------------------------------------------------------------------
from GUI.GUI_Controller import GUI_Controller  # Assuming GUI_Controller is implemented separately


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.controller = GUI_Controller(self)
        self.init_connections()

    def init_ui(self):
        self.setWindowTitle("Speech Transcription App")
        self.setGeometry(200, 200, 1200, 800)

        # Set application-wide styles
        self.setStyleSheet("""
            QMainWindow {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, fx:0.5, fy:0.5,
                                            stop:0 #333333, stop:1 #111111); /* Dark grey radial gradient */
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3); /* Semi-transparent white */
                border: 2px solid rgba(255, 255, 255, 0.5); /* Semi-transparent white border */
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.4); /* Slightly more opaque on hover */
            }
            QLabel#mainTitle {
                color: rgba(30, 144, 255, 1); /* Electric blue */
                font-size: 30px;
                font-family: Arial, sans-serif;
                font-weight: bold;
            }
            QLabel#namesLabel {
                color: rgba(30, 144, 255, 1); /* Electric blue */
                font-size: 18px;
                font-family: Arial, sans-serif;
            }
            QLabel#standardLabel {
                color: white;
                font-size: 16px;
                font-family: Arial, serif;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Main title
        self.main_title = QLabel('DOCTOR-AI HELP', self)
        self.main_title.setObjectName('mainTitle')
        self.main_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.main_title)

        # Descriptive image
        self.descriptive_image = QLabel(self)
        pixmap = QPixmap(r'img/background.png')  # Replace with your image path
        pixmap = pixmap.scaled(500, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Resize the image
        self.descriptive_image.setPixmap(pixmap)
        self.descriptive_image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.descriptive_image)

        # Live Transcription section
        live_transcription_layout = QVBoxLayout()
        live_transcription_title = QLabel('Live Transcription:', self)
        live_transcription_title.setObjectName('standardLabel')
        live_transcription_layout.addWidget(live_transcription_title)

        self.live_transcription_edit = QTextEdit(self)
        self.live_transcription_edit.setReadOnly(True)
        live_transcription_layout.addWidget(self.live_transcription_edit)

        main_layout.addLayout(live_transcription_layout)

        # Buttons for live transcription
        live_buttons_layout = QHBoxLayout()
        self.record_audio_button = QPushButton('Record Audio', self)
        live_buttons_layout.addWidget(self.record_audio_button)

        self.save_live_transcription_button = QPushButton('Save Live Transcription', self)
        self.save_live_transcription_button.setEnabled(False)
        live_buttons_layout.addWidget(self.save_live_transcription_button)

        self.edit_live_transcription_button = QPushButton('Edit Transcription', self)
        self.edit_live_transcription_button.setEnabled(False)
        live_buttons_layout.addWidget(self.edit_live_transcription_button)

        main_layout.addLayout(live_buttons_layout)

        # Local Transcription section
        local_transcription_layout = QVBoxLayout()
        local_transcription_title = QLabel('Local Transcription:', self)
        local_transcription_title.setObjectName('standardLabel')
        local_transcription_layout.addWidget(local_transcription_title)

        self.transcription_list = QListWidget(self)
        local_transcription_layout.addWidget(self.transcription_list)

        main_layout.addLayout(local_transcription_layout)

        # Buttons for local transcription
        local_buttons_layout = QHBoxLayout()
        self.open_file_button = QPushButton('Select File', self)
        local_buttons_layout.addWidget(self.open_file_button)

        self.play_files_button = QPushButton('Play Files', self)
        self.play_files_button.setEnabled(False)
        local_buttons_layout.addWidget(self.play_files_button)

        self.save_file_transcription_button = QPushButton('Save File Transcription', self)
        self.save_file_transcription_button.setEnabled(False)
        local_buttons_layout.addWidget(self.save_file_transcription_button)

        self.edit_transcription_button = QPushButton('Edit Transcription', self)
        self.edit_transcription_button.setEnabled(False)
        local_buttons_layout.addWidget(self.edit_transcription_button)

        main_layout.addLayout(local_buttons_layout)

        # Error message label
        self.error_label = QLabel('', self)
        self.error_label.setStyleSheet("color: red; font-weight: bold;")
        main_layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

        # Exit button
        exit_action = QAction(QIcon(r'img/exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exit_action)

        # Logo at the bottom-right corner with names
        bottom_widget = QWidget(self)
        bottom_layout = QHBoxLayout(bottom_widget)

        names_label = QLabel('Katharina & Ermanno', self)
        names_label.setObjectName('namesLabel')
        names_label.setAlignment(Qt.AlignLeft)
        bottom_layout.addWidget(names_label)

        # Load and scale the logo
        pixmap = QPixmap(r'img/th.jpeg')
        pixmap = pixmap.scaledToWidth(150)
        logo_label = QLabel(self)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignRight)
        bottom_layout.addWidget(logo_label)

        # Set the layout for the bottom widget
        bottom_widget.setLayout(bottom_layout)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()
        main_layout.addWidget(bottom_widget, alignment=Qt.AlignRight)

        # Initialize QMediaPlayer for playing audio
        self.media_player = QMediaPlayer(self)
        self.media_player.setVolume(50)

    def init_connections(self):
        # Connect UI buttons to controller methods
        self.record_audio_button.clicked.connect(self.controller.toggle_recording)
        self.save_live_transcription_button.clicked.connect(self.controller.save_live_transcription)
        self.edit_live_transcription_button.clicked.connect(self.controller.correct_transcription)
        self.open_file_button.clicked.connect(self.controller.open_file)
        self.play_files_button.clicked.connect(self.controller.play_selected_files)
        self.save_file_transcription_button.clicked.connect(self.controller.save_file_transcription)
        self.edit_transcription_button.clicked.connect(self.controller.correct_transcription)
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Main application entry point
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
