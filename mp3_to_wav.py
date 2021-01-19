import os
import pydub


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


mp3_path = '../cv-corpus-5.1-2020-06-22/en/test_tmp/'
wav_path = '../cv-corpus-5.1-2020-06-22/en/clips_wav/'
for i in find_all_file(mp3_path):
    print(i)
    name_suffix = i.split(".")
    name = name_suffix[0]
    sound = pydub.AudioSegment.from_mp3(mp3_path + i)
    sound.export(wav_path + name + '.wav', format='wav')



