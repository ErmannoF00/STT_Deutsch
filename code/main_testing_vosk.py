import os
import numpy as np
import vosk
from Transcriber import TranscriptionEvaluator
from PreProcess.Preprocessing import Preprocessor
from dir.DatasetLoader import SpeechDataset


def main():
    # Define the base directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Define the directories relative to the base directory
    audio_dir = os.path.join(base_dir, 'Audio/shit/Audio')
    metadata_dir = os.path.join(base_dir, 'Audio/shit')

    # Initialize Vosk model
    vosk_model = vosk.Model(os.path.join(base_dir, "Model/vosk-model-de-0.21"))

    try:
        # Initialize preprocessor
        preprocessor = Preprocessor(audio_dir)
        preprocessed_data = preprocessor.preprocess_directory()

        # Initialize transcription evaluator
        evaluator = TranscriptionEvaluator(audio_dir, metadata_dir, 'transcriptions.txt')

        # Create dataset from preprocessed data
        dataset = SpeechDataset(preprocessed_data, preprocessor.filenames)

        # Evaluate transcriptions
        results = evaluator.transcribe_and_evaluate(vosk_model, dataset)
        wer_results = [result[1] for result in results]

        # Calculate average WER
        avg_wer = np.mean(wer_results)
        print("Average WER: ", avg_wer)

    except Exception as e:
        print(f"Error in main process: {e}")


if __name__ == "__main__":
    main()
