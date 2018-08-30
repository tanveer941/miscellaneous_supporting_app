

"""
Works only for python 2.7
Ceate PCD file from BSIG
extract x and y co-ordinates(f_DistX, f_DistY) for all the objects in the BSIG file
Export the data to an H5 file
"""



# from signalreader import SignalReader
# from signal_loader import SignalLoader
from datetime import datetime
import numpy as np
import h5py
bsig_path = r"D:\Work\2018\code\Github_repo\PCD_generation\Continuous_2017.06.01_at_12.12.18.bsig"
# bsig_path = r"D:\Work\2018\code\LT5G\OLT\Radar_labelling_bsig\bsig_readers\20160608_1306_{4556C7A6-7F27-4A91-923E-4392C9785675}.bsig"

SAMPLE_COUNT = 75
H5_PCD_FILE = r'PCD_ordinate.h5'
## ======================================================================================================================

sig_name_lst = [
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].KinematicRel.f_DistX',
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].KinematicRel.f_DistY'
        ]

obj_signals = [ech_sig for ech_sig in sig_name_lst if '%' in str(ech_sig)]

start_time = datetime.now()

def create_h5_frm_bsig():
    with SignalReader(bsig_path) as sr:
        pcd_dt_lst = []
        for ech_obj_num in range(100):
            new_sig_lst = []

            for ech_signal in sig_name_lst:
            # for ech_signal in obj_signals:
                if '%' in str(ech_signal):
                    ech_signal = ech_signal.replace('%', str(ech_obj_num))
                new_sig_lst.append(ech_signal)
            existing_sgnls_lst = list(set(new_sig_lst) & set(sr.signal_names))
            print ("existing_sgnls_lst :: ", existing_sgnls_lst)
            # print ">> ", new_sig_lst
            signals = sr[existing_sgnls_lst]  # retrieves a list of both signals --> [[<sig1>], [<sig2>]]
            # print ":>>", signals, len(signals)
            specific_sig_values = [ech_sig_lst[SAMPLE_COUNT] for ech_sig_lst in signals]
            specific_sig_values.append(0)
            print("specific_sig_values >> ", specific_sig_values)
            pcd_dt_lst.append(specific_sig_values)
            # pcd_dt_lst.append([specific_sig_values[0], specific_sig_values[2], specific_sig_values[1]])
        arr_data = np.array(pcd_dt_lst)

    end_time = datetime.now()
    duration = end_time - start_time
    print("duration :: ", duration.total_seconds(), duration.total_seconds()/60)

    ##================= Create HDF5 file=================
    h5_file_obj = h5py.File(H5_PCD_FILE, "a")
    h5_file_obj.create_dataset('/pcd', data=arr_data)
    h5_file_obj.close()



## ======================================================================================================================
def create_pcd_from_h5_bsig():
    h5_file_obj = h5py.File(H5_PCD_FILE, "r")
    arr_data = h5_file_obj['/pcd']
    # print(dir(arr_data))
    # print(type(arr_data.value))
    from pypcd.pypcd import PointCloud
    pc = PointCloud(pc_data=arr_data.value,
                        metadata={'version': .5, 'fields': ['x', 'y', 'z'], 'type': ['F', 'F', 'F'], 'size': [4, 4, 4],
                                  'count': [1, 1, 1], 'width': len(arr_data.value), 'height': 1, 'points': len(arr_data.value), 'data': 'ascii',
                                  'viewpoint': [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]})
    pc.save_pcd(fname='bsig_rec.pcd', compression=None)

if __name__ == '__main__':

    # create_h5_frm_bsig()
    create_pcd_from_h5_bsig()

# Note : Function create_h5_frm_bsig works in python 2.7.10, Function create_pcd_from_h5_bsig works in Python 3.5.2
# Point cloud library for python compiles only for Python 3.5.2

