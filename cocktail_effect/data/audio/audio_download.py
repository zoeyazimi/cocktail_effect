import sys
import pandas as pd
import librosa
sys.path.append("../cocktail_effect/data")  # path to the AVHandler.py
import AVHandler as avh
import cocktail_effect.data.audio.audio_norm as audio_norm
import os

dirname = os.path.dirname(__file__)

class AudioDownload(object):

    def __init__(self, loc, name,cat, start_idx, end_idx):
        "This class helps with downloading the audio"


        # self.youtube_id = youtube_id
        self.loc = loc
        self.name = name
        self.cat = cat
        self.start_idx = start_idx
        self.end_idx = end_idx

    def m_link(self, youtube_id):
        # return the youtube actual link
        link = 'https://www.youtube.com/watch?v=' + youtube_id

        return link


    def m_audio(self):
        # make concatenated audio following by the catalog from AVSpeech
        # loc       | the location for file to store
        # name      | name for the wav mix file
        # cat       | the catalog with audio link and time :cat_train csv file
        # start_idx | the starting index of the audio to download and concatenate
        # end_idx   | the ending index of the audio to download and concatenate

        for i in range(self.start_idx, self.end_idx):
            f_name = self.name + str(i)
            link = self.m_link(self.cat.loc[i, 'link'])
            start_time = self.cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            avh.download(self.loc, f_name, link)
            avh.cut(self.loc, f_name, start_time, end_time)

    def collect_audio(self):
        header = ["link", "start_time", "end_time", "x_coord", "y_coord"]
        cat_train = pd.read_csv(os.path.join(dirname, '../../../raw_data/avspeech_test.csv'), names=header)
        #cat_test = pd.read_csv('catalog/avspeech_test.csv', names=header)
        # first_indx = 1
        # last_indx = 2

        # create 80000-90000 audios data in the range of index
        # self.m_audio(self.loc, self.loc, cat_train, first_indx, last_indx)
        self.m_audio()

#make sure to change the RANGE value before running audio_norm
audio_norm
