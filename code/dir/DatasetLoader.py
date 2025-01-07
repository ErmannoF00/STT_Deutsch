from torch.utils.data import Dataset

class SpeechDataset(Dataset):
    def __init__(self, preprocessed_data, filenames):
        """
        Constructor for the SpeechDataset class.

        Args:
        - preprocessed_data (list): List of preprocessed data (e.g., tensors representing mel-spectrograms).
        - filenames (list): List of corresponding filenames (e.g., audio file names).

        This class is designed to work with PyTorch's Dataset class, allowing seamless integration with DataLoader.
        """
        self.preprocessed_data = preprocessed_data  # Store the preprocessed data
        self.filenames = filenames  # Store the corresponding filenames

    def __len__(self):
        """
        Returns the number of samples in the dataset.

        Returns:
        - int: Number of samples in the dataset.
        """
        return len(self.preprocessed_data)

    def __getitem__(self, idx):
        """
        Retrieves a sample from the dataset based on index.

        Args:
        - idx (int): Index of the sample to retrieve.

        Returns:
        - tuple: A tuple containing the preprocessed data and its corresponding filename.
        """
        return self.preprocessed_data[idx], self.filenames[idx]
