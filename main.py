import pyaudio
import wave
import numpy as np
import time
from aip import AipSpeech
import threading

# 百度APPID AK SK
APP_ID = '103707598'
API_KEY = 'aAgj6S5C4kJwpcyL4xurKUXI'
SECRET_KEY = 'cQbCeokbaMAb2dan3rwtLhk0kk8xtYl5'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 录音设置
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = 'D:/UseForRuanjianbei/Speech-Recognition/audio.wav'
SILENCE_THRESHOLD = 10000  # 静音阈值
SILENCE_DURATION = 1.5  # 静音持续时间秒数

class AutoRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.recording = False

    def detect_voice(self):
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        silence_count = 0
        self.recording = False

        while True:
            data = self.stream.read(CHUNK)
            audio_data = np.frombuffer(data, dtype=np.int16)
            # 检测音量
            volume = np.linalg.norm(audio_data)

            if volume > SILENCE_THRESHOLD:
                if not self.recording:
                    print("检测到声音，开始录音...")
                    self.start_recording()
                silence_count = 0
            elif self.recording:
                silence_count += 1
                if silence_count > SILENCE_DURATION * RATE / CHUNK:
                    print("检测到静音，停止录音...")
                    self.stop_recording()
                    break

            if self.recording:
                self.frames.append(data)

    def start_recording(self):
        self.frames = []
        self.recording = True

    def stop_recording(self):
        self.recording = False

        # 保存录音文件
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))

        # 读取音频文件并识别
        with open(WAVE_OUTPUT_FILENAME, 'rb') as f:
            audio_data = f.read()
        result = client.asr(audio_data, 'wav', 16000, {'dev_pid': 1537})
        if result['err_no'] == 0:
            print("识别结果: " + result['result'][0])
        else:
            print(f"语音识别失败，错误码：{result['err_no']}, 错误信息：{result['err_msg']}")

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

def main():
    recorder = AutoRecorder()
    while True:
        try:
            recorder.detect_voice()
        finally:
            recorder.terminate()
        # 停止5s
        time.sleep(5)

if __name__ == '__main__':
    main()