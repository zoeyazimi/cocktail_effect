# Before running, make sure avspeech_train.csv and avspeech_test.csv are in catalog.
# if not, see the requirement.txt
# download and preprocess the data from AVspeech dataset
#class
class AudioDownloader(object):

    def __init__(self, youtube_id, loc, name, cat, start_idx, end_idx):
        "This class helps with downloading the audio"
        self.youtube_id = youtube_id
        self.loc = loc
        self.name = name
        self.cat = cat
        self.start_idx = start_idx
        self.end_idx = end_idx

    def m_link(self):
        # return the youtube actual link
        link = 'https://www.youtube.com/watch?v=' + self.youtube_id

        return link

    def m_audio(self):
        # make concatenated audio following by the catalog from AVSpeech
        # loc       | the location for file to store
        # name      | name for the wav mix file
        # cat       | the catalog with audio link and time
        # start_idx | the starting index of the audio to download and concatenate
        # end_idx   | the ending index of the audio to download and concatenate

        for i in range(self.start_idx, self.end_idx):
            f_name = self.name + str(i)
            link = m_link(self.cat.loc[i, 'link'])
            start_time = self.cat.loc[i, 'start_time']
            end_time = start_time + 3.0
            avh.download(self.loc, f_name, link)
            avh.cut(self.loc, f_name, start_time, end_time)

    def collect_audio(self):
        header = ["link", "start_time", "end_time", "x_coord", "y_coord"]
        cat_train = pd.read_csv('./raw_data/avspeech_train.csv', names=header)
        #cat_test = pd.read_csv('catalog/avspeech_test.csv', names=header)

        # create 80000-90000 audios data from 290K
        avh.mkdir(self.loc)
        m_audio(self.loc, self.loc, cat_train, 1, 3)
