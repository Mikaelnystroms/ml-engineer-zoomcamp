import tensorflow as tf
from tensorflow import keras


model = keras.models.load_model('clothing-model.h5')

tf.saved_model.save(model, 'clothing-model')