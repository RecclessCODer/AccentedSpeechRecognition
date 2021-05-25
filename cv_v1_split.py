from utils import read_csv_manifest, write_csv_manifest


def read_accent_split_list(path):
    with open(path, encoding='UTF-8') as f:
        accent_list = [line.strip().split(' ') for line in f.readlines()]
    return accent_list


def extract_accent_data(data):
    accent_data = []
    for sample in data:
        accent = sample[6]
        if accent != '':
            accent_data.append(sample)
    return accent_data


def find_element(data, element):
    for e in data:
        path = e[0]
        name2 = path.split('/')[1].split('.')[0]
        if element == name2:
            return e
    print("could not found in data" + name2)


def compare_list(dev_data_, train_data_, test_data_, list_given):
    """
    check the difference between original list and the given list.
    merge given list to dataset.
    """
    data = []
    for element in list_given:
        path = element[1]
        name1 = path.split('/')[3]
        name2 = path.split('/')[4].split('.')[0]
        if name1 == 'cv-valid-dev':
            ele = find_element(dev_data_, name2)
            data.append(ele)
            dev_data_.remove(ele) if ele is not None else None
        elif name1 == 'cv-valid-train':
            ele = find_element(train_data_, name2)
            data.append(ele)
            train_data_.remove(ele) if ele is not None else None
        elif name1 == 'cv-valid-test':
            ele = find_element(test_data_, name2)
            data.append(ele)
            test_data_.remove(ele) if ele is not None else None
        else:
            print("do not belong to any cv-valid data Error element" + name1 + '/' + name2)
    return data


dev_data = read_csv_manifest('../../cv_corpus_v1/cv-valid-dev.csv')
train_data = read_csv_manifest('../../cv_corpus_v1/cv-valid-train.csv')
test_data = read_csv_manifest('../../cv_corpus_v1/cv-valid-test.csv')
dev_accent_list = read_accent_split_list('../../cv_corpus_v1/dev')
train_accent_list = read_accent_split_list('../../cv_corpus_v1/train')
test_accent_list = read_accent_split_list('../../cv_corpus_v1/test')
testnz_accent_list = read_accent_split_list('../../cv_corpus_v1/testnz')
testindian_accent_list = read_accent_split_list('../../cv_corpus_v1/testindian')
path_list = './data/'

dev_accent_data = extract_accent_data(dev_data)
train_accent_data = extract_accent_data(train_data)
test_accent_data = extract_accent_data(test_data)

testindian_accent_data = compare_list(dev_accent_data, train_accent_data, test_accent_data, testindian_accent_list)
testnz_accent_data = compare_list(dev_accent_data, train_accent_data, test_accent_data, testnz_accent_list)
dev_accent_data = compare_list(dev_accent_data, train_accent_data, test_accent_data, dev_accent_list)
train_accent_data = compare_list(dev_accent_data, train_accent_data, test_accent_data, train_accent_list)
test_accent_data = compare_list(dev_accent_data, train_accent_data, test_accent_data, test_accent_list)

write_csv_manifest(testindian_accent_data, path_list, 'testindian.csv')
write_csv_manifest(testnz_accent_data, path_list, 'testnz.csv')
write_csv_manifest(dev_accent_data, path_list, 'dev.csv')
write_csv_manifest(train_accent_data, path_list, 'train.csv')
write_csv_manifest(test_accent_data, path_list, 'test.csv')

print("ok")
