import streamlit as st
from streamlit.report_thread import add_report_ctx
from PIL import Image
import base64
import sqlite3
import os
import pathlib
from pydub import AudioSegment

import threading
import time

from omnizart.music import app as mapp

def write_title(char, ft_size= 100):
    st.markdown(f"<h1 style='text-align: center; color: DodgerBlue; font-size: {ft_size}px;'>{char}</h1>", unsafe_allow_html=True)
        
def make_cell(char, link=""):
    st.markdown(f"## ***<span style='color:DodgerBlue'>[{char}]({link})</span>***", unsafe_allow_html=True)
    st.text("")
    return st.empty()

def make_button(link, path):
    image_base64=img_to_bytes(path) 
    html = f"<a href='{link}'><img src='data:image/png;base64,{image_base64}'></a>"
    return html

def progress_bar(p_bar, t):
    for i in range(100):
        time.sleep(t/100)
        p_bar.progress(i+1)
        print(i)

def main():
    title = '국악 WAV 음원 MID 변환 모델'
    write_title(title, ft_size= 50)
    
    uploaded_file = st.file_uploader('WAV 파일을 업로드하세요.')   
    
    if uploaded_file:
        audio = AudioSegment.from_wav(uploaded_file)
        f_name = uploaded_file.name
        
        audio.export("./demo_files/"+f_name, format="wav")
        
        p_bar = st.progress(0)
        t = threading.Thread(target=progress_bar, args=(p_bar, 10))
        st.report_thread.add_report_ctx(t)
        t.start()
        # progress_bar(p_bar, 15)
        with st.spinner('MID 파일을 만드는 중... (약 10초)'):
            
            mid = mapp.transcribe("./demo_files/"+f_name, model_path='Piano', output="./demo_files")
        
        # mid = mapp.transcribe("./demo_files/"+f_name, model_path='Piano', output="./demo_files")

        with open("./demo_files/"+f_name.split('.')[0]+".mid", 'rb') as mid_file:
            st.download_button('MID 파일을 다운로드 받으세요', mid_file, f_name.split('.')[0]+'.mid')
        pass

if __name__ == '__main__':
    main()