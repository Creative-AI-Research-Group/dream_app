#  SplitAudio.py
#  Copyright (c) 11/02/2020, 23:26.
#  Fabrizio Augusto Poltronieri  (fabrizio@fabriziopoltronieri.com)
#  Craig Vear (cvear@dmu.ac.uk)
#  Thom Corah (tcorah@dmu.ac.uk)

# a very simple class to
# split audio files
# and save them as wav
# using pydub - https://github.com/jiaaro/pydub

from pydub import AudioSegment


class SplitAudio:
    def __init__(self, audio_directory, audio_file, verbose=True):
        self.verbose = verbose
        self.audio_directory = audio_directory
        self.message('Loading audio file {}'.format(audio_file))
        self.audio_file = AudioSegment.from_mp3(audio_file)
        self.message('Audio file {} is loaded'.format(audio_file))

    def split_audio(self, start, end, filename, file_format='wav'):
        start *= 1000
        end *= 1000
        splitted_audio = self.audio_file[start:end]
        splitted_audio.export('{}{}'.format(self.audio_directory,
                                            filename,
                                            format=file_format))
        self.message('Exported: {}'.format(filename))

    def message(self, message):
        if self.verbose:
            print(message)
