from pathlib import Path
import wave
import contextlib

TRIM_SECONDS = 2.5


def trim_wav_in_place(path, seconds):
    with contextlib.closing(wave.open(str(path), "rb")) as r:
        framerate = r.getframerate()
        nchannels = r.getnchannels()
        sampwidth = r.getsampwidth()

        frames_to_keep = int(seconds * framerate)
        frames_to_keep = min(frames_to_keep, r.getnframes())

        audio = r.readframes(frames_to_keep)

    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with contextlib.closing(wave.open(str(tmp_path), "wb")) as w:
        w.setnchannels(nchannels)
        w.setsampwidth(sampwidth)
        w.setframerate(framerate)
        w.writeframes(audio)

    tmp_path.replace(path)


def trim_folder(folder_path, seconds=TRIM_SECONDS):
    for wav in Path(folder_path).glob("*.wav"):
        trim_wav_in_place(wav, seconds)
        print(f"Trimmed: {wav.name}")


if __name__ == "__main__":
    folder = r"/Users/KevMcK/Dropbox/2 Work/Anechoic Chamber/anechoic_um_app/experiment files/audio_testing"  # change this
    trim_folder(folder)
    print("Done.")
