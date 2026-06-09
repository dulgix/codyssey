import os
import wave
from datetime import datetime

import sounddevice as sd


RECORD_FOLDER = "records"
SAMPLE_RATE = 44100
CHANNELS = 1
RECORD_SECONDS = 5
BLOCK_SIZE = 1024


def make_records_folder():
    if not os.path.exists(RECORD_FOLDER):
        os.makedirs(RECORD_FOLDER)


def make_file_name():
    now = datetime.now()
    file_name = now.strftime("%m-%d-%H-%M-%S") + ".wav"
    return os.path.join(RECORD_FOLDER, file_name)


def record_audio():
    print("녹음을 시작합니다.")

    audio_frames = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_frames.append(bytes(indata))

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=CHANNELS,
        callback=callback
    ):
        sd.sleep(RECORD_SECONDS * 1000)

    print("녹음이 완료되었습니다.")
    return b"".join(audio_frames)


def save_audio(file_path, audio_data):
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data)

    print("파일이 저장되었습니다:", file_path)


def main():
    make_records_folder()

    file_path = make_file_name()
    audio_data = record_audio()
    save_audio(file_path, audio_data)


if __name__ == "__main__":
    main()