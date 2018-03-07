import pyaudio
import wave

class SongPlayer(object):

    def __init__(self, filename):
        self.filename = filename


    def play(self):
        chunk = 1024
        # Open file
        wf = wave.open(self.filename, 'rb')
        # Instantiate PyAudio
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)

        # Read data
        data = wf.readframes(chunk)

        # Play stream
        while data != '':
            stream.write(data)
            data = wf.readframes(chunk)
        # Stop stream
        stream.close()
        # Close PyAudio
        p.terminate()
