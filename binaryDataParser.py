import struct

sensor_type_data_lengths = {
    52: 1,
    12: 4,
    22: 1,
    38: 1,
}

sensor_type_names = {
    52: 'battery',
    12: 'temperature',
    22: 'luminance',
    38: 'leafWetness'
}

# This is still an issue, it was already reported: https://github.com/Libelium/waspmoteapi/issues/22
frame_type_names = {
    6: ['EVENT_FRAME', 'NOTHING', 'SERVICE1_FRAME'],
    7: ['TIMEOUT_FRAME', ' ALARM_FRAME', 'SERVICE2_FRAME'],
}


def parse_data(data):
    byte_data = data
    pos_delimitter = -1
    for index, byte in enumerate(data):
        if byte == 35:
            pos_delimitter = index

    header = byte_data[0:pos_delimitter+2]
    data = byte_data[pos_delimitter+2:]

    waspmote_id = header[13:-2].decode('utf-8')

    sensor_data = get_sensors_from_payload_body(data)
    frame_type = get_name_to_frame_type(header[3])
    return {
        'frameType':  frame_type,
        'sequenceId': header[-1],
        'nodeId':     waspmote_id,
        'sensors':    sensor_data
    }


def get_length_to_sensor_type(sensor_type):
    try:
        return sensor_type_data_lengths[sensor_type]
    except KeyError:
        return -1


def get_name_to_sensor_type(sensor_type):
    try:
        return sensor_type_names[sensor_type]
    except KeyError:
        return sensor_type


def get_name_to_frame_type(frame_type):
    try:
        return frame_type_names[frame_type]
    except KeyError:
        return frame_type


def convert_byte_data(sensor_type, data):
    if sensor_type_data_lengths[sensor_type] == 1:
        return int.from_bytes(data, byteorder='big')
    elif sensor_type_data_lengths[sensor_type] == 4:
        return struct.unpack('f', data)[0]


def get_sensors_from_payload_body(data):
    processed_data = {}
    current_sensor = 0

    while current_sensor < len(data):
        sensor_type = data[current_sensor]
        name = get_name_to_sensor_type(sensor_type)
        data_length = get_length_to_sensor_type(sensor_type)
        if data_length == -1:
            break
        sensor_byte_data = data[current_sensor + 1: current_sensor + 1 + data_length]

        processed_data[name] = convert_byte_data(sensor_type, sensor_byte_data)

        current_sensor = current_sensor + 1 + data_length

    return processed_data


if __name__ == '__main__':
    parse_data(b'<=>\x06\x13Ueg\x05|\x10TVnode_01#\x134]')
    # <=>            start
    # \x06           frame id
    # \x13           number of fields
    # Ueg\x05        serial id
    # |\x10TVnode_01 Waspmote id
    # #              Separator
    # \x13           sensor
    # 4]             data