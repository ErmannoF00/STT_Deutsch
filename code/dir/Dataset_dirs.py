import os
import csv
import glob
import soundfile as sf

# Define input and output directories
input_dataset_dirs = glob.glob(os.path.expanduser(r'.\Audio2\*'))
output_dir = 'kaldi_dataset'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize dictionaries for speaker-utterance and speaker-gender mappings
spk2utt_dict = {}
spk2gender_dict = {}

# Open necessary output files in write mode
with open(os.path.join(output_dir, 'wav.scp'), 'w') as wav_scp_file, \
        open(os.path.join(output_dir, 'text'), 'w') as text_file, \
        open(os.path.join(output_dir, 'utt2spk'), 'w') as utt2spk_file, \
        open(os.path.join(output_dir, 'spk2gender'), 'w') as spk2gender_file, \
        open(os.path.join(output_dir, 'corpus.txt'), 'w') as corpus_file, \
        open(os.path.join(output_dir, 'segments'), 'w') as segments_file:

    utterance_id = 1

    # Iterate over each gender folder (M or F)
    for gender_folder in input_dataset_dirs:
        gender = gender_folder[-1]  # Extract gender from folder path
        speaker_folders = glob.glob(os.path.join(gender_folder, '*'))

        # Iterate over each speaker folder within the gender folder
        for speaker_folder in speaker_folders:
            speaker_id = os.path.basename(speaker_folder)

            # Write to spk2gender file
            spk2gender_file.write(f'{speaker_id} {gender}\n')
            spk2gender_dict[speaker_id] = gender

            # Iterate through subfolders of each speaker folder
            subfolders = glob.glob(os.path.join(speaker_folder, '*'))

            # Iterate over each subfolder (assuming they contain audio and metadata)
            for subfolder in subfolders:
                if os.path.isdir(subfolder):
                    csv_path = os.path.join(subfolder, 'metadata.csv')

                    if os.path.exists(csv_path):
                        with open(csv_path, 'r') as csvfile:
                            reader = csv.reader(csvfile, delimiter='|')

                            # Iterate over the rows in the CSV file
                            for row in reader:
                                file_name = row[0]
                                transcription = row[1]

                                # New file name format: speaker_id_utterance_id
                                new_file_name = f'{speaker_id}_{utterance_id}'

                                # Full path to the wav file
                                wav_file_path = os.path.join(subfolder, 'wavs', f'{file_name}.wav')

                                # Calculate duration using soundfile
                                try:
                                    with sf.SoundFile(wav_file_path, 'r') as f:
                                        duration_seconds = len(f) / f.samplerate
                                except Exception as e:
                                    print(f"Error processing {wav_file_path}: {e}")
                                    continue

                                # Write to the wav.scp file
                                wav_scp_file.write(f'{new_file_name} {wav_file_path}\n')

                                # Write to the text file
                                text_file.write(f'{new_file_name} {transcription}\n')

                                # Write to the utt2spk file
                                utt2spk_file.write(f'{new_file_name} {speaker_id}\n')

                                # Update the spk2utt dictionary
                                if speaker_id not in spk2utt_dict:
                                    spk2utt_dict[speaker_id] = []
                                spk2utt_dict[speaker_id].append(new_file_name)

                                # Write to corpus.txt (transcription file)
                                corpus_file.write(f'{new_file_name} {transcription}\n')

                                # Calculate start and end time in seconds (you can adjust this logic)
                                start_time = 0.0
                                end_time = duration_seconds

                                # Write to segments file
                                segments_file.write(f'{new_file_name} {new_file_name} {start_time:.2f} {end_time:.2f}\n')

                                # Increment the utterance ID
                                utterance_id += 1

# Write the spk2utt file
with open(os.path.join(output_dir, 'spk2utt'), 'w') as spk2utt_file:
    for speaker_id, utt_ids in spk2utt_dict.items():
        spk2utt_file.write(f'{speaker_id} {" ".join(utt_ids)}\n')

print("Dataset preparation complete.")
