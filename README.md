<h1 align="center"> Doctor-AI Help GUI </h1>

![Doctor-AI Help GUI](code/img/doctor-ai-help.png)

### Description

The **Doctor-AI Help GUI** is a tool designed to assist doctors in evaluating transcriptions of audio recordings. This graphical user interface allows users to view, modify, play, and save transcriptions. It supports both local file transcriptions and live transcription from recorded audio. The GUI integrates features for recording audio, editing transcriptions, and saving them in appropriate directories.

### Features

#### 🟢 Live Transcription:
- **Record Audio**: Click "Record Audio" to start recording. Click again to stop.
- **Save Live Transcription**: Save the live transcription to a text file.
- **Edit Transcription**: Modify the live transcription manually.

#### 📁 Local Transcription:
- **Select File**: Choose audio files from your system.
- **Play Files**: Play selected audio files.
- **Save File Transcription**: Save each transcription to a separate text file.
- **Edit Transcription**: Edit transcriptions of selected files.

### Folder Structure

```
.
├── GUI/
│   ├── GUI_Controller.py      
│   ├── GUI_Transcriber.py         
│   ├── Audio_recorder.py        
│   ├── Recording_Popup.py      
├── img/                       
│   ├── background.png      
│   ├── doctor-ai-help.png    
│   └── exit.png             
├── mainGUI.py                    
├── requirements.txt       
└── README.md                
```

### Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ErmannoF00/STT_Deutsch.git
    cd STT_Deutsch
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download Required Models**
    - Download the Vosk model for your language: [Vosk Models](https://alphacephei.com/vosk/models)
    - Update the model path inside `GUI_Controller.py`

4. **Run the Application**
    ```bash
    python mainGUI.py
    ```

### VOSK INFERENCE

To compute the average Word Error Rate (WER) using the Vosk model:

1. **Prepare Audio Folder**
   - Place WAV files in a directory for testing.

2. **Run Inference**
   - Modify `main_testing_vosk.py` to use your dataset directory.
   - Execute the script:
     ```bash
     python main_testing_vosk.py
     ```

3. **View Results**
   - The script will output the average WER across the audio files.

### Contributions

Contributions are welcome! Fork the repo, make improvements, and open a pull request.

### License

This project is licensed under the [MIT License](LICENSE).

