import os
import re
import sys

"""
### dictionary check ###

import config

confs = config.Config()
for x in confs:
    print(confs[x])



### diretory

manifest = '../cv-corpus-5.1-2020-06-22/en/train.tsv'
with open(manifest, encoding='UTF-8') as f:
    data_key = f.readline().strip().split('\t')  # keys' names
    samples = [x.strip().split('\t') for x in f.readlines()]  # x samples list


print(len(samples))

for x in range(0, 2):
    print(samples[x])


acc_set = set()
for __, __, __, __, __, __, __, accent, __, in samples:
    acc_set.add(accent)
enum = enumerate(sorted(acc_set))  # sorted set for consistent results
acc_dic = {acc: i for i, acc in enum}
print(acc_dic)


### dataset and dataloader

# import pydub

sound = pydub.AudioSegment.from_mp3("E:/projects/cv-corpus-5.1-2020-06-22/en/clips/common_voice_en_10.mp3")
sound.export("test.wav", format="wav")


import librosa

wav_signal, fs = librosa.load('test.wav', sr=None)
mfccs = librosa.feature.mfcc(wav_signal, sr=fs, n_mfcc=40)

import os


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            yield f


wav_path = '../cv-corpus-5.1-2020-06-22/en/clips_wav/'

with open("wav.scp", 'w') as f:
    for i in find_all_file(wav_path):
        print(i)
        name_suffix = i.split(".")
        name = name_suffix[0]
        line = name + " " + "test/" + i + "\n"
        f.write(line)
f.close()


# tensor
import torch
import json


def load_array(path):
    with open(path) as f:
        array = json.load(f)
    return torch.FloatTensor(array)


mfcc_path = '../cv-corpus-5.1-2020-06-22/en/mfcc/common_voice_en_1.json'
mfcc = load_array(mfcc_path)
print(mfcc)
print(mfcc.__class__)




import os

mp3_path = '../cv-corpus-5.1-2020-06-22/en/clips/'
file_list = []

for files in os.listdir(mp3_path):
    names = files.split('_')
    key = names[3]
    key = key.split('.')[0]
    key = int(key)
    file_list.append(key)

print(file_list)

import json
import torch

with open('../cv-corpus-5.1-2020-06-22/en/mfcc/common_voice_en_1447.json') as f:
    array = json.load(f)
    tensor_mfcc = torch.FloatTensor(array)

print(tensor_mfcc.size())
print(tensor_mfcc.data)


# test dataloader

from dataloader import MultiDataset, MultiDataLoader

_train_manifest = "./data/new_test.tsv"
_labels = "_'ABCDEFGHIJKLMNOPQRSTUVWXYZ "
train_dataset = MultiDataset(_train_manifest,
                             _labels,
                             use_mfcc_in=True,
                             use_ivectors_in=False,
                             use_embeddings_in=False,
                             embedding_size=256,
                             use_transcripts_out=True,
                             use_accents_out=True)

sample = train_dataset[5]

train_loader = MultiDataLoader(train_dataset,
                               batch_size=20,
                               shuffle=True,
                               num_workers=1)
print(sample)
print(train_dataset)



def parse_transcript(self, transcript_path):

    with open(transcript_path, 'r', encoding='utf8') as transcript_file:
        transcript = transcript_file.read().replace('\n', '')

    transcript = list(filter(None, [self.labels_map.get(x) for x in list(transcript)]))
    return transcript


def read_csv_manifest(path):
    small_data = []
    segment = ""
    with open(path, encoding='UTF-8') as f:
        f.readline()
        # data_key = f.readline().strip().split('\t')  # keys' names
        data = [line.strip().split(',') for line in f.readlines()]  # samples list
    # append an empty segment string to which does not have one, to keep the size of info same.
    for x in range(0, len(data)):
        if len(data[x]) == 9:
            data[x].append(segment)
    return data


def read_accent_split_list(path):
    with open(path, encoding='UTF-8') as f:
        accent_list = [line.strip().split(' ') for line in f.readlines()]
    return accent_list


train_accent_data = read_csv_manifest('./data/train.csv')
train_accent_list = read_accent_split_list('../../cv_corpus_v1/train')
print(len(train_accent_list))
print(len(train_accent_data))

test_accent_data = read_csv_manifest('./data/test.csv')
test_accent_list = read_accent_split_list('../../cv_corpus_v1/test')
print(len(test_accent_list))
print(len(test_accent_data))

"""













