

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


def name_str(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]


dev_data = read_csv_manifest('../../cv_corpus_v1/dev.csv')
train_data = read_csv_manifest('../../cv_corpus_v1/train.csv')
test_data = read_csv_manifest('../../cv_corpus_v1/test.csv')

for e_data in dev_data, train_data, test_data:
    for element in e_data:
        element.append('ivector_path')
        element.append('embedding_path')
        temp = element[2]
        element[2] = element[4]
        element[4] = temp
    write_csv_manifest(e_data, 'list_' + name_str(e_data, globals())[0] + '.csv')

