* 只接入扬声器
```bash
pygame 2.6.0 (SDL 2.28.4, Python 3.10.12)
Hello from the pygame community. https://www.pygame.org/contribute.html
ALSA lib pcm.c:2664:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2664:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2664:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
ALSA lib pcm_route.c:877:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:877:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:877:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_route.c:877:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_oss.c:397:(_snd_pcm_oss_open) Cannot open device /dev/dsp
ALSA lib pcm_oss.c:397:(_snd_pcm_oss_open) Cannot open device /dev/dsp
ALSA lib confmisc.c:160:(snd_config_get_card) Invalid field card
ALSA lib pcm_usb_stream.c:482:(_snd_pcm_usb_stream_open) Invalid card 'card'
ALSA lib confmisc.c:160:(snd_config_get_card) Invalid field card
ALSA lib pcm_usb_stream.c:482:(_snd_pcm_usb_stream_open) Invalid card 'card'
[Log] Audio initialization compelete.
[Audio Device List]
输入设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) inputchannel: 2
输出设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) outputchannel: 2
输出设备 ID  1  -  HDA Intel PCH: HDMI 0 (hw:0,3) outputchannel: 8
输出设备 ID  2  -  HDA Intel PCH: HDMI 1 (hw:0,7) outputchannel: 8
输出设备 ID  3  -  HDA Intel PCH: HDMI 2 (hw:0,8) outputchannel: 8
输出设备 ID  4  -  HDA Intel PCH: HDMI 3 (hw:0,9) outputchannel: 8
输入设备 ID  5  -  sysdefault inputchannel: 128
输出设备 ID  5  -  sysdefault outputchannel: 128
输出设备 ID  6  -  front outputchannel: 2
输出设备 ID  7  -  surround40 outputchannel: 2
输出设备 ID  8  -  surround51 outputchannel: 2
输出设备 ID  9  -  surround71 outputchannel: 2
输出设备 ID  10  -  hdmi outputchannel: 8
输入设备 ID  11  -  samplerate inputchannel: 128
输出设备 ID  11  -  samplerate outputchannel: 128
输入设备 ID  12  -  speexrate inputchannel: 128
输出设备 ID  12  -  speexrate outputchannel: 128
输入设备 ID  13  -  pulse inputchannel: 32
输出设备 ID  13  -  pulse outputchannel: 32
输入设备 ID  14  -  upmix inputchannel: 8
输出设备 ID  14  -  upmix outputchannel: 8
输入设备 ID  15  -  vdownmix inputchannel: 6
输出设备 ID  15  -  vdownmix outputchannel: 6
输出设备 ID  16  -  dmix outputchannel: 2
输入设备 ID  17  -  default inputchannel: 32
输出设备 ID  17  -  default outputchannel: 32
```

* 没接入麦克风 扬声器
```bash
输入设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) inputchannel: 2
输出设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) outputchannel: 2
输出设备 ID  1  -  HDA Intel PCH: HDMI 1 (hw:0,7) outputchannel: 8
输出设备 ID  2  -  HDA Intel PCH: HDMI 2 (hw:0,8) outputchannel: 8
输出设备 ID  3  -  HDA Intel PCH: HDMI 3 (hw:0,9) outputchannel: 8
输入设备 ID  4  -  sysdefault inputchannel: 128
输出设备 ID  4  -  sysdefault outputchannel: 128
输出设备 ID  5  -  front outputchannel: 2
输出设备 ID  6  -  surround40 outputchannel: 2
输出设备 ID  7  -  surround51 outputchannel: 2
输出设备 ID  8  -  surround71 outputchannel: 2
输入设备 ID  9  -  samplerate inputchannel: 128
输出设备 ID  9  -  samplerate outputchannel: 128
输入设备 ID  10  -  speexrate inputchannel: 128
输出设备 ID  10  -  speexrate outputchannel: 128
输入设备 ID  11  -  pulse inputchannel: 32
输出设备 ID  11  -  pulse outputchannel: 32
输入设备 ID  12  -  upmix inputchannel: 8
输出设备 ID  12  -  upmix outputchannel: 8
输入设备 ID  13  -  vdownmix inputchannel: 6
输出设备 ID  13  -  vdownmix outputchannel: 6
输出设备 ID  14  -  dmix outputchannel: 2
输入设备 ID  15  -  default inputchannel: 32
输出设备 ID  15  -  default outputchannel: 32
```
* 只接入麦克风
```bash
输入设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) inputchannel: 2
输出设备 ID  0  -  HDA Intel PCH: ALC269VB Analog (hw:0,0) outputchannel: 2
输出设备 ID  1  -  HDA Intel PCH: HDMI 0 (hw:0,3) outputchannel: 8
输出设备 ID  2  -  HDA Intel PCH: HDMI 1 (hw:0,7) outputchannel: 8
输出设备 ID  3  -  HDA Intel PCH: HDMI 2 (hw:0,8) outputchannel: 8
输出设备 ID  4  -  HDA Intel PCH: HDMI 3 (hw:0,9) outputchannel: 8
输入设备 ID  5  -  sysdefault inputchannel: 128
输出设备 ID  5  -  sysdefault outputchannel: 128
输出设备 ID  6  -  front outputchannel: 2
输出设备 ID  7  -  surround40 outputchannel: 2
输出设备 ID  8  -  surround51 outputchannel: 2
输出设备 ID  9  -  surround71 outputchannel: 2
输出设备 ID  10  -  hdmi outputchannel: 8
输入设备 ID  11  -  samplerate inputchannel: 128
输出设备 ID  11  -  samplerate outputchannel: 128
输入设备 ID  12  -  speexrate inputchannel: 128
输出设备 ID  12  -  speexrate outputchannel: 128
输入设备 ID  13  -  pulse inputchannel: 32
输出设备 ID  13  -  pulse outputchannel: 32
输入设备 ID  14  -  upmix inputchannel: 8
输出设备 ID  14  -  upmix outputchannel: 8
输入设备 ID  15  -  vdownmix inputchannel: 6
输出设备 ID  15  -  vdownmix outputchannel: 6
输出设备 ID  16  -  dmix outputchannel: 2
输入设备 ID  17  -  default inputchannel: 32
输出设备 ID  17  -  default outputchannel: 32
```