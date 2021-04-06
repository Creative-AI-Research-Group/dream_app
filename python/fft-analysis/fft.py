#  fft.py
#  Copyright (c) 25/02/2020, 03:18.
#  Fabrizio Augusto Poltronieri  (fabrizio@fabriziopoltronieri.com)
#  Craig Vear (cvear@dmu.ac.uk)
#  Thom Corah (tcorah@dmu.ac.uk)

# thanks to john harquist and
# https://github.com/sevenfx/fastai_audio/blob/master/notebooks/01.%20Audio%2C%20STFT%2C%20Melspectrograms%20with%20Python.ipynb
# for the general design of this process

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import sys

# the following 'if' ignores the warning
# librosa/core/audio.py:161: UserWarning: PySoundFile failed. Trying audioread instead.
# warnings.warn('PySoundFile failed. Trying audioread instead.')
# see: https://github.com/librosa/librosa/issues/1015
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

sys.path.append('../utils/')

from scipy.fftpack import fft
from utils import check_slash
from utils import check_file_folder


parser = argparse.ArgumentParser(description='I generate PNGs image files based on FFT analysis of WAV files')
parser.add_argument('-a', '--audio', required=True, type=str, help='WAW directory containing the .wav files to be '
                                                                   'analysed')
parser.add_argument('-p', '--png_dir', required=True, type=str, help='PNG directory to save the .png files')

args = parser.parse_args()

WAV_DIRECTORY = check_slash(args.audio)
PNG_DIRECTORY = check_slash(args.png_dir)
my_list = os.listdir(WAV_DIRECTORY)

errors = []

for file in os.listdir(os.fsdecode(WAV_DIRECTORY)):
    filename = os.fsdecode(file)
    dest_file_name = PNG_DIRECTORY + filename[: -4] + '.png'

    # skip if the file already exists
    if check_file_folder(dest_file_name):
        print('Skipping {}\n'.format(dest_file_name))
        continue

    if filename.endswith(".wav") or filename.endswith(".WAV"):
        try:
            clip, sample_rate = librosa.load('{}{}'.format(WAV_DIRECTORY, filename), sr=None)
        except:
            error = 'An exception occurred opening {}'.format(filename)
            print(error)
            errors.append(error)
            continue

        # print some info, although it is not really necessary
        print('PROCESSING {}'.format(filename))
        print('\tSample Rate\t{} Hz'.format(sample_rate))
        print('\tClip Length\t{} seconds'.format(len(clip)/sample_rate))

        # compute (real) FFT, we don't need to display the image
        n_fft = 1024        # frame length
        start = 45000       # start at a part of the sound that it is not silence
        x = clip[start:start+n_fft]
        X = fft(x, n_fft)
        X_magnitude, X_phase = librosa.magphase(X)
        X_magnitude_db = librosa.amplitude_to_db(X_magnitude)

        timesteps = np.arange(len(clip)) / sample_rate  # in seconds

        # We only use the first (n_fft/2)+1 numbers of the output,
        # as the second half is redundant
        X = X[:n_fft//2+1]

        # Convert from rectangular to polar, usually only care about magnitude
        X_magnitude = librosa.magphase(X)

        # we hear loudness in decibels (on a log scale of amplitude)
        hop_length = 512
        stft = librosa.stft(clip, n_fft=n_fft, hop_length=hop_length)
        stft_magnitude, stft_phase = librosa.magphase(stft)
        stft_magnitude_db = librosa.amplitude_to_db(stft_magnitude, ref=np.max)

        # number of mel frequency bands
        n_mels = 64
        fig = plt.figure(figsize=(5, 5))
        fmin = 20
        fmax = 8000
        mel_spec = librosa.feature.melspectrogram(clip, n_fft=n_fft, hop_length=hop_length,
                                                  n_mels=n_mels, sr=sample_rate, power=1.0,
                                                  fmin=fmin, fmax=fmax)
        mel_spec_db = librosa.amplitude_to_db(mel_spec, ref=np.max)
        librosa.display.specshow(mel_spec_db, x_axis='time',  y_axis='mel',
                                 sr=sample_rate, hop_length=hop_length,
                                 fmin=fmin, fmax=fmax)

        print('SAVING {}\n'.format(dest_file_name))
        plt.savefig(dest_file_name)

# list the errors
for error in errors:
    print(error)
