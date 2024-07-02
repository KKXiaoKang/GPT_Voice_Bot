import os
import pyaudio
import wave
from sound_list import soundList


class AudioPlayer(object):
    def __init__(
        self,
        sampleRate: int = 16000,
        channel: int = 1,
        deviceIndex: int = None,
        audio: pyaudio.PyAudio = None,
    ) -> None:
        self.sampleRate = sampleRate
        self.channel = channel
        self.deviceIndex = deviceIndex

        if audio == None:
            self.audio = pyaudio.PyAudio()
        else:
            self.audio = audio

    def playWavFile(self, path: str):
        with wave.open(path, "rb") as wf:
            stream = self.audio.open(
                format=self.audio.get_format_from_width(2),
                channels=self.channel,
                rate=self.sampleRate,
                output=True,
                output_device_index=self.deviceIndex,
            )

            while True:
                data = wf.readframes(1024)
                if not data:
                    break
                stream.write(data)

            stream.close()

    def playPcmFile(self, path: str):
        stream = self.audio.open(
            format=self.audio.get_format_from_width(2),
            channels=self.channel,
            rate=self.sampleRate,
            output=True,
            output_device_index=self.deviceIndex,
        )

        with open(path, "rb") as f:
            stream.write(f.read())

        stream.stop_stream()
        stream.close()

    def playFile(self, path: str):
        suffix = os.path.splitext(path)[1]
        if suffix == ".wav":
            self.playWavFile(path)
        elif suffix == ".pcm":
            self.playPcmFile(path)

    def playSoundList(self, name: str):
        self.playWavFile(soundList[name][1] + ".wav")

    def isPlaying(self):
        return False

    def waitForPlayer(self):
        while self.isPlaying():
            pass

    def terminate(self):
        self.audio.terminate()


if __name__ == "__main__":
    player = AudioPlayer()
    for sound in soundList:
        player.playSoundList(sound)
        player.waitForPlayer()
