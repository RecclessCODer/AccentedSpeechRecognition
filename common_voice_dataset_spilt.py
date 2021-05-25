import random
from utils import read_manifest, write_manifest
import os

"""
script function: use cv-corpus-5.1-2020-06-22 English corpus. 
split it by using accent labels.
using four manifest, train, test, dev and validated manifest.
16 accents, 2 accents scotland, ireland as unseen test set, others as train, dev and test.
split these into train_data, dev_data, test_data, test_scotland, test_ireland
"""


def count_accent(manifest):
    """
    count accents in all manifests
    """
    acc_set = set()
    for __, __, __, __, __, __, __, accent, __, __, in manifest:
        acc_set.add(accent)
    if "" in acc_set:
        acc_set.remove("")  # no usage in accent speech recognition, delete
    if 'other' in acc_set:
        acc_set.remove("other")
    enum = enumerate(sorted(acc_set))  # sorted set for consistent results
    acc_dic = {acc: x for x, acc in enum}
    return acc_dic, acc_set


def count_speaker(manifest):
    """
    count the number of speakers
    """
    speaker_set = set()
    for speaker, __, __, __, __, __, __, __, __, __, in manifest:
        speaker_set.add(speaker)
    enum = enumerate(sorted(speaker_set))
    speaker_dic = {speaker: x for x, speaker in enum}
    return speaker_dic


def statistic_accent(manifest, _accent_dic, _accent_set):
    """
    count accent sentence for each accents.
    """
    _all_accent_data = []
    count = _accent_dic.copy()  # create a dict of {accents: numbers of sentences}
    for accent_name in _accent_dic.keys():
        count[accent_name] = 0  # initial count number
    for i in range(0, len(manifest)):
        no, no, no, no, no, no, no, a, no, no, = manifest[i]
        if a in _accent_set:
            _all_accent_data.append(all_data[i])  # create a manifest with accent labels
            count[a] = count[a] + 1  # count numbers of accent sentences
    return _all_accent_data, count


def split_manifest(data):
    """
    split data into five data, train_accent_data 90%, dev_accent_data 5%, test_accent_data 5%
    test_scotland_data, test_ireland_data.
    """
    refine_data = []  # stored data except scotland data and ireland data
    test_scot_data, test_ire_data = [], []
    for i in range(0, len(data)):
        no, no, no, no, no, no, no, a, no, no, = data[i]
        if a == 'scotland':
            test_scot_data.append(data[i])
        elif a == 'ireland':
            test_ire_data.append(data[i])
        else:
            refine_data.append(data[i])
    train_accent_data_length = int(len(refine_data) * 0.9)  # 90% train data
    dev_accent_data_length = int(len(refine_data) * 0.05)  # 5% dev data
    # test_accent_data_length = int(len(refine_data) - train_accent_data_length - dev_accent_data_length)
    # others as test data
    shuffled_data = random.sample(refine_data, len(refine_data))  # shuffle the data and split it
    train_accent_data = shuffled_data[0: train_accent_data_length]
    dev_accent_data = shuffled_data[train_accent_data_length: train_accent_data_length + dev_accent_data_length]
    test_accent_data = shuffled_data[train_accent_data_length + dev_accent_data_length:]
    return train_accent_data, dev_accent_data, test_accent_data, test_scot_data, test_ire_data


def create_tiny_dataset(data, _accent_set):
    """
    create a comparatively small one of the giant dataset.
    origin size 770,629 - > cut size 70,000
    """
    # cut the data by cutting every accent data with same ratio
    ratio = 0.1
    shuffled_data = random.sample(data, len(data))  # shuffle the a_data and split it
    acc_data_tiny = (shuffled_data[0: int(ratio * len(shuffled_data))])
    # cut and save in acc_data_tiny
    return acc_data_tiny


dev_manifest_path = '../cv-corpus-5.1-2020-06-22/en/dev.tsv'
train_manifest_path = '../cv-corpus-5.1-2020-06-22/en/train.tsv'
test_manifest_path = '../cv-corpus-5.1-2020-06-22/en/test.tsv'
validated_manifest_path = '../cv-corpus-5.1-2020-06-22/en/validated.tsv'
_mp3_path = '..//cv-corpus-5.1-2020-06-22/en/clips/'

dev_data = read_manifest(dev_manifest_path)
train_data = read_manifest(train_manifest_path)
test_data = read_manifest(test_manifest_path)
validated_data = read_manifest(validated_manifest_path)
all_data = dev_data + train_data + test_data + validated_data

# remove those lines which do not have mp3 reference
print("###### accent data ######")
print("size:", len(all_data))
accent_dic, accent_set = count_accent(all_data)  # count the number of accents
print("------ accents structure ------")
print(accent_dic)
all_accent_data, accent_sentence_count = statistic_accent(all_data, accent_dic, accent_set)
# count number of sentences for each accent
print("------ the number of sentences in each accent ------")
print(accent_sentence_count)
train_data, dev_data, test_data, test_scot, test_ire = split_manifest(all_accent_data)
print("------ split data structure ------")
print("train_data size: ", len(train_data), " dev_data size: ", len(dev_data),
" test_data size: ", len(test_data), " test_scot size: ", len(test_scot),
" test_ire size: ", len(test_ire))

# tiny data cut from origin one.
print("###### tiny data ######")
all_data_t = create_tiny_dataset(all_accent_data, accent_set)
print("size:", len(all_data_t))
accent_dic, accent_set = count_accent(all_data_t)
print("------ accents structure -------")
print(accent_dic)
all_accent_data_t, accent_sentence_count_t = statistic_accent(all_data_t, accent_dic, accent_set)
print("------ the number of sentences in each accent ------")
print(accent_sentence_count_t)
train_data_t, dev_data_t, test_data_t, test_scot_t, test_ire_t = split_manifest(all_data_t)
print("------ split data structure ------")
print("train_data_t size: ", len(train_data_t), " dev_data_t size: ", len(dev_data_t),
" test_data_t size: ", len(test_data_t), " test_scot_t size: ", len(test_scot_t),
" test_ire_t size: ", len(test_ire_t))


# write into tsv format
write_manifest(train_data, 'train_accent_manifest.tsv')
write_manifest(dev_data, 'dev_accent_manifest.tsv')
write_manifest(test_data, 'test_accent_manifest.tsv')
write_manifest(test_scot, 'test_scotland_accent_manifest.tsv')
write_manifest(test_ire, 'test_ireland_accent_manifest.tsv')
write_manifest(train_data_t, 'train_accent_t_manifest.tsv')
write_manifest(dev_data_t, 'dev_accent_t_manifest.tsv')
write_manifest(test_data_t, 'test_accent_t_manifest.tsv')
write_manifest(test_scot_t, 'test_scotland_accent_t_manifest.tsv')
write_manifest(test_ire_t, 'test_ireland_accent_t_manifest.tsv')
print("------ finished split ------")

