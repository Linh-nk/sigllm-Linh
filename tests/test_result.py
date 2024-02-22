# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pytest import fixture

from sigllm.result import *


@fixture
def text():
    return '1,2,3,4,5,6,7,8,9'

@fixture
def text_1(): 
    return 'Result: 1 2 3, 2 3 4,'

@fixture
def anomaly_list_within_seq(): 
    return [np.array([2, 3, 7, 9]),
            np.array([5]), 
            np.array([2, 5]),
            np.array([8, 9])]

@fixture
def anomaly_list_across_seq(): 
    return [np.array([0]),
            np.array([2,3]), 
            np.array([2,4]),
            np.array([4,5]), 
            np.array([5])]

@fixture
def window_size(): 
    return 3

@fixture
def step_size(): 
    return 1

@fixture
def signal(): 
    d = {'timestamp': [1222819200, 1222840800, 1222862400, 1222884000, 1222905600],'value': [-1.0, -1.0, -1.0, -1.0, -1.0]}
    return pd.DataFrame(data = d)

@fixture
def ind_list(): 
    return np.array([0, 1, 3])

def test_str2ind(text):
    expected = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    result = str2ind(text, len_seq = 20)

    np.testing.assert_equal(result, expected)
    
    
def test_str2ind_spurious(text_1):
    expected = np.array([123, 234])

    result = str2ind(text_1, len_seq = 500)

    np.testing.assert_equal(result, expected)
    
    
def test_str2ind_overflow(text):
    expected = np.array([1, 2, 3, 4, 5, 6, 7])

    result = str2ind(text, len_seq = 8)

    np.testing.assert_equal(result, expected)

    
def test_get_anomaly_list_within_seq(anomaly_list_within_seq):
    expected = np.array([2, 5, 9])
    
    result = get_anomaly_list_within_seq(anomaly_list_within_seq)
    
    np.testing.assert_equal(result, expected)
    
    
def test_get_anomaly_list_across_seq(anomaly_list_across_seq, window_size, step_size): 
    expected = np.array([2, 4, 5])
    
    result = get_anomaly_list_across_seq(anomaly_list_across_seq, window_size, step_size)
    
    np.testing.assert_equal(result, expected)
    
    
def test_ind2time(signal, ind_list):
    expected = np.array([1222819200, 1222840800, 1222884000])

    result = ind2time(signal, ind_list)

    np.testing.assert_equal(result, expected)
    


