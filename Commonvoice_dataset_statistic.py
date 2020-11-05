

dev_manifest_path = '../cv-corpus-5.1-2020-06-22/en/dev.tsv'
train_manifest_path = '../cv-corpus-5.1-2020-06-22/en/train.tsv'
test_manifest_path = '../cv-corpus-5.1-2020-06-22/en/test.tsv'
validated_manifest_path = '../cv-corpus-5.1-2020-06-22/en/validated.tsv'
segment = ""


def read_manifest(path):
    """
    read manifest into samples data
    """
    with open(path, encoding='UTF-8') as f:
        f.readline()
        # data_key = f.readline().strip().split('\t')  # keys' names
        data = [line.strip().split('\t') for line in f.readlines()]  # samples list
    # append an empty segment string to those who doesnt have one
    for x in range(0, len(data)):
        if len(data[x]) == 9:
            data[x].append(segment)
    return data


def count_accent(_dev_data, _train_data, _test_data, _validated_data):
    """
    count accents in all spilt manifest
    """
    acc_set = set()
    for manifest in _dev_data, _train_data, _test_data, _validated_data:
        for __, __, __, __, __, __, __, accent, __, __, in manifest:
            acc_set.add(accent)
    acc_set.remove("")  # no usage in accent speech recognition, delete
    acc_set.remove("other")
    enum = enumerate(sorted(acc_set))  # sorted set for consistent results
    acc_dic = {acc: x for x, acc in enum}
    return acc_dic, acc_set


def count_speaker(manifest):
    speaker_set = set()
    for speaker, __, __, __, __, __, __, __, __, __, in manifest:
        speaker_set.add(speaker)
    enum = enumerate(sorted(speaker_set))
    speaker_dic = {speaker: x for x, speaker in enum}
    return speaker_dic


def statistic_accent(_dev_data, _train_data, _test_data, _validated_data, _accent_set):
    """
    count accent sentence for each accents.
    """
    all_data = dev_data + train_data + test_data + validated_data
    all_accent_data = []
    accent_sentence_count = accent_dic.copy()
    for accent_name in accent_dic.keys():
        accent_sentence_count[accent_name] = 0  # initial count number
    for i in range(0, len(all_data)):
        no, no, no, no, no, no, no, a, no, no, = all_data[i]
        if a in _accent_set:
            all_accent_data.append(all_data[i])  # create a manifest with accent labels
            accent_sentence_count[a] = accent_sentence_count[a] + 1
    return all_accent_data, accent_sentence_count


def spilt_manifest(all_acc_data, _accent_set): #  TODO implement
    """
    spilt data into five data, train_accent_data, dev_accent_data, test_accent_data
    test_scotland_data, test_ireland_data.
    """

    train_accent_data

    return train_accent_data, dev_accent_data, test_accent_data, test_scotland_data, test_ireland_data


dev_data = read_manifest(dev_manifest_path)
train_data = read_manifest(train_manifest_path)
test_data = read_manifest(test_manifest_path)
validated_data = read_manifest(validated_manifest_path)

accent_dic, accent_set = count_accent(dev_data, train_data, test_data, validated_data)  # count accents number
print(accent_dic)

new_accent_data, accent_sentence_num = statistic_accent(dev_data, train_data, test_data, validated_data, accent_set)  # count sentences for each accent
print(accent_sentence_num)



