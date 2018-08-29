



import sys
import signalreader
# from signalreader import BsigReader, SignalReaderException
import Radar_pb2
import ecal
import os
import time
from datetime import datetime

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print '%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te - ts)
        return result

    return timed
class RadarSignalInfo(object):

    def __init__(self):

        # Subscribe to the eCAL message to get the bsig path and the
        # signal names

        # self.bsig_path = bsig_pth
        #
        ecal.initialize(sys.argv, "Python signal value publisher")
        # Subscribe to RadarSignalRequest topic
        self.bsig_subscr_obj = ecal.subscriber(topic_name="BsigSignalNames")
        self.bsig_pub_obj = ecal.publisher(topic_name="BsigSignalValues")
        self.bsig_tmstamp_lst = []
        self.sig_name_lst = []
        self.subscribe_ecal_msgs()


    @timeit
    def subscribe_ecal_msgs(self):

        print "Subscribing to the signals.........."
        # Publish the signal values
        bsig_obj = None
        # Subscribe on the algo interface object
        bsig_proto_req_obj = Radar_pb2.BsigDataRequest()
        bsig_proto_resp_obj = Radar_pb2.BsigDataResponse()
        while ecal.ok():
            ret, msg, time = self.bsig_subscr_obj.receive(500)
            # print("---:: ", ret, msg, time, type(msg))
            if msg is not None:
                start_time = datetime.now()
                bsig_proto_req_obj.ParseFromString(msg)
                bsig_pth = bsig_proto_req_obj.bsigPath
                obj_num = bsig_proto_req_obj.objectIdCount
                tmstamp_rdr = bsig_proto_req_obj.timestamp
                # Segregate object signals and non-object signals
                cmn_signals = [ech_sig for ech_sig in bsig_proto_req_obj.signalNames if '%' not in str(ech_sig)]
                obj_signals = [ech_sig for ech_sig in bsig_proto_req_obj.signalNames if '%' in str(ech_sig)]
                print "--> ", bsig_pth, obj_num
                # print "cmn_signals :: ",
                # if len(cmn_signals) == 1 and 'TimeStamp' in str(cmn_signals[0])

                try:
                    if bsig_obj is None:
                        print "{{{{"
                        bsig_obj = signalreader.BsigReader(bsig_pth)
                    # print("bsig_obj >> ", bsig_obj)
                    # Read and Publish the common signals velocity, acceleration just once
                    print "Reading common signals..."
                    for ech_cmn_signal in cmn_signals:
                        cmn_sig_val_lst = list(bsig_obj.signal(ech_cmn_signal))
                        # print "cmn_sig_val_lst >> ", cmn_sig_val_lst
                        if len(cmn_signals) == 1 and 'TimeStamp' in str(cmn_signals[0]):
                            # self.publ_timestamps()
                            self.bsig_tmstamp_lst.extend(cmn_sig_val_lst)
                        if self.bsig_tmstamp_lst:
                            # Get the index/sample count for the timestamp
                            if tmstamp_rdr != -1:
                                try:
                                    sample_cnt = self.bsig_tmstamp_lst.index(tmstamp_rdr)
                                    # print "cmn_sig_val_lst :: ", cmn_sig_val_lst
                                    print "sample_cnt >> ", sample_cnt, cmn_sig_val_lst[sample_cnt]
                                    cmn_sig_val_lst = [cmn_sig_val_lst[sample_cnt]]
                                except ValueError as e:
                                    print "No signal value for this timestamp %d and signal %s" % (tmstamp_rdr, ech_cmn_signal)
                                    pass
                        else:
                            print "TimeStamp data not fetched from Bsig file"
                            continue

                        ech_sig_data = bsig_proto_resp_obj.eachSigValues.add()
                        # If data is present for signal send the values else do not send anything
                        # print "cmn_sig_val_lst :: ", cmn_sig_val_lst
                        if cmn_sig_val_lst:
                            ech_sig_data.signalName = ech_cmn_signal
                            ech_sig_data.objectId = -1
                            for ech_sig_val in cmn_sig_val_lst:
                                ech_sig_data.signalvalues.append(ech_sig_val)
                        # else:
                        #     ech_sig_data.signalvalues.append(0)
                    # Iterate over the objects
                    if tmstamp_rdr != -1:
                        for ech_obj_num in range(0, obj_num):
                            print "Reading signals for object %s" % str(ech_obj_num)
                            # print("ech_obj_num > ", ech_obj_num)
                            # Parse the signal names and iterate over them
                            for ech_signal in obj_signals:
                                if '%' in str(ech_signal):
                                    ech_signal = ech_signal.replace('%', str(ech_obj_num))
                                print("ech_signal > ", ech_signal)
                                obj_sig_val_lst = list(bsig_obj.signal(ech_signal))
                                ech_obj_sig_data = bsig_proto_resp_obj.eachSigValues.add()
                                # If data is present for signal send the values else do not send anything
                                if obj_sig_val_lst:
                                    if self.bsig_tmstamp_lst:
                                        # Get the index/sample count for the timestamp
                                        if tmstamp_rdr != -1:
                                            try:
                                                sample_cnt = self.bsig_tmstamp_lst.index(tmstamp_rdr)
                                                # print "cmn_sig_val_lst :: ", cmn_sig_val_lst
                                                print "sample_cnt >> ", sample_cnt, obj_sig_val_lst[sample_cnt]
                                                obj_sig_val_lst = [obj_sig_val_lst[sample_cnt]]
                                            except ValueError as e:
                                                print "No signal value for this timestamp %d and signal %s" % (
                                                tmstamp_rdr, ech_signal)
                                                pass
                                    else:
                                        print "TimeStamp data not fetched from Bsig file"
                                        continue
                                    ech_obj_sig_data.signalName = ech_signal
                                    ech_obj_sig_data.objectId = ech_obj_num
                                    for ech_obj_sig_val in obj_sig_val_lst:
                                        ech_obj_sig_data.signalvalues.append(ech_obj_sig_val)
                                # else:
                                #     ech_obj_sig_data.signalvalues.append(0)
                except signalreader.SignalReaderException, e:
                    print "Signal not found", str(e)
                data_payload = bsig_proto_resp_obj.SerializeToString()
                # print "data_payload :: ", data_payload
                self.bsig_pub_obj.send(data_payload)
                end_time = datetime.now()
                duration = end_time - start_time
                print("duration :: ", duration.total_seconds(), duration.total_seconds()/60)

if __name__ == '__main__':

    # read_the_signals()
    RadarSignalInfo()

# D:\Work\2018\code\Tensorflow_code\Protobuf_compilers\protoc3.5\bin\protoc -I=.\ --python_out=.\ Radar.proto

# C:\Python27\Scripts\pyinstaller --onefile bsig_sig_val_publish.py --add-data _ecal_py_2_7_x86.pyd;.


# 1. Request for all the timestamps. store it in the instance variable
# 2. Send all the signal names only once, store it in instance variable
# 3. Each button clicked, send in the next timestamp
#       Verify the existence of the signals in the bsig file from the property 'signal_names'
#       Get the sample count for each of the signals based on their timestamp
# 4. Each of the signal value field will have just one value in its array
