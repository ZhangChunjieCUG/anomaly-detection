import logging
import numpy as np
import pandas as pd
import scipy.io
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)


def get_train(label=0, scale=False, *args):
    """Get training dataset for Thyroid dataset"""
    return _get_adapted_dataset("train", scale)


def get_test(label=0, scale=False, *args):
    """Get testing dataset for Thyroid dataset"""
    return _get_adapted_dataset("test", scale)


def get_valid(label=0, scale=False, *args):
    """Get validation dataset for Thyroid dataset"""
    # return None
    return _get_adapted_dataset("valid", scale)




def get_shape_input():
    """Get shape of the dataset for Thyroid dataset"""
    return (None, 5)


def get_shape_input_flatten():
    """Get shape of the dataset for Thyroid dataset"""
    return (None, 5)


def get_shape_label():
    """Get shape of the labels in Thyroid dataset"""
    return (None,)


def get_anomalous_proportion():
    return 0.05


def _get_dataset(scale):
    """ Gets the basic dataset
    Returns :
            dataset (dict): containing the data
                dataset['x_train'] (np.array): training images shape
                (?, 120)
                dataset['y_train'] (np.array): training labels shape
                (?,)
                dataset['x_test'] (np.array): testing images shape
                (?, 120)
                dataset['y_test'] (np.array): testing labels shape
                (?,)
    """
    path_ = 'D:/1_data science/1_code/ALAD_myDATA_LOSS2/data/arrhythmia.mat'


    data = scipy.io.loadmat(path_)



    full_x_data = data["X"]
    full_y_data = data['Y']
    full_deposit_value=data['df']
    full_temp=data['temp']

    # x_train, x_test, \
    # y_train, y_test,\
    # Df_train, Df_test,\
    # temp_train,temp_test = train_test_split(full_x_data,
    #                                    full_y_data,
    #                                 full_deposit_value,
    #                                     full_temp,
    #                                    test_size=0.3,
    #                                  random_state=42)
    #K_fold valiation ,Need to set paratmer by hand
    k = 6
    mun_valiation_samples = int(len(full_y_data)/k)
    validaton_scores = []
    iter=5
    x_vaild = full_x_data[(mun_valiation_samples) * iter:mun_valiation_samples * (iter + 1)]
    y_vaild=full_y_data[(mun_valiation_samples) * iter:mun_valiation_samples * (iter  + 1)]
    Df_vaild=full_deposit_value[(mun_valiation_samples) * iter :mun_valiation_samples * (iter + 1)]
    temp_vaild=full_temp[(mun_valiation_samples) * iter:mun_valiation_samples * (iter + 1)]
    x_train = np.concatenate((full_x_data[:mun_valiation_samples * iter] , full_x_data[mun_valiation_samples * (iter + 1):]),axis=0)
    y_train = np.concatenate((full_y_data[: mun_valiation_samples * iter] , full_y_data[mun_valiation_samples * (iter + 1):]),axis=0)
    Df_train = np.concatenate((full_deposit_value[: mun_valiation_samples * iter] , full_deposit_value[mun_valiation_samples * (iter + 1):]),axis=0)
    temp_train = np.concatenate((full_temp[: mun_valiation_samples * iter] , full_temp[mun_valiation_samples * (iter + 1):]),axis=0)



    x_test=full_x_data
    y_test=full_y_data
    Df_test=full_deposit_value
    temp_test=full_temp

    y_train = y_train.flatten().astype(int)
    y_test = y_test.flatten().astype(int)
    y_vaild=y_vaild.flatten().astype(int)


    if scale:
        print("Scaling dataset")
        scaler = MinMaxScaler()
        scaler.fit(x_train)
        x_train = scaler.transform(x_train)
        x_test = scaler.transform(x_test)

    dataset = {}
    dataset['x_train'] = x_train.astype(np.float32)
    dataset['y_train'] = y_train.astype(np.float32)
    dataset['x_test'] = x_test.astype(np.float32)
    dataset['y_test'] = y_test.astype(np.float32)
    dataset['df_train'] = Df_train.astype(np.float32)
    dataset['df_test'] = Df_test.astype(np.float32)
    dataset['temp_train']=temp_train.astype(np.float32)
    dataset['temp_test']=temp_test.astype(np.float32)
    dataset['x_valid']=x_vaild.astype(np.float32)
    dataset['y_valid'] = y_vaild.astype(np.float32)
    dataset['df_valid']=Df_vaild.astype(np.float32)
    dataset['temp_valid'] = temp_vaild.astype(np.float32)



    return dataset


def _get_adapted_dataset(split, scale):
    """ Gets the adapted dataset for the experiments

    Args :
            split (str): train or test or valid
    Returns :
            (tuple): <training, testing> images and labels
    """
    # print("_get_adapted",scale)
    dataset = _get_dataset(scale)
    key_img = 'x_' + split
    key_lbl = 'y_' + split
    key_Df = 'df_' + split
    key_temp='temp_'+split

    print("Size of split", split, ":", dataset[key_lbl].shape[0])

    return (dataset[key_img], dataset[key_lbl],dataset[key_Df],dataset[key_temp])


def _to_xy(df, target):
    """Converts a Pandas dataframe to the x,y inputs that TensorFlow needs"""
    result = []
    for x in df.columns:
        if x != target:
            result.append(x)
    dummies = df[target]
    return df.as_matrix(result).astype(np.float32), dummies.as_matrix().astype(np.float32)
