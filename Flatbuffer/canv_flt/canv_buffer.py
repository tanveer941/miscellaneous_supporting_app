"""
flatc -p -b obl.fbs obl.json

"""

from SequenceList import SequenceList, SequenceListStart, SequenceListEnd,\
    SequenceListAddSequence, SequenceListStartSequenceVector
# import SequenceList, Seq, sequence_details
from Seq import Seq, SeqAddSequenceDetails, SeqStart, SeqEnd
from sequence_details import sequence_details, \
    sequence_detailsAddFolderName, sequence_detailsStart, sequence_detailsEnd
import flatbuffers
from datetime import datetime
import time
import json

def write_into_flt_buffr():

    # buf = open('obl.bin', 'rb').read()
    # # print "buf::", type(buf)
    # buf = bytearray(buf)
    # seq_lst_obj = SequenceList.GetRootAsSequenceList(buf, 0)
    # seq_obj = seq_lst_obj.Sequence(0)
    # fl_name = seq_obj.SequenceDetails().FolderName()
    # print "fl_name::", fl_name

    # Serialize
    builder = flatbuffers.Builder(0)
    fldr_name_flt = builder.CreateString("XYZ")

    sequence_detailsStart(builder)
    sequence_detailsAddFolderName(builder, fldr_name_flt)
    fldr_name = sequence_detailsEnd(builder)

    SeqStart(builder)
    SeqAddSequenceDetails(builder, fldr_name)
    seq_obj = SeqEnd(builder)

    SequenceListStart(builder)
    # SequenceListAddSequence(builder, seq_obj)
    SequenceListStartSequenceVector(builder, 4)
    builder.PrependUOffsetTRelative(seq_obj)
    builder.EndVector(4)
    orc = SequenceListEnd(builder)

    builder.Finish(orc)

    buf = builder.Output()
    # De serialize
    print "buf::", type(buf)
    seq_lst_obj = SequenceList.GetRootAsSequenceList(buf, 0)
    seq_obj = seq_lst_obj.Sequence(0)
    fl_name = seq_obj.SequenceDetails().FolderName()
    print "fl_name::", fl_name


def read_flat_buffr_attrib():

    st_time = time.time()
    buf = open('obl.bin', 'rb').read()
    buf = bytearray(buf)

    seq_lst_obj = SequenceList.GetRootAsSequenceList(buf, 0) #.Sequence(0).Labels(0).Devices(0).Channels(0).ObjectLabels(0).TimeStamp()
    seq_obj = seq_lst_obj.Sequence(0)
    lbl_obj = seq_obj.Labels(0)
    dvc_obj = lbl_obj.Devices(0)
    chnl_obj = dvc_obj.Channels(0)
    # obj_lbl_obj = chnl_obj.ObjectLabels(2)
    # name = obj_lbl_obj.TimeStamp()

    t1 = chnl_obj.ObjectLabels(0).TimeStamp()
    t2 = chnl_obj.ObjectLabels(1).TimeStamp()
    t3 = chnl_obj.ObjectLabels(2).TimeStamp()

    tx = chnl_obj.ObjectLabels(2).FrameObjectLabels(0).Height()
    print tx
    ed_time = time.time()
    duration = ed_time - st_time

    print "duration of flatbuff::", duration

#===================================================
def read_json_attrib():
    st_timej = time.time()
    with open('obl.json') as ldroi_json:
        ldroi = json.load(ldroi_json)
    obl = ldroi["Sequence"][0]["Labels"][0]["Devices"][0]["Channels"][0]["ObjectLabels"]
    k1 = obl[0]["TimeStamp"]
    k2 = obl[1]["TimeStamp"]
    k3 = obl[2]["TimeStamp"]
    ty = obl[1]["FrameObjectLabels"][0]["height"]
    print k1, k2, k3, ty
    ed_timej = time.time()
    duration_json = ed_timej - st_timej
    print "duration of JSON::", duration_json

if __name__ == '__main__':

    # read_flat_buffr_attrib()
    # read_json_attrib()

    write_into_flt_buffr()
