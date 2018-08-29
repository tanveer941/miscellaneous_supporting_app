
import h5py
import os
import sys
import numpy as np
import cv2

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

class H5ReaderSequence(object):
    def __init__(self, fname):
        if not os.path.isfile(fname):
            print("Error - H5 file not available: %s!" % fname)
            sys.exit()
        self.data = h5py.File(fname, "r")
        self.h5_dataset_lst = []
        self.intensity_path, self.dist_path = self.get_intensity_and_dist_path()
        self.reset(fname)
        self.lastLoadFilename = ""

    def get_img_dataset(self, name, obj):

        if isinstance(obj, h5py.Dataset):
            self.h5_dataset_lst.append(name)

    def get_intensity_and_dist_path(self):
        # self.data
        self.data.visititems(self.get_img_dataset)
        print "self.h5_dataset_lst :: ", self.h5_dataset_lst
        intensity_path = [ech_dtset_path for ech_dtset_path in self.h5_dataset_lst if 'Intensity' in ech_dtset_path][0]
        dist_path = [ech_dtset_path for ech_dtset_path in self.h5_dataset_lst if 'Dist' in ech_dtset_path][0]
        print "paths :: ", intensity_path, dist_path
        # exit(0)
        return intensity_path, dist_path

    def reset(self, fname):

        self.img_w = 128
        self.img_h = 32
        self.max_d = 30
        self.i = 0
        self.max_i = len(self.data[self.intensity_path])

    def getI(self):
        return self.i

    def setI(self, i):
        if i >= self.getMaxI():
            i = 0
        if i < 0:
            i = self.getMaxI() - 1
        self.i = i

    def getMaxI(self):
        return self.max_i

    def get(self, i):
        self.setI(i)
        raw_int = self.data["/HFL130/PCA/PcaDebugData/Data/m_Intensity_au16"][self.i][0][:(self.img_h * self.img_w)]
        raw_ran = self.data["/HFL130/PCA/PcaDebugData/Data/m_Dist_MF_as32"][self.i][0][:(self.img_h * self.img_w)]
        mask = raw_ran > (self.max_d * 4096)
        raw_ran[mask] = self.max_d * 4096
        raw_int[mask] = 0
        dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(self.img_w, self.img_h))
        dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(self.img_w, self.img_h))
        return (dat_int, dat_ran)

    def get_all_timestamps(self, filename):

        data = h5py.File(filename, "r")
        self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
        return self.idxlist

    def loadData(self, filename, timestamp):

        data = h5py.File(filename, "r")
        if self.lastLoadFilename != filename:
            self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
        # print("self.idxlist :: ", self.idxlist)
        idx = self.idxlist.index(timestamp)
        try:
            # timestamp = self.idxlist[idx]
            raw_int = data[self.intensity_path][idx][0][:(self.img_h * self.img_w)]
            raw_ran = data[self.dist_path][idx][0][:(self.img_h * self.img_w)]
            mask = raw_ran > (self.max_d * 4096)
            raw_ran[mask] = self.max_d * 4096
            raw_int[mask] = 0
            dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(self.img_w, self.img_h))
            dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(self.img_w, self.img_h))
            data.close()
            self.lastfilename = filename
        except IndexError, e:
            pass
            print "Time stamp does not exist for this index"
        return (dat_int, dat_ran)

    def loadPreviouseData(self, filename, timestamp):
        data = h5py.File(filename, "r")
        if self.lastLoadFilename != filename:
            self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
        idx = self.idxlist.index(timestamp) - 1
        if idx < 0:
            return ([], [])
        raw_int = data[self.intensity_path][idx][0][:(self.img_h * self.img_w)]
        raw_ran = data[self.dist_path][idx][0][:(self.img_h * self.img_w)]
        mask = raw_ran > (self.max_d * 4096)
        raw_ran[mask] = self.max_d * 4096
        raw_int[mask] = 0
        dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(self.img_w, self.img_h))
        dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(self.img_w, self.img_h))
        data.close()
        self.lastfilename = filename
        return (dat_int, dat_ran)

    def loadStartStopTimestamp(self, filename):

        data = h5py.File(filename, "r")
        starttimestamp = data["/MTS/Package/TimeStamp"][0]
        stoptimestamp = data["/MTS/Package/TimeStamp"][-1]
        data.close()
        return (starttimestamp, stoptimestamp)

    def getInfo(self, i):

        return [str(self.data.filename),
                str(self.data["/MTS/Package/TimeStamp"][i]),
                str(self.data["/MTS/Package/CycleID"][i]),
                str(self.data["/MTS/Package/CycleCount"][i])]

if __name__ == '__main__':

    fname = r'D:\Work\2018\code\LT5G\HDF5_reader\2017.09.07_at_20.37.57_camera-mi_1449.h5'
    outdir = r'D:\Work\2018\code\LT5G\HDF5_reader\HFL_LabelToolExample\hfl_labeltool\hfl_ecal\hfl_image_generator\HFL_images'

    print "ARGUMENT 1 : H5  file path. ex: D:\\2017.09.07_at_20.37.57_camera-mi_1449.h5"
    print "ARGUMENT 2 : H5  Image folder ex: D:\\\HFL_images"

    fname = sys.argv[1]
    outdir = sys.argv[2]

    h5file_obj = H5ReaderSequence(fname)
    # st_time, end_time = h5file_obj.loadStartStopTimestamp(fname)
    # print("st_time, end_time :: ", st_time, end_time)
    tmstamps_lst = h5file_obj.get_all_timestamps(fname)
    # tm_stamp = '1504816686729381'
    # outdir = r"D:\Work\2018\code\LT5G\HDF5_reader\h5_read_v1\imgdir"
    # outdir = r"\HFL_Images"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    print outdir
    for tm_stamp in tmstamps_lst:
        inten_data, dist_data = h5file_obj.loadData(fname, tm_stamp)
        # print("arr_data :: ", arr_data)
        print("timestamp :: ", tm_stamp)
        cv2.imwrite(outdir + "\\HFL130INTENSITY_%s.jpg" % tm_stamp, inten_data)
        cv2.imwrite(outdir + "\\HFL130DISTANCE_%s.jpg" % tm_stamp, dist_data)

# pyinstaller --onefile hfl_img_generator.py