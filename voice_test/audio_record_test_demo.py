import pyaudio
import speech_recognition as sr
import configparser

# 读取配置文件
configFile = configparser.ConfigParser()
configFile.read("config.txt", encoding='utf-8')
config = dict(configFile.items("config"))

# 配置参数
AUDIO_INPUT_DEVICE_INDEX = int(config["audio_input_device_index"])
ENERGY_THRESHOLD = int(config["energy_threashold"])
RECORD_TIME = 7  # 录音时长，单位：秒
RECORD_FILE_PATH = "./record.pcm"  # 保存录音的文件路径

def calibrate_energy_threshold(mic: sr.Microphone):
    rec = sr.Recognizer()
    rec.adjust_for_ambient_noise(mic)
    print("Calibrated energy threshold: ", rec.energy_threshold)
    return rec.energy_threshold

def record_voice(mic: sr.Microphone, save_file="record.pcm", timeout=10):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = ENERGY_THRESHOLD
    print("Listening...")

    audio = recognizer.listen(mic, timeout)
    with open(save_file, "wb") as f:
        f.write(audio.get_wav_data())

    print("Recording complete.")

def main():
    audio = pyaudio.PyAudio()

    with sr.Microphone(device_index=AUDIO_INPUT_DEVICE_INDEX, sample_rate=16000) as mic:
        print("[Log] Audio initialization complete.")
        
        # 校准环境噪音
        print("[Measure Ambient Noise]")
        calibrate_energy_threshold(mic)
        print()

        # 开始录音
        print("[Start Recording]")
        record_voice(mic, RECORD_FILE_PATH)
        print(f"Audio recorded and saved to {RECORD_FILE_PATH}")

if __name__ == "__main__":
    main()
