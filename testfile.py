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

"""

### dataset and dataloader


