from keras.models import Sequential
from keras.layers import LSTM, TimeDistributed, Dense
from keras.applications.inception_v3 import InceptionV3
from params import *
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from inputs import get_data


model = Sequential([
    TimeDistributed(
        InceptionV3(include_top=False, weights='imagenet', input_shape=((299, 299, 3)), pooling='max'),
        input_shape=(INPUT_SEQ_LENGTH, 299, 299, 3)
    ),
    LSTM(HL_SIZE, activation='softplus'),
    Dense(N_CLASSES, activation='softmax')
])

adam = Adam(lr=LR, decay=0.0)
model.compile(loss='mean_squared_error', optimizer=adam, metrics=['accuracy'])


if __name__ == '__main__':
    train_X, train_Y, test_X, test_Y = get_data()

    history = model.fit(train_X, train_Y, epochs=EPOCHS, batch_size=BATCH_SIZE)
    model.save(MODEL_PATH)

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model Accuracy (HL_SIZE={})'.format(HL_SIZE))
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss (HL_SIZE={})'.format(HL_SIZE))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    model.evaluate(test_X, test_Y)
