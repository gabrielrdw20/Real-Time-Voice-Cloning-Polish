'''Author: Gabriel R.
Github: gabrielrdw20
 '''

from csv import writer
from multiprocessing import Process
from os.path import exists
from pathlib import Path
from pydub import AudioSegment
from pydub import silence, AudioSegment
from pydub.utils import make_chunks
from pydub.utils import which
from random import sample
from typing import Final
from youtube_dl import YoutubeDL
import csv
import datetime
import errno
import ffmpeg 
import itertools
import multiprocessing as mp
import numpy as np
import os
import os.path
import pandas as pd
import pydub
import random
import re
import shutil
import speech_recognition as sr
import speech_recognition as sr   
import subprocess
import sys
import time
import winsound


global_dir : Final = str(os.getcwd())
main_folder_name : Final = 'voicecloning'
subdir : Final = f'{global_dir}\\{main_folder_name}'
catalogue = ['male','female','mix']
by_book_dir = f'{subdir}\\datasets\\by_book'
wav_to_remove : Final = []

# STEP 1 - CREATE DIRS --------------------------------------------------------

def get_video_from_yt(video_path : str):
    os.chdir(video_path)
    name = 'sample_video'
    url = 'https://www.youtube.com/watch?v=wvsE8jm1GzE&ab_channel=GoogleDevelopers' # sample video from YT
    audio_downloader = YoutubeDL({'format':'bestaudio','outtmpl': str(name) +'.%(ext)s' })
    audio_downloader.extract_info(url,download = True)


def create_basic_folders():
    os.chdir(global_dir)    
    #name your main folder, e.g. voicecloning
    #you can change that +
    #do not change  varaibles and paths below
    root = f'{global_dir}\\{main_folder_name}\\'
    by_book = f'{root}\\datasets\\by_book\\'        
    directories = ['male\\lector_1\\book_title_1\\wavs','female\\lector_1\\book_title_1\\wavs','mix\\lector_1\\book_title_1\\wavs']
    
    if os.path.exists(global_dir):
        if not os.path.isdir(root):
            if not os.path.exists(root):
                os.makedirs(main_folder_name)
        else:
            print("Folder {root_dir} already exists.")
        

        for d in directories:
            path = os.path.join(by_book, d)
            os.makedirs(path)  
        
        
        file = f'{root}\\README.txt'
        try:
            f = open(file, 'a').close()
            f = open(file, 'w')
            f.write('Place the RTVC code in this folder and remove this README.txt file. Some sample videos were downloaded, converted to mp3 and saved into ./male/lector_1/book_title_1, ./female/lector_1/book_title_1 and ./mix/lector_1/book_title_1 folders. You need to wait around 1 min for a sample wav file to be downloaded.')
            f.close()
        except OSError:
            print('Failed creating the file')
        else:
            print(f'File {file} created')
        

def download_sample_create_empty_wav():
    directory = f'{global_dir}\\{main_folder_name}'
    by_book = f'{directory}\\datasets\\by_book\\'
    get_video_from_yt(f'{by_book}\\male\\lector_1\\book_title_1\\')
    original = f'{by_book}\\male\\lector_1\\book_title_1\\sample_video.webm'
    target_1 = f'{by_book}\\female\\lector_1\\book_title_1\\sample_video.webm'
    target_2 = f'{by_book}\\mix\\lector_1\\book_title_1\\sample_video.webm'
    shutil.copy(original, target_1)
    shutil.copy(original, target_2)
   
        
# STEP 2 - MODIFY FILES  ------------------------------------------------------    
 
# Conver MP3, WEBM, FLAC, OGG to WAV:            
def from_file_to_wav():
    current_dir = f'{subdir}\\datasets\\by_book\\'
    os.chdir(current_dir)
    directory = os.getcwd()
    end_cut = 0
    file_format = ''
    
    for c in catalogue:
        directory = f'{current_dir}\\{c}\\'
        
        for root, subdirectories, files in os.walk(directory):
            for file in files:
                fff = os.path.join(root, file) 
                file_str = str(file)
                if re.search('\.mp3$',file_str,flags=re.IGNORECASE):
                    end_cut = 4
                    file_format = '.mp3'
                if re.search('\.webm$',file_str,flags=re.IGNORECASE):
                    end_cut = 5
                    file_format = '.webm'
                if re.search('\.flac$',file_str,flags=re.IGNORECASE):
                    end_cut = 5
                    file_format = '.flac'
                if re.search('\.ogg$',file_str,flags=re.IGNORECASE):
                    end_cut = 4
                    file_format = '.ogg'
                    
                name = str(file)[:-end_cut]
                
                if file.endswith('.wav'):
                    continue
                else:
                    if not(file.endswith('.mp4')):
                        sound = pydub.AudioSegment.from_file(fff)
                        sound.export(f'{root}\\{name}.wav', format="wav") 
                        if file.endswith(f'{file_format}'): # webm can be changed to mp3
                            os.remove(f'{root}\\{name}{file_format}') # webm can be changed to mp3
    print('All files are wav now.')


# This function is used by cut_wavs_to_10s_audios() 
# to remove used wav files that are already cut to chunks            
def remove_main_wavs(files_directory : str, files):
   
    for file in files:
        os.remove(file)
        print(f'\n Removed: {file} \n')
    
               
# In order to use free Google Speech API, prepare files up to 10s of length
# Provide the dataset directory, e.g. E:\\test\\datasets\\
def cut_wavs_to_10s_audios():    
    os.chdir(by_book_dir)
    directory = os.getcwd()
    file_name = []
    
    for c in catalogue:
        directory = f'{by_book_dir}\\{c}\\'
        for root, subdirectories, files in os.walk(directory):
            for file in files:
                last_path = os.path.basename(os.path.normpath(root))
                if last_path != 'wavs' and file not in file_name:
                    file_name.append(f'{root}\\{file}')
                #fff = os.path.join(root, file) 
                name = str(file)[:-4] 
                sound = AudioSegment.from_file(f'{root}\\{name}.wav', format="wav")
                size = 10000 # file will be cut per ten seconds each
                chunks = make_chunks(sound, size)
                
                for i, chunk in enumerate(chunks):
                    if root.endswith('wavs'):
                        root1 = f'{root}'
                            #tmp = root1[:-5]
                    else: 
                        root1 = f'{root}\\wavs'
                            #tmp = root1[:-5]
                        #Enumeration, i is the index, chunk is the cut file
                        chunk_name = f'{name}'+"_{0}.wav".format(i)
                        chunk.export(f'{root1}\\{chunk_name}', format="wav") 
                    
        # comment the below function if you don't want to remove the main wav files
    remove_main_wavs(by_book_dir, file_name)             

    

# when you download ebook, sometimes the opening lector != main lecotr
# that's why it's useful to remove first N files
def remove_first_10_files():
    os.chdir(by_book_dir)
    directory = os.getcwd()
    
    for c in catalogue: 
        directory = f'{by_book_dir}\\{c}\\'
        for root, subdirectories, files in os.walk(directory):
            for f in files:
                # numeracja wymuszona z uwagi na błędne sortowanie (1, 11, 11*, 2, 22, 21*)
                if f.endswith('_0.wav') or f.endswith('_1.wav') or f.endswith('_2.wav') or f.endswith('_3.wav') or f.endswith('_4.wav') or f.endswith('_5.wav') or f.endswith('_6.wav') or f.endswith('_7.wav') or f.endswith('_8.wav') or f.endswith('_9.wav') or f.endswith('_10.wav'):
                    os.remove(f'{root}\\{f}')
                    print(f'{root}\\{f}')
                else:
                    continue    


# if your dataset is big, run rhis for each dir separately, e.g. male, female, mix
def txt_to_speech_single_speaker(lang : str):
    mydir = f'{subdir}\\datasets\\by_book\\'
    r = sr.Recognizer()
    os.chdir(mydir)
    wav_to_remove = []
    
    for root, dirs, files in os.walk(mydir):
        if root.endswith('wavs'):
            #print(root, '-----------', files)
            i = 0
            dir_len =''
            tmp_name = []
            
            for file in files:
                if file.endswith('.wav'):
                    wav_file = file
                    if wav_file not in tmp_name:
                        with sr.AudioFile(f'{root}\\{wav_file}') as source:
                            audio_data = r.record(source) 
                            mydir = f'{root}'
                            dir_len = int(
                                len(
                                    [item for item in os.listdir(mydir) if (os.path.isfile(os.path.join(mydir, item)) and item.endswith('.wav'))]
                                )
                            )
                            #print(dir_len, i)
                            try:
                                if(i < dir_len):
                                    text = r.recognize_google(audio_data, language=lang)
                                    title = str(wav_file).replace('.wav', '')
                                    txtfile = f'{title}.txt'
    
                                    if txtfile not in root:
                                        with open(f'{root}\\{title}.txt', "w") as wav_file:
                                            wav_file.write(f'{text}')
    
                                    i = i + 1
                                    #print(f'{i} z {dir_len}')
                                    #print(f'{root}\\{title}.txt')
                                    #print('------------------------------')
                                else:
                                    i = 0
                                    tmp_name = []
                                    break
                            except:
                                print(f'To remove: {root}\\{file}  | {datetime.datetime.now()}')
                                wav_to_remove.append(f'{root}\\{file}')
                else:
                    continue
                

def txt_to_speech_all_speakers(lang : str):
    mydir =  f'{subdir}\\datasets\\by_book\\'
    r = sr.Recognizer()
    os.chdir(mydir)
    global wav_to_remove 
    wav_to_remove = []
    
    for root, dirs, files in os.walk(mydir):
        if root.endswith('wavs'):
            #print(root, '-----------', files)
            i = 0
            dir_len =''
            tmp_name = []
            
            for file in files:
                if file.endswith('.wav'):
                    wav_file = file
                    if wav_file not in tmp_name:
                        with sr.AudioFile(f'{root}\\{wav_file}') as source:
                            audio_data = r.record(source) 
                            mydir = f'{root}'
                            dir_len = int(
                                len(
                                    [item for item in os.listdir(mydir) if (os.path.isfile(os.path.join(mydir, item)) and item.endswith('.wav'))]
                                )
                            )
                            #print(dir_len, i)
                            try:
                                if(i < dir_len):
                                    text = r.recognize_google(audio_data, language=lang)
                                    title = str(wav_file).replace('.wav', '')
                                    txtfile = f'{title}.txt'
    
                                    if txtfile not in root:
                                        with open(f'{root}\\{title}.txt', "w") as wav_file:
                                            wav_file.write(f'{text}')
    
                                    i = i + 1
                                    
                                else:
                                    i = 0
                                    tmp_name = []
                                    break
                            except:
                                print(f'To remove: {root}\\{file}  | {datetime.datetime.now()}')
                                wav_to_remove.append(f'{root}\\{file}')
                else:
                    continue
                
                
    # WAV files that could not be read properly by Google Speech API are deleted  
    remove_uneligable_wavs_all_speakers(wav_to_remove)
    

def remove_uneligable_wavs_single_speaker(wav_to_remove):
    # can be done for each folder separately, e.g.
    directory = f'{subdir}\\datasets\\by_book\\male'
    
    for root, subdirectories, files in os.walk(directory):
        for f in files:
            to_delete = (f'{root}\\{f}')
            file_del = to_delete[:-4]
            txt_del = f'{file_del}.txt'
            if to_delete in wav_to_remove:
                print(f'Removed file:{to_delete}')
                print(f'Txt rem: {txt_del}')
                print('----------------------------------')
                os.remove(to_delete)
    print("Done")              
    
    
def remove_uneligable_wavs_all_speakers(wav_to_remove):
    # can be done for each folder separately
    
    mydir = f'{subdir}\\datasets\\by_book'
    
    for c in catalogue:
        directory = f'{mydir}\\{c}\\'
        for root, subdirectories, files in os.walk(directory):
            for f in files:
                to_delete = (f'{root}\\{f}')
                file_del = to_delete[:-4]
                if to_delete in wav_to_remove:
                    print(f'Removed file:{to_delete}')
                    print('----------------------------------')
                    os.remove(to_delete)
        
        
    
# PART 3 - TESTING ------------------------------------------------------------

# checking if the number of wav files equals the number of txt files

def is_equal_txt_wav():
    mydir =  f'{subdir}\\datasets\\by_book'
    os.chdir(mydir)
    
    wav_t = []
    txt_t = []
    
    for c in catalogue:
        directory = f'{mydir}\\{c}\\'
        for root, subdirectories, files in os.walk(directory):
            for file in files:
                if file.endswith('.wav'):
                    file = file[:-4]  #trims str '.wav'
                    wav_t.append(file) 
                    
                if file.endswith('.txt'):
                    file = file[:-4]  #trims str '.txt'
                    txt_t.append(file) 
                
            
    #shows if there are any unique, unmaching wav files            
    for f in wav_t:
        if f not in txt_t:
            print(f'Unexpected WAV: {root}\\{f}')
        
    #shows if there are any unique, unmaching txt files 
    for f in txt_t:
        if f not in wav_t:
            print(f'Unexpected TXT:{root}\\{f}') 
            


#check if any unwanted files are in a dir
def unwanted_files():
    mydir =  f'{subdir}\\datasets'
    encoder_dir = "{mydir}\\SV2TTS\\encoder\\" 
    
    #search through wav a txt files
    for c in catalogue:
        directory = f'{mydir}\\{c}'
        for root, subdirectories, files in os.walk(directory):
                for file in files:
                    if not file.endswith('.wav') or not file.endswith('.txt'):
                        print(f'{root}\\{file}')    
                
            
    if os.path.isfile(encoder_dir):
        for root, subdirectories, files in os.walk(encoder_dir):
            for file in files:
                if not file.endswith('.npy'):
                    print(f'{root}\\{file}')     
                    
                
                
                
                
