# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers

class Dvc(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDvc(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Dvc()
        x.Init(buf, n + offset)
        return x

    # Dvc
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Dvc
    def DeviceName(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Dvc
    def Channels(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from Chnl import Chnl
            obj = Chnl()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Dvc
    def ChannelsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def DvcStart(builder): builder.StartObject(2)
def DvcAddDeviceName(builder, DeviceName): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(DeviceName), 0)
def DvcAddChannels(builder, Channels): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(Channels), 0)
def DvcStartChannelsVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def DvcEnd(builder): return builder.EndObject()
