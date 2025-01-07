import os
import json
import vosk
import wave
from jiwer import wer  # Library for Word Error Rate calculation
from silero import silero_te  # Library for text enhancement
from torchmetrics.text import CharErrorRate  # Torch library for Character Error Rate calculation


class TranscriptionEvaluator:
    """
    Class for transcribing audio files using Vosk, evaluating the transcriptions against ground truth,
    and saving the results to a text file.
    """

    def __init__(self, audio_dir, metadata_dir, output_txt):
        """
        Initializes the TranscriptionEvaluator.

        Args:
        - audio_dir (str): Directory containing audio files to transcribe.
        - metadata_dir (str): Directory containing metadata (metadata.csv) with ground truth transcriptions.
        - output_txt (str): Output text file to save the results of the evaluation.
        """
        self.audio_dir = audio_dir
        self.metadata_dir = metadata_dir
        self.output_txt = output_txt
        self.transcription = None
        self.ground_truth_transcription = None
        self.char_to_index = {}  # Dictionary to map characters to indices

    def prepare_char_to_index(self):
        """
        Prepares a character-to-index mapping based on unique characters found in the metadata transcriptions.
        """
        metadata_file = os.path.join(self.metadata_dir, 'metadata.csv')
        with open(metadata_file, mode='r', encoding='utf-8') as file:
            unique_chars = set()
            for row in file:
                _, transcription = row.strip().split('|')
                unique_chars.update(set(transcription))

            # Assign an index to each unique character
            for i, char in enumerate(sorted(unique_chars)):
                self.char_to_index[char] = i

    def transcribe_and_evaluate(self, vosk_model, dataset):
        """
        Transcribes audio files using Vosk, evaluates each transcription against ground truth using WER and CER,
        and saves results to the output_txt file.

        Args:
        - vosk_model: Vosk model for speech recognition.
        - dataset: Dataset containing preprocessed data for transcription.

        Returns:
        - results (list): List of tuples (filename, WER score, CER score) for each transcribed audio file.
        """
        results = []

        with open(self.output_txt, mode='w', encoding='utf-8') as file:
            for spectrograms, filenames in dataset:
                for i in range(len(spectrograms)):
                    audio_file = os.path.join(self.audio_dir, filenames + '.wav')

                    # Transcribe audio using Vosk
                    try:
                        self.transcription = self.post_processing(self.transcribe_audio_vosk(audio_file, vosk_model))
                    except Exception as e:
                        print(f"Error transcribing {audio_file}: {e}")
                        self.transcription = ""

                    # Evaluate transcription
                    self.ground_truth_transcription = self.get_ground_truth_transcription(filenames)
                    wer_score = wer(self.ground_truth_transcription, self.transcription)
                    cer_score = self.compute_cer()

                    # Save transcription to file
                    file.write(f"{filenames}: '{self.transcription}' | '{self.ground_truth_transcription}'. "
                               f"WER = {wer_score}\n")

                    results.append((filenames, wer_score, cer_score))

        return results

    def transcribe_audio_vosk(self, audio_file, vosk_model):
        """
        Transcribes an audio file using Vosk.

        Args:
        - audio_file (str): Path to the audio file to transcribe.
        - vosk_model: Vosk model for speech recognition.

        Returns:
        - transcription (str): Transcribed text from the audio file.
        """
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

    def get_ground_truth_transcription(self, filename):
        """
        Retrieves the ground truth transcription for a given filename from metadata.

        Args:
        - filename (str): Filename of the audio file.

        Returns:
        - transcription (str): Ground truth transcription.
        """
        metadata_file = os.path.join(self.metadata_dir, 'metadata.csv')
        with open(metadata_file, mode='r', encoding='utf-8') as file:
            for row in file:
                file_name, transcription = row.strip().split('|')
                if file_name == filename:
                    if not transcription:  # Check if the transcription is empty
                        return "<EMPTY_TRANSCRIPTION>"  # Return a default value for empty transcriptions
                    return transcription
        return "<TRANSCRIPTION_NOT_FOUND>"

    def compute_cer(self):
        """
        Computes the Character Error Rate (CER) between ground truth and transcribed text.

        Returns:
        - cer_score (float): Character Error Rate (CER) score.
        """
        cer = CharErrorRate()
        cer.update(self.ground_truth_transcription, self.transcription)
        return cer.compute().item()

    def post_processing(self, text):
        """
        Applies post-processing to the transcribed text using functions from the Silero library.

        Args:
        - text (str): Transcribed text.

        Returns:
        - processed_text (str): Processed text.
        """
        _, _, _, _, apply_te_func = silero_te()
        return apply_te_func(text=text, lan='de')
