# GPT_Voice_Bot（检索question关键字）
## 机器人语音小助手Ver1.0 rev正式发布（语音交互 | 技能集配置 | 人机交互）
* 语音交互（科大讯飞 NLP -> 智浦AI LLM -> 科大讯飞 tts）
* 人机交互
* 技能集配置（检索question里是否包含了技能的关键字），非LLM自己输出决策

## 安装 SpeechRecognition | SpeechRecognition 3.10.4
```bash
pip install SpeechRecognition
```

## 安装 pyaudio
### （1）安装portaudio
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev
```
### （2）安装pyaudio | PyAudio 0.2.14
```bash 
pip install PyAudio
```

## 环境下接入realsense摄像头、usb/耳机线扬声器、麦克风
* output 扬声器的输出设备 index 为 2 
* input  麦克风的输入设备 index 为 3
```shell
kuavo@kuavo-NUC12WSKi7:~/kuavo_ros_application$ pactl list short sources
2       alsa_output.pci-0000_00_1f.3.analog-stereo.monitor      module-alsa-card.c      s16le 2ch 44100Hz       SUSPENDED
3       alsa_input.pci-0000_00_1f.3.analog-stereo       module-alsa-card.c      s16le 2ch 44100Hz       SUSPENDED
```

## 安装pygame
```bash
pip install pygame
```

## 安装websocket
```bash
pip install websocket
```

## 安装zhipuai
```bash
pip install zhipuai
```

## 安装websocket-client
```bash
pip install websocket-client
```

## requirements.txt
```bash
pip3 install venv
python -m venc .venv

pip install -r requirements.txt
```
