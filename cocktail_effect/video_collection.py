from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import datetime

from cocktail_effect.AVHandler import *

class VideoCollect:
    '''
    A class to download the videos and generate respective frames.

    Args:
        loc(str) = the location for downloaded file
        cat(pd.DataFrame) = the catalog with video link and time (avspeech_train.csv)
        start_idx(int) = the starting index of the video to download
        end_idx(int) = the ending index of the video to download
        rm_video(bool) = boolean value for delete video and only keep the frames (True by default)

        start_idx and end_idx allow you to choose the # of videos to analyse
    '''

    def __init__(self, loc, cat, start_idx, end_idx, rm_video=True):
        self.loc = loc
        self.cat = cat
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.rm_video = rm_video

    def video_download(self):

        for i in range(self.start_idx, self.end_idx):
            command = 'cd %s;' % self.loc
            f_name = str(i)
            link = m_link(self.cat.loc[i, 'link'])
            start_time = self.cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            start_time = datetime.timedelta(seconds=start_time)
            end_time = datetime.timedelta(seconds=end_time)
            command += 'ffmpeg -i $(youtube-dl -f ”mp4“ --get-url ' + link + ') ' + '-c:v h264 -c:a copy -ss %s -to %s %s.mp4' \
                    % (start_time, end_time, f_name)
            os.system(command)

    def generate_frames(self):

        mkdir('frames')
        for i in range(self.start_idx, self.end_idx):
            command = 'cd %s;' % self.loc
            f_name = str(i)
            command += 'ffmpeg -i %s.mp4 -y -f image2  -vframes 75 ../frames/%s-%%02d.jpg' % (
                f_name, f_name)
            os.system(command)

    def download_video_frames(self):

        mkdir('frames')
        for i in range(self.start_idx, self.end_idx + 1):
            command = 'cd %s;' % self.loc
            f_name = str(i)
            link = m_link(self.cat.loc[i, 'link'])
            start_time = self.cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            start_time = datetime.timedelta(seconds=start_time)
            end_time = datetime.timedelta(seconds=end_time)
            command += 'ffmpeg -i $(youtube-dl -f ”mp4“ --get-url ' + link + ') ' + '-c:v h264 -c:a copy -ss %s -to %s %s.mp4;' \
                    % (start_time, end_time, f_name)

            # converts to frames
            command += 'ffmpeg -i %s.mp4 -vf fps=25 ../frames/%s-%%02d.jpg;' % (
                f_name, f_name)

            if self.rm_video:
                command += 'rm %s.mp4' % f_name
            os.system(command)
