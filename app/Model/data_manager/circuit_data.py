from app.Model.data_manager.audio_abstract import Audio_Abstract
from app.Model.data_manager.audio_abstract import TARGET_SR
from app.Model.data_manager.csv_class import CSVFile

from scipy.signal import resample_poly
import soundfile as sf
import numpy as np
import os



def base_path(relative_path):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_script_dir)))
    new_path = os.path.join(base_dir, relative_path)
    return new_path


# -------------------------------------------------
# LOADING DATA   ----------------------------------
# _________________________________________________



def normalize_audio_file(path, target_sr=TARGET_SR, target_sec=None):
    # Always read as float32; make 2D so stereo/mono handled the same
    data, sr = sf.read(str(path), dtype="float32", always_2d=True)  # (N, C)

    # Resample if needed (this is the correct way to change sample rate)
    if sr != target_sr:
        data = resample_poly(data, up=target_sr, down=sr, axis=0)
        sr = target_sr

    # Enforce exact length if requested
    if target_sec is not None:
        target_len = int(round(target_sec * sr))
        n = data.shape[0]
        if n > target_len:
            data = data[:target_len, :]
        elif n < target_len:
            pad = np.zeros((target_len - n, data.shape[1]), dtype=data.dtype)
            data = np.vstack([data, pad])

        # guarantee
        assert data.shape[0] == target_len

    return data, sr  # still 2D


def create_testing_audio(length_of_testing_audio):
    audio_filepath = base_path('experiment files/audio')
    audio_testing_filepath = base_path('experiment files/audio_testing')
    os.makedirs(audio_testing_filepath, exist_ok=True)

    audio_files = {f for f in os.listdir(audio_filepath) if f.lower().endswith(".wav")}
    testing_files = {f for f in os.listdir(audio_testing_filepath) if f.lower().endswith(".wav")}

    for fname in audio_files:
        src = os.path.join(audio_filepath, fname)
        dst = os.path.join(audio_testing_filepath, fname)

        data2d, sr = normalize_audio_file(src, target_sr=48828, target_sec=length_of_testing_audio)
        sf.write(dst, data2d, sr)

    for fname in testing_files - audio_files:
        os.remove(os.path.join(audio_testing_filepath, fname))




# Build list of exp names
def load_audio_names(experiment_number):
    audio_csv_filepath = base_path(f'experiment files/experiments/experiment_{experiment_number}.csv')
    audio_csv = CSVFile(file_path=audio_csv_filepath)
    sample_names = audio_csv.get_column(column_name='audio_name')
    sample_numbers = audio_csv.get_column(column_name='audio_number')

    sample_names_list = []
    for name, number in zip(sample_names, sample_numbers):
        audio_title = f'{name}_{number}'
        sample_names_list.append(audio_title)

    return sample_names_list

# Build list of audio objects in correct order from file
def load_audio_samples(experiment_number, testing_audio):
    sample_names_list = load_audio_names(experiment_number)

    audio_sample_buffer = []

    for sample_name in sample_names_list:

        audio_name = f'{sample_name}.wav'
        # print(audio_name)
        if testing_audio:
            filepath = base_path('experiment files/audio_testing')
        else:
            filepath = base_path('experiment files/audio')

        audio = Audio_Abstract(filepath=f'{filepath}/{audio_name}')
        # print(audio.num_channels)
        audio_sample_buffer.append(audio)

    return audio_sample_buffer

# Build list of channels to play samples from
def load_channel_numbers(experiment_number):

    channel_csv_filepath = base_path(f'experiment files/experiments/experiment_{experiment_number}.csv')
    channel_csv = CSVFile(file_path=channel_csv_filepath)
    channel_numbers = channel_csv.get_column(column_name='speaker')

    return channel_numbers

# Build list of bursts
def load_bursts(experiment_number):
    audio_csv_filepath = base_path(f'experiment files/experiments/experiment_{experiment_number}.csv')
    audio_csv = CSVFile(file_path=audio_csv_filepath)
    sample_names = audio_csv.get_column(column_name='burst_type')

    sample_names_list = [name for name in sample_names]
    audio_sample_buffer = []

    for sample_name in sample_names_list:
        if sample_name.lower() == 'none':
            audio_sample_buffer.append('none')
        else:
            audio_name = f'{sample_name}.wav'
            # print(audio_name)
            filepath = base_path('experiment files/audio_bursts')
            audio = Audio_Abstract(filepath=f'{filepath}/{audio_name}')
            # print(audio.num_channels)
            audio_sample_buffer.append(audio)

    return audio_sample_buffer


# Build list of test data
def load_warmup_data(testing_audio):
    warmup_csv_filepath = base_path(f'experiment files/warmup.csv')
    warmup_csv = CSVFile(file_path=warmup_csv_filepath)
    sample_names = warmup_csv.get_column(column_name='audio_name')
    sample_numbers = warmup_csv.get_column(column_name='audio_number')
    burst_types = warmup_csv.get_column(column_name='burst_type')
    channel_buffer = warmup_csv.get_column(column_name='speaker')

    audio_sample_buffer = []
    burst_buffer = []

    for name, num, burst in zip(sample_names, sample_numbers, burst_types):
        audio_name = f'{name}_{num}.wav'

        if testing_audio:
            filepath = base_path('experiment files/audio_testing')
        else:
            filepath = base_path('experiment files/audio')
        audio = Audio_Abstract(filepath=f'{filepath}/{audio_name}')
        audio_sample_buffer.append(audio)

        if burst.lower() == 'none':
            burst_buffer.append('none')
        else:
            filepath = base_path('experiment files/audio_bursts')
            audio_burst = Audio_Abstract(filepath=f'{filepath}/{burst}.wav')
            burst_buffer.append(audio_burst)

    return audio_sample_buffer, burst_buffer, channel_buffer


def load_calibration_sample(audio_name, time):
    filepath = base_path('experiment files/audio_bursts')
    audio_name = audio_name
    audio = Audio_Abstract(filepath=f'{filepath}/{audio_name}.wav')
    audio.crop(time)

    return audio

# -------------------------------------------------
# TESTS -------------------------------------------
# _________________________________________________

# Shows output of audio samples and channels match
def test_num_audio_channels():
    for i in range(1, 21):
        sample_buffer = load_audio_samples(experiment_number=i)
        channel_buffer = load_channel_numbers(experiment_number=i)
        print(f'{i}: Audio: {len(sample_buffer)} / Chan: {len(channel_buffer)}')

# Shows output of warm up data
def test_warmup_data():
    test_audio_buffer, test_channel_buffer = load_warmup_data()

    for audio, channel in zip(test_audio_buffer, test_channel_buffer):
        print(f'Audio: {audio.name} / Chan: {channel}')


if __name__ == '__main__':

    # Experiment is selected from program
    experiment = 1
    # sample_buffer = load_audio_samples(experiment_number=experiment)
    # channel_buffer = load_channel_numbers(experiment_number=experiment)
    # test_audio_buffer, test_channel_buffer = load_warmup_data()

    # test_num_audio_channels()
    # test_warmup_data()