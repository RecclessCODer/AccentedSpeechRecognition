import os
import librosa
import json


def find_all_file(base):
    for root, ds, files in os.walk(base):
        for file in files:
            yield file


wav_path = '../cv-corpus-5.1-2020-06-22/en/clips_wav/'
mfcc_path = '../cv-corpus-5.1-2020-06-22/en/mfcc/'

for i in find_all_file(wav_path):
    name_suffix = i.split(".")
    name = name_suffix[0]
    with open(mfcc_path + name + ".json", 'w') as f:
        wav_signal, fs = librosa.load(wav_path + i, sr=None)
        mfccs = librosa.feature.mfcc(wav_signal, sr=fs, n_mfcc=40)  # extract mfcc
        mfccs = mfccs.T  # transpose. first axis is frames, second axis is mfcc dimensions.
        mfcc = mfccs.tolist()
        json.dump(mfcc, f)  # save as json format
    f.close()
