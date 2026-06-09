import csv
import os
import wave
from datetime import datetime

import sounddevice as sd
import speech_recognition as sr


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

    print("음성 파일이 저장되었습니다:", file_path)


def get_audio_duration(file_path):
    with wave.open(file_path, "rb") as wav_file:
        frame_count = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        duration = frame_count / frame_rate

    return duration


def format_time(seconds):
    minutes = int(seconds // 60)
    remain_seconds = int(seconds % 60)
    return f"{minutes:02d}:{remain_seconds:02d}"


def get_wav_files():
    wav_files = []

    if not os.path.exists(RECORD_FOLDER):
        return wav_files

    for file_name in os.listdir(RECORD_FOLDER):
        if file_name.endswith(".wav"):
            wav_files.append(os.path.join(RECORD_FOLDER, file_name))

    return wav_files


def speech_to_text(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ko-KR")
    except sr.UnknownValueError:
        text = "인식 실패"
    except sr.RequestError:
        text = "STT 서비스 요청 실패"

    return text


def save_text_to_csv(wav_file_path, text):
    duration = get_audio_duration(wav_file_path)

    base_name = os.path.splitext(wav_file_path)[0]
    csv_file_path = base_name + ".csv"

    with open(csv_file_path, "w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["시간", "인식된 텍스트"])
        writer.writerow([f"00:00 ~ {format_time(duration)}", text])

    print("CSV 파일이 저장되었습니다:", csv_file_path)


def convert_records_to_text():
    wav_files = get_wav_files()

    if not wav_files:
        print("변환할 음성 파일이 없습니다.")
        return

    for wav_file in wav_files:
        print("STT 변환 중:", wav_file)
        text = speech_to_text(wav_file)
        save_text_to_csv(wav_file, text)


def main():
    make_records_folder()

    file_path = make_file_name()
    audio_data = record_audio()
    save_audio(file_path, audio_data)

    convert_records_to_text()


if __name__ == "__main__":
    main()