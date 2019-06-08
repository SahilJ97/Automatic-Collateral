from params import *
import numpy as np
import glob
from matplotlib.image import imread
import os
import csv
import random

scores = {}
zero_frame = np.zeros((299, 299))

with open("scores.csv", "r") as f:
    reader = csv.reader(f)
    headers = next(reader)[1:]
    for row in reader:
        scores[row[0]] = {key: value for key, value in zip(headers, row[1:])}


def zero_pad(raw_seq):
    seq = raw_seq
    n = INPUT_SEQ_LENGTH - len(seq)
    if n < 0:
        raise ValueError('INPUT_SEQ_LENGTH is less than raw sequence length by a difference of {}'.format(n))
    for i in range(n):
        seq = np.append(seq, zero_frame)
    return seq


def label(dir):
    label = [0 for i in range(len(CLASS_INDICES))]
    dir = dir.replace('./Images/', '')
    patient_name = ''
    for c in dir:
        if c == '/':
            break
        patient_name = patient_name + c
    grade = int(scores[patient_name]['mCTA collateral score'])
    label[CLASS_INDICES[grade]] = 1
    return label


def get_data():
    x = []
    y = []
    for item in glob.glob('./Images/*/*'):  # for each patient
        if not os.path.isdir(item):
            continue
        y.append(label(item))
        data_point = []
        for subdir in glob.glob(item + '/*'):  # for each phase
            channel_seq = []
            for file in glob.glob(subdir + '/*.jpg'):
                channel_seq.append(imread(file))
            data_point = np.append(data_point, zero_pad(channel_seq))
        x.append(np.reshape(data_point, (INPUT_SEQ_LENGTH, 299, 299, 3)))

    return np.array(x), np.array(y)

if __name__ == '__main__':
    get_data()
