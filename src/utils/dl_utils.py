# common functions to initialize keras session, load data and plot optimization history

from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
sns.set_context('paper')
sns.set_style('darkgrid')

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

# function to initialize keras/tensorflow session
def init_session():    
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True  # dynamically grow the memory used on the GPU
    config.log_device_placement = True  # to log device placement (on which device the operation ran)
                                        # (nothing gets printed in Jupyter, only if you run it standalone)
    sess = tf.Session(config=config)
    set_session(sess)  # set this TensorFlow session as the default session for Keras
    return
 
# function required by hyperas to retrieve train and test data for optimization
def data():
    # change to appropriate data folder
    data_folder = '/media/siri/78C6823EC681FD1E/minio/data/dq-data/dl/'
    input_folder = '/media/siri/78C6823EC681FD1E/minio/data/dq-data/'
    q1_train_w2v = pickle.load(open(data_folder+'q1_train_w2v.p', 'rb'))
    q2_train_w2v = pickle.load(open(data_folder+'q2_train_w2v.p', 'rb'))
    q1_test_w2v = pickle.load(open(data_folder+'q1_test_w2v.p', 'rb'))
    q2_test_w2v = pickle.load(open(data_folder+'q2_test_w2v.p', 'rb'))
    x_train = np.concatenate([np.expand_dims(q1_train_w2v, axis=1),np.expand_dims(q2_train_w2v, axis=1)], axis=1)
    x_test = np.concatenate([np.expand_dims(q1_test_w2v, axis=1),np.expand_dims(q2_test_w2v, axis=1)], axis=1)
    y_train = pickle.load(open(input_folder+'y_train.p', 'rb'))
    y_test = pickle.load(open(input_folder+'y_test.p', 'rb'))
    return x_train, y_train, x_test, y_test

# function to plot the validation and training accuracy throughout the hyperas/hyperopt optimization run 
def plot_optimization_history(trials):    
    x = range(1, len(trials.results)+1)
    y1 = [eval_run['train_acc'] for eval_run in trials.results]
    y2 = [-eval_run['loss'] for eval_run in trials.results]
    df1 = pd.DataFrame(np.array(x), columns=['evaluation run'])
    df1['accuracy'] = pd.Series(np.array(y1))
    df1['run'] = 'training'
    df2 = pd.DataFrame(np.array(x), columns=['evaluation run'])
    df2['accuracy'] = pd.Series(np.array(y2))
    df2['run'] = 'validation'
    df = pd.concat([df1, df2])
    pal = {'validation':'#3498db', 'training':'#e74c3c'}
    ax = sns.relplot('evaluation run','accuracy', hue='run', style='run', data=df, 
                linewidth=2.0, palette=pal, kind="line", legend='full', height=5, aspect=7/5)
    ax.set(xlim=(0, len(trials.results)+.5), ylim=(-.05, 1.0), title='history of optimization')
    return
