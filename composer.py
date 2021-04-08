#
#
#   Dream_App composer
#   with actors
#   © Craig Vear
#   cvear@dmu.ac.uk
#   7 April 2021
#
#

# todo binaural
# todo implement nebula
# todo

import trio
import glob
import random
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import pickle
import socket


# global vars and paths
instrument_path = 'datasets/mock/song/resample/accompaniment/*.wav'
vocal_path = 'datasets/mock/song/resample/vocal/*.wav'
environment_path = 'datasets/real_data/environmental_sounds/*.wav'
word_path = 'datasets/real_data/wav/*.wav'
full_play_path = 'datasets/real_data/speech/*.wav'

# instantiate a AudioBot for each actor
class Audio:
    def __init__(self, audio_folder, transform=False, keep_length=True, pan=False, loop=False):
        print (f'Audio bot for {audio_folder} is now working')
        self.transform = transform
        self.keep_length = keep_length
        self.pan = pan
        self.loop = loop
        self.logging = True

        # state variables
        self.list_all_audio = glob.glob(audio_folder)
        self.num = len(self.list_all_audio)
        self.seed_rnd = random.randrange(self.num)
        random.seed(self.seed_rnd)
        random.shuffle(self.list_all_audio)

    # controls sound design shaping
    def audio_composer(self):
        # get random file from folder
        rnd_file = random.randrange(self.num)
        sound_file = self.list_all_audio[rnd_file]
        if self.logging:
            print('sound file = ', sound_file)
        sound = AudioSegment.from_wav(sound_file)

        if self.keep_length == False:
            sound = self.random_length(sound)

        if self.loop:
            # loop short words
            rnd_loop_count = random.randrange (1, 9)
            sound = sound * rnd_loop_count

        if self.transform:
            # add shaping
            sound  = self.random_design(sound)

        # add pan
        if self.pan:
            rnd_pan = random.randrange(-100, 100) / 100
            if self.logging:
                print(f'pan = {rnd_pan}')
            sound = sound.pan(rnd_pan)

        play_length = sound.duration_seconds

        # plays sound
        play(sound)

        return play_length

    def random_length(self, sound):
        # calc overall length in ms
        length = sound.duration_seconds * 1000
        if self.logging:
            print('length in milliseconds = ', length)

        # random end point of slice
        rnd_endpoint = random.randrange(int(length))

        # random start point of slice
        rnd_startpoint = random.randrange(rnd_endpoint)

        # calc new length in ms
        slice_length = length - rnd_endpoint - rnd_startpoint

        # cap overall duration to 40 seconds
        if slice_length > 40000:
            rnd_endpoint = rnd_startpoint + 40000
            slice_length = rnd_endpoint - rnd_startpoint
        elif slice_length < 3000:
            rnd_endpoint = rnd_startpoint + 3000
            slice_length = rnd_endpoint - rnd_startpoint

        # slice =
        slice_of_sound = sound[rnd_startpoint:rnd_endpoint]

        # generate fades (shorter in fade, longer out
        rnd_fade_in = random.randrange(int(slice_length) + 2000)
        rnd_fade_out = random.randrange(int(slice_length - rnd_fade_in) + 3000)

        # apply fades
        fade_sound = slice_of_sound.fade_in(rnd_fade_in).fade_out(rnd_fade_out)

        # logging opt
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
# controls the orchestration
###

class Composer:
    def __init__(self):
        # instantiates all actors
        self.singing_bot = Audio(vocal_path, transform=False, keep_length=False, pan=True)
        self.orchestra_bot = Audio(instrument_path, transform=True, keep_length=False, pan=False)
        self.sound_design_bot = Audio(environment_path, transform=True, keep_length=False, pan=False)
        self.individual_word_bot = Audio(word_path, transform=False, keep_length=True, pan=True, loop=True)
        self.full_play_bot = Audio(full_play_path, transform=False, keep_length=False, pan=True)

        # timer var
        self.go_bang = True

        # client-server vars
        self.PORT = 65432
        self.HOST = "127.0.0.1"
        self.emr_input_stream = 0

    async def singing_actor(self):
        while self.go_bang:
            print("  child1: started singing voice")

            # if random.randrange(100) < 65:
            if self.emr_input_stream < 65:
                play_length = self.singing_bot.audio_composer()
                await trio.sleep(play_length + 1)

            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def sound_design_actor(self):
        while self.go_bang:
            print("  child2: started singing voice")

            # if random.randrange(100) < 65:
            if self.emr_input_stream < 65:
                play_length = self.sound_design_bot.audio_composer()
                await trio.sleep(play_length + 1)

            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def individual_word_actor(self):
        # todo FABRIZIO = replace with waveGAN generation
        while self.go_bang:
            print("  child3: started singing voice")

            # if random.randrange(100) < 25:
            if self.emr_input_stream < 25:
                play_length = self.individual_word_bot.audio_composer()
                await trio.sleep(play_length + 1)

            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def full_play_actor(self):
        while self.go_bang:
            print("  child4: started singing voice")

            # if random.randrange(100) < 45:
            if self.emr_input_stream < 45:
                play_length = self.full_play_bot.audio_composer()
                await trio.sleep(play_length + 1)

            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)

    async def orchestra_actor(self):
        while self.go_bang:
            print("  child5: started orchestra")

            # if self.emr_input_stream < 65:
            if self.emr_input_stream < 65:
                play_length = self.orchestra_bot.audio_composer()
                await trio.sleep(play_length + 1)

            else:
                # wait 3 - 8 seconds
                rnd_wait = random.randrange(3, 8)
                await trio.sleep(rnd_wait)


    async def timer(self):
        while self.go_bang:
            pass

    # listens to the EMR Ai engine and parses the var to global
    async def emr_engine_listener(self):
        print("client: started!")
        while True:
            print(f"client: connecting to {self.HOST}:{self.PORT}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.HOST, self.PORT))
                s.listen()
                client_stream, addr = s.accept()
                with client_stream:
                    print('Connected by', addr)
                    while True:
                        # get data from stream
                        data = client_stream.recv(1024)
                        data_loaded = pickle.loads(data)
                        print(f"receiver: got data {data_loaded}")
                        self.emr_input_stream = data_loaded * 100

                        # # send it to the mincer for soundBot control
                        # # NB play_with_simpleaudio does not hold thread
                        # master_data = data_loaded['master_output']
                        # rhythm_rate = data_loaded['rhythm_rate']
                        # self.mincer(master_data, rhythm_rate)
                        #
                        # # send out-going data to server
                        # send_data = pickle.dumps(self.send_data_dict, -1)
                        # client_stream.sendall(send_data)

        #
        # while self.go_bang:
        #     async for data in client_stream:
        #         print(f"receiver: got data {data!r}")
        #         load_data = pickle.loads(data)
        #         self.emr_input_stream = load_data * 100

    async def main(self):
        print("parent: started!")
        # print("parent: connecting to 127.0.0.1:{}".format(self.PORT))
        # client_stream = await trio.open_tcp_stream(self.IP_ADDR, self.PORT)

        # starts the plate spinning
        async with trio.open_nursery() as nursery:
            print("parent: spawning child1...")
            nursery.start_soon(self.singing_actor)

            print("parent: spawning child2...")
            nursery.start_soon(self.orchestra_actor)

            print("parent: spawning child3...")
            nursery.start_soon(self.sound_design_actor)

            print("parent: spawning child4...")
            nursery.start_soon(self.individual_word_actor)

            print("parent: spawning child5...")
            nursery.start_soon(self.full_play_actor)

            # print("parent: spawning child6...")
            # nursery.start_soon(self.timer)

            print("parent: spawning child7...")
            nursery.start_soon(self.emr_engine_listener)

        print("parent: all done!")

if __name__ == '__main__':
    dream_composer = Composer()
    trio.run(dream_composer.main)