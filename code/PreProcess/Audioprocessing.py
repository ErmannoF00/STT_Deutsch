import numpy as np
import librosa
import torch
import pyworld as pw
from scipy.signal import butter, lfilter

MAX_AUDIO_LENGTH = 44100 * 30  # 30 seconds


class AudioProcessor:
    def __init__(self):
        self.audio = None
        self.sr = None

    def preprocess_audio(self, audio_file):
        """
        Preprocesses audio data by loading, removing silence, applying low-pass filtering,
        and extracting mel-spectrogram features.

        Args:
        - audio_file (str): Path to the audio file.

        Returns:
        - torch.Tensor or None: Preprocessed mel-spectrogram features with channel dimension added, or None if error occurs.
        """
        try:
            self.audio, self.sr = librosa.load(audio_file, sr=None, dtype=np.float64)  # Load audio with 'float64' dtype
        except Exception as e:
            print(f"Error loading audio file {audio_file}: {e}")
            return None

        # Check for non-finite values in loaded audio
        if not np.isfinite(self.audio).all():
            print(f"Audio buffer is not finite everywhere in {audio_file}")
            return None

        # Apply silence removal
        try:
            self.audio = self.remove_silence(self.audio)
        except Exception as e:
            print(f"Error removing silence from {audio_file}: {e}")
            return None

        sampling_frequency = self.sr

        # Apply low-pass filtering
        try:
            self.audio = self.lpf(self.audio, sampling_frequency)
        except Exception as e:
            print(f"Error applying low-pass filter to {audio_file}: {e}")
            return None

        # Ensure audio length does not exceed maximum allowed
        if len(self.audio) > MAX_AUDIO_LENGTH:
            self.audio = self.audio[:MAX_AUDIO_LENGTH]
        else:
            self.audio = np.pad(self.audio, (0, max(0, MAX_AUDIO_LENGTH - len(self.audio))), 'constant')

        # Extract mel-spectrogram features
        try:
            mel_spectrogram = librosa.feature.melspectrogram(y=self.audio, sr=sampling_frequency, n_mels=80)
            mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
            return torch.tensor(mel_spectrogram_db).unsqueeze(0)  # Add channel dimension
        except Exception as e:
            print(f"Error extracting mel-spectrogram features from {audio_file}: {e}")
            return None

    def butter_lowpass(self, cutoff, fs, order=5):
        """
        Butterworth low-pass filter.

        Args:
        - cutoff (float): Cutoff frequency.
        - fs (float): Sampling frequency.
        - order (int): Filter order.

        Returns:
        - tuple: Numerator (b) and denominator (a) of the filter.
        """
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def lpf(self, data, fs):
        """
        Applies low-pass filtering to audio data.

        Args:
        - data (np.ndarray): Audio signal.
        - fs (float): Sampling frequency of the signal.

        Returns:
        - np.ndarray: Filtered audio signal.
        """
        nyquist = fs / 2
        cutoff = min(8000 / nyquist, 1)
        b, a = self.butter_lowpass(cutoff, fs)
        y = lfilter(b, a, data)
        return y

    def remove_silence(self, audio, top_db=20):
        """
        Removes silent intervals from the audio.

        Args:
        - audio (np.ndarray): Audio signal.
        - top_db (float): Threshold (in decibels) below reference to consider as silence.

        Returns:
        - np.ndarray: Audio signal with silence removed.
        """
        non_silent_intervals = librosa.effects.split(audio, top_db=top_db)
        non_silent_audio = np.concatenate([audio[start:end] for start, end in non_silent_intervals])
        return non_silent_audio

    def extract_pitch(self):
        """
        Extracts pitch (fundamental frequency) from the audio.

        Returns:
        - float: Mean pitch value.
        """
        f0, _ = pw.harvest(self.audio, self.sr)
        return np.mean(f0)

    def extract_intensity(self):
        """
        Extracts intensity (amplitude) from the audio.

        Returns:
        - float: Mean intensity value.
        """
        f0, sp, ap = pw.wav2world(self.audio.astype(np.float64), self.sr)
        return np.mean(ap)

    def extract_spectral_features(self):
        """
        Extracts spectral features from the audio.

        Returns:
        - np.ndarray: Mean spectral features.
        """
        f0, sp, ap = pw.wav2world(self.audio.astype(np.float64), self.sr)
        return np.mean(sp, axis=1)

    def time_stretch(self, rate):
        """
        Applies time stretching to the audio.

        Args:
        - rate (float): Stretching rate.

        Returns:
        - np.ndarray: Stretched audio signal.
        """
        y_stretch = librosa.effects.time_stretch(self.audio, rate)
        return y_stretch

    def pitch_shift(self, n_steps):
        """
        Shifts pitch of the audio.

        Args:
        - n_steps (float): Number of semitones to shift.

        Returns:
        - np.ndarray: Shifted audio signal.
        """
        y_shifted = librosa.effects.pitch_shift(self.audio, self.sr, n_steps)
        return y_shifted, self.sr

    def add_noise(self, noise_level):
        """
        Adds noise to the audio.

        Args:
        - noise_level (float): Amplitude of noise to add.

        Returns:
        - np.ndarray: Noisy audio signal.
        """
        noise = np.random.randn(len(self.audio))
        y_noisy = self.audio + noise_level * noise
        return y_noisy
