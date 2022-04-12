import seaborn as sns
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers

from sklearn.metrics import classification_report, confusion_matrix

import tensorflow as tf

import cv2
import os

import numpy as np

from resources.Globals import *

labels = ['houses', 'other']
img_size = 400


def get_data(data_dir):
    data = []
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))  # Convert BGR to RGB format
                resized_arr = cv2.resize(img_arr, (img_size, img_size))  # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data, dtype="object")


def main():
    train = get_data('E:/Projects/Pycharm Projects/sapper/files/Neural_networks/Train')
    val = get_data('E:/Projects/Pycharm Projects/sapper/files/Neural_networks/Test')

    # Visualize the data
    l = []
    for i in train:
        if i[1] != 0:
            l.append("houses")
        else:
            l.append("other")
    sns.set_style('darkgrid')
    sns.countplot(l)

    # House
    plt.figure(figsize=(5, 5))
    plt.imshow(train[1][0])
    plt.title(labels[train[0][1]])

    # Other
    plt.figure(figsize=(5, 5))
    plt.imshow(train[-1][0])
    plt.title(labels[train[-1][1]])

    # Data Preprocessing
    x_train = []
    y_train = []
    x_val = []
    y_val = []

    for feature, label in train:
        x_train.append(feature)
        y_train.append(label)

    for feature, label in val:
        x_val.append(feature)
        y_val.append(label)

    # Normalize the data
    x_train = np.array(x_train) / 255
    x_val = np.array(x_val) / 255

    x_train.reshape(-1, img_size, img_size, 1)
    y_train = np.array(y_train)

    x_val.reshape(-1, img_size, img_size, 1)
    y_val = np.array(y_val)

    # Data augmentation
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=30,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range=0.2,  # Randomly zoom image
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    print('Pretrain')

    datagen.fit(x_train)

    print('After train')

    # Define the Model
    model = Sequential()
    model.add(Conv2D(32, 3, padding="same", activation="relu", input_shape=(img_size, img_size, 3)))
    model.add(MaxPool2D())

    model.add(Conv2D(64, 3, padding="same", activation="relu", input_shape=(img_size, img_size, 3)))
    model.add(MaxPool2D())
    model.add(Dropout(DROPOUT))

    model.add(Flatten())
    model.add(Dense(128, activation="relu", input_shape=(img_size, img_size, 3)))
    model.add(Dense(2, activation="softmax"))

    model.summary()

    # Compile the model
    opt = keras.optimizers.Adam(lr=0.000001)  # Adam as optimizer and SparseCategoricalCrossentropy as the loss function
    model.compile(optimizer=opt, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    print('Pretrain #2')
    # Train model
    history = model.fit(x_train, y_train, epochs=AMOUNT_OF_EPOCHS, validation_data=(x_val, y_val))
    print('After train #2')

    model.save("../../files/Neural_networks/model/training_3")

    print('Model saved')

    # Evaluating the result
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(1, AMOUNT_OF_EPOCHS + 1)

    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')

    # Precision and accuracy report
    predictions = model.predict_classes(x_val)
    predictions = predictions.reshape(1, -1)[0]
    print(classification_report(y_val, predictions, target_names=['Rugby (Class 0)', 'Soccer (Class 1)']))

    # Show all plots
    plt.show()


if __name__ == '__main__':
    main()
