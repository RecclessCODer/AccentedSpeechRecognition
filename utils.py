import torch
import numpy as np
import time


def tile(a, dim, n_tile):
    """Expands a tensor amongst a given dimension, repeating its components."""
    init_dim = a.size(dim)
    repeat_idx = [1] * a.dim()
    repeat_idx[dim] = n_tile
    a = a.repeat(*(repeat_idx))
    order_index = torch.LongTensor(np.concatenate([init_dim * np.arange(n_tile) + i for i in range(init_dim)]))
    if a.is_cuda:
        order_index = order_index.cuda()
    return torch.index_select(a, dim, order_index)


def now_str():
    return time.strftime("%d-%m-%Y_%Hh%Mm%S")


def read_manifest(path):
    """
    read tsv manifest into samples data
    """
    small_data = []
    segment = ""
    with open(path, encoding='UTF-8') as f:
        f.readline()
        # data_key = f.readline().strip().split('\t')  # keys' names
        data = [line.strip().split('\t') for line in f.readlines()]  # samples list
    # append an empty segment string to which does not have one, to keep the size of info same.
    for x in range(0, len(data)):
        if len(data[x]) == 9:
            data[x].append(segment)
    return data


def write_manifest(manifest, name):
    """
    write manifest into a tsv format.
    stored in data/
    """
    f = open('./data/' + name, 'w', encoding='UTF-8')
    for i in range(0, len(manifest)):
        line = manifest[i][0]
        for j in range(1, len(manifest[i])):  # create tsv format lines
            line = line + '\t' + manifest[i][j]
        f.writelines(line)
        f.writelines('\n')
    return 0


def read_csv_manifest(path):
    """
    read csv manifest into samples data
    """
    with open(path, encoding='UTF-8') as f:
        f.readline()
        data = [line.strip().split(',') for line in f.readlines()]  # samples list
    # append an empty segment string to which does not have one, to keep the size of info same.
    return data


def read_csv_nt_manifest(path):
    """
    read csv manifest into samples data
    """
    with open(path, encoding='UTF-8') as f:
        data = [line.strip().split(',') for line in f.readlines()]  # samples list
    # append an empty segment string to which does not have one, to keep the size of info same.
    return data


def write_csv_manifest(manifest, path, name):
    """
    write manifest into a csv format.
    stored in data/
    """
    f = open(path + name, 'w', encoding='UTF-8')
    for i in range(0, len(manifest)):
        line = manifest[i][0]
        for j in range(1, len(manifest[i])):  # create tsv format lines
            line = line + ',' + manifest[i][j]
        f.writelines(line)
        f.writelines('\n')
    return 0

