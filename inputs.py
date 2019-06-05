from params import *
import numpy as np
import glob
from matplotlib.image import imread
import re

zero_frame = np.zeros((299, 299))


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


def zero_pad(raw_seq):
    seq = raw_seq
    print(np.shape(seq))
    n = INPUT_SEQ_LENGTH - len(seq)
    if n < 0:
        raise ValueError('INPUT_SEQ_LENGTH is less than raw sequence length by a difference of {}'.format(n))
    for i in range(n):
        seq = np.append(seq, zero_frame)
    print(np.shape(seq))
    return np.array(seq)


def label(dir):
    pattern = re.compile(r'(?<="./Images/")(.*?)(?="")')
    patient_name = re.findall(pattern, dir)[0]
    print(patient_name)


def get_data():
    x = []
    y = []
    for dir in glob.glob('./Images/*/*'):  # for each patient
        y.append(label(dir))
        data_point = []
        for subdir in glob.glob(dir + '/*'):  # for each phase
            channel_seq = []
            for file in glob.glob(subdir + '/*.jpg'):
                channel_seq.append(rgb2gray(imread(file)))
            data_point.append(zero_pad(channel_seq))
        print(np.shape(data_point))
        x.append(np.reshape(np.array(data_point), (INPUT_SEQ_LENGTH, 299, 299, 3)))






if __name__ == '__main__':
    get_data()
