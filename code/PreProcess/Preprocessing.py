import os
import random
from PreProcess.Audioprocessing import AudioProcessor


class Preprocessor:
    """
    Preprocessor class for processing audio files in a directory.

    Attributes:
        audio_dir (str): Directory containing audio files.
        num_files (int or None): Number of files to preprocess (default: None, preprocess all).
        audio_files (list): List of audio file paths.
        filenames (list): List of audio file names without extensions.
        audio_processor (AudioProcessor): Instance of AudioProcessor for audio preprocessing.
    """

    def __init__(self, audio_dir, num_files=None):
        """
        Initialize Preprocessor with audio directory and optional number of files.

        Args:
            audio_dir (str): Directory containing audio files.
            num_files (int or None): Number of files to preprocess (default: None, preprocess all).
        """
        self.audio_dir = audio_dir
        self.num_files = num_files
        self.audio_files = [os.path.join(self.audio_dir, f) for f in os.listdir(self.audio_dir) if f.endswith('.wav')]
        self.filenames = [os.path.splitext(os.path.basename(f))[0] for f in self.audio_files]
        self.audio_processor = AudioProcessor()

    def preprocess_directory(self):
        """
        Preprocess audio files in the directory.

        Returns:
            list: List of preprocessed data for each audio file.
        """
        if self.num_files is None:
            selected_files = self.audio_files
        else:
            selected_files = random.sample(self.audio_files, self.num_files)
        preprocessed_data = []

        for audio_file in selected_files:
            preprocessed_data.append(self.audio_processor.preprocess_audio(audio_file))

        return preprocessed_data
