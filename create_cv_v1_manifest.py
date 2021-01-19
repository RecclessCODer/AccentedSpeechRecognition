import json
import librosa
import pydub


def read_csv_manifest(path):
    """
    read csv manifest into samples data
    """
    with open(path, encoding='UTF-8') as f:
        data = [line.strip().split(',') for line in f.readlines()]  # samples list
    # append an empty segment string to which does not have one, to keep the size of info same.
    return data


def write_csv_manifest(manifest, name):
    """
    write manifest into a csv format.
    stored in ../../cv_corpus_v1/
    """
    f = open('../../cv_corpus_v1/' + name, 'w', encoding='UTF-8')
    for i in range(0, len(manifest)):
        line = manifest[i][0]
        for j in range(1, len(manifest[i])):  # create csv format lines
            line = line + ',' + manifest[i][j]
        f.writelines(line)
        f.writelines('\n')
    return 0


def create_manifest(data):
    new_list = []

    for element in data:

        data_list = []
        mp3_path = element[0]
        audio_name1 = mp3_path.split('/')[0]
        audio_name2 = mp3_path.split('/')[1].split('.')[0]
        name = audio_name1 + '-' + audio_name2

        # convert mp3 to wav
        sound = pydub.AudioSegment.from_mp3(path_base + mp3_path)
        sound.export(wav_path + name + '.wav', format='wav')

        # extract mfcc and save as json format
        with open(mfcc_path + name + ".json", 'w') as f:
            wav_signal, fs = librosa.load(wav_path + name + '.wav', sr=None)
            mfccs = librosa.feature.mfcc(wav_signal, sr=fs, n_mfcc=40)
            mfccs = mfccs.T  # transpose. first axis is frames, second axis is mfcc dimensions.
            mfcc = mfccs.tolist()
            json.dump(mfcc, f)  # save as json format
        f.close()
        # write mfcc path into list
        list_mfcc_path = mfcc_path + name + '.json'
        data_list.append(list_mfcc_path)

        # create transcript json files
        transcript = element[1]
        with open(transcript_path + name + ".json", 'w') as f:
            json.dump(transcript, f)  # save as json format
        f.close()
        # write transcript path into list
        list_transcript_path = transcript_path + name + '.json'
        data_list.append(list_transcript_path)

        # write accent label into list
        accent_label = element[6]
        data_list.append(accent_label)

        new_list.append(data_list)

    return new_list


manifest_path = './data/'
path_base = '../../cv_corpus_v1/'

test_list = ['dev.csv', 'test.csv', 'testnz.csv', 'testindian.csv']
for test in test_list:
    mfcc_path = path_base + 'mfcc/' + test.split('.')[0] + '/'
    transcript_path = path_base + 'transcript/' + test.split('.')[0] + '/'
    wav_path = path_base + 'wav/' + test.split('.')[0] + '/'
    accent_data = read_csv_manifest(manifest_path + test)
    new_list_t = create_manifest(accent_data)
    write_csv_manifest(new_list_t, test)
    print('each list length:')
    print(test)
    print(len(new_list_t))
