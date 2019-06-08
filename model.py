from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model
from keras.layers import LSTM, TimeDistributed, Dense
from keras.applications.inception_v3 import InceptionV3
from params import *
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from inputs import get_data


model = Sequential([
    TimeDistributed(
        InceptionV3(include_top=False, weights='imagenet', input_shape=(299, 299, 3), pooling='max'),
        input_shape=(INPUT_SEQ_LENGTH, 299, 299, 3)
    ),
    LSTM(HL_SIZE, activation='softplus'),
    Dense(len(CLASS_INDICES), activation='softmax')
])

if LOAD_OLD:
    model = load_model(MODEL_PATH)

checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
adam = Adam(lr=LR, decay=0.0)
model.compile(loss='mean_squared_error', optimizer=adam, metrics=['accuracy'])


if __name__ == '__main__':
    print('Loading data...')
    X, Y = get_data()
    print('Fitting model...')

    history = model.fit(X, Y, validation_split=VAL_SPLIT, epochs=EPOCHS, batch_size=BATCH_SIZE, shuffle=True, callbacks=[checkpoint])

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model Accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
