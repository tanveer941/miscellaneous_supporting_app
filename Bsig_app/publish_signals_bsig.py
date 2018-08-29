import ecal
import sys
import Radar_pb2
import time
# from rdr_signal_info_pblsh import timeit


# @timeit
def publ_signal_names():

    print "Publish bsig signal names......."

    ecal.initialize(sys.argv, "Python Signal name publisher")

    BSIG_INFO_OBJ = Radar_pb2.BsigDataRequest()


    publisher_roi_obj = ecal.publisher(topic_name="BsigSignalNames")

    bsig_path = r"D:\Work\2018\code\LT5G\OLT\Radar_labelling_bsig\bsig_readers\Continuous_2014.05.15_at_08.48.40.bsig"
    # bsig_path = r"D:\Work\2018\code\LT5G\OLT\Radar_labelling_bsig\bsig_readers\20160608_1306_{4556C7A6-7F27-4A91-923E-4392C9785675}.bsig"
    # sig_name = "SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Longitudinal.MotVar.Velocity"
    sig_name_lst = ['SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Longitudinal.MotVar.Velocity',
                    'MTS.Package.TimeStamp',
     'SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Longitudinal.MotVar.Accel',
     'SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Lateral.YawRate.YawRate',
     'SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Lateral.SlipAngle.SideSlipAngle',

     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].Kinematic.fDistX',
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].Kinematic.fDistY',
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].Kinematic.fVrelX',
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].Legacy.uiLifeTime',
     'SIM VFB ALL.DataProcCycle.EMPublicObjData.Objects[%].Attributes.eDynamicProperty',

     'SIM VFB ALL.AlgoSenCycle.gSI_OOI_LIST.SI_OOI_LIST[%].object_id',
     'SIM VFB ALL.AlgoSenCycle.gSI_OOI_LIST.SI_OOI_LIST[%].long_displacement',
     'SIM VFB ALL.AlgoSenCycle.gSI_OOI_LIST.SI_OOI_LIST[%].lat_displacement_to_curvature']

    # sig_name_lst = ['MTS.Package.TimeStamp'
    #                 ]
    BSIG_INFO_OBJ.bsigPath = bsig_path
    BSIG_INFO_OBJ.objectIdCount = 40
    for sig_name in sig_name_lst:
        BSIG_INFO_OBJ.signalNames.append(sig_name)

    # while ecal.ok():
    #     print("BSIG_INFO_OBJ.SerializeToString() :: ", BSIG_INFO_OBJ.SerializeToString())
    time.sleep(1)
    publisher_roi_obj.send(BSIG_INFO_OBJ.SerializeToString())

        # break

    # publisher_roi_obj.send(img_req_obj.SerializeToString())
    # while ecal.ok():
    #     x = publisher_roi_obj.send(BSIG_INFO_OBJ.SerializeToString())
    #     print ">>>>", x

#=================================================================================================================


if __name__ == '__main__':

    publ_signal_names()
    # subscribe_signl_vals()