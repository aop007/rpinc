#!/usr/bin/env python

import threading

import wave
import pyaudio


class AudioRecorder(object):
    # Audio class based on pyAudio and Wave
    def __init__(self, input_device_index: int):

        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "temp_audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.frames_per_buffer,
            input_device_index=input_device_index,
        )
        self.audio_frames = []
    # end __init__()

    def record(self):
        """
        Audio starts being recorded

        :return:
        """
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break
            # end if
        # end while
    # end record()

    def stop(self):
        """
        Finishes the audio recording therefore the thread too

        :return:
        """
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            with wave.open(self.audio_filename, 'wb') as waveFile:
                waveFile.setnchannels(self.channels)
                waveFile.setsampwidth(self.audio.get_sample_size(self.format))
                waveFile.setframerate(self.rate)
                waveFile.writeframes(b''.join(self.audio_frames))
            # end with
        # end if
    # end stop()

    def start(self):
        """
        Launches the audio recording function using a thread

        :return:
        """
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()
    # end start()

    @staticmethod
    def show_recording_devices():
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    # end show_recording_devices()
# end class AudioRecorder


if __name__ == '__main__':
    import time

    # AudioRecorder.show_recording_devices()
    # exit()

    audio_thread = AudioRecorder(0)
    print("audio_thread created!")
    # print("sleeping!")
    # time.sleep(5.0)

    print("audio_thread.start")
    audio_thread.start()
    time.sleep(5.0)
    audio_thread.stop()
# end if
