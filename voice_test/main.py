# config microphone: Bothlent UAC Dongle: USB Audio (hw:1,0) inputchannel: 8
# config speaker: 输入设备 ID  0  -  USB Audio Device: - (hw:0,0) inputchannel: 1




import json
import pyaudio
import speech_recognition as sr
import os
import configparser
import pygame
import time
from voice_record import recordVoice
from audio_tool import wav2pcm
from voice_recognition import voiceRecognition
from voice_synthesis import voiceSynthesis
from audio_device import listAudioDevice
from audio_player import AudioPlayer
from zhipuai import ZhipuAI
import re

client = ZhipuAI(
    api_key = "d36a30c392305de3735e51ecdb536b42.o0GUdJVlEKH3lSNi"
    #api_key ="419e54a6fcd665e02f27089c19feb7a3.4y2FVddBJBvuXJFM"
    #api_key=os.environ["ZHIPUAI_API_KEY"]
)

configFile = configparser.ConfigParser()
configFile.read("config.txt",encoding='utf-8')
config = dict(configFile.items("config"))

#OPENAI_API_KEY = config["openai_api_key"]
NETWORK_PROXY = config["network_proxy"]

RECOGNITION_APPID = config["recognition_app_id"]
RECOGNITION_API_KEY = config["recognition_api_key"]
RECOGNITION_API_SECRET = config["recognition_api_secret"]
RECOGNITION_FILE_PATH = "./temp/record.pcm"

SYNTHESIS_APPID = config["synthesis_app_id"]
SYNTHESIS_API_KEY = config["synthesis_api_key"]
SYNTHESIS_API_SECRET = config["synthesis_api_secret"]
SYNTHESIS_FILE_PATH = "./temp/synthesis.pcm"

AUDIO_INPUT_DEVICE_INDEX = eval(config["audio_input_device_index"])
AUDIO_INPUT_DEVICE_CHANNEL = 1
AUDIO_OUTPUT_DEVICE_INDEX = eval(config["audio_output_device_index"])
ENERGY_THREASHOLD = int(config["energy_threashold"])

RECORD_TIME = 7
RECORD_WAV_PATH = "./temp/record.wav"

text =[]

def recordVoiceSmart(mic: sr.Microphone, save_file="record.pcm", timeout=10):
    r = sr.Recognizer()
    r.energy_threshold = ENERGY_THREASHOLD

    print("Listening....")

    audio = r.listen(mic, timeout)
    with open(save_file, "wb") as f:
        f.write(audio.get_wav_data())
        #print(audio.get_wav_data())
        #f.close()
        

    print("Record complete.")


def voiceToText(audio: pyaudio.PyAudio=None, mic: sr.Microphone=None, smart=True):
    if smart:
        recordVoiceSmart(mic, RECOGNITION_FILE_PATH)
        print("smart")
    else:
        recordVoice(audio, RECORD_TIME, RECORD_WAV_PATH, AUDIO_INPUT_DEVICE_INDEX)
        wav2pcm(RECORD_WAV_PATH, RECOGNITION_FILE_PATH)
        print("not smart")

    recognition = voiceRecognition(
        RECOGNITION_FILE_PATH,
        RECOGNITION_APPID,
        RECOGNITION_API_KEY,
        RECOGNITION_API_SECRET,
    )

    return recognition

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    



def remove_periods(s: str):
    # 删除字符串中的所有句号
    s.replace('！', '')
    s.replace('？', '')
    s.replace('。', '')
    s.replace('，', '')
    return s



def gen_glm_params(prompt: str):
    '''
    构造 GLM 模型请求参数 messages

    请求参数：
        prompt: 对应的用户提示词
    '''
    #cleaned_prompt = remove_chinese_symbols(prompt)
    #cleaned_prompt = prompt[:-1]
    print("prompt type : ", type(prompt))
    
    ## process
    if str(type(prompt)) == "<class 'list'>":
        prompt = prompt.pop()
    else:
        prompt = remove_periods(prompt)
        #prompt = prompt[:-1]
        
        
    ## 
    print("gen_glm",prompt)    
    messages = [{"role": "user", "content": prompt}]
    print("gen_glm_result",messages)    
    return messages


def get_completion(prompt: str, model="glm-4", temperature=0.95):
    '''
    获取 GLM 模型调用结果

    请求参数：
        prompt: 对应的提示词
        model: 调用的模型，默认为 glm-4，也可以按需选择 glm-3-turbo 等其他模型
        temperature: 模型输出的温度系数，控制输出的随机程度，取值范围是 0~1.0，且不能设置为 0。温度系数越低，输出内容越一致。
    '''
    
    messages = gen_glm_params(prompt)
    print("remove chinese sym",messages)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"

def askChatGPT(question: str):
    #Input = input("\n" +"我:")
    question = checklen(getText("user",question))
    answer_zhipu = get_completion(question, model="glm-4")    

    return answer_zhipu


def calibrateEnergyThreashold(mic: sr.Microphone):
    rec = sr.Recognizer()
    rec.adjust_for_ambient_noise(mic)
    print("energy_threashold: ", rec.energy_threshold)

def remove_some_rules(word:str):
    """
    返回的answer有两种形式，需要进行字符处理
    [1]  {role=assistant, content=珠穆朗玛峰，也被称为珠峰，是地球上最高的山峰，海拔高度为8,848.86米（根据2020年的测量数据）。它位于中国与尼泊尔边界的喜马拉雅山脉中。}
    [2]  珠穆朗玛峰，又称珠穆朗玛峰，是世界上最高的山峰，位于中国与尼泊尔的边界上。它的海拔高度为8,848米。这座峰以其壮丽的自然风光和攀登挑战而闻名于世。
    """
    # 定义匹配 {role=assistant, content=...} 的正则表达式
    pattern = r'\{role=[^,]+, content=([^}]+)\}'
    
    # 使用正则表达式查找匹配的内容
    match = re.search(pattern, word)
    
    if match:
        # 如果匹配到，则返回 content 中的内容
        return match.group(1).strip()
    else:
        # 如果没有匹配到，则返回原始字符串
        return word.strip()
    
def main():
    #openai.api_key = OPENAI_API_KEY
    while True:
        count = 0
        audio = pyaudio.PyAudio()
        player = AudioPlayer()

        time.sleep(2)

        with sr.Microphone(AUDIO_INPUT_DEVICE_INDEX, 16000) as mic:
            if count == 0:
                
                print("[Log] Audio initialization compelete.")

                print("[Audio Device List]")
                listAudioDevice(audio)
                print()

                print("[Measure Ambient Noise]")
                calibrateEnergyThreashold(mic)
                print()

                print("[Start ChatGPT]")
        
            player.playSoundList("speak")
            player.waitForPlayer()
            # question = input("> ")
            question = " "
            question = voiceToText(audio=audio, mic=mic)
            #question = "what is your name "
            a_result = type(question)
            print(a_result)
            print("> ", question)

            answer = askChatGPT(question)
            answer = remove_some_rules(answer)
            print(type(answer))
            print(answer)
            print()

            audioFile = voiceSynthesis(
                answer, SYNTHESIS_APPID, SYNTHESIS_API_KEY, SYNTHESIS_API_SECRET
            )
            player.playPcmFile(audioFile)

            print("[Log] Dialog complete.")
            input("Press Enter to continue...")
        
        count += 1
        
if __name__ == "__main__":
    main()
    pygame.quit()
