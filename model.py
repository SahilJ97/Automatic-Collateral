from keras.models import Sequential
from keras.layers import Activation, LSTM
from keras.applications.inception_v3 import InceptionV3
from params import *


model = Sequential([
    InceptionV3(include_top=False, weights='imagenet', input_shape=(3, 299, 299), pooling='max'),
    LSTM(HL_SIZE, activation='softplus'),
    LSTM(N_CLASSES, activation='softmax')
])