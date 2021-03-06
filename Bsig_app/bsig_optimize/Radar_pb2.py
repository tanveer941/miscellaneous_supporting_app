# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Radar.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Radar.proto',
  package='Radar',
  syntax='proto3',
  serialized_pb=_b('\n\x0bRadar.proto\x12\x05Radar\"b\n\x0f\x42sigDataRequest\x12\x10\n\x08\x62sigPath\x18\x01 \x01(\t\x12\x15\n\robjectIdCount\x18\x02 \x01(\x05\x12\x13\n\x0bsignalNames\x18\x03 \x03(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\x03\"R\n\x14\x42SigDataOfEachSignal\x12\x12\n\nsignalName\x18\x01 \x01(\t\x12\x10\n\x08objectId\x18\x02 \x01(\x05\x12\x14\n\x0csignalvalues\x18\x03 \x03(\x02\"Y\n\x10\x42sigDataResponse\x12\x11\n\ttimeStamp\x18\x01 \x03(\x04\x12\x32\n\reachSigValues\x18\x02 \x03(\x0b\x32\x1b.Radar.BSigDataOfEachSignalB\x02H\x01\x62\x06proto3')
)




_BSIGDATAREQUEST = _descriptor.Descriptor(
  name='BsigDataRequest',
  full_name='Radar.BsigDataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bsigPath', full_name='Radar.BsigDataRequest.bsigPath', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='objectIdCount', full_name='Radar.BsigDataRequest.objectIdCount', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signalNames', full_name='Radar.BsigDataRequest.signalNames', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Radar.BsigDataRequest.timestamp', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=120,
)


_BSIGDATAOFEACHSIGNAL = _descriptor.Descriptor(
  name='BSigDataOfEachSignal',
  full_name='Radar.BSigDataOfEachSignal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='signalName', full_name='Radar.BSigDataOfEachSignal.signalName', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='objectId', full_name='Radar.BSigDataOfEachSignal.objectId', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signalvalues', full_name='Radar.BSigDataOfEachSignal.signalvalues', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=122,
  serialized_end=204,
)


_BSIGDATARESPONSE = _descriptor.Descriptor(
  name='BsigDataResponse',
  full_name='Radar.BsigDataResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timeStamp', full_name='Radar.BsigDataResponse.timeStamp', index=0,
      number=1, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eachSigValues', full_name='Radar.BsigDataResponse.eachSigValues', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=206,
  serialized_end=295,
)

_BSIGDATARESPONSE.fields_by_name['eachSigValues'].message_type = _BSIGDATAOFEACHSIGNAL
DESCRIPTOR.message_types_by_name['BsigDataRequest'] = _BSIGDATAREQUEST
DESCRIPTOR.message_types_by_name['BSigDataOfEachSignal'] = _BSIGDATAOFEACHSIGNAL
DESCRIPTOR.message_types_by_name['BsigDataResponse'] = _BSIGDATARESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BsigDataRequest = _reflection.GeneratedProtocolMessageType('BsigDataRequest', (_message.Message,), dict(
  DESCRIPTOR = _BSIGDATAREQUEST,
  __module__ = 'Radar_pb2'
  # @@protoc_insertion_point(class_scope:Radar.BsigDataRequest)
  ))
_sym_db.RegisterMessage(BsigDataRequest)

BSigDataOfEachSignal = _reflection.GeneratedProtocolMessageType('BSigDataOfEachSignal', (_message.Message,), dict(
  DESCRIPTOR = _BSIGDATAOFEACHSIGNAL,
  __module__ = 'Radar_pb2'
  # @@protoc_insertion_point(class_scope:Radar.BSigDataOfEachSignal)
  ))
_sym_db.RegisterMessage(BSigDataOfEachSignal)

BsigDataResponse = _reflection.GeneratedProtocolMessageType('BsigDataResponse', (_message.Message,), dict(
  DESCRIPTOR = _BSIGDATARESPONSE,
  __module__ = 'Radar_pb2'
  # @@protoc_insertion_point(class_scope:Radar.BsigDataResponse)
  ))
_sym_db.RegisterMessage(BsigDataResponse)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('H\001'))
# @@protoc_insertion_point(module_scope)
