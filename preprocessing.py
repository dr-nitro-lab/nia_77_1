#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 23:38:02 2022

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

import librosa
import json
import pathlib

def load_json(_path_):
    f = open(_path_)
    meta = json.load(f)

    return meta

def preprocess(path_meta, num_mfcc=40, n_fft=2048,
               hop_length=512, num_segment=10):
    # data = {"labels": [], "mfcc": []}

    # 1. load .json files
    meta = load_json(path_meta)
    source_info = meta['music_source.Info']

    # 2. read .wav file
    try:
        y, sr = librosa.load((path_meta.parent / source_info['music.src_nm'])\
                             .with_suffix('.' + source_info['music.src_FMT']),\
                             sr=int(source_info['samplingRate']))
    except:
        return

    # 3. feature extractions
    #  3.1 MFCC (.mfcc.npy, params..?)    
    mfcc = librosa.feature.mfcc(y, sr, n_mfcc = num_mfcc, n_fft = n_fft,
                                hop_length = hop_length)
    #  3.2 mel-spectrogram (.melspec.npy, params..?)

    #  3.3 onsets (.onsets.npy)

    print('okay')
    

    # return data
    return

if __name__ == '__main__': 
    _path_meta_ = pathlib.Path('labeling_test_220729/S4-932-001.json')
    preprocess(_path_meta_)
    