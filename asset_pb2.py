# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: asset.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='asset.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0b\x61sset.proto\x1a\x1cgoogle/protobuf/struct.proto\"\xe1\x01\n\x07\x41ssetPB\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x1e\n\x06inputs\x18\x02 \x03(\x0b\x32\x0e.AssetPB.Input\x12\x1e\n\x06\x61ssets\x18\x03 \x03(\x0b\x32\x0e.AssetPB.Block\x1aJ\n\x05Input\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12%\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\x1a<\n\x05\x42lock\x12\x0c\n\x04type\x18\x01 \x01(\t\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Structb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])




_ASSETPB_INPUT = _descriptor.Descriptor(
  name='Input',
  full_name='AssetPB.Input',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='AssetPB.Input.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='AssetPB.Input.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='AssetPB.Input.data', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=135,
  serialized_end=209,
)

_ASSETPB_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='AssetPB.Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='AssetPB.Block.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='AssetPB.Block.data', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=211,
  serialized_end=271,
)

_ASSETPB = _descriptor.Descriptor(
  name='AssetPB',
  full_name='AssetPB',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='AssetPB.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='inputs', full_name='AssetPB.inputs', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='assets', full_name='AssetPB.assets', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ASSETPB_INPUT, _ASSETPB_BLOCK, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=46,
  serialized_end=271,
)

_ASSETPB_INPUT.fields_by_name['data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_ASSETPB_INPUT.containing_type = _ASSETPB
_ASSETPB_BLOCK.fields_by_name['data'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_ASSETPB_BLOCK.containing_type = _ASSETPB
_ASSETPB.fields_by_name['inputs'].message_type = _ASSETPB_INPUT
_ASSETPB.fields_by_name['assets'].message_type = _ASSETPB_BLOCK
DESCRIPTOR.message_types_by_name['AssetPB'] = _ASSETPB
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AssetPB = _reflection.GeneratedProtocolMessageType('AssetPB', (_message.Message,), dict(

  Input = _reflection.GeneratedProtocolMessageType('Input', (_message.Message,), dict(
    DESCRIPTOR = _ASSETPB_INPUT,
    __module__ = 'asset_pb2'
    # @@protoc_insertion_point(class_scope:AssetPB.Input)
    ))
  ,

  Block = _reflection.GeneratedProtocolMessageType('Block', (_message.Message,), dict(
    DESCRIPTOR = _ASSETPB_BLOCK,
    __module__ = 'asset_pb2'
    # @@protoc_insertion_point(class_scope:AssetPB.Block)
    ))
  ,
  DESCRIPTOR = _ASSETPB,
  __module__ = 'asset_pb2'
  # @@protoc_insertion_point(class_scope:AssetPB)
  ))
_sym_db.RegisterMessage(AssetPB)
_sym_db.RegisterMessage(AssetPB.Input)
_sym_db.RegisterMessage(AssetPB.Block)


# @@protoc_insertion_point(module_scope)