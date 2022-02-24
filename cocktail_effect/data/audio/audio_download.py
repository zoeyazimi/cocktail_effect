import sys
import os
import pandas as pd
import librosa

# file_path = os.path.abspath(__file__)
# modules_path = os.path.join('../../', file_path)
sys.path.append('../../')
from data import AVHandler as avh
import audio_norm

def m_link(youtube_id):
    # return the youtube actual link
    link = 'https://www.youtube.com/watch?v=' + youtube_id
    return link


def m_audio(loc, name, cat, start_idx, end_idx):
    # make concatenated audio following by the catalog from AVSpeech
    # loc       | the location for file to store
    # name      | name for the wav mix file
    # cat       | the catalog with audio link and time
    # start_idx | the starting index of the audio to download and concatenate
    # end_idx   | the ending index of the audio to download and concatenate

    for i in range(start_idx, end_idx):
        f_name = name + str(i)
        link = m_link(cat.loc[i, 'link'])
        start_time = cat.loc[i, 'start_time']
        end_time = start_time + 3.0
        avh.download(loc, f_name, link)
        avh.cut(loc, f_name, start_time, end_time)

if __name__ == "__main__":
    header = ["link", "start_time", "end_time", "x_coord", "y_coord"]
    cat_train = pd.read_csv('../avspeech_train.csv', names=header)

    test = pd.read_csv('../avspeech_test.csv', names=header)
    RANGE = (1, 5)  # then we will download 10 soundtrack
    avh.mkdir('audio_train')
    m_audio('audio_train', 'audio_train', cat_train,
            RANGE[0],
            RANGE[1])

    #make sure to change the RANGE value before running audio_norm
    audio_norm
