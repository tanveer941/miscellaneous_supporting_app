

import ecal
import sys
import json
import os
import time
import h5py
import pointcloud_pb2
import common_pb2
from datetime import datetime

BEXIT = True
SERVICE_READINESS = True
with open('topics.json') as data_file:
    json_data = json.load(data_file)

class H5ReaderSequence(object):
    def __init__(self, fname):
        self.reset(fname)
        self.h5_obj = h5py.File(fname, "r")
        self.pcl_dataset_dict = {}
        self.h5_grp_lst = []

    def reset(self, fname):
        if not os.path.isfile(fname):
            print("Error - H5 file not available: %s!" % fname)
            sys.exit()

    def print_groups(self, name, obj):

        if isinstance(obj, h5py.Group):
            self.h5_grp_lst.append(name)

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

    # def get_all_timestamps(self):
    #     """
    #     Get all the timestamps from the H5 file in a list
    #     :return:
    #     """
    #     timestamp_dtset_obj = self.h5_obj['/MTS/Timestamp']
    #     # print("timestamp_dtset_obj ::", timestamp_dtset_obj.value, dir(timestamp_dtset_obj))
    #     tmstamp_lst = list(timestamp_dtset_obj.value)
    #     print("tmstamp_lst::", len(tmstamp_lst))
    #     return tmstamp_lst

    def get_all_timestamps(self):
        """
        Get all the timestamps from the H5 file in a list
        :return:
        """
        timestamp_dtset_obj = self.h5_obj['/HFLXXX/POINTCLOUD']
        # print("timestamp_dtset_obj ::", dir(timestamp_dtset_obj))
        # print(timestamp_dtset_obj.values())
        tmstamp_lst = []
        for tmstamp, pcl_data in timestamp_dtset_obj.iteritems():
            # print(k, v)
            tmstamp_lst.append(tmstamp)
        # tmstamp_lst = list(timestamp_dtset_obj.value)
        print("tmstamp_lst::", len(tmstamp_lst))
        return tmstamp_lst

    # def get_pcl_points_for_tmstamp(self, time_stamp):
    #     timestamp_dtset_obj = self.h5_obj['/MTS/Timestamp']
    #     # print("timestamp_dtset_obj ::", timestamp_dtset_obj.value, dir(timestamp_dtset_obj))
    #     all_tmstamps = list(timestamp_dtset_obj.value)
    #     tmstamp_idx = all_tmstamps.index(time_stamp)
    #     print("tmstamp_idx ::>", tmstamp_idx)
    #     pnt_cld_obj = self.h5_obj['/MTS/POINTCLOUD']
    #     pcd_dt_lst = []
    #     for name, evry_pntCld_member in pnt_cld_obj.items():
    #         # print("name::", name, evry_pntCld_member)
    #         if isinstance(evry_pntCld_member, h5py.Group):
    #             ordinate_lst = []
    #             for pcd_infoname, evry_pntCld_info in evry_pntCld_member.items():
    #                 # print("entry confirm")
    #                 pointCloud_member_names = ['Xpoint', 'Ypoint', 'Zpoint', 'Ampl']
    #                 if isinstance(evry_pntCld_info, h5py.Dataset):
    #                     if pcd_infoname in pointCloud_member_names:
    #                         # Only if x,y and z co-ordinates exist
    #                         ordinate_values = evry_pntCld_info.value
    #                         # print("evry_pntCld_info ::", pcd_infoname, ordinate_values)
    #                         ordinate_lst.append(ordinate_values[tmstamp_idx] / 1.0)
    #             if ordinate_lst:
    #                 pcd_dt_lst.append(ordinate_lst)
    #     # print("pcd_dt_lst ::", pcd_dt_lst)
    #     return pcd_dt_lst

    def get_pcl_dataset(self, name, obj):
        if isinstance(obj, h5py.Dataset):
            self.pcl_dataset_dict[name] = obj

    def save_ref_imf(self, img_pnt_dist_lst, img_pnt_intn_lst, tmstamp_str):
        # print "save_ref_imf >>"
        img_w = 128
        img_h = 32
        max_d = 30
        import numpy as np
        import cv2
        # raw_int = data[self.intensity_path][idx][0][:(img_h * img_w)]
        # raw_ran = data[self.dist_path][idx][0][:(img_h * img_w)]
        img_dist_arr = np.asarray(img_pnt_dist_lst)
        img_intn_arr = np.asarray(img_pnt_intn_lst)

        # img_arr = img_pnt_lst
        # print "img_arr ::", img_arr
        raw_ran = img_dist_arr[:(img_h * img_w)]
        raw_int = img_intn_arr[:(img_h * img_w)]
        mask = raw_ran > (max_d * 4096)
        raw_ran[mask] = max_d * 4096
        raw_int[mask] = 0
        dat_int = np.rot90(np.asarray(raw_int, dtype=np.uint8).reshape(img_w, img_h))
        dat_ran = np.rot90(np.asarray(raw_ran / 4096.0, dtype=np.float32).reshape(img_w, img_h))
        # print "dat_ran >>", dat_ran, dat_ran.shape
        cv2.imwrite(r"distance//distance_%s.jpg"%tmstamp_str, dat_ran)
        cv2.imwrite(r"intensity//intensity_%s.jpg" % tmstamp_str, dat_int)

    def get_pcl_points_for_tmstamp(self, time_stamp):

        # pcl_path = '/POINTCLOUD' + r'/' + str(time_stamp)
        # print("------------------------------------------", pcl_path)
        # pnt_cld_dtset_obj = self.h5_obj[pcl_path]
        st_time = datetime.now()
        pnt_cld_dtset_obj = self.h5_obj['/HFLXXX/POINTCLOUD']

        # print("pnt_cld_dtset_obj >", dir(pnt_cld_dtset_obj), type(pnt_cld_dtset_obj))
        if not self.pcl_dataset_dict:
            pnt_cld_dtset_obj.visititems(self.get_pcl_dataset)
        # print("self.pcl_dataset_dict :: ", self.pcl_dataset_dict)
        pcl_dtset = self.pcl_dataset_dict[str(time_stamp)]
        # print("pcl_dtset ::", pcl_dtset, dir(pcl_dtset))
        # print pcl_dtset.value

        # Read the distance image which is written with the PCL points
        if len(pcl_dtset.value[0]) > 4:
            imag_pnt_dist_lst = [evry_tupl[4] for evry_tupl in pcl_dtset.value]
            imag_pnt_intn_lst = [evry_tupl[5] for evry_tupl in pcl_dtset.value]
            self.save_ref_imf(imag_pnt_dist_lst, imag_pnt_intn_lst, str(time_stamp))
        else:
            print "No reference image data"

        # pcl_dtset.value
        ed_time = datetime.now()
        duration = ed_time-st_time
        print("duration::", duration.total_seconds())
        return pcl_dtset.value


class PointCloudService(object):

    def __init__(self, H5FileName):

        self.h5_file_name = H5FileName
        self.tmstamp_lst = []

        # Initialize eCAL
        ecal.initialize(sys.argv, "Point cloud data publisher")
        global ALGO_READINESS
        ALGO_READINESS = False
        self.initialize_subscr_topics()
        self.initialize_publsr_topics()

        self.define_subscr_callbacks()

    def initialize_subscr_topics(self):

        # Initialize all the subscriber topics
        self.pnt_cld_dvc_subscr_obj = ecal.subscriber(json_data['pointcloud_device_request'])
        self.pnt_cld_data_subscr_obj = ecal.subscriber(json_data['pointcloud_data_request'])
        self.pnt_cld_end_subscr_obj = ecal.subscriber(json_data['pointcloud_end_response'])

    def initialize_publsr_topics(self):

        # Initialize all the publisher topics
        self.pnt_cld_dvc_publr_obj = ecal.publisher(json_data['pointcloud_device_response'])
        self.pnt_cld_data_publr_obj = ecal.publisher(json_data['pointcloud_data_response'])
        self.pnt_cld_ready_obj = ecal.publisher(json_data['pointcloud_begin_response'])

    def pub_pnt_cld_dvc_data(self, topic_name, msg, time):
        dvc_dt_proto_obj = common_pb2.DevicesDataRequest()
        dvc_dt_proto_obj.ParseFromString(msg)
        bool_dvc_req = dvc_dt_proto_obj.requiredDevicesData
        # pnt_cld_resp_proto_obj = pointcloud_pb2.PointCloudDataResponse()
        tmstamp_resp_proto_obj = common_pb2.DevicesDataResponse()
        if bool_dvc_req:
            h5file_obj = H5ReaderSequence(self.h5_file_name)
            dvc_chnl_name_dict = h5file_obj.get_device_channel_name()
            print "dvc_chnl_name_dict ::", dvc_chnl_name_dict
            tmstamps_lst = h5file_obj.get_all_timestamps()
            print("tmstamps_lst::", tmstamps_lst)
            if tmstamps_lst:
                tmstamp_resp_proto_obj.deviceCount = 1
                dvc_info_obj = tmstamp_resp_proto_obj.deviceDataInfo.add()
                dvc_info_obj.deviceName = dvc_chnl_name_dict.keys()[0]
                dvc_info_obj.numOfChannels = 1
                chnl_info_obj = dvc_info_obj.channelInfoAttr.add()
                chnl_info_obj.channelName = dvc_chnl_name_dict[dvc_chnl_name_dict.keys()[0]][0]
                for evry_tmstamp in tmstamps_lst:
                    # print "evry_tmstamp :: ", evry_tmstamp
                    chnl_info_obj.timeStamp.append(int(evry_tmstamp))
            else:
                tmstamp_resp_proto_obj.deviceCount = -1

            self.pnt_cld_dvc_publr_obj.send(tmstamp_resp_proto_obj.SerializeToString())

    def pub_pnt_cld_points_data(self, topic_name, msg, time):
        # print "pub_pnt_cld_points_data ::"
        data_pcl_proto_obj = common_pb2.DataRequest()
        data_pcl_proto_obj.ParseFromString(msg)
        time_stamp = data_pcl_proto_obj.requiredTimestamp
        device_name = data_pcl_proto_obj.requestDeviceName
        channel_name = data_pcl_proto_obj.requestChannelName
        unique_id = data_pcl_proto_obj.uniqueId
        pcl_resp_proto_obj = pointcloud_pb2.PointCloudDataResponse()
        print("time_stamp ::", time_stamp, device_name, channel_name, unique_id)
        if time_stamp is not None:
            # pcl_resp_proto_obj.recievedTimestamp = time_stamp
            pcl_resp_proto_obj.responseDeviceName = device_name
            pcl_resp_proto_obj.responseChannelName = channel_name
            pcl_resp_proto_obj.uniqueId = unique_id
            h5file_obj = H5ReaderSequence(self.h5_file_name)
            if not self.tmstamp_lst:
                self.tmstamp_lst = h5file_obj.get_all_timestamps()
                self.tmstamp_lst = [int(evry_tmstamp) for evry_tmstamp in self.tmstamp_lst]
            # print "self.tmstamp_lst::", self.tmstamp_lst
            if time_stamp in self.tmstamp_lst:
                clst_tmstamp = time_stamp
            else:
                clst_tmstamp = min(self.tmstamp_lst, key=lambda x: abs(x-time_stamp))
            print "clst_tmstamp::", clst_tmstamp
            pcl_resp_proto_obj.recievedTimestamp = clst_tmstamp
            pcl_points_lst = h5file_obj.get_pcl_points_for_tmstamp(clst_tmstamp)
            pnt_cld_obj = pcl_resp_proto_obj.pointClouds.add()
            pnt_cld_obj.pointType = 'a'
            pnt_cld_obj.cloudWidth = len(pcl_points_lst)
            pnt_cld_obj.cloudHeight = 1
            pnt_cld_obj.pointsCount = len(pcl_points_lst) * 1
            # for ech_pnt_type_idx in range(4):
            #     pcl_pnt_obj = pnt_cld_obj.points.add()
            #     pnt_attrib_obj = pcl_pnt_obj.pointAtributes.add()
            # pcl_points_lst = [['0.0', '-11472.0', '-828.0', '10600.0'], ['0.0', '-13880.0', '-333.0', '7946.0'], ['0.0', '-13972.0', '2530.0', '7543.0']]

            for evry_point_lst in pcl_points_lst:
                # evry_point_lst = ['0.0', '-11472.0', '-828.0', '10600.0']
                evry_point_lst = [float(evry_pnt) for evry_pnt in evry_point_lst]
                # print("evry_point_lst ::", evry_point_lst, type(evry_point_lst[0]))
                pcl_pnt_obj = pnt_cld_obj.points.add()
                for ech_pnt in evry_point_lst:
                    # ech_pnt = '-11472.0'
                    # print("ech_pnt >", ech_pnt)
                    pnt_val_obj = pcl_pnt_obj.pointAtributes.add()
                    pnt_val_obj.pointValue = ech_pnt
                    # pnt_val_obj.pointValue.append(int(ech_pnt))
                    # pcl_pnt_obj.pointAtributes.append(int(ech_pnt))
            print("Point cloud sent..")
        else:
            pcl_resp_proto_obj.recievedTimestamp = 0
        self.pnt_cld_data_publr_obj.send(pcl_resp_proto_obj.SerializeToString())

    def abort_algo(self, topic_name, msg, time):

        if topic_name == json_data['pointcloud_end_response']:
            global BEXIT
            BEXIT = False

    def inform_model_loaded(self):
        # Inform model is loaded
        # time.sleep(2)

        lbl_response_obj = common_pb2.ServiceState()
        lbl_response_obj.serviceStatus = "True"
        self.pnt_cld_ready_obj.send(lbl_response_obj.SerializeToString())

    def define_subscr_callbacks(self):

        self.pnt_cld_dvc_subscr_obj.set_callback(self.pub_pnt_cld_dvc_data)
        self.pnt_cld_data_subscr_obj.set_callback(self.pub_pnt_cld_points_data)
        self.pnt_cld_end_subscr_obj.set_callback(self.abort_algo)
        print("Point Cloud service initialized")
        while ecal.ok() and BEXIT:
            time.sleep(0.1)
            if SERVICE_READINESS:
                self.inform_model_loaded()

if __name__ == '__main__':

    # H5FileName = sys.argv[1]
    # Ticket_fld_path = sys.argv[1]
    Ticket_fld_path = r'C:\Users\uidr8549\Desktop\tech_demo\Batch_Ticket'
    # Check if the .h5 file exists in the ticket folder
    sub_folder = r'\Input'
    # sub_folder = r'\Images'
    # try:
    for fname in os.listdir(Ticket_fld_path + sub_folder):
        if fname.endswith('.h5'):
            # print("H5 file exists", fname)
            H5FilePath = Ticket_fld_path + sub_folder + r'\\' + fname
            # H5FileName = r'optimized.h5'
            # break
            h5_obj = h5py.File(H5FilePath, "r")
            if type(h5_obj['/HFLXXX']) is h5py.Group:
                print("HFLXXX device name exists")
            else:
                print("HFLXXX device name does not exist")
            if type(h5_obj['/HFLXXX/POINTCLOUD']) is h5py.Group:
                print("POINTCLOUD channel name exists")
            else:
                print("POINTCLOUD channel name does not exist")
        # else:
        #     H5FilePath = None
    # except Exception as e:
    #     print(str(e))
    if H5FilePath is None:
        print("No H5 file present in folder")
    else:
        PointCloudService(H5FilePath)

# pyinstaller --onefile point_cloud_service.py --add-data _ecal_py_2_7_x86.pyd;.
# D:\Work\2018\code\Tensorflow_code\Protobuf_compilers\protoc3.5\bin\protoc.exe -I=.\ --python_out=.\ pointcloud.proto