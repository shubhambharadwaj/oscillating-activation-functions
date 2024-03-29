# -*- coding: utf-8 -*-
"""Paper_code_demo

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10lxL8Tl-1Z3rgAju_-OReesV2kBXMvq9
"""

# Commented out IPython magic to ensure Python compatibility.
# Load the TensorBoard notebook extension
!pip install keras-tuner
!pip install tensorflow-addons
# %load_ext tensorboard
# Clear any logs from previous runs
!rm -rf ./logs/
import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')
import math as m
# Clear any logs from previous runs
!rm -rf /content/drive/My\ Drive/Colab\ Notebooks/logs/
import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.python.ops.numpy_ops import np_config
np_config.enable_numpy_behavior()
#from tensorboard.plugins.hparams import api as hp
from tensorflow.keras.datasets import cifar10
#from kerastuner.engine.hyperparameters import HyperParameters as HP
import tensorflow.keras.backend as K
import tensorflow.keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, LeakyReLU
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorboard.plugins.hparams import api as hp
from sklearn.model_selection import train_test_split, GridSearchCV

import os
gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Select the Runtime > "Change runtime type" menu to enable a GPU accelerator, ')
  print('and then re-execute this cell.')
else:
  print(gpu_info)
#################################################################################################################################################################################

batch_size = 32 #64
num_classes = 10
epochs = 100

#relu_valloss = []
#relu_valacc = []
data_list = []
data_list_2 = []

#fashion_mnist = tf.keras.datasets.fashion_mnist
(x_train, y_train),(x_test, y_test) = cifar10.load_data()


#y_train = tf.keras.utils.to_categorical(y_train, num_classes)
#y_test = tf.keras.utils.to_categorical(y_test, num_classes)
x_train, x_test = x_train / 255.0, x_test / 255.0
#x_train, x_test = x_train.astype('float32'), x_test.astype('float32')

def act_sine(x):
    '''Sine'''
    return tf.sin(x)

def GCU(x):
    '''Growing Cosine Unit'''
    return x * tf.cos(x)

def cos_2(x):
    '''Cos_2'''
    return tf.square(x) * tf.cos(x)

def act_sign_sin(x):
    '''Act_Sign_Sin'''
    return tf.sign(x)*tf.square(tf.sin(x))

#def swish(x):
#   '''Swish'''
#  return x * tf.sigmoid(x)

def new_act_1(x):
    '''New_Act_1'''
    return tf.math.pow(x + 1, 3)

pi = tf.constant(m.pi)

def act_signum(x):
    '''Signum'''
    return tf.sign(x)

def act_identity(x):
    '''Identity'''
    return tf.identity(x)

#def act_step(x):
#    '''Step'''
#    #tf.step(x)
#    if tf.greater_equal(x,0):
#      return 1
#    return 0

def act_SiLU(x):
    '''SiLU'''
    return (x/(1+tf.math.exp(-x)))

def act_LiSHT(x):
    '''LiSHT'''
    return x*tf.tanh(x)

def act_ReSech(x):
    '''ReSech'''
    return x/tf.tanh(x)

def act_bipolar(x):
    '''Bipolar'''
    return ((1-tf.math.exp(-x)) / (1+tf.math.exp(-x)))

def act_absolute(x):
    '''Absolute'''
    return abs(x)

def act_elliott(x):
    '''Elliott'''
    return (1/(1+abs(x)))

#################### TO BE DONE #########################

## FILL IN NEW ACTIVATION FUNCTIONS HERE (IF ANY)

#'ThresholdedReLU',new_act_1,softmax,exponential,act_elliott,act_ReSech

activation_inputs = ['sigmoid','softplus','softsign',
                     'relu','PReLU','gelu','elu',
                     'LeakyReLU','tanh','selu',
                     act_absolute,
                     GCU,
                    #  act_DSU,
                    #  act_NMcubic,
                     act_SiLU,
                     act_LiSHT,
                    #  act_Mcubic,
                    #  act_quadratic,
                     act_sine,
                     cos_2,
                     tf.keras.activations.swish,
                     tfa.activations.mish,
                     act_sign_sin,
                     act_signum,
                     act_identity,
                     act_bipolar,
                    #  act_shiftedSinc
                     ]

# rechecking #
#activation_inputs = ['sigmoid']#,act_DSU,act_Mcubic]

for q in range(0,1):
  for k in activation_inputs:
      if type(k) == str:
          continue
      print(k(float(q)))
      print(Activation(k))

from tensorflow import keras
y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

#csv_logger = tf.keras.callbacks.CSVLogger('/content/drive/My Drive/Colab Notebooks/training.log')
def train_test_model(activation_fn):
    cifar10_model=tf.keras.models.Sequential()
    cifar10_model.add(tf.keras.layers.Conv2D(filters=32,kernel_size=3,padding="same", activation= activation_fn, input_shape=[32,32,3]))
    cifar10_model.add(tf.keras.layers.Conv2D(filters=32,kernel_size=3,padding="same", activation= activation_fn))
    cifar10_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    cifar10_model.add(tf.keras.layers.Conv2D(filters=64,kernel_size=3,padding="same", activation= activation_fn))
    cifar10_model.add(tf.keras.layers.Conv2D(filters=64,kernel_size=3,padding="same", activation= activation_fn))
    cifar10_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    cifar10_model.add(tf.keras.layers.Flatten())
    cifar10_model.add(tf.keras.layers.Dropout(0.5,noise_shape=None,seed=None))
    cifar10_model.add(tf.keras.layers.Dense(units=128,activation= activation_fn))
    cifar10_model.add(tf.keras.layers.Dense(units=10,activation='softmax'))
    cifar10_model.compile(loss="categorical_crossentropy", optimizer='Adam', metrics=["accuracy"])
    # GET GRADIENT FUNCTION INTEGRATED #
    call_back = tf.keras.callbacks.EarlyStopping(patience=20, restore_best_weights=True)
    history = cifar10_model.fit(x_train,y_train,epochs=epochs, validation_data=(x_test, y_test), batch_size=batch_size, callbacks=[call_back])#, callbacks=[])#,callbacks=[get_gradients])
    # MODEL EVALUATE #
    test_loss, test_accuracy = cifar10_model.evaluate(x_test, y_test)
    act_func_str = activation_fn

    if act_func_str == tfa.activations.mish:
        act_func_str = 'Mish'

    if act_func_str == tf.keras.activations.swish:
        act_func_str = 'Swish'

    if type(act_func_str) != str:
        act_func_str = act_func_str.__doc__

    data_list.append([act_func_str,test_loss,test_accuracy])
    #data_list_2.append(act_func_str,)

    #data_list_2.append()
    # return test_accuracy

for activation_input in activation_inputs: #in activation_inputs:
    train_test_model(activation_input)
    # break

data = pd.DataFrame(data_list)
data = data.rename(columns={0:'Activation Function',1:'Loss',2:'Test_Accuracy'})
data.head()
data.to_csv('/content/drive/My Drive/Colab Notebooks/AFOutputs_NewRun_1.csv',index=False)

