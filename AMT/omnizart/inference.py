import random
random.seed(10)

import os
import pickle
from os.path import join as jpath

import h5py
import numpy as np
import tensorflow as tf

print(tf.__version__)
import pretty_midi

import glob

# from omnizart.music import app as mapp
from omnizart.music.app import MusicTranscription

from sklearn.metrics import accuracy_score




def note_accum_each(midfile1, midfile2):
    midi1 = pretty_midi.PrettyMIDI(midfile1)
    midi2 = pretty_midi.PrettyMIDI(midfile2)
    
    midi1_note_list = midi1.instruments[0].notes
    midi2_note_list = midi2.instruments[0].notes
    
    end_time1 = round(midi1_note_list[-1].end, 3)
    end_time2 = round(midi2_note_list[-1].end, 3)
    mat_size = int(max(end_time1, end_time2)*1000)
    
    if mat_size == 0:
        print(midfile1, midfile2)
    
    pitch_mat1 = [0] * mat_size
    pitch_mat2 = [0] * mat_size
    
    for i in range(len(midi1_note_list)):
        for j in range(int(round(midi1_note_list[i].start, 3)*1000), int(round(midi1_note_list[i].end, 3)*1000)):
            pitch_mat1[j] = midi1_note_list[i].pitch
            
    for i in range(len(midi2_note_list)):
        for j in range(int(round(midi2_note_list[i].start, 3)*1000), int(round(midi2_note_list[i].end, 3)*1000)):
            pitch_mat2[j] = midi2_note_list[i].pitch

    return pitch_mat1, pitch_mat2




# mid path: '/home/ubuntu/workspace/jaeyoon/GUGAK/omnizart/dataset/yuhyun/new_string_dataset/test_dataset/mid'
# mid_list = ['example1.mid', 'example2.mid']
# mid_file = 'example1.mid'
# mid_file_full_path = '/home/ubuntu/workspace/jaeyoon/GUGAK/omnizart/dataset/yuhyun/new_string_dataset/test_dataset/mid/example1.mid'
# total_mid ['home/ubuntu/workspace/jaeyoon/GUGAK/omnizart/dataset/yuhyun/new_string_dataset/test_dataset/mid/example1.mid'
#            '/home/ubuntu/workspace/jaeyoon/GUGAK/omnizart/dataset/yuhyun/new_string_dataset/test_dataset/mid/example2.mid'


path_list = ['/mnt/dataset/string',
             '/mnt/dataset/vocal',
             '/mnt/dataset/wind']

model_paths = ['/mnt/checkpoints/music/music_string_piano-v2_1222',
              '/mnt/checkpoints/music/music_vocal_piano-v2_1222',
              '/mnt/checkpoints/music/music_wind_piano-v2_1222']


testset_dic = {}
result_dic = {}



for i in range(0, len(path_list)):
    path = path_list[i]
    model = model_paths[i]
    mapp = MusicTranscription(conf_path=None, model_path=model)
    
    
    category = path.split("/")[-1]
    
    

    total_mid = []
    mid_path = os.path.join(path, 'test_dataset/mid')
    mid_list = [file for file in os.listdir(mid_path) if file.endswith('.mid')]

    
    for mid_file in mid_list:
        mid_file_full_path = os.path.join(mid_path, mid_file)
        total_mid.append(mid_file_full_path)
        
    
    
     
    wav_path = os.path.join(path, 'test_dataset/wav')
    wav_list = [file for file in os.listdir(wav_path) if file.endswith('.wav')]
    num_wav_list = len(wav_list)
    
    inf_path = os.path.join(path, 'test_dataset/inf')
    
    if not os.path.exists(inf_path):
        print("created " + inf_path)
        os.mkdir(inf_path)
        
        
    mid = []
    inf = []
    count = 0
    for wav_file in wav_list: # im tyring to fix here ma brotha
        count += 1
        wav_file_full_path = os.path.join(wav_path, wav_file)
        try:
            midi = mapp.transcribe(wav_file_full_path, output=inf_path)
            file_basename = wav_file.split('.')[0]
            
            mid_file = file_basename + '.mid'
            mid_file_full_path = os.path.join(mid_path, mid_file)
            
            inf_file = file_basename + '.mid'
            inf_file_full_path = os.path.join(inf_path, inf_file)
            
            each_mid = []
            each_inf = []
            
            each_mid, each_inf = note_accum_each(mid_file_full_path, inf_file_full_path)
            mid += each_mid
            inf += each_inf
            each_accuracy = accuracy_score(each_mid, each_inf)
            
            print("[" + str(count) + "/" + str(num_wav_list) + "] " "Accuracy of a file " + wav_file + " is: " + str(each_accuracy))
            
            
        except Exception as e:
            print(wav_file_full_path, e)
            continue
    accuracy = accuracy_score(mid, inf)
    print("Accuracy of " + category + " is: "+ str(accuracy))
    result_dic[category] = accuracy
    
    
    total_inf = []
    inf_list = [file for file in os.listdir(inf_path) if file.endswith('.mid')]
    for inf_file in inf_list:
        inf_file_full_path = os.path.join(inf_path, inf_file)
        total_inf.append(inf_file_full_path)
    

    
    testset_dic[category]={}
    testset_dic[category]['mid'] = total_mid
    testset_dic[category]['inf'] = total_inf
    print(len(total_mid), len(total_inf))

    
for key in result_dic.keys():
    print(key)
    print(result_dic[key])