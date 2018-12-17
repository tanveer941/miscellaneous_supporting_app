
import h5py
import sys
import os

class H5ReaderSequence(object):
    def __init__(self, fname):
        self.reset(fname)
        self.h5_obj = h5py.File(fname, "r")

    def reset(self, fname):
        if not os.path.isfile(fname):
            print("Error - H5 file not available: %s!" % fname)
            sys.exit()

    def get_all_timestamps(self):
        """
        Get all the timestamps from the H5 file in a list
        :return:
        """
        timestamp_dtset_obj = self.h5_obj['/MTS/Timestamp']
        # print("timestamp_dtset_obj ::", timestamp_dtset_obj.value, dir(timestamp_dtset_obj))
        tmstamp_lst = list(timestamp_dtset_obj.value)
        print("tmstamp_lst::", len(tmstamp_lst))
        return tmstamp_lst

    def get_pcl_points_for_tmstamp(self, time_stamp):
        timestamp_dtset_obj = self.h5_obj['/MTS/Timestamp']
        # print("timestamp_dtset_obj ::", timestamp_dtset_obj.value, dir(timestamp_dtset_obj))
        all_tmstamps = list(timestamp_dtset_obj.value)
        tmstamp_idx = all_tmstamps.index(time_stamp)
        print("tmstamp_idx ::>", tmstamp_idx)
        pnt_cld_obj = self.h5_obj['/MTS/POINTCLOUD']
        pcd_dt_lst = []
        for name, evry_pntCld_member in pnt_cld_obj.items():
            # print("name::", name, evry_pntCld_member)
            if isinstance(evry_pntCld_member, h5py.Group):
                ordinate_lst = []
                for pcd_infoname, evry_pntCld_info in evry_pntCld_member.items():
                    # print("entry confirm")
                    pointCloud_member_names = ['Xpoint', 'Ypoint', 'Zpoint', 'Ampl']
                    if isinstance(evry_pntCld_info, h5py.Dataset):
                        if pcd_infoname in pointCloud_member_names:
                            # Only if x,y and z co-ordinates exist
                            ordinate_values = evry_pntCld_info.value
                            # print("evry_pntCld_info ::", pcd_infoname, ordinate_values)
                            ordinate_lst.append(ordinate_values[tmstamp_idx] / 1.0)
                if ordinate_lst:
                    pcd_dt_lst.append(ordinate_lst)
        # print("pcd_dt_lst ::", pcd_dt_lst)
        return pcd_dt_lst

    def generate_optimized_point_cloud_h5(self):

        h5_obj_new = h5py.File('optimized.h5', 'a')
        # get all the timestamps
        tmstamps_lst = h5file_obj.get_all_timestamps()
        for ech_tmstamp in tmstamps_lst:
            print("ech_tmstamp ::", ech_tmstamp)
            # Get point cloud info on each timestamp
            pcd_dt_lst = h5file_obj.get_pcl_points_for_tmstamp(ech_tmstamp)
            pcl_pnt_pth = '/POINTCLOUD' + r'/' + str(ech_tmstamp)
            h5_obj_new.create_dataset(pcl_pnt_pth, data=pcd_dt_lst)


if __name__ == '__main__':
    h5_file_name = r'2018.03.16_at_18.34.54_camera-mi_191-no-object_pointCloud.h5'
    h5file_obj = H5ReaderSequence(h5_file_name)
    h5file_obj.generate_optimized_point_cloud_h5()