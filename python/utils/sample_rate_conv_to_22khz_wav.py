from pydub import AudioSegment
import glob

folder = 'vocal/*.wav'
list_all = glob.glob(folder)

for i in list_all:
    print (i)
    sound = AudioSegment.from_file(i, format="wav", frame_rate=44100)
    sound = sound.set_frame_rate(16000)
    sound = sound.set_channels(1)
    sound.export('resample/' + i, format="wav")
