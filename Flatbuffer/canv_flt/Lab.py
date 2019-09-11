# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers

class Lab(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsLab(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Lab()
        x.Init(buf, n + offset)
        return x

    # Lab
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Lab
    def SourceType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return None

    # Lab
    def Devices(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from Dvc import Dvc
            obj = Dvc()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Lab
    def DevicesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def LabStart(builder): builder.StartObject(2)
def LabAddSourceType(builder, SourceType): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(SourceType), 0)
def LabAddDevices(builder, Devices): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(Devices), 0)
def LabStartDevicesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def LabEnd(builder): return builder.EndObject()