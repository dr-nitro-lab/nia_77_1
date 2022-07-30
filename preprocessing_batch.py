#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 18:44:06 2022

@author: K.S. Chun ( kschun@kaist.ac.kr )
"""

###
#
# 1. load .json file
# 2. read .wav file
# 3. feature extractions
#  3.1 MFCC (.mfcc.npy, params..?)
#  3.2 mel-spectrogram (.melspec.npy, params..?)
#  3.3 onsets (.onsets.npy)
# 4. save features
#

import librosa
import json
# import jsonpickle
import pathlib

def load_json(_path_):
    f = open(_path_)
    meta = json.load(f)

    return meta

if __name__ == '__main__': 
    data_dir = pathlib.Path('./labeling_test_220729')
    list_meta = list(pathlib.Path(data_dir).glob('*.json'))
    
    for path_meta in list_meta:
        print(path_meta)
        meta = load_json(path_meta)
        source_info = meta['music_source.Info']
        wav = librosa.load((data_dir / source_info['music.src_nm'])\
                           .with_suffix('.' + source_info['music.src_FMT']),\
                           sr=int(source_info['samplingRate']))
        print('okay')