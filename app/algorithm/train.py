from keras.callbacks import ModelCheckpoint, TensorBoard
import time
import os
from datetime import datetime
from app.algorithm.generator import Generator
from app.algorithm import helper
from app.algorithm import model

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
                                       verbose=1,
                                       save_best_only=True,
                                       mode='min')
    tboard = TensorBoard(log_dir=data_path + '/tboard/' + datetime.now().strftime('%Y-%m-%d-%H-%M'))

    callbacks = [model_checkpoint, tboard]

    nn.fit_generator(generator=generator.flow(train=True),
                     epochs=epochs,
                     steps_per_epoch=int(num_training_samples / batch_size),
                     validation_data=generator.flow(train=False),
                     validation_steps=int(num_validation_samples / batch_size),
                     callbacks=callbacks,
                     verbose=1)


def main():
    start = time.time()
    run(epochs=100, batch_size=64)
    end = time.time()
    seconds = end - start
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("Train time: %d:%02d:%02d" % (h, m, s))
    