from keras.callbacks import ModelCheckpoint, TensorBoard
import time
import os
from datetime import datetime
from src.algorithm.generator import Generator
from src.utils import helper
from src.algorithm import model

import numpy as np


def run(epochs=5000, batch_size=256):
    data_path = helper.root_dir() + '/data/'

    generator = Generator(batch_size=batch_size)
    num_training_samples = generator.training_dataset.shape[0]
    num_validation_samples = generator.validation_dataset.shape[0]

    print('Number of training samples:', num_training_samples)
    print('Number of validation samples:', num_validation_samples)

    nn = model.generate(max_token_length=generator.MAX_TOKEN_LENGTH, vocabulary_size=generator.VOCABULARY_SIZE)
    nn.compile(loss='categorical_crossentropy', optimizer='adam')

    models_path = data_path + '/weights/' + datetime.now().strftime('%Y-%m-%d-%H-%M')
    os.makedirs(models_path)
    model_names = (models_path + '/nn_weights.{epoch:02d}-{val_loss:.2f}.hdf5')
    model_checkpoint = ModelCheckpoint(model_names,
                                       monitor='loss',
                                       verbose=0,
                                       save_best_only=True,
                                       mode='min')
    tboard = TensorBoard(log_dir=data_path + '/tboard/' + datetime.now().strftime('%Y-%m-%d-%H-%M'))

    callbacks = [model_checkpoint, tboard]

    # model.fit_generator(generator=generator.flow(mode='train'),
    #                     steps_per_epoch=int(num_training_samples / batch_size),
    #                     epochs=num_epochs,
    #                     verbose=1,
    #                     callbacks=callbacks,
    #                     validation_data=generator.flow(mode='validation'),
    #                     validation_steps=int(num_validation_samples / batch_size))

    nn.fit_generator(generator=generator.flow(train=True),
                     epochs=epochs,
                     steps_per_epoch=int(num_training_samples / batch_size),
                     validation_data=generator.flow(train=False),
                     validation_steps=int(num_validation_samples / batch_size),
                     callbacks=callbacks,
                     verbose=1)

    features = generator.image_names_to_features['1000268201_693b08cb0e.jpg']
    text = np.zeros((1, generator.MAX_TOKEN_LENGTH, generator.VOCABULARY_SIZE))

    begin_token_id = generator.word_to_id[generator.BOS]
    text[0, 0, begin_token_id] = 1
    image_features = np.zeros((1, generator.MAX_TOKEN_LENGTH, generator.IMG_FEATS))
    image_features[0, 0, :] = features
    print(generator.BOS, end=' ')
    for word_arg in range(generator.MAX_TOKEN_LENGTH - 1):
        predictions = nn.predict([text, image_features])
        word_id = np.argmax(predictions[0, word_arg, :])
        next_word_arg = word_arg + 1
        text[0, next_word_arg, word_id] = 1
        word = generator.id_to_word[word_id]

        if word != generator.EOS:
            print(word, end=' ')

    print(generator.EOS)


if __name__ == '__main__':
    start = time.time()
    run(epochs=1, batch_size=1)
    end = time.time()
    seconds = end - start
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("Train time: %d:%02d:%02d" % (h, m, s))
