import cv2
from mtcnn_cv2 import MTCNN
import pandas as pd
import os


class FaceDetector:
    '''
    This class detect the faces from the frames extracted from the video files.

        Args:
            csv_path(str): path and the name of the csv file, which is a
            dataframe containing the youtube_id of the videos, start and end
            timepoint to be extracted and the x and y coordiantes of the face
            within the frame.
            frame_dir(str): the path to the extracted frames
            output_dir(str): the directory which detected faces within each
            frame will be saved.
    '''
    def __init__(self, csv_path, frame_dir, output_dir):

        self._frame_dir = frame_dir
        self._output_dir = output_dir
        self._detector = MTCNN()
        self._cat_train_df = pd.read_csv(csv_path)
        if not os.path.isdir(self._output_dir):
            os.mkdir(self._output_dir)

    def _bounding_box_check(self, faces, x, y):
        # check the center
        for face in faces:
            bounding_box = face['box']
            if (bounding_box[1] < 0):
                bounding_box[1] = 0
            if (bounding_box[0] < 0):
                bounding_box[0] = 0
            if (bounding_box[0] - 50 > x
                    or bounding_box[0] + bounding_box[2] + 50 < x):
                print('change person from')
                print(bounding_box)
                print('to')
                continue
            if (bounding_box[1] - 50 > y
                    or bounding_box[1] + bounding_box[3] + 50 < y):
                print('change person from')
                print(bounding_box)
                print('to')
                continue
            return bounding_box

    def _face_detect(self, file):
        name = file.replace('.jpg', '').split('-')
        log = self._cat_train_df.iloc[int(name[0])]
        x = log.iloc[3] # this column contain the x-coordiante of the face
        y = log.iloc[4]  # this column contain the y-coordiante of the face

        img = cv2.imread('%s%s' % (self._frame_dir, file))
        x = img.shape[1] * x
        y = img.shape[0] * y
        faces = self._detector.detect_faces(img)
        # check if detected faces
        if (len(faces) == 0):
            print('no face detect: ' + file)
            return  #no face
        bounding_box = self._bounding_box_check(faces, x, y)
        if (bounding_box == None):
            print('face is not related to given coord: ' + file)
            return
        print(file, " ", bounding_box)
        print(file, " ", x, y)
        crop_img = img[bounding_box[1]:bounding_box[1] + bounding_box[3],
                    bounding_box[0]:bounding_box[0] + bounding_box[2]]
        crop_img = cv2.resize(crop_img, (160, 160))
        cv2.imwrite('%s/frame_' % self._output_dir + name[0] + '_' + name[1] + '.jpg',
                    crop_img)

    def detect(self, detect_range):
        for i in range(detect_range[0], detect_range[1]):
            for j in range(1, 76):
                file_name = "%d-%02d.jpg" % (i, j)
                if (not os.path.exists('%s%s' % (self._frame_dir, file_name))):
                    print('cannot find input: ' + '%s%s' %
                          (self._frame_dir, file_name))
                    continue
                self._face_detect(file_name)