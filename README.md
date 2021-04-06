# DREAM APP
## part of the _Audiences of the Future_ research project

### List of requirements:
#### Python:
See ``requirements.txt`` file.

---
### To perform the Speech-to-Text using IBM Cloud:
**To submit the job:**
```
curl -X POST -u "apikey:Unc9StQ-MALgnGqtWGuX5QPWZdPGUnTcZ9nlkNtGf4ls" --header "Content-Type: audio/flac" --data-binary @AMidsummerNightsDreamBBCRadio3mono.flac "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/75e0de0f-80ec-4270-a67f-93c21f898de5/v1/recognitions?timestamps=true&max_alternatives=3&model=en-GB_BroadbandModel"
```
* Replace _AMidsummerNightsDreamBBCRadio3mono.flac_ by the actual file.
* Check [The asynchronous HTTP interface](https://cloud.ibm.com/docs/speech-to-text-data?topic=speech-to-text-data-async) for more info.

**To check the job status:**
```
curl -X GET -u "apikey:Unc9StQ-MALgnGqtWGuX5QPWZdPGUnTcZ9nlkNtGf4ls" "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/75e0de0f-80ec-4270-a67f-93c21f898de5/v1/recognitions/290ee5a4-4c5b-11ea-81a6-0b82c55a8eae"
```
* Replace _290ee5a4-4c5b-11ea-81a6-0b82c55a8eae_ by the actual job id.
---

### Useful links / references:
#### Git:
* [git - the simple guide](https://rogerdudler.github.io/git-guide/)
* [Learn git in 20 minutes](https://www.youtube.com/watch?v=Y9XZQO1n_7c)

#### Markdown (to edit & format this file):
* [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

#### Audio operations:
* Convert stereo audio to mono:
```
ffmpeg -i _originalStereoAudioFileName_ -ac 1 _MonoAudioFileName_
```

#### Deep Learning:
##### Sound & Music:
* [WaveGAN](https://github.com/chrisdonahue/wavegan)
* [Magenta](https://magenta.tensorflow.org/)
* [Magenta GitHub - with installation instructions](https://github.com/tensorflow/magenta/blob/master/README.md)
* [GANSynth: Adversarial Neural Audio Synthesis - Part of Magenta - Online Supplement](https://storage.googleapis.com/magentadata/papers/gansynth/index.html)
