

import ecal
import json
import h5py
import os
import sys
import numpy as np
import cv2
import imageservice_pb2
import time
from PyQt4 import QtCore
from PyQt4 import QtGui
from PIL import Image

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

        # Fetch all the timestamps
        # self.timestamps = self.get_all_timestamps()
        # print "info >>> ", self.dvc_chnl_map

        # # Get timestamps based on channel name
        # tmstamps = self.get_all_tmstamps_chnls('svu32x_rear')
        # print "tmstamps :: ", tmstamps

        # # Will fetch you an encoded image for a given channel and timestamp
        # self.get_img_for_tmstamp_and_chnl('svu32x_left', 1524659294095512)

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
        # else:
        #     return None


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
        # for ec

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
        self.h5_pixel_obj = h5py.File(fpixelfile, "w")
        self.define_subscr_callbacks()


    def initialize_subscr_topics(self):

        # Initialize all the subscriber topics
        # self.h5_dvc_subscr_obj = ecal.subscriber(json_data['device_request'])
        self.h5_chnl_subscr_obj = ecal.subscriber(json_data['channel_request'])
        self.h5_img_subscr_obj = ecal.subscriber(json_data['hfl_request'])
        self.h5_pixelwriter_obj = ecal.subscriber(json_data['pixelwrite_request'])

    def initialize_publsr_topics(self):

        # Initialize all the publisher topics
        # self.h5_dvc_publr_obj = ecal.publisher(json_data['device_response'])
        self.h5_chnl_publr_obj = ecal.publisher(json_data['channel_response'])
        self.h5_img_publr_obj = ecal.publisher(json_data['hfl_response'])

    # def pub_dvc_data(self, topic_name, msg, time):
    #     # print "pub_dvc_data >> ", topic_name, msg
    #     dvctyp_req_proto_obj = imageservice_pb2.deviceTypeRequest()
    #     dvctyp_req_proto_obj.ParseFromString(msg)
    #     dvc_type = dvctyp_req_proto_obj.device_type
    #     # print "dvc_type >> ", dvc_type
    #     # Publish device type
    #     dvctyp_resp_proto_obj = imageservice_pb2.deviceTypeResp()
    #     if dvc_type == "True":
    #         h5file_obj = H5ReaderSequence(fname)
    #         print "device_name :: ", h5file_obj.device_name
    #         dvctyp_resp_proto_obj.device_type = h5file_obj.device_name
    #     else:
    #         dvctyp_resp_proto_obj.device_type = ""

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
            chnl_resp_proto_obj.deviceCount = len(dvc_chnl_dict.keys())
            if dvc_chnl_dict.keys():
                for ech_dvc_name in dvc_chnl_dict.keys():
                    dvc_data_obj = chnl_resp_proto_obj.devicedata.add()
                    # Send in the device name
                    dvc_data_obj.deviceName = str(ech_dvc_name)
                    channel_lst = dvc_chnl_dict[ech_dvc_name]
                    # print "channel_lst :: ", channel_lst
                    if channel_lst:
                        dvc_data_obj.no_of_channels = len(channel_lst)
                    else:
                        dvc_data_obj.no_of_channels = -1
                    for ech_channel in channel_lst:
                        print "ech_channel :> ", ech_channel
                        # Get the timestamps for the device and channel
                        tmstamp_lst = h5file_obj.get_tmstamps_for_dvc_chnl(device_name=str(ech_dvc_name), channel=str(ech_channel))
                        print "tmstamp_lst >> ", tmstamp_lst
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


    def subscribe_pixel_images(self,topic_name,msg,time):
        print "received data for pixel label write"
        pixel_img_req_proto_obj = imageservice_pb2.PixelLabelWriteRequest()
        pixel_img_req_proto_obj.ParseFromString(msg)
       # devicename = pixel_img_req_proto_obj.devicename
        channelname = pixel_img_req_proto_obj.response_channel_name
        timestamp = pixel_img_req_proto_obj.recieved_timestamp
        print("12334455")
        obj_PixelImageData = pixel_img_req_proto_obj.image
        # print('object data',obj_PixelImageData)

        for ech_pixel_item in obj_PixelImageData:
            print("inside the loop")
            imageName = ech_pixel_item.name
            #format = ech_pixel_item.format
            data = ech_pixel_item.data
            width = ech_pixel_item.width
            height = ech_pixel_item.height
            print('name',imageName)

            key = str(channelname) + '/'+str(timestamp)+'/'+str(imageName)
            print('key',key)
            # print('data',data)
            nparray = np.fromstring(data, np.uint8)
            print "nparray :: ", nparray
            re_img_np_ary = cv2.imencode(mask_layer, cv2.IMREAD_COLOR)


            # print "QBuffer.data() 1:: "
            # from PyQt4.QtGui import QImage
            # from PyQt4.QtCore import QBuffer
            # print "QBuffer.data() 2:: "
            # print('type: ',type(ech_pixel_item.data))
            # QBuffer.setData(ech_pixel_item.data)
            # print "QBuffer.data() :: ", QBuffer.data()
            # b = QImage.loadFromData(QBuffer.data())
            # print "b>> ", b

            import PIL.ImageColor as ImageColor
            # rgb = ImageColor.getrgb('red')
            # solid_color = np.expand_dims(np.ones_like(nparray), axis=2) * np.reshape(list(rgb), [1, 1, 3])
            # print "solid_color >> ", solid_color
            pil_mask = Image.fromarray(np.uint8(255.0 * 0.4 * nparray)).convert('L')
            print "pil_mask >> ", pil_mask
            mask_layer = np.array(pil_mask.convert('RGB'))
            print "mask_layer : ", mask_layer


            # CV_LOAD_IMAGE_COLOR
            re_img_np_ary = cv2.imdecode(mask_layer, cv2.IMREAD_COLOR)
            cv2.imshow("window", re_img_np_ary)
            cv2.imwrite("image.png", re_img_np_ary)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            print ">>>"
            # self.h5_pixel_obj.create_dataset('SVFront/296/876876876_SVFront_296_Vehicle_24',data=re_img_np_ary)
            # cv2.imshow("window", solid_color)
            # cv2.imwrite("image.png", solid_color)
            self.h5_pixel_obj.close()





    def define_subscr_callbacks(self):

        # For device data
        # Deprecating device request
        # self.h5_dvc_subscr_obj.set_callback(self.pub_dvc_data)
        # For Channel data
        self.h5_chnl_subscr_obj.set_callback(self.pub_chnl_data)
        # For Image data
        self.h5_img_subscr_obj.set_callback(self.pub_img_data)
        self.h5_pixelwriter_obj.set_callback(self.subscribe_pixel_images)
        while ecal.ok():
            time.sleep(0.1)


if __name__ == '__main__':

    # D:\\Work\\2018\\code\\LT5G\\HDF5_reader\\2017.09.07_at_20.37.57_camera-mi_1449.h5
    # C:\\Users\\uidr8549\\My Documents\\SametimeFileTransfers\\2018.04.25_at_12.28.14_svu-mi5_149.h5

    # fname = r'D:\Work\2018\code\LT5G\HDF5_reader\20161215_1114_{C24EDA32-C92E-40A9-9AC6-75307E1001F5}.h5'
    fname = r'C:\Users\uidr8549\My Documents\SametimeFileTransfers\2018.04.25_at_12.28.14_svu-mi5_149.h5'
    # fname = 'D:\\Work\\2018\\code\\LT5G\\HDF5_reader\\2017.09.07_at_20.37.57_camera-mi_1449.h5'
    # outdir = r'D:\Work\2018\code\LT5G\HDF5_reader\HFL_LabelToolExample\hfl_labeltool\hfl_ecal\hfl_image_generator\HFL_images'
    #fname = sys.argv[1]
    # fname = 'D:\\Continuous_2013.12.19_at_14.10.48\\2018.04.25_at_12.28.14_svu-mi5_149.h5'
    fpixelfile = 'D:\\PixelData.h5'

    # h5file_obj = H5ReaderSequence(fname)
    # h5file_obj.get_imgarry_for_tmstamp(timestamp='1481800461765472')

    h5_ecal_inst = H5EcalDataPublisher()


# pyinstaller --onefile hfl_img_generator.py