import os
import vosk
import spacy

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTextEdit,
                             QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem,
                             QAction, QFileDialog, QLineEdit)
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QTextCharFormat, QTextCursor, QColor, QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
# ----------------------------------------------------------------------------------------------------------------------
from GUI.GUI_Transcriber import TranscriptionWorker
from GUI.Audio_recorder import AudioRecorder
from GUI.Recording_Popup import RecordingPopup


class GUI_Controller(QObject):
    transcriptionUpdated = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.audio_recorder = AudioRecorder()
        self.recording_popup = RecordingPopup(self)
        self.recording = False
        self.selected_files = []
        self.editing_mode = False

        # Connect signal to slot
        self.transcriptionUpdated.connect(self.update_live_transcription)

        # Initialize QMediaPlayer
        self.main_window.media_player = QMediaPlayer(self.main_window)
        self.main_window.media_player.setVolume(50)

        # Disable buttons initially
        self.disable_buttons()

        # Preload transcription model
        self.load_transcription_model()

        # Load spaCy model for named entity recognition (NER)
        self.nlp = spacy.load("de_core_news_sm")  # Adjust to the appropriate language model

    def load_transcription_model(self):
        try:
            # model_path = r'path/to/the/model'
            model_path = r'C:\Users\ermix\OneDrive\Desktop\RWTH\I_SEM\ML-PRO\speech-to-text\Model\vosk-model-de-0.21'
            self.vosk_model = vosk.Model(model_path)
        except Exception as e:
            self.main_window.error_label.setText(f'Error initializing Vosk model: {e}')

    def disable_buttons(self):
        # Disable all relevant buttons
        self.main_window.save_live_transcription_button.setEnabled(False)
        self.main_window.save_file_transcription_button.setEnabled(False)
        self.main_window.play_files_button.setEnabled(False)
        self.main_window.edit_transcription_button.setEnabled(False)

    def enable_buttons(self):
        # Enable buttons based on current state
        self.main_window.save_live_transcription_button.setEnabled(bool(self.main_window.live_transcription_edit.toPlainText()))
        self.main_window.play_files_button.setEnabled(bool(self.selected_files))
        self.main_window.save_file_transcription_button.setEnabled(bool(self.main_window.transcription_list.count() > 0))
        self.main_window.edit_transcription_button.setEnabled(bool(self.main_window.transcription_list.count() > 0
                                                                   and not self.editing_mode))

    def open_file(self):
        # Open file dialog to select audio files
        try:
            file_paths, _ = QFileDialog.getOpenFileNames(self.main_window, 'Select Files', '',
                                                         'Audio Files (*.wav *.mp3)')
            if file_paths:
                self.selected_files = file_paths
                self.transcribe_audio_files(file_paths)
                self.main_window.error_label.clear()
                self.main_window.open_file_button.setEnabled(False)
                self.enable_buttons()
            else:
                print("No files selected")
        except Exception as e:
            self.main_window.error_label.setText(f"Error selecting files: {e}")

    def transcribe_audio_files(self, audio_files):
        # Transcribe selected audio files
        try:
            self.main_window.transcription_list.clear()
            self.main_window.error_label.setText(f'Transcribing {len(audio_files)} files...')
            self.main_window.error_label.setStyleSheet("color: white;")
            self.main_window.repaint()

            transcription_worker = TranscriptionWorker(audio_files, self.vosk_model)
            transcription_worker.run()

            results = transcription_worker.get_results()
            self.handle_file_transcription_result(results)
        except Exception as e:
            self.main_window.error_label.setText(f"Error transcribing audio files: {e}")

    def handle_file_transcription_result(self, results):
        # Handle transcription results and update UI
        self.main_window.transcription_list.clear()
        for index, (filename, transcription) in enumerate(results, start=1):
            doc = self.nlp(transcription)
            highlighted_transcription = self.highlight_entities(doc)

            # Create QListWidgetItem with formatted text
            item_text = f"File {index}: {filename}\n{highlighted_transcription}"
            item = QListWidgetItem(item_text)
            item.setFont(QFont("Arial", 10))
            self.main_window.transcription_list.addItem(item)

        self.main_window.transcription_list.scrollToBottom()
        self.main_window.error_label.setText('File transcription complete.')
        self.enable_buttons()

    def highlight_entities(self, doc):
        # Highlight entities in the transcribed text
        formatted_text = ""
        for token in doc:
            if token.ent_type_:  # Check if the token has an entity type
                formatted_text += f"[!|{token.text}|!]{token.whitespace_}"
            else:
                formatted_text += f"{token.text}{token.whitespace_}"
        return formatted_text.strip()

    def play_selected_files(self):
        # Play selected audio files
        try:
            for audio_file in self.selected_files:
                media_content = QMediaContent(QUrl.fromLocalFile(audio_file))
                self.main_window.media_player.setMedia(media_content)
                self.main_window.media_player.play()

            self.main_window.play_files_button.setEnabled(False)
        except Exception as e:
            self.main_window.error_label.setText(f"Error playing audio files: {e}")

    def toggle_recording(self):
        # Toggle audio recording
        if not self.recording:
            self.recording_popup.show()
            self.recording_popup.start_recording()
        else:
            self.recording_popup.stop_recording()

    def start_recording(self):
        # Start recording audio
        self.recording = True
        self.main_window.record_audio_button.setEnabled(False)
        self.main_window.error_label.setText('Recording audio...')
        self.main_window.error_label.setStyleSheet("color: black; font-weight: normal;")
        self.enable_buttons()

    def stop_recording(self):
        # Stop recording audio
        self.recording = False
        self.main_window.record_audio_button.setEnabled(True)

    def save_live_transcription(self):
        # Save live transcription to a file
        transcription = self.main_window.live_transcription_edit.toPlainText()
        if transcription:
            with open('live_transcription.txt', mode='w', encoding='utf-8') as file:
                file.write(transcription)

            self.main_window.live_transcription_edit.clear()
            self.main_window.save_live_transcription_button.setEnabled(False)
            self.main_window.record_audio_button.setEnabled(True)
            self.main_window.play_files_button.setEnabled(False)
            self.main_window.error_label.setText('Live transcription saved.')

    def save_file_transcription(self):
        # Save file transcriptions to individual files
        items = self.main_window.transcription_list.count()
        if items > 0:
            processed_dir = 'PROCESSED_TRANSCRIPTION'
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)

            for i in range(items):
                item = self.main_window.transcription_list.item(i)
                text = item.text()

                colon_split = text.split(':')
                if len(colon_split) < 2:
                    continue

                transcription_part = colon_split[-1].strip()

                parts = transcription_part.split('.mp3')
                if len(parts) < 2:
                    parts = transcription_part.split('.wav')
                if len(parts) < 2:
                    continue

                file_name_part = parts[0]
                base_name_parts = file_name_part.split('_')

                base_name = None
                for part in base_name_parts:
                    if any(char.isdigit() for char in part):
                        break
                    if base_name is None:
                        base_name = part
                    else:
                        base_name += '_' + part

                if base_name is None:
                    with open('no_root_name.txt', mode='a', encoding='utf-8') as no_root_file:
                        no_root_file.write(file_name_part + '\n')
                    continue

                file_path = os.path.join(processed_dir, f"{base_name}.txt")

                with open(file_path, mode='a', encoding='utf-8') as file:
                    file.write(f"{transcription_part}\n")

            self.main_window.transcription_list.clear()
            self.main_window.save_file_transcription_button.setEnabled(False)
            self.main_window.open_file_button.setEnabled(True)
            self.main_window.play_files_button.setEnabled(False)
            self.main_window.edit_transcription_button.setEnabled(False)
            self.main_window.edit_transcription_button.setText('Finish Editing')
            self.main_window.error_label.setText('File transcriptions saved.')

    def correct_transcription(self):
        # Enable editing of selected transcription item
        selected_item = self.main_window.transcription_list.currentItem()
        if selected_item and not self.editing_mode:
            edit_line = QLineEdit(selected_item.text())
            self.main_window.transcription_list.setItemWidget(selected_item, edit_line)
            edit_line.returnPressed.connect(lambda: self.finish_editing(selected_item, edit_line))
            self.editing_mode = True
            self.update_edit_button()

    def finish_editing(self, item, line_edit):
        # Finish editing of transcription item
        new_text = line_edit.text()
        self.main_window.transcription_list.setItemWidget(item, None)
        item.setText(new_text)
        item.setFont(QFont("Arial", 10))
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable & ~Qt.ItemIsEditable)
        self.editing_mode = False
        self.update_edit_button()

    def update_edit_button(self):
        # Update editing button text and state
        if self.editing_mode:
            self.main_window.edit_transcription_button.setText('Finish Editing')
        else:
            self.main_window.edit_transcription_button.setText('Edit Transcription')
            self.main_window.edit_transcription_button.setEnabled(True)

        self.enable_buttons()

    def update_live_transcription(self, text):
        # Update live transcription text area
        self.main_window.live_transcription_edit.setPlainText(text)
        self.main_window.save_live_transcription_button.setEnabled(bool(text))


