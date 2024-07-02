#```python
from zhipuai import ZhipuAI

client = ZhipuAI(
    #api_key = "2ed622a64cd59489557bf88ab570bc1e.hdWhRouuja0IFy1S"
    api_key = "96a303b8a3befeb9149eb3ac94cde00b.oRbTSvV8oY2nrHRc"
    #api_key=os.environ["ZHIPUAI_API_KEY"]
)

def gen_glm_params(prompt):
    '''
    构造 GLM 模型请求参数 messages

    请求参数：
        prompt: 对应的用户提示词
    '''
    messages = [{"role": "user", "content": prompt}]
    return messages


def get_completion(prompt, model="glm-4", temperature=0.95):
    '''
    获取 GLM 模型调用结果

    请求参数：
        prompt: 对应的提示词
        model: 调用的模型，默认为 glm-4，也可以按需选择 glm-3-turbo 等其他模型
        temperature: 模型输出的温度系数，控制输出的随机程度，取值范围是 0~1.0，且不能设置为 0。温度系数越低，输出内容越一致。
    '''

    messages = gen_glm_params(prompt)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"
#```


#```python
#answer = get_completion("你好")
#print(answer)

#```

##micro phone sdk used 
#speech_recognition 简述

#Python的speech_recognition库是一个用于语音识别的Python包，它可以使Python程序能够识别和翻译来自麦克风、音频文件或网络流的语音。它支持多种语音识别引擎，包括Google Speech Recognition、CMU Sphinx、Microsoft Bing Voice Recognition等，可以根据需要选择不同的引擎进行语音识别。

#创建录音对象

import speechrecognition as sr
 
r = sr.Recognizer()
直接录音

with sr.Microphone() as source:
    audioData = recognizer_instance.listen(source,time)
#哈工大代码当中主要的录制部分python代码如下

    # 收到websocket连接建立的处理
    def on_open(ws):
        def run_iamhere():
          # time.sleep(0.5)
          time1 = datetime.now()
          play(AudioSegment.from_mp3(iamhere)+10)
          global flagover
          flagover = True
          print('runtime = ', datetime.now()-time1)
        def run(*args):
            frameSize = 3000  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            # 打开麦克风录音
            r = sr.Recognizer()
            global flagover
            # r.energy_threshold = 3000   # threshold for background noise 
            r.pause_threshold = 0.8   # minimum length of silence (in seconds) that will register as the end of a phrase.  
            # r.dynamic_energy_adjustment_damping = 5

            try:
                with sr.Microphone() as source: 
                                     
                    # run iam here
                    thread.start_new_thread(run_iamhere, ())

                    # calibrate ambient noise
                    r.adjust_for_ambient_noise(source, duration=1)  # we only need to calibrate once, before we start listening
                     
        
                    # r.listen start recording when there is audio input higher than threshold (set this to a reasonable number),
                    # and stops recording when silence >0.8s(changable)
                    time1 = datetime.now()
                    while flagover == False: continue

                    print("I am listening....", datetime.now() - time1)
                    audio = r.listen(source, timeout=5, phrase_time_limit=20)
                    
                    # get wav data from AudioData object 
                    wav = audio.get_wav_data(convert_rate=16000, convert_width=2) # width=2 gives 16bit audio.
                    
                    # # 保存 wav
                    # write audio to a RAW file
                    # with open(wsParam.AudioFile, "wb") as f:
                    #     f.write(audio.get_raw_data())

                    audio_file = wsParam.AudioFile
                    print('----+-', audio_file)
                    wf = wave.open(audio_file, 'wb')
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(wav)
                    wf.close()
                    print('sr is over')

            except sr.exceptions.WaitTimeoutError as e:
                print(e)
                ws.close()
                return 
            with open(wsParam.AudioFile, "rb") as fp:
                print('start audio')
                time1 = datetime.now()
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    # 发送第一帧音频，带business 参数
                    # appid 必须带上，只需第一帧发送
                    if status == STATUS_FIRST_FRAME:
                        d = {"common": wsParam.CommonArgs,
                                "business": wsParam.BusinessArgs,
                                "data": {"status": 0, "format": "audio/L16;rate=16000",
                                        "audio": str(base64.b64encode(buf), 'utf-8'),
                                        "encoding": "raw"}}
                        d = json.dumps(d)
                        print('send first audio')
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                        "audio": str(base64.b64encode(buf), 'utf-8'),
                                        "encoding": "raw"}}
                        print('send mid audio')
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                        "audio": str(base64.b64encode(buf), 'utf-8'),
                                        "encoding": "raw"}}
                        print('send last audio')
                        ws.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
                    if (datetime.now() - time1).seconds > 4:
                        break
                ws.close()
        time1 = datetime.now()
        thread.start_new_thread(run, ())
        time2 = datetime.now()
        print('speechrecognition cost = ', time2 - time1)

    time1 = datetime.now()

    wsParam = Ws_Param(APPID='c57ccaf5', APISecret='NjM0NjcxNmI4OGVhMWUzOTNhMDAxOTYx',
                       APIKey='b1d7d520b0c50e9442d0be07545b76d5',
                       AudioFile=savepath)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    print(f"socket time cost:{datetime.now()-time1}")
    
    print(wsParam.result)
    print('-------iat is over----------')
    return wsParam.result   
        




