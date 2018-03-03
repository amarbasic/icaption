import numpy as np
import pickle
from src.utils import helper
import pandas as pd


class Generator(object):
    def __init__(self, batch_size=1):
        self.data_path = helper.root_dir() + '/data/'
        self.dictionary = None
        self.training_dataset = None
        self.validation_dataset = None
        self.image_names_to_features = None

        data_logs = np.genfromtxt(self.data_path + 'data_parameters.log', delimiter=' ', dtype='str')
        data_logs = dict(zip(data_logs[:, 0], data_logs[:, 1]))

        self.MAX_TOKEN_LENGTH = int(data_logs['max_caption_length:']) + 2
        self.IMG_FEATS = int(data_logs['IMG_FEATS:'])
        self.BOS = str(data_logs['BOS:'])
        self.EOS = str(data_logs['EOS:'])
        self.PAD = str(data_logs['PAD:'])
        self.VOCABULARY_SIZE = None
        self.word_to_id = None
        self.id_to_word = None
        self.BATCH_SIZE = batch_size

        self._load_dataset()
        self._load_vocabulary()
        self._load_image_features()

    def _load_dataset(self):
        print('Load dataset ...', end=' ')
        # Loading train data
        train_data = pd.read_table(self.data_path + '/train.txt', delimiter='*')
        train_data = np.asarray(train_data, dtype=str)
        self.training_dataset = train_data
        # Load validation data
        test_data = pd.read_table(self.data_path + '/test.txt', delimiter='*')
        test_data = np.asarray(test_data, dtype=str)
        self.validation_dataset = test_data
        print('Done')

    def _load_vocabulary(self):
        print('Load vocabulary ...', end=' ')
        word_to_id = pickle.load(open(self.data_path + '/word_to_id.p', 'rb'))
        id_to_word = pickle.load(open(self.data_path + '/id_to_word.p', 'rb'))
        self.VOCABULARY_SIZE = len(word_to_id)
        self.word_to_id = word_to_id
        self.id_to_word = id_to_word
        print('Done')

    def _load_image_features(self):
        print('Load image features ...', end=' ')
        self.image_names_to_features = pickle.load(open(self.data_path + '/extracted_features.p', 'rb'))
        print('Done')

    def _make_empty_batch(self):
        captions_batch = np.zeros((self.BATCH_SIZE, self.MAX_TOKEN_LENGTH,
                                   self.VOCABULARY_SIZE))
        images_batch = np.zeros((self.BATCH_SIZE, self.MAX_TOKEN_LENGTH,
                                 self.IMG_FEATS))
        targets_batch = np.zeros((self.BATCH_SIZE, self.MAX_TOKEN_LENGTH,
                                  self.VOCABULARY_SIZE))
        return captions_batch, images_batch, targets_batch

    def _format_to_one_hot(self, caption):
        tokenized_caption = caption.split()
        tokenized_caption = [self.BOS] + tokenized_caption + [self.EOS]
        one_hot_caption = np.zeros((self.MAX_TOKEN_LENGTH,
                                    self.VOCABULARY_SIZE))
        word_ids = [self.word_to_id[word] for word in tokenized_caption
                    if word in self.word_to_id]
        for sequence_arg, word_id in enumerate(word_ids):
            one_hot_caption[sequence_arg, word_id] = 1
        return one_hot_caption

    def _get_image_features(self, image_name):
        image_features = self.image_names_to_features[image_name]
        image_input = np.zeros((self.MAX_TOKEN_LENGTH, self.IMG_FEATS))
        image_input[0, :] = image_features
        return image_input

    def _get_one_hot_target(self, one_hot_caption):
        one_hot_target = np.zeros_like(one_hot_caption)
        one_hot_target[:-1, :] = one_hot_caption[1:, :]
        return one_hot_target

    def _wrap_in_dictionary(self, one_hot_caption,
                            image_features,
                            one_hot_target):

        return [{'text': one_hot_caption,
                'image': image_features},
                {'output': one_hot_target}]

    def _check_if_image_features_exists(self, image_name):
        if image_name in self.image_names_to_features:
            return True
        print("Image {} does not exist.".format(image_name))
        return False

    def flow(self, train=True):
        if train:
            data = self.training_dataset
        else:
            data = self.validation_dataset
        image_names = data[:, 0].tolist()
        captions_batch, images_batch, targets_batch = self._make_empty_batch()
        batch_counter = 0

        while True:
            for data_arg, image_name in enumerate(image_names):
                if self._check_if_image_features_exists(image_name):
                    caption = data[data_arg, 1]

                    one_hot_caption = self._format_to_one_hot(caption)
                    captions_batch[batch_counter, :, :] = one_hot_caption
                    targets_batch[batch_counter, :, :] = self._get_one_hot_target(one_hot_caption)
                    images_batch[batch_counter, :, :] = self._get_image_features(image_name)

                    if batch_counter >= (self.BATCH_SIZE - 1):
                        yield_dictionary = self._wrap_in_dictionary(captions_batch,
                                                                    images_batch,
                                                                    targets_batch)
                        yield yield_dictionary

                        captions_batch, images_batch, targets_batch = self._make_empty_batch()
                        batch_counter = 0
                    else:
                        batch_counter += 1
