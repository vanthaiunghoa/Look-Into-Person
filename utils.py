import multiprocessing

import cv2 as cv
import numpy as np
import keras.backend as K
from tensorflow.python.client import device_lib
from config import num_classes

# Load the color prior factor that encourages rare classes
prior_factor = np.load("data/prior_factor.npy")
prior_factor = prior_factor.astype(np.float32)


def cross_entropy(y_true, y_pred):
    y_true = K.reshape(y_true, (-1, num_classes))
    y_pred = K.reshape(y_pred, (-1, num_classes))

    idx_max = K.argmax(y_true, axis=1)
    weights = K.gather(prior_factor, idx_max)
    weights = K.reshape(weights, (-1, 1))

    # multiply y_true by weights
    y_true = y_true * weights

    cross_ent = K.categorical_crossentropy(y_pred, y_true)
    cross_ent = K.mean(cross_ent, axis=-1)

    return cross_ent


# getting the number of GPUs
def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


# getting the number of CPUs
def get_available_cpus():
    return multiprocessing.cpu_count()


def draw_str(dst, target, s):
    x, y = target
    cv.putText(dst, s, (x + 1, y + 1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv.LINE_AA)
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.LINE_AA)
