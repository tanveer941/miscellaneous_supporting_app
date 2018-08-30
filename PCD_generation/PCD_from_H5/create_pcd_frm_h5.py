

import h5py
# import pypcd
from pypcd.pypcd import PointCloud
import numpy as np


def generate_sample_pcd():

    fname = r'../2017.11.29_at_00.33.01_camera-mi_1449_TestPattern.h5'
    h5_obj = h5py.File(fname, "r")
    print ("h5_obj :: ", h5_obj)
    tmstamp = h5_obj['/MTS/Package/TimeStamp']
    print ("tmstamp :: ", tmstamp)
    idx = 0
    tmstamp1 = tmstamp[idx]
    pcd_data = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]']
    print ("pcd_data >> ", pcd_data.keys())
    # [u's16_x', u's16_y', u's16_z', u'u16_ampl']

    pcd_x = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]/s16_x'][idx]
    pcd_y = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]/s16_y'][idx]
    pcd_z = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]/s16_z'][idx]

    print (">>: ", pcd_x/1.0, pcd_y/1.0, pcd_z/1.0)
    #  size=[4, 4, 4], ascii
    dt = [[0.02886, 0.02886, 0.02886]]
    arr_data = np.array(dt)
    # print("length::", len(arr_data))
    # arr_data = np.array([0.02886])
    pc = PointCloud(pc_data=arr_data, metadata={'version': .5, 'fields': ['x', 'y', 'z'], 'type': ['F', 'F', 'F'], 'size': [4, 4, 4],
                                           'count': [1, 1, 1], 'width': 1, 'height': 1, 'points': 1, 'data': 'ascii',
                                           'viewpoint': [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]})
    pc.save_pcd(fname='sample.pcd', compression=None)

def generate_pcd_frm_h5():
    fname = r'../2017.11.29_at_00.33.01_camera-mi_1449_TestPattern.h5'
    h5_obj = h5py.File(fname, "r")
    print("h5_obj :: ", h5_obj)
    tmstamp = h5_obj['/MTS/Package/TimeStamp']
    # print("tmstamp :: ", tmstamp)
    idx = 0
    tmstamp1 = tmstamp[idx]

    pcd_data_lst = h5_obj['/HFL130/PCA/PCA_RESULT']
    # print("pcd_data_lst ::", pcd_data_lst, dir(pcd_data_lst))
    # print(dir(pcd_data_lst.items()))
    pcd_dt_lst = []
    for name, evry_pntCld_member in pcd_data_lst.items():
        # print("evry_pntCld_member>>", evry_pntCld_member)
        # pcd_x = evry_pntCld_member

        if isinstance(evry_pntCld_member, h5py.Group):
            print("pcd_x::", name, evry_pntCld_member, type(evry_pntCld_member))
            ordinate_lst = []
            for pcd_infoname, evry_pntCld_info in evry_pntCld_member.items():
                pointCloud_member_names = ['s16_x', 's16_y', 's16_z', 'u16_ampl']
                if isinstance(evry_pntCld_info, h5py.Dataset):
                    # print("pcd_infoname::", pcd_infoname, evry_pntCld_info, type(evry_pntCld_info))

                    if pcd_infoname in pointCloud_member_names:
                        # Only if x,y and z co-ordinates exist
                        ordinate_values = evry_pntCld_info.value
                        # print("evry_pntCld_info ::", pcd_infoname, ordinate_values)
                        ordinate_lst.append(ordinate_values[idx]/1.0)
            if ordinate_lst:
                pcd_dt_lst.append(ordinate_lst)
    arr_data = np.array(pcd_dt_lst)
    # print(">{{", ordinate_lst)
    print(">>", arr_data, len(arr_data))

    pc = PointCloud(pc_data=arr_data,
                    metadata={'version': .5, 'fields': ['x', 'y', 'z', 'i'], 'type': ['F', 'F', 'F', 'F'], 'size': [4, 4, 4, 4],
                              'count': [1, 1, 1, 1], 'width': len(arr_data), 'height': 1, 'points': len(arr_data), 'data': 'ascii',
                              'viewpoint': [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]})
    pc.save_pcd(fname='sample1.pcd', compression=None)

        # break
                # pcd_y = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]/s16_y'][idx]
                # pcd_z = h5_obj['/HFL130/PCA/PCA_RESULT/pointcloud[457]/s16_z'][idx]




if __name__ == '__main__':
    generate_sample_pcd()
    # generate_pcd_frm_h5()