import cv2
import numpy
import numpy as np
import tensorflow
import tensorflow.keras as keras
from PIL import Image, ImageFilter
from scipy.ndimage.filters import gaussian_filter
from tensorflow.keras import backend as K
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        ReduceLROnPlateau, TensorBoard)
from tensorflow.keras.layers import (Conv2D, Conv2DTranspose, Dense, Dropout,
                                     Flatten, Input, Lambda, MaxPooling2D,
                                     concatenate)
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical


class CaptchaSolver:
    def __init__(self, weights="model.h5"):
        self.model = self.CNN()
        self.model.load_weights(weights)
        self.model.compile(
            optimizer="adam",
            loss=[
                tensorflow.keras.losses.binary_crossentropy,
                tensorflow.keras.losses.binary_crossentropy,
                tensorflow.keras.losses.binary_crossentropy,
                tensorflow.keras.losses.binary_crossentropy,
            ],
        )

    def preprocess_image(self, image):
        th1 = 165
        th2 = 165  # threshold after blurring
        sig = 1  # the blurring sigma
        black_and_white = image.convert("L")  # converting to black and white
        first_threshold = black_and_white.point(lambda p: p > th1 and 255)
        blur = np.array(first_threshold)  # create an image array
        blurred = gaussian_filter(blur, sigma=sig)
        blurred = Image.fromarray(blurred)
        final = blurred.point(lambda p: p > th2 and 255)
        final = final.filter(ImageFilter.EDGE_ENHANCE_MORE)
        final = final.filter(ImageFilter.SHARPEN)
        image = np.array(final)
        image = image[..., None]
        return image

    def predict(self, image):
        guess = self.model.predict(image[None, :])
        result = f"{np.argmax(guess[0])}{np.argmax(guess[1])}{np.argmax(guess[2])}{np.argmax(guess[3])}"
        return result

    def CNN(self, input_shape=(40, 120, 1)):
        inputs = Input(shape=input_shape)
        inputs2 = Lambda(lambda x: x / 255.0)(inputs)
        conv1 = Conv2D(32, (3, 3), activation="relu", padding="same")(inputs2)
        conv1 = Conv2D(32, (3, 3), activation="relu", padding="same")(conv1)
        # conv1 = keras.layers.add([conv1, inputs])
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        pool1 = Conv2D(64, (3, 3), activation="relu", padding="same")(pool1)

        conv2 = Conv2D(64, (3, 3), activation="relu", padding="same")(pool1)
        conv2 = Conv2D(64, (3, 3), activation="relu", padding="same")(conv2)
        conv2 = keras.layers.add([conv2, pool1])
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        pool2 = Conv2D(128, (3, 3), activation="relu", padding="same")(pool2)

        conv3 = Conv2D(128, (3, 3), activation="relu", padding="same")(pool2)
        conv3 = Conv2D(128, (3, 3), activation="relu", padding="same")(conv3)
        conv3 = keras.layers.add([conv3, pool2])
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
        # pool3 = Dropout(0.5)(pool3)
        pool3 = Conv2D(256, (3, 3), activation="relu", padding="same")(pool3)

        conv4 = Conv2D(256, (3, 3), activation="relu", padding="same")(pool3)
        conv4 = Conv2D(256, (3, 3), activation="relu", padding="same")(conv4)
        conv4 = keras.layers.add([conv4, pool3])
        # pool4 = Dropout(0.5)(conv4)
        pool4 = Conv2D(512, (3, 3), activation="relu", padding="same")(conv4)  # 512

        conv5 = Conv2D(512, (3, 3), activation="relu", padding="same")(pool4)  # 512
        conv5 = Conv2D(512, (3, 3), activation="relu", padding="same")(conv5)  # 512
        conv5 = keras.layers.add([conv5, pool4])

        conv5 = Flatten()(conv5)

        fully = Dense(256, activation="relu")(conv5)

        output1 = Dense(10, activation="softmax")(fully)
        output2 = Dense(10, activation="softmax")(fully)
        output3 = Dense(10, activation="softmax")(fully)
        output4 = Dense(10, activation="softmax")(fully)

        model = Model(inputs=[inputs], outputs=[output1, output2, output3, output4])

        return model
