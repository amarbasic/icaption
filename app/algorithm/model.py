from keras import Input, Model
from keras.layers import Masking, TimeDistributed, Dense, Dropout, Add, LSTM
from keras.regularizers import l2
from keras.utils import plot_model


def generate(max_token_length, vocabulary_size):
    num_image_features = 1000
    hidden_size = 1024
    embedding_size = 512
    regularizer = 1e-8

    text_input = Input(shape=(max_token_length, vocabulary_size), name='text')
    text_mask = Masking(mask_value=0.0, name='text_mask')(text_input)
    text_to_embedding = TimeDistributed(Dense(units=embedding_size,
                                              kernel_regularizer=l2(regularizer),
                                              name='text_embedding'))(text_mask)

    text_dropout = Dropout(.5, name='text_dropout')(text_to_embedding)

    # image embedding
    image_input = Input(shape=(max_token_length, num_image_features),
                        name='image')
    image_embedding = TimeDistributed(Dense(units=embedding_size,
                                            kernel_regularizer=l2(regularizer),
                                            name='image_embedding'))(image_input)
    image_dropout = Dropout(.5, name='image_dropout')(image_embedding)

    recurrent_inputs = [text_dropout, image_dropout]

    merged_input = Add()(recurrent_inputs)

    recurrent_network = LSTM(units=hidden_size,
                             recurrent_regularizer=l2(regularizer),
                             kernel_regularizer=l2(regularizer),
                             bias_regularizer=l2(regularizer),
                             return_sequences=True,
                             name='recurrent_network')(merged_input)

    output = TimeDistributed(Dense(units=vocabulary_size,
                                   kernel_regularizer=l2(regularizer),
                                   activation='softmax'),
                             name='output')(recurrent_network)

    inputs = [text_input, image_input]
    model = Model(inputs=inputs, outputs=output)
    return model
