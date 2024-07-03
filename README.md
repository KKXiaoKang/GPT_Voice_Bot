# GPT_Voice_Bot（检索question关键字）
* a simple demo to talk to gpt each other
* 请注意，此版本GPT_Voice_Bot关于技能集的配置是通过检索question关键字进行配置

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
