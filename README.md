# Doctor-AI Help GUI

![Doctor-AI Help GUI](code/img/doctor-ai-help.png)

## Overview

**Doctor-AI Help GUI** is an interactive tool designed to assist doctors in evaluating and managing transcriptions of clinical audio recordings. The application offers both **live audio transcription** and **file-based transcription**, with support for recording, playback, editing, and saving transcripts.

Built with an intuitive interface, the GUI integrates the **Vosk speech recognition model**, enabling offline transcription workflows tailored for medical professionals.

---

## Key Features

### 🔴 Live Transcription
- **Record Audio**: Start/stop recording with a single button.
- **Edit Transcription**: Modify live transcription output before saving.
- **Save Transcription**: Export transcribed text to a `.txt` file.

### 📁 Local File Transcription
- **Select Audio File**: Choose existing audio files for transcription.
- **Playback Support**: Play the selected audio before or after transcription.
- **Edit Transcription**: Make adjustments to the transcribed output.
- **Save File Transcription**: Export each transcription to its own `.txt` file.

---

## 🗂 Project Structure

```
├── GUI/
│   ├── GUI_Controller.py       # Main logic and UI controls
│   ├── GUI_Transcriber.py      # Vosk transcription backend
│   ├── Audio_recorder.py       # Audio recording module
│   └── Recording_Popup.py      # Popup UI for recording
│
├── img/
│   ├── background.png
│   ├── doctor-ai-help.png
│   └── exit.png
│
├── mainGUI.py                  # Main entry point for the GUI
├── requirements.txt            # Required Python packages
└── README.md                   # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://git-ce.rwth-aachen.de/teamdb/speech-to-text.git
cd speech-to-text
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the Vosk Model

- Visit [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
- Download the language model that fits your needs.
- Update the model path in `GUI_Controller.py` accordingly.

### 4. Run the GUI

```bash
python mainGUI.py
```

---

## Vosk Inference & Evaluation

You can evaluate the performance of the Vosk model using Word Error Rate (WER) on your dataset.

### Steps:

1. **Prepare Dataset**
   - Organize your dataset in a folder with audio files.

2. **Edit Inference Script**
   - Modify `main_testing_vosk.py` to point to your audio directory.

3. **Run Inference**
   ```bash
   python main_testing_vosk.py
   ```

4. **Output**
   - The script will display the **average WER** for your dataset.

---

## Contributions

Contributions are welcome!  
Feel free to fork the repository, work on improvements or features, and submit a pull request.

---

## 📄 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for more details.
