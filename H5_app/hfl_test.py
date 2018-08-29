
import ecal
import AlgoInterface_pb2
import imageservice_pb2
import sys

ecal.initialize(sys.argv, "HFL data requestor")
hfl_publ_obj = ecal.publisher("Request_Image")
import time
time.sleep(2)
hfl_req_proto_obj = imageservice_pb2.ImageRequest()

def request_hfl_data():

    # while ecal.ok():
    # hfl_req_proto_obj.required_timestamp = 1504816617728550
    hfl_req_proto_obj.image_index = 8   #1504816617788522
    # hfl_req_proto_obj.hfl_file_name = "D:\\Work\\2018\\code\\LT5G\\HDF5_reader\\2017.09.07_at_20.37.57_camera-mi_1449.h5"

    hfl_publ_obj.send(hfl_req_proto_obj.SerializeToString())

    ecal.finalize()


request_hfl_data()
