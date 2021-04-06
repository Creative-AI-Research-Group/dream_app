for i in *.wav; do ffmpeg -y -i $i -acodec pcm_s16le -ac 1 -ar 16000 ../new_wav/$i; done
