import cv2
import tensorflow as tf
import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.model = tf.keras.models.load_model("../../files/Neural_networks/model/training_500_epochs_ser")

    def Prediction(self, x, y, field):
        IMG_SIZE = 400
        img_array = cv2.imread(field.large_image_array_filepath[x][y])
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        new_array = np.array(new_array) / 255
        image = new_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)

        prediction = self.model.predict([image])

        return prediction


