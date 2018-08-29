

from signalreader import SignalReader
from signal_loader import SignalLoader
from datetime import datetime
bsig_path = r"D:\Work\2018\code\LT5G\OLT\Radar_labelling_bsig\bsig_readers\Continuous_2014.05.15_at_08.48.40.bsig"
# bsig_path = r"D:\Work\2018\code\Github_repo\PCD_generation\Continuous_2017.06.01_at_12.12.18.bsig"
# bsig_path = r"D:\Work\2018\code\LT5G\OLT\Radar_labelling_bsig\bsig_readers\20160608_1306_{4556C7A6-7F27-4A91-923E-4392C9785675}.bsig"

## ======================================================================================================================

sig_name_lst = ['MTS.Package.TimeStamp',
                'SIM VFB ALL.DataProcCycle.ObjSyncEgoDynamic.Longitudinal.MotVar.Velocity',
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

obj_signals = [ech_sig for ech_sig in sig_name_lst if '%' in str(ech_sig)]



with SignalReader(bsig_path) as sr:
    start_time = datetime.now()
    for ech_obj_num in range(40):
        new_sig_lst = []

        for ech_signal in sig_name_lst:
        # for ech_signal in obj_signals:
            if '%' in str(ech_signal):
                ech_signal = ech_signal.replace('%', str(ech_obj_num))
            new_sig_lst.append(ech_signal)
        existing_sgnls_lst = list(set(new_sig_lst) & set(sr.signal_names))
        # print "existing_sgnls_lst :: ", existing_sgnls_lst
        # print ">> ", new_sig_lst

        signals = sr[existing_sgnls_lst]  # retrieves a list of both signals --> [[<sig1>], [<sig2>]]
        # print ":>>", signals, len(signals)
        specific_sig_values = [ech_sig_lst[500] for ech_sig_lst in signals]
        # print "specific_sig_values >> ", specific_sig_values

    end_time = datetime.now()
    duration = end_time - start_time
    print("duration :: ", duration.total_seconds(), duration.total_seconds()/60)

## ======================================================================================================================



