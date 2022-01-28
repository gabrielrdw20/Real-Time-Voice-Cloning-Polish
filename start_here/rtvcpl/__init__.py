'''Author: Gabriel Rodewald
Github: gabrielrdw20
 '''

import modify_audio as ma
from pydub import AudioSegment
import pydub


''' 
There are 3 steps:
    1 - create directory
    2 - modifying video / audio files
    3 - testing & dealing with technical issues
'''

if __name__ == "__main__":
    

        
# STEP  1 ---------------------------------------------------------------------   
     
    # DOWNLAOD EXE FFMPEG FILES AND PROVIDE PATH TO THOSE FILES
    pydub.AudioSegment.converter = r"C:\\Users\\1\\ffmpeg\\ffmpeg.exe"
    AudioSegment.ffprobe   = r"C:\\Users\\1\\ffmpeg\\ffprobe.exe" 
    
    
    ma.create_basic_folders()
    
    # wait until sample audio is downloaded, usually around 1 minute
    ma.download_sample_create_empty_wav()
    
# STEP  2 --------------------------------------------------------------------- 
   
    ma.from_file_to_wav()
    ma.cut_wavs_to_10s_audios()
    ma.remove_first_10_files()
    
    # processing steps not shown due to Jupyter / Spyder limited cache limit
    # enter language using in the audio files
    # Check here: https://cloud.google.com/speech-to-text/docs/languages
    ma.txt_to_speech_all_speakers('en-US') #e.g. 'pl-PL'
    
    
# STEP  3 ---------------------------------------------------------------------

    ma.is_equal_txt_wav() 
    ma.unwanted_files()