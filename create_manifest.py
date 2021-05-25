import json
import librosa
from utils import read_manifest, write_manifest
import pydub
import os


def search(root_path, file_name):
    for files in os.listdir(root_path):
        if file_name in files:
            return 1
    return 0


manifest_path = './data/'
mfcc_path_base = '../cv-corpus-5.1-2020-06-22/en/mfcc/'
transcript_path_base = '../cv-corpus-5.1-2020-06-22/en/transcript/'
test = 'dev_accent_manifest.tsv'
wav_path = '../cv-corpus-5.1-2020-06-22/en/clips_wav/'
mp3_path = '../cv-corpus-5.1-2020-06-22/en/clips/'


def create_new_manifest(data):
    new_list = []
    i = 0
    for x in data:
        if i > 10:
            break
        data_list = []
        mp3_name = x[1]
        str_tmp = mp3_name.split('.')
        name = str_tmp[0]  # common voice name
        # extract mfcc and write into json and write mfcc path
        if search(mp3_path, mp3_name):  # if mp3 files not exits then throw this line and continue
            print(mp3_name + " file not exits continue!")
            continue
        sound = pydub.AudioSegment.from_mp3(mp3_path + mp3_name)  # convert mp3 to wav
        sound.export(wav_path + name + '.wav', format='wav')
        with open(mfcc_path_base + name + ".json", 'w') as f:
            wav_signal, fs = librosa.load(wav_path + name + '.wav', sr=None)
            mfccs = librosa.feature.mfcc(wav_signal, sr=fs, n_mfcc=40)  # extract mfcc
            mfccs = mfccs.T  # transpose. first axis is frames, second axis is mfcc dimensions.
            mfcc = mfccs.tolist()
            json.dump(mfcc, f)  # save as json format
        f.close()
        mfcc_path = mfcc_path_base + name + '.json'
        data_list.append(mfcc_path)
        # create transcript json files and write transcript path
        transcript = x[2]
        with open(transcript_path_base + name + ".json", 'w') as f:
            json.dump(transcript, f)  # save as json format
        f.close()
        transcript_path = transcript_path_base + name + '.json'
        data_list.append(transcript_path)
        # write accent labels
        accent_label = x[7]
        data_list.append(accent_label)
        new_list.append(data_list)
        i = i + 1
    return new_list


dev_accent_t_data = read_manifest(manifest_path + test)
new_test = create_new_manifest(dev_accent_t_data)
write_manifest(new_test, 'new_test.tsv')
