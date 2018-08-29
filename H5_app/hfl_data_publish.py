
import h5py
import os
import sys
import numpy as np
import ecal
# import AlgoInterface_pb2
import imageservice_pb2
import json
import cv2

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

with open('topics.json') as data_file:
    json_data = json.load(data_file)
    # print(json_data)

request = str(json_data['request'])
response = str(json_data['response'])
h5_filename = str(json_data['h5_filename'])

ecal.initialize(sys.argv, "HFL data publisher")
hfl_subscr_obj = ecal.subscriber(request)
hfl_publs_obj = ecal.publisher(topic_name=response)

hfl_req_proto_obj = imageservice_pb2.ImageRequest()
hfl_resp_proto_obj = imageservice_pb2.HFLResponse()

class H5ReaderSequence(object):
    def __init__(self, fname):
        self.reset(fname)
        self.lastLoadFilename = ""

    def reset(self, fname):
        if not os.path.isfile(fname):
            print("Error - H5 file not available: %s!" % fname)
            sys.exit()
        # self.data = h5py.File(fname, "r")
        self.img_w = 128
        self.img_h = 32
        self.max_d = 30
        self.i = 0
    #     self.max_i = len(self.data["/HFL130/PCA/PcaDebugData/Data/m_Intensity_au16"])
    #
    # def getI(self):
    #     return self.i
    #
    # def setI(self, i):
    #     if i >= self.getMaxI():
    #         i = 0
    #     if i < 0:
    #         i = self.getMaxI() - 1
    #     self.i = i
    #
    # def getMaxI(self):
    #     return self.max_i
    #
    # def get(self, i):
    #     self.setI(i)
    #     raw_int = self.data["/HFL130/PCA/PcaDebugData/Data/m_Intensity_au16"][self.i][0][:(self.img_h * self.img_w)]
    #     raw_ran = self.data["/HFL130/PCA/PcaDebugData/Data/m_Dist_MF_as32"][self.i][0][:(self.img_h * self.img_w)]
    #     mask = raw_ran > (self.max_d * 4096)
    #     raw_ran[mask] = self.max_d * 4096
    #     raw_int[mask] = 0
    #     dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(self.img_w, self.img_h))
    #     dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(self.img_w, self.img_h))
    #     return (dat_int, dat_ran)
    #
    # def get_all_timestamps(self, filename):
    #
    #     data = h5py.File(filename, "r")
    #     self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
    #     return self.idxlist

    def loadData(self, filename, idx):

        data = h5py.File(filename, "r")
        if self.lastLoadFilename != filename:
            self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
        # print("self.idxlist :: ", self.idxlist)
        # idx = self.idxlist.index(timestamp)
        try:
            timestamp = self.idxlist[idx]
            raw_int = data["/HFL130/PCA/PcaDebugData/Data/m_Intensity_au16"][idx][0][:(self.img_h * self.img_w)]
            raw_ran = data["/HFL130/PCA/PcaDebugData/Data/m_Dist_MF_as32"][idx][0][:(self.img_h * self.img_w)]
            mask = raw_ran > (self.max_d * 4096)
            raw_ran[mask] = self.max_d * 4096
            raw_int[mask] = 0
            dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(self.img_w, self.img_h))
            dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(self.img_w, self.img_h))

            # cv2.imwrite('color_img.jpg', dat_ran)
            # cv2.imshow('Color image', dat_ran)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            dat_int = cv2.imencode('.png', dat_int)[1].tostring()
            dat_ran = cv2.imencode('.png', dat_ran)[1].tostring()
            data.close()
            self.lastfilename = filename
        except IndexError, e:
            print "Time stamp does not exist for this index"
            timestamp = 0
            dat_int = ''
            dat_ran = ''
        return (timestamp, dat_int, dat_ran)

    def loadPreviouseData(self, filename, timestamp):
        data = h5py.File(filename, "r")
        if self.lastLoadFilename != filename:
            self.idxlist = [str(d) for d in data["/MTS/Package/TimeStamp"]]
        idx = self.idxlist.index(timestamp) - 1
        if idx < 0:
            return ([], [])
        raw_int = data["/HFL130/PCA/PcaDebugData/Data/m_Intensity_au16"][idx][0][:(self.img_h * self.img_w)]
        raw_ran = data["/HFL130/PCA/PcaDebugData/Data/m_Dist_MF_as32"][idx][0][:(self.img_h * self.img_w)]
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

def publish_hfl_data():

    # subscribe the HFL request to receive the timestamp and file name

    while ecal.ok():
        ret, msg, time = hfl_subscr_obj.receive(500)
        # print("---:: ", ret, msg, time, type(msg))
        if msg is not None:
            hfl_req_proto_obj.ParseFromString(msg)
            idx_req = hfl_req_proto_obj.image_index
            # timestamp = int(timestamp)
            print("--->", idx_req, h5_filename)
            h5file_obj = H5ReaderSequence(h5_filename)
            timestamp, inten_data, dist_data = h5file_obj.loadData(h5_filename, int(idx_req))
            print("timestamp :: ", timestamp)
            hfl_resp_proto_obj.timestamp = int(timestamp)
            hfl_resp_proto_obj.HFL_image_index = int(idx_req)
            if inten_data != '' or dist_data != '':
                hfl_resp_proto_obj.intensity_image = inten_data
                hfl_resp_proto_obj.distance_image = dist_data
            else:
                hfl_resp_proto_obj.intensity_image = inten_data
                hfl_resp_proto_obj.distance_image = dist_data

            hfl_publs_obj.send(hfl_resp_proto_obj.SerializeToString())


if __name__ == '__main__':

    publish_hfl_data()

    # fname = r'D:\Work\2018\code\LT5G\HDF5_reader\2017.09.07_at_20.37.57_camera-mi_1449.h5'
    # h5file_obj = H5ReaderSequence(fname)
    # # st_time, end_time = h5file_obj.loadStartStopTimestamp(fname)
    # # print("st_time, end_time :: ", st_time, end_time)
    # tmstamps_lst = h5file_obj.get_all_timestamps(fname)
    # # tm_stamp = '1504816686729381'
    # outdir = r"D:\Work\2018\code\LT5G\HDF5_reader\h5_read_v1\imgdir"
    # for tm_stamp in tmstamps_lst:
    #     inten_data, dist_data = h5file_obj.loadData(fname, tm_stamp)
    #     # print("arr_data :: ", arr_data)
    #     print("timestamp :: ", tm_stamp)
    #     cv2.imwrite(outdir + "\\HFL130INTENSITY_%s.jpg" % tm_stamp, inten_data)
    #     cv2.imwrite(outdir + "\\HFL130DISTANCE_%s.jpg" % tm_stamp, dist_data)
