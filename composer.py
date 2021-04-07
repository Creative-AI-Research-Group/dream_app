#
#
#   Dream_App composer
#   with actors
#   © Craig Vear
#   cvear@dmu.ac.uk
#   7 April 2021
#
#


import trio
import glob
import random
from pydub import AudioSegment
from pydub.playback import play

# global vars and paths
instrument_path = 'datasets/mock/song/resample/accompaniment/*.wav'
vocal_path = 'datasets/mock/song/resample/vocal/*.wav'
environment_path = 'datasets/real_data/environmental_sounds/*.wav'


# instantiate a AudioBot for each actor
class Audio:
    def __init__(self, audio_folder):
        print (f'Audio bot for {audio_folder} is now working')
        self.go_bang = True
        self.logging = True

        # state variables
        self.list_all_audio = glob.glob(audio_folder)
        self.num = len(self.list_all_audio)
        self.seed_rnd = random.randrange(self.num)
        random.seed(self.seed_rnd)
        random.shuffle(self.list_all_audio)

    # controls sound design shaping
    def audio_composer(self, manipulate=False):
        # get random file from folder
        rnd_file = random.randrange(self.num)
        sound_file = self.list_all_audio[rnd_file]
        if self.logging:
            print('sound file = ', sound_file)
        sound = AudioSegment.from_wav(sound_file)

        designed_sound = self.random_length(sound)

        if manipulate:
            # add shaping
            designed_sound = self.random_design(designed_sound)

        # plays sound
        play(designed_sound)

    def random_length(self, sound):
        # calc overall length in ms
        length = sound.duration_seconds * 1000
        if self.logging:
            print('length in milliseconds = ', length)

        # random end point of slice
        rnd_endpoint = random.randrange(int(length))

        # random start point of slice
        rnd_startpoint = random.randrange(rnd_endpoint)

        # slice =
        slice_of_sound = sound[rnd_startpoint:rnd_endpoint]

        # calc new length in ms
        slice_length = length - rnd_endpoint - rnd_startpoint

        # generate fades (shorter in fade, longer out
        rnd_fade_in = random.randrange(int(slice_length / 3))
        rnd_fade_out = random.randrange(int(slice_length - rnd_fade_in / 2))

        # apply fades
        fade_sound = slice_of_sound.fade_in(rnd_fade_in).fade_out(rnd_fade_out)
        if self.logging:
            print(f'slice stats are, length = {slice_length}, fades = {rnd_fade_in, rnd_fade_out}')

        return fade_sound

    # changes sound
    def random_design(self, sound):
        # add gain change
        rnd_gain = random.randrange(10) / 10

        # randomly generate playback speed 0.3-1.0
        rnd_speed = random.randrange(3, 10) / 10

        if self.logging:
            print('change of speed = ', rnd_speed)
            print('change of gain = ', rnd_gain)
        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * rnd_speed)
        })

        # change gain
        sound_with_altered_frame_rate_and_gain = sound_with_altered_frame_rate.apply_gain(rnd_gain)
        # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate_and_gain.set_frame_rate(sound.frame_rate)



###
# controls the threading
###

class Composer:
    def __init__(self):
        # instantiates all actors
        self.singing_bot = Audio(vocal_path)
        self.orchestra_bot = Audio(instrument_path)
        self.sound_design_bot = Audio(environment_path)

    async def singing_actor(self):
        while True:
            print("  child1: started singing voice")

            if random.randrange(2) == 0:
                self.singing_bot.audio_composer()
            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def orchestra_actor(self):
        while True:
            print("  child2: started orchestra")

            if random.randrange(2) == 0:
                self.orchestra_bot.audio_composer()
            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def main(self):
        print("parent: started!")

        # starts the plate spinning
        async with trio.open_nursery() as nursery:
            print("parent: spawning child1...")
            nursery.start_soon(self.singing_actor)

            print("parent: spawning child2...")
            nursery.start_soon(self.orchestra_actor)

            print("parent: waiting for children to finish...")
            # -- we exit the nursery block here --
        print("parent: all done!")

if __name__ == '__main__':
    dream_composer = Composer()
    trio.run(dream_composer.main)