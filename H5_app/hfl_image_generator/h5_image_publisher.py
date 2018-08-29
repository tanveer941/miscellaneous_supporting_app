

import ecal
import json
import h5py
import os
import sys
import numpy as np
import cv2
import imageservice_pb2
import time

with open('topics.json') as data_file:
    json_data = json.load(data_file)

# fname = json_data['h5_filename']

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

class H5ReaderSequence(object):
    def __init__(self, fname):
        self.reset(fname)
        self.h5_obj = h5py.File(fname, "r")
        # self.h5_obj = h5py.File(r'C:\Users\uidr8549\Documents\SametimeFileTransfers\2018.04.25_at_12.28.14_svu-mi5_149.h5', "r")
        self.h5_grp_lst = []
        self.img_pth_lst = []
        self.dvc_chnl_map = self.get_device_channel_name()

    def get_img_for_tmstamp_and_chnl(self, device_name, channel_name, timestamp):

        # get the channel group for channel
        # chanl_grp = [evry_chnl for evry_chnl in self.h5_grp_lst[1:] if channel_name in str(evry_chnl)]

        h5_img_pth = device_name + '/' + channel_name + '/' + str(timestamp)
        print "h5_img_pth:: ", h5_img_pth
        if h5_img_pth:
            img_data = self.h5_obj[h5_img_pth]
            print "img_data :: ", img_data
            if isinstance(img_data, h5py.Dataset):
                img_arr = np.zeros(img_data.shape, dtype=np.uint8)
                img_data.read_direct(img_arr)

                # cv2.imshow("Output", img_arr)
                # cv2.waitKey(0)

                # Encode the image to be sent across protobuf
                ecal_encode_img = cv2.imencode('.png', img_arr)[1].tostring()
                return ecal_encode_img
            else:
                return None
        else:
            return None

    def get_tmstamps_for_dvc_chnl(self, device_name, channel):

        # make channel group for channel
        # chanl_grp = [evry_chnl for evry_chnl in self.h5_grp_lst if channel in str(evry_chnl)]
        print "\n"
        # print "channel -> ", channel
        # print "device name -> ", device_name
        # print "self.h5_grp_lst : ", self.h5_grp_lst
        for evry_chnl in self.h5_grp_lst[:]:
            dvc_chnl_lst = str(evry_chnl).split('/')
            # print "----------------", evry_chnl, dvc_chnl_lst
            if len(dvc_chnl_lst) == 2:
                if ('/' in str(evry_chnl)) :
                    if (device_name == dvc_chnl_lst[0]) and (channel == dvc_chnl_lst[1]):
                        chanl_grp = str(evry_chnl)
                        print "chanl_grp %s exists " %chanl_grp
                        timestamps = self.h5_obj[chanl_grp]
                        # timestamps = data["mfc4xx/MFC4xx_long_image_right"]
                        timestamps = [str(ech_tmstamp) for ech_tmstamp in timestamps.keys()]
                        # print("timestamps >> ", timestamps)
                        return timestamps
                else:
                    print "No matching channel group found for %s %s " %device_name %channel
                    return None


    def get_device_channel_name(self):
        self.h5_obj.visititems(self.print_groups)
        # print "self.h5_grp_lst :: ", self.h5_grp_lst
        device_names_lst = [evry_chnl for evry_chnl in self.h5_grp_lst if '/' not in str(evry_chnl)]
        # chnl_names_lst = [evry_chnl.split('/')[1] for evry_chnl in self.h5_grp_lst if '/' in str(evry_chnl)]
        # print "chnl_names_lst ::: ", device_names_lst, chnl_names_lst
        dvc_chnl_map = {}
        for evry_dvc_name in device_names_lst:
            chnl_lst = []
            for evry_chnl in self.h5_grp_lst:

                if '/' in str(evry_chnl) and evry_chnl.split('/')[0] == evry_dvc_name:
                    chnl_lst.append(evry_chnl.split('/')[1])
                    # print "evry_chnl :>>", evry_dvc_name, evry_chnl
                    # dvc_chnl_map[evry_dvc_name] = [evry_chnl]
            dvc_chnl_map[evry_dvc_name] = chnl_lst
        # print "dvc_chnl_map :: ", dvc_chnl_map
        # chnl_name = str(self.h5_grp_lst[1]).split('/')[1]
        return dvc_chnl_map


    def reset(self, fname):
        if not os.path.isfile(fname):
            print("Error - H5 file not available: %s!" % fname)
            sys.exit()

    # mylist = []
    def print_groups(self, name, obj):

        if isinstance(obj, h5py.Group):
            self.h5_grp_lst.append(name)

    def get_all_timestamps(self):
        # print "????", self.device_name, self.chnl_name,
        timestamps = self.h5_obj[self.h5_grp_lst[1]]
        # timestamps = data["mfc4xx/MFC4xx_long_image_right"]
        timestamps = [str(ech_tmstamp) for ech_tmstamp in timestamps.keys()]
        # print("timestamps >> ", timestamps)
        return timestamps

    def print_img_tmstamp(self, name, obj):

        if isinstance(obj, h5py.Dataset):
            self.img_pth_lst.append(name)

    def get_images(self):

        self.h5_obj.visititems(self.print_img_tmstamp)
        # print "self.img_pth_lst > ", self.img_pth_lst
        for ech_img_pth in self.img_pth_lst:
            img_data = self.h5_obj[ech_img_pth]
            print "img_data :>> ", img_data, img_data.shape
            arr = np.zeros(img_data.shape, dtype=np.uint8)
            # print arr
            # break
            img_data.read_direct(arr)
            # print "arr >> ", arr
            # cv2.imwrite('color_img.jpg', arr)
            # cv2.imshow("Output", arr)
            # cv2.waitKey(0)
            # break

    def get_imgarry_for_tmstamp(self, timestamp):

        self.h5_obj.visititems(self.print_img_tmstamp)
        # print "self.img_pth_lst > ", self.img_pth_lst
        corresondng_img_pth = [ech_img_pth for ech_img_pth in self.img_pth_lst if timestamp in ech_img_pth][0]
        print "......", corresondng_img_pth
        img_data = self.h5_obj[corresondng_img_pth]
        img_arr = np.zeros(img_data.shape, dtype=np.uint8)
        img_data.read_direct(img_arr)

        # cv2.imshow("Output", img_arr)
        # cv2.waitKey(0)

        return img_arr

class H5EcalDataPublisher(object):

    def __init__(self):
        # Initialize ecal service for H5 reader
        # Initialize the proto message object
        ecal.initialize(sys.argv, "H5 data publisher")

        self.initialize_subscr_topics()
        self.initialize_publsr_topics()

        self.define_subscr_callbacks()


    def initialize_subscr_topics(self):

        # Initialize all the subscriber topics
        # self.h5_dvc_subscr_obj = ecal.subscriber(json_data['device_request'])
        self.h5_chnl_subscr_obj = ecal.subscriber(json_data['channel_request'])
        self.h5_img_subscr_obj = ecal.subscriber(json_data['hfl_request'])

    def initialize_publsr_topics(self):

        # Initialize all the publisher topics
        self.h5_chnl_publr_obj = ecal.publisher(json_data['channel_response'])
        self.h5_img_publr_obj = ecal.publisher(json_data['hfl_response'])


    def pub_chnl_data(self, topic_name, msg, time):

        chnl_req_proto_obj = imageservice_pb2.devicesDataRequest()
        chnl_req_proto_obj.ParseFromString(msg)
        bool_chnl_req = chnl_req_proto_obj.required_devicesData
        chnl_resp_proto_obj = imageservice_pb2.devicesDataResponse()
        if bool_chnl_req:
            h5file_obj = H5ReaderSequence(fname)
            # From H5 file we map the dictionary to have device name as
            # keys and value to be their list of corresponding channels
            dvc_chnl_dict = h5file_obj.dvc_chnl_map
            print "dvc_chnl_dict :: ", dvc_chnl_dict
            chnl_resp_proto_obj.deviceCount = len(dvc_chnl_dict.keys())
            if dvc_chnl_dict.keys():
                for ech_dvc_name in dvc_chnl_dict.keys():
                    dvc_data_obj = chnl_resp_proto_obj.devicedata.add()
                    # Send in the device name
                    dvc_data_obj.deviceName = str(ech_dvc_name)
                    channel_lst = dvc_chnl_dict[ech_dvc_name]
                    print "channel_lst :: ", channel_lst
                    if channel_lst:
                        dvc_data_obj.no_of_channels = len(channel_lst)
                    else:
                        dvc_data_obj.no_of_channels = -1
                    for ech_channel in channel_lst:
                        print "ech_channel :> ", ech_channel
                        # Get the timestamps for the device and channel
                        tmstamp_lst = h5file_obj.get_tmstamps_for_dvc_chnl(device_name=str(ech_dvc_name), channel=str(ech_channel))
                        # print "tmstamp_lst >> ", tmstamp_lst
                        if tmstamp_lst is not None:
                            chnl_info_obj = dvc_data_obj.channel_Info.add()
                            chnl_info_obj.channel_name = str(ech_channel)
                            for evry_tmstamp in tmstamp_lst:
                                # print "evry_tmstamp :: ", evry_tmstamp
                                chnl_info_obj.timestamp.append(int(evry_tmstamp))
        else:
            chnl_resp_proto_obj.deviceCount = -1

        self.h5_chnl_publr_obj.send(chnl_resp_proto_obj.SerializeToString())

    def pub_img_data(self, topic_name, msg, time):

        img_req_proto_obj = imageservice_pb2.ImageRequest()
        img_resp_proto_obj = imageservice_pb2.ImageResponse()

        img_req_proto_obj.ParseFromString(msg)
        device_name = img_req_proto_obj.request_device_name
        channel_name = img_req_proto_obj.request_channel_name
        timestamp = img_req_proto_obj.required_timestamp
        print ">>>>..", channel_name, timestamp
        h5file_obj = H5ReaderSequence(fname)
        encoded_img_arr = h5file_obj.get_img_for_tmstamp_and_chnl(device_name, channel_name, timestamp)

        if encoded_img_arr is not None:
            img_resp_proto_obj.response_device_name = device_name
            img_resp_proto_obj.recieved_timestamp = timestamp
            img_resp_proto_obj.response_channel_name = channel_name
            img_resp_proto_obj.base_image = encoded_img_arr
        else:
            img_resp_proto_obj.recieved_timestamp = -1
        self.h5_img_publr_obj.send(img_resp_proto_obj.SerializeToString())


    def define_subscr_callbacks(self):

        # For device data
        # Deprecating device request
        # self.h5_dvc_subscr_obj.set_callback(self.pub_dvc_data)
        # For Channel data
        self.h5_chnl_subscr_obj.set_callback(self.pub_chnl_data)
        # For Image data
        self.h5_img_subscr_obj.set_callback(self.pub_img_data)
        while ecal.ok():
            time.sleep(0.1)


if __name__ == '__main__':

    # D:\\Work\\2018\\code\\LT5G\\HDF5_reader\\2017.09.07_at_20.37.57_camera-mi_1449.h5
    # C:\\Users\\uidr8549\\My Documents\\SametimeFileTransfers\\2018.04.25_at_12.28.14_svu-mi5_149.h5

    # fname = r'D:\Work\2018\code\LT5G\HDF5_reader\20161215_1114_{C24EDA32-C92E-40A9-9AC6-75307E1001F5}.h5'
    # fname = r'C:\Users\uidr8549\My Documents\SametimeFileTransfers\2018.04.25_at_12.28.14_svu-mi5_149.h5'
    # fname = 'D:\\Work\\2018\\code\\LT5G\\HDF5_reader\\2017.09.07_at_20.37.57_camera-mi_1449.h5'
    # outdir = r'D:\Work\2018\code\LT5G\HDF5_reader\HFL_LabelToolExample\hfl_labeltool\hfl_ecal\hfl_image_generator\HFL_images'
    fname = sys.argv[1]

    h5_ecal_inst = H5EcalDataPublisher()


# pyinstaller --onefile hfl_img_generator.py --add-data _ecal_py_2_7_x86.pyd;.