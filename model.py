from keras.models import Sequential
from keras.layers import Activation, LSTM
from keras.applications.inception_v3 import InceptionV3
from params import *
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from inputs import get_data


model = Sequential([
    InceptionV3(include_top=False, weights='imagenet', input_shape=(3, 299, 299), pooling='max'),
    LSTM(HL_SIZE, activation='softplus'),
    LSTM(N_CLASSES, activation='softmax')
])

adam = Adam(lr=0.001, decay=0.0)
model.compile(loss='mean_squared_error', optimizer=adam)


if __name__ == '__main__':
    train_X, train_Y, test_X, test_Y = get_data()

    history = model.fit(train_X, train_Y, epochs=EPOCHS, batch_size=BATCH_SIZE, metrics=['accuracy'])
    model.save(MODEL_PATH)

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    model.evaluate(test_X, test_Y)
