from tkinter import PhotoImage

import cv2
import tensorflow as tf
import numpy as np
from keras_preprocessing.image import ImageDataGenerator

from bin.Classess.Field import Field

field = Field()

CATEGORIES = ['houses', 'other']


def prepare(filepath):
    IMG_SIZE = 400
    img_array = cv2.imread(filepath)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    new_array = np.array(new_array) / 255
    return new_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)


model = tf.keras.models.load_model("../../files/Neural_networks/model/training_50_epochs")
model.summary()

test = prepare("E:/Projects/Pycharm Projects/sapper/files/large_images_houses/IMG_2573.png")
# test = prepare("E:/Projects/Pycharm Projects/sapper/files/large_images/IMG_3208.png")


pred = test

prediction = model.predict([pred])
print(prediction)  # will be a list in a list.

house = prediction[0][0]
other = prediction[0][1]

if house > other:
    prediction = 0
else:
    prediction = 1

print(f'house: {house}\nother: {other}')

print(f'prediction: {prediction}')

print(CATEGORIES[int(prediction[0][0])])
