#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:44:06 2022

@author: K.S. Chun ( kschun@kaist.ac.kr )
"""

###
#
# 1. load .json files
# 2. read .wav file
# 3. feature extractions
#  3.1 MFCC (.mfcc.npy, params..?)
#  3.2 mel-spectrogram (.melspec.npy, params..?)
#  3.3 onsets (.onsets.npy)
# 4. save features
#

import pathlib
from preprocessing import preprocess

if __name__ == '__main__': 
    # data_dir = pathlib.Path('./labeling_test_220729')
    data_dir = pathlib.Path('./220801')
    list_meta = list(pathlib.Path(data_dir).glob('*.json'))
    
    for path_meta in list_meta:
        print(path_meta)
        preprocess(path_meta)