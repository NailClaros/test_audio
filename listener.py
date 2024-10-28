import wave
from dataclasses import dataclass, asdict
import pyaudio
import os
import glob
import uuid
##this code is originally by musikalkemist and has been implemented into our program for educational purposes
##link to the original work https://github.com/musikalkemist/recorder
@dataclass
class StreamParams:
    format: int = pyaudio.paInt16
    channels: int = 1
    rate: int = 44100
    frames_per_buffer: int = 1024
    input: bool = True
    output: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class Recorder:
    """Recorder uses the blocking I/O facility from pyaudio to record sound
    from mic.

    Attributes:
        - stream_params: StreamParams object with values for pyaudio Stream
            object
    """
    def __init__(self, stream_params: StreamParams) -> None:
        self.stream_params = stream_params
        self._pyaudio = None
        self._stream = None
        self._wav_file = None

    def record(self, duration: int, save_path: str) -> None:

        self._create_recording_resources(save_path)
        self._write_wav_file_reading_from_stream(duration)
        self._close_recording_resources()
        

    def _create_recording_resources(self, save_path: str) -> None:
        
        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(**self.stream_params.to_dict())
        self._create_wav_file(save_path)

    def _create_wav_file(self, save_path: str):
        self._wav_file = wave.open(save_path, "wb")
        self._wav_file.setnchannels(self.stream_params.channels)
        self._wav_file.setsampwidth(self._pyaudio.get_sample_size(self.stream_params.format))
        self._wav_file.setframerate(self.stream_params.rate)

    def _write_wav_file_reading_from_stream(self, duration: int) -> None:
        for _ in range(int(self.stream_params.rate * duration / self.stream_params.frames_per_buffer)):
            audio_data = self._stream.read(self.stream_params.frames_per_buffer)
            self._wav_file.writeframes(audio_data)

    def _close_recording_resources(self) -> None:
        if self._wav_file is not None:
            self._wav_file.close()
            self._wav_file = None  # Set to None to prevent further access
        if self._stream is not None:
            self._stream.close()
            self._stream = None  # Set to None to prevent further access
        if self._pyaudio is not None:
            self._pyaudio.terminate()
            self._pyaudio = None  # Set to None to prevent further access


from splitter import auto_split
from apis import run_apis_1
from discount import step2
import uuid
if __name__ == "__main__":
    cycles = 3
    secs = 3
    name = ""
    code = 0
    uu = uuid.uuid4()
    import time
    st = time.time()
    files = glob.glob('audio_stream/clips/*')
    for f in files:
        os.remove(f)


    for x in range (cycles):
        stream_params = StreamParams()
        recorder = Recorder(stream_params)
        recorder.record((secs + 1), f"audio_stream/clips/clip_{x}.wav")
        exa = f"audio_stream/clips/clip_{x}.wav"
        
        code, name = step2(exa)
        if code == 3: #perfect run
            print(name)
            print("NEW WAY FOUND!!!")
            et = time.time()
            print(f"time = {et - st} seconds")
            break
        if code == 2: #confirmed instrumental
            print(name)
            print("Confirmed Intrumental")
            et = time.time()
            print(f"time = {et - st} seconds")
            break
        if code == 1: #likely lyrics not recorded or is an instrumental
            print(name)
            print("Unlucky")
            et = time.time()
            print(f"time = {et - st} seconds")
            break
    if code == 0:
        print("Could retrieve nothing....")
        et = time.time()
        print(f"time = {et - st} seconds")
    
    #original method of calling listener.py
    # stream_params = StreamParams()
    #recorder = Recorder(stream_params)
    #recorder.record(8, "audio_stream/audio.wav")
    # auto_split()
    # run_apis_1()

def run():
    cycles = 3
    secs = 3
    name = ""
    art = ""
    lang = ""
    lyric = ""
    ca = ""
    code = 0
    import time
    st = time.time()
    files = glob.glob('audio_stream/clips/*')
    for f in files:
        os.remove(f)


    for x in range (cycles):
        stream_params = StreamParams()
        recorder = Recorder(stream_params)
        recorder.record((secs + 1), f"audio_stream/clips/clip_{x}.wav")
        exa = f"audio_stream/clips/clip_{x}.wav"
        
        code, name, art, lang, lyric, ca = step2(exa)
        if code == 3: #perfect run
            print(name)
            print("NEW WAY FOUND!!!")
            et = time.time()
            print(f"time = {et - st} seconds")
            return code, name, art, lang, lyric, ca
        if code == 2: #confirmed instrumental
            print(name)
            print("Confirmed Intrumental")
            et = time.time()
            print(f"time = {et - st} seconds")
            return code, name, art, lang, lyric, ca
        if code == 1: #likely lyrics not recorded or is an instrumental
            print(name)
            print("Unlucky")
            et = time.time()
            print(f"time = {et - st} seconds")
            return code, name, art, lang, lyric, ca
    if code == 0:
        print("Could retrieve nothing....")
        et = time.time()
        print(f"time = {et - st} seconds")
        return code, name, art, lang, lyric, ca