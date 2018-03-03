from app.repository import images_repository
from PIL import Image
import io
import base64
import cv2
import numpy as np
from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.preprocessing import image
import os
from app.algorithm.generator import Generator
from app.algorithm import model
from app.algorithm import helper
from app.helpers.singleton import Singleton

@Singleton
class CaptionGenerator:
    def __init__(self):
        self.image_model = InceptionV3(weights='imagenet')
        self.generator = Generator(batch_size=32)
        self.nn = model.generate(max_token_length=self.generator.MAX_TOKEN_LENGTH, vocabulary_size=self.generator.VOCABULARY_SIZE)
        data_path = helper.root_dir() + '/data/'
        models_path = data_path + '/weights/2018-02-10-20-13'
        model_names = (models_path + '/nn_weights.01-3.13.hdf5')
        self.nn.load_weights(model_names)

    def generate_caption(self, image_id):
        captions = ""
        # Load image from base64
        image_data = images_repository.get_image_by_id(image_id).data.decode()
        # image = Image.open(io.BytesIO(base64.b64decode(image_data.split(",")[1])))
        # image_array = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

        filename = 'working_image.jpg'  # I assume you have a way of picking unique filenames
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(image_data.split(",")[1]))
        
        # Get image features InceptionV3
        
        img = image.load_img(filename, target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = self.image_model.predict(img)

        # Generate captions
        
        text = np.zeros((1, self.generator.MAX_TOKEN_LENGTH, self.generator.VOCABULARY_SIZE))
        
        begin_token_id = self.generator.word_to_id[self.generator.BOS]
        text[0, 0, begin_token_id] = 1
        image_features = np.zeros((1, self.generator.MAX_TOKEN_LENGTH, self.generator.IMG_FEATS))
        image_features[0, 0, :] = features
        
        for word_arg in range(self.generator.MAX_TOKEN_LENGTH - 1):
            predictions = self.nn.predict([text, image_features])
            word_id = np.argmax(predictions[0, word_arg, :])
            next_word_arg = word_arg + 1
            text[0, next_word_arg, word_id] = 1
            word = self.generator.id_to_word[word_id]

            if word != self.generator.EOS:
                captions += word + " "

        os.remove(filename)

        images_repository.update_image_caption(image_id, captions)

        return captions
