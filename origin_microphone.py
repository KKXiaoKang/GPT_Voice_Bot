声源定位麦克风的调用流程
一、当触发唤醒指令后，麦克风驱动节点将会发布话题

文件路径：catkin_ws/src/ros_mic_arrays/src/main.cpp
当roban机器人的麦克风接受到唤醒词之后。会在test_ivw_fn函数当中发布话题/micarrays/wakeup，里面包含了声音的角度文本等信息


void test_ivw_fn(short angle, short channel, float power, short CMScore, short beam, char *param1, void *param2, void *userData)
{	
    std::vector<ros::Publisher> pubs = *(std::vector<ros::Publisher> *)userData;
    std_msgs::String msg;
    std::ostringstream ss;
    ss << "{'key_word': 'lu3', 'score': '" << int(CMScore) << "', 'angle': '" << int(angle) << "'}";
    ROS_INFO_STREAM(ss.str());
    msg.data = ss.str();
    pubs[0].publish(msg);
}
二、订阅唤醒话题，用于接收唤醒指令并开始声源定位

文件路径：catkin_ws/src/ros_sound_source_localization/src/node.py


  # 订阅唤醒话题，用于接收唤醒指令并开始声源定位
  rospy.Subscriber(WAKEUP_TOPIC, String, self.wakeup_cb, queue_size=1)

此路径包含了对于 /micarrays/wakeup 的读取，读取到声音话题后，通过回调函数wakeup_cb处理声音话题，并且控制roban机器人转向声源处


    def wakeup_cb(self, msg):
        """
        唤醒话题的回调函数，用于响应唤醒事件。

        Args:
            msg: 唤醒话题的消息。

        """
        # 将唤醒数据转换为字典格式
        wakeup_data = json.loads(msg.data.replace("'", '"'))
        # 获取声源角度并播放“我在”的 TTS 语音
        sound_source_angle = int(wakeup_data['angle'])
        self.play_tts_audio(IM_HERE)
        # 将原始角度转换为麦克风阵列的角度，并转向声源
        calculated_angle = self.cal_micarrays_angle(sound_source_angle)
        self.turn_to_sound_source(calculated_angle)
        # 进入人脸检测状态
        self.move_to_face_detection()
        
        
        
目前哈工大的麦克风驱动程序及设备调用方法如下

调用讯飞语音听写流式WebAPI的Python程序
通过speech_recognition 库对麦克风进行打开及录音,同时如果没有在0.8内有声音信息，会自动掐断声音的录制
录完音之后将音频上传至科大讯飞进行调用结果


speech_recognition 简述

Python的speech_recognition库是一个用于语音识别的Python包，它可以使Python程序能够识别和翻译来自麦克风、音频文件或网络流的语音。它支持多种语音识别引擎，包括Google Speech Recognition、CMU Sphinx、Microsoft Bing Voice Recognition等，可以根据需要选择不同的引擎进行语音识别。

创建录音对象

import speechrecognition as sr
 
r = sr.Recognizer()
直接录音

with sr.Microphone() as source:
    audioData = recognizer_instance.listen(source,time)
哈工大代码当中主要的录制部分python代码如下

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
        
        
        
        

