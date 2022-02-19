import os
import librosa
import scipy.io.wavfile as wavfile
import numpy as np
# A file for downloading files and handling audio and video

# command line functions #

def mkdir(dir_name,loc=''):
    # make directory use command line
    # dir_name  | name of the directory
    # loc       | the location for the directory to be created
    command = ""
    if loc != '':
        command += "cd %s" % loc
    command += 'mkdir ' + dir_name
    os.system(command)

def m_link(youtube_id):
    # return the youtube actual link
    link = 'https://www.youtube.com/watch?v='+youtube_id
    return link

def download(loc,name,link,sr=16000,type='audio'):
    # download audio from the link
    # loc   | the location for downloaded file
    # name  | the name for the audio file
    # link  | the link to downloaded by youtube-dl
    # type  | the type of downloaded file


    if type == 'audio':
        # download wav file from the youtube link
        command = 'cd %s;' % loc
        command += 'youtube-dl -x --audio-format wav -o o' + name + '.wav ' + link + ';'
        command += 'ffmpeg -i o%s.wav -ar %d -ac 1 %s.wav;' % (name,sr,name)
        command += 'rm o%s.wav' % name
        os.system(command)
