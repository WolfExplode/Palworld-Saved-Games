from typing import Any, Sequence

from palworld_save_tools.archive import *


def decode(
    reader: FArchiveReader, type_name: str, size: int, path: str
) -> dict[str, Any]:
    if type_name != "ArrayProperty":
        raise Exception(f"Expected ArrayProperty, got {type_name}")
    value = reader.property(type_name, size, path, nested_caller_path=path)
    data_bytes = value["value"]["values"]
    value["value"] = decode_bytes(reader, data_bytes)
    return value


def decode_bytes(
    parent_reader: FArchiveReader, b_bytes: Sequence[int]
) -> dict[str, Any]:
    reader = parent_reader.internal_copy(bytes(b_bytes), debug=False)
    data: dict[str, Any] = {}
    data["model_instance_id"] = reader.guid()
    pitch, yaw, roll = reader.compressed_short_rotator()
    x, y, z = reader.packed_vector(1)
    data["world_transform"] = {
        "rotator": {
            "pitch": pitch,
            "yaw": yaw,
            "roll": roll,
        },
        "location": {
            "x": x,
            "y": y,
            "z": z,
        },
        "scale_x": reader.float(),
    }
    data["hp"] = reader.i32()
    if not reader.eof():
        data["unknown_data"] = [int(b) for b in reader.read_to_end()]
        # raise Exception("Warning: EOF not reached")
    return data


def encode(
    writer: FArchiveWriter, property_type: str, properties: dict[str, Any]
) -> int:
    if property_type != "ArrayProperty":
        raise Exception(f"Expected ArrayProperty, got {property_type}")
    del properties["custom_type"]
    encoded_bytes = encode_bytes(properties["value"])
    properties["value"] = {"values": [b for b in encoded_bytes]}
    return writer.property_inner(property_type, properties)


def encode_bytes(p: dict[str, Any]) -> bytes:
    writer = FArchiveWriter()

    writer.guid(p["model_instance_id"])
    writer.compressed_short_rotator(
        p["world_transform"]["rotator"]["pitch"],
        p["world_transform"]["rotator"]["yaw"],
        p["world_transform"]["rotator"]["roll"],
    )
    writer.packed_vector(
        1,
        p["world_transform"]["location"]["x"],
        p["world_transform"]["location"]["y"],
        p["world_transform"]["location"]["z"],
    )
    writer.float(p["world_transform"]["scale_x"])
    writer.i32(p["hp"])
    if "unknown_data" in p:
        writer.write(bytes(p["unknown_data"]))

    encoded_bytes = writer.bytes()
    return encoded_bytes
