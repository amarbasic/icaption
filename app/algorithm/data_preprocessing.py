import time
from collections import Counter
from itertools import chain
from string import digits

import numpy as np
import pickle

import os

from keras.applications.inception_v3 import preprocess_input
from keras.applications import InceptionV3
from keras.preprocessing import image

from app.algorithm import helper


class DataPreprocessing(object):
    def __init__(self, run_inception=False, word_threshold=-1):
        self.root_path = helper.root_dir()
        self.word_threshold = word_threshold
        self.max_caption_length = 0
        self.run_inception = run_inception
        self.IMG_FEATURES = 1000 # inception model
        self.BOS = '<S>'  # Beginning Of Sentence
        self.EOS = '<E>'  # End Of Sentence
        self.PAD = '<P>'
        self.word_frequencies = None
        self.captions = None
        self.image_files = None
        self.image_features = None
        self.word_to_id = None
        self.id_to_word = None
        self.extracted_features = None
        self.features_file_names = None
        self.image_feature_files = None
        self.vocabulary_size = 0

    def run(self):
        start = time.time()
        self._load()
        self._process_captions()
        self.word_frequencies = Counter(chain(*self.captions)).most_common()
        self._remove_infrequent_words()
        self._construct_dictionary()
        if self.run_inception:
            self._extract_image_features()
        self._write_data()
        end = time.time()
        seconds = end - start
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print("Processing time: %d:%02d:%02d" % (h, m, s))

    def _write_data(self):
        log_file = open(self.root_path + '/data/data_parameters.log', 'w')
        log_file.write('BOS: %s \n' % self.BOS)
        log_file.write('EOS: %s \n' % self.EOS)
        log_file.write('PAD: %s \n' % self.PAD)
        log_file.write('IMG_FEATS: %s \n' % self.IMG_FEATURES)
        log_file.write('word_frequency_threshold: %s \n' % self.word_threshold)
        log_file.write('max_caption_length: %s \n' % self.max_caption_length)
        log_file.close()

        data_file = open(self.root_path + '/data/data.txt', 'w')
        data_file.write('image_names*caption\n')
        for image_arg, image_name in enumerate(self.image_files):
            caption = ' '.join(self.captions[image_arg])
            data_file.write('%s*%s\n' % (image_name, caption))
        data_file.close()

    def _extract_image_features(self):
        print('Extracting image features')
        image_model = InceptionV3(weights='imagenet')
        self.extracted_features = {}
        self.image_feature_files = list(set(self.image_files))
        number_of_images = len(self.image_feature_files)
        for image_arg, image_file in enumerate(self.image_feature_files):
            image_path = self.root_path + '/data/Flicker8k_Dataset/' + image_file
            if image_arg % 100 == 0:
                print('%.2f %% completed' % round(100 * image_arg / number_of_images, 2))
            if os.path.exists(image_path):
                img = image.load_img(image_path, target_size=(224, 224))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                img = preprocess_input(img)
                CNN_features = image_model.predict(img)
                self.extracted_features[image_file] = np.squeeze(CNN_features)
        print('100 % completed')
        print('Writing image features ... ', end='')
        pickle.dump(self.extracted_features, open(self.root_path + '/data/' + 'extracted_features.p', 'wb'))
        print('Done')

    def _construct_dictionary(self):
        print('Build dictionary ... ', end='')
        words = [word for word, freq in self.word_frequencies]
        self.word_to_id = {self.PAD: 0, self.BOS: 1, self.EOS: 2}
        self.word_to_id.update({word: word_id for word_id, word in enumerate(words, 3)})
        self.id_to_word = {word_id: word for word, word_id in self.word_to_id.items()}
        pickle.dump(self.word_to_id, open(self.root_path + '/data/word_to_id.p', 'wb'))
        pickle.dump(self.id_to_word, open(self.root_path + '/data/id_to_word.p', 'wb'))
        print('Done')

    def _remove_infrequent_words(self):
        print('Removing words with a frequency less than {} ... '.format(self.word_threshold), end='')
        word_frequencies = []
        for word, freq in self.word_frequencies:
            if freq > self.word_threshold:
                word_frequencies.append((word, freq))
        self.word_frequencies = word_frequencies
        self.vocabulary_size = len(self.word_frequencies)
        print('Done')
        print('Vocabulary size: {}'.format(self.vocabulary_size))

    def _process_captions(self):
        captions = []
        for caption in self.captions:
            lemmatized_caption = self._lemmatize_sentence(caption)
            if len(lemmatized_caption) > self.max_caption_length:
                self.max_caption_length = len(lemmatized_caption)
            captions.append(lemmatized_caption)
        self.captions = captions

    def _lemmatize_sentence(self, caption):
        incorrect_chars = digits + ";.,'/*?¿><:{}[\]|+()"
        char_translator = str.maketrans('', '', incorrect_chars)
        quotes_translator = str.maketrans('', '', '"')
        clean_caption = caption.strip().lower()
        clean_caption = clean_caption.translate(char_translator)
        clean_caption = clean_caption.translate(quotes_translator)
        clean_caption = clean_caption.split(' ')
        return clean_caption

    def _load(self):
        print('Loading data ... ', end='')
        path = self.root_path + '/data/Flickr8k.token.txt'
        self.image_files = []
        self.captions = []
        with open(path, 'r') as file:
            for line in file:
                row = line.split("#")
                self.image_files.append(row[0])
                self.captions.append(row[1].split('\t')[1].strip())

        print('{} images loaded'.format(len(self.image_files)))


def main():
    DataPreprocessing(run_inception=True, word_threshold=5).run()
