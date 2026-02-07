import os
import csv
from app.Model.data_manager.audio_abstract import Audio_Abstract

# Define the folder path and output CSV file path
folder_path = '/Users/KevMcK/Dropbox/2 Work/Projects/Anechoic Chamber/anechoic_um_app/experiment files/audio'
output_csv = '/Users/KevMcK/Dropbox/2 Work/Projects/Anechoic Chamber/anechoic_um_app/testing/audio_info.csv'
interval_time = 1

audio_data = []

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".wav") and "pink_noise" not in filename:
        file_path = os.path.join(folder_path, filename)

        audio = Audio_Abstract(filepath=file_path)
        audio_length = round(audio.sample_length + interval_time, 2)

        # Append the name and length to the list
        audio_data.append((audio.name, audio_length))

# Sort the audio data by the first column (name) alphabetically
audio_data.sort(key=lambda x: x[0])

# Write the sorted data to the CSV file
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Name', 'Length'])

    # Write each row of sorted data
    for row in audio_data:
        writer.writerow(row)

print(f"Audio information has been exported to {output_csv} in alphabetical order.")
