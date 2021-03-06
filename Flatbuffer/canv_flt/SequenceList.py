# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

import flatbuffers

class SequenceList(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsSequenceList(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = SequenceList()
        x.Init(buf, n + offset)
        return x

    # SequenceList
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # SequenceList
    def Sequence(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from Seq import Seq
            obj = Seq()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # SequenceList
    def SequenceLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def SequenceListStart(builder): builder.StartObject(1)
def SequenceListAddSequence(builder, Sequence): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(Sequence), 0)
def SequenceListStartSequenceVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def SequenceListEnd(builder): return builder.EndObject()
