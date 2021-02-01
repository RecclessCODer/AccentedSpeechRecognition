from __future__ import print_function
from model import MultiTask
import torch.nn as nn
import torch
from decoder import GreedyDecoder, BeamCTCDecoder
import sys
from pathlib import Path
import librosa

model_path = './saved_models/TrainMulti_TRAIN__in_mfcc__out_transcripts_accents-mix1.0-CE__nblyrs-head-4-speech-1-accent-1__bnf-256__31-01-2021_18h54m38.pth'

model, __ = MultiTask.load_model(model_path)
model = model.cuda()


# mfcc extraction
wav_path = '../../cv_corpus_v1/dev/sample-000020.wav'
transcript = 'coming home a party of tourists passed us singing and playing music'
wav_signal, fs = librosa.load(wav_path, sr=None)
mfccs = librosa.feature.mfcc(wav_signal, sr=fs, n_mfcc=40)  # extract mfcc
mfccs = mfccs.T  # transpose. first axis is frames, second axis is mfcc dimensions.
mfcc = mfccs.tolist()
print(mfcc)

# token
labels = "_'ABCDEFGHIJKLMNOPQRSTUVWXYZ "
labels_map = dict([(labels[i], i) for i in range(len(labels))])  # labels dictionary
transcript_map = dict([(i, labels[i]) for i in range(len(labels))]) # token map to transcript
transcript = list(filter(None, [labels_map.get(x) for x in list(transcript.upper())]))

inputs = mfcc
inputs_lens = len(mfcc)
transcript_lens = len(transcript)
inputs = inputs.cuda()
inputs_lens = inputs_lens.cuda()

# forward
out_text, out_accent, out_lens, __ = model(inputs, inputs_lens)

# decode
decoder = BeamCTCDecoder(labels,
                         lm_path='./data/language_models/cv.lm',
                         alpha=0.8,
                         beta=1.,
                         cutoff_top_n=40,
                         cutoff_prob=1.,
                         beam_width=100,
                         num_processes=4)
target_decoder = GreedyDecoder(labels)
split_transcripts = []
offset = 0
for size in transcript_lens:
    split_transcripts.append(transcript[offset:offset + size])
    offset += size
decoded_output, _ = decoder.decode(out_text.data.transpose(0, 1), out_lens)
target_strings = target_decoder.convert_to_strings(split_transcripts)


# output
print(model._meta['accents_dict'])
print(out_text, out_accent)
print(target_strings)
transcript_out = list(filter(None, [transcript_map.get(x) for x in list(target_strings)]))
print(transcript_out)
