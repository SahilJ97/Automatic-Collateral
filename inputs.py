from params import *
import numpy as np

zero_frame = np.zeros((299, 299))


def zero_pad(raw_seq):
    seq = raw_seq
    n = INPUT_SEQ_LENGTH - len(seq)
    if n < 0:
        raise ValueError('INPUT_SEQ_LENGTH is less than raw sequence length by a difference of {}'.format(n))
    for i in range(n):
        seq.append(zero_frame)
    return seq


def get_data():
    train_X, train_Y, test_X, test_Y = None, None, None, None
    return train_X, train_Y, test_X, test_Y