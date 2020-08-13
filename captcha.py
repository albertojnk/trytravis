

import numpy as np
import tensorflow
import tensorflow.keras as keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose, Dropout, Lambda, Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K
import cv2
from PIL import Image
from PIL import Image
from scipy.ndimage.filters import gaussian_filter
import numpy
from PIL import ImageFilter


def mudar_image(image):
        th1 = 165
        th2 = 165 # threshold after blurring 
        sig = 1 # the blurring sigma
        black_and_white =image.convert("L") #converting to black and white 
        first_threshold = black_and_white.point(lambda p: p > th1 and 255)
        blur=np.array(first_threshold) #create an image array
        blurred = gaussian_filter(blur, sigma=sig)
        blurred = Image.fromarray(blurred)
        final = blurred.point(lambda p: p > th2 and 255)
        final = final.filter(ImageFilter.EDGE_ENHANCE_MORE)
        final = final.filter(ImageFilter.SHARPEN)
        return final


class CaptchaSolver():
    def __init__(self, weights = 'model.h5'):
        self.model = self.CNN()
        self.model.load_weights(weights)
        self.model.compile(optimizer="adam", loss= [tensorflow.keras.losses.binary_crossentropy, tensorflow.keras.losses.binary_crossentropy, 
                                        tensorflow.keras.losses.binary_crossentropy, tensorflow.keras.losses.binary_crossentropy])

    def preprocess_image(self, image):
        image = np.array(mudar_image(image)) 
        image = image[ ..., None]
        return image

    def predict(self, image):
        chutar_valor = self.model.predict(image[None, :])
        codigo = f"{np.argmax(chutar_valor[0])}{np.argmax(chutar_valor[1])}{np.argmax(chutar_valor[2])}{np.argmax(chutar_valor[3])}"
        return codigo

    def CNN(self, input_shape=(40, 120, 1)):
        inputs = Input(shape=input_shape)
        inputs2 = Lambda(lambda x: x / 255.)(inputs)
        conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs2)
        conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
        #conv1 = keras.layers.add([conv1, inputs])
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        pool1 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)

        conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
        conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
        conv2 = keras.layers.add([conv2, pool1])
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        pool2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)

        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
        conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
        conv3 = keras.layers.add([conv3, pool2])
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
        #pool3 = Dropout(0.5)(pool3)
        pool3 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)

        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
        conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
        conv4 = keras.layers.add([conv4, pool3])
        #pool4 = Dropout(0.5)(conv4)
        pool4 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv4)#512

        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)#512
        conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)#512
        conv5 = keras.layers.add([conv5, pool4])

        conv5 = Flatten()(conv5)

        fully = Dense(256, activation='relu')(conv5)

        saida1= Dense(10, activation = 'softmax')(fully)
        saida2= Dense(10, activation = 'softmax')(fully)
        saida3= Dense(10, activation = 'softmax')(fully)
        saida4= Dense(10, activation = 'softmax')(fully)

        model = Model(inputs=[inputs], outputs=[saida1, saida2, saida3, saida4])
        
        return model