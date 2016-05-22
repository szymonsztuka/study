
def login_accepted_packet(session, sequence_number):
    bin_packet_length = (21).to_bytes(2, byteorder='big')
    bin_packet_type = "A".encode()
    bin_session = (str(session).ljust(10)).encode()
    bin_sequence_number = (str(sequence_number).ljust(20)).encode()
    return bin_packet_length + bin_packet_type + bin_session + bin_sequence_number

def login_rejected_packet_not_authorized():
    bin_packet_length = (2).to_bytes(2, byteorder='big')
    bin_packet_type = "J".encode()
    bin_reject_reason = "A".encode()
    return bin_packet_length + bin_packet_type + bin_reject_reason

def login_rejected_packet_session_not_available():
    bin_packet_length = (2).to_bytes(2, byteorder='big')
    bin_packet_type = "J".encode()
    bin_reject_reason = "S".encode()
    return bin_packet_length + bin_packet_type + bin_reject_reason

def sequenced_data_packet(message):
    bin_packet_type = "S".encode()
    bin_message = message.encode()
    bin_packet_length = (len(bin_message)+1).to_bytes(2, byteorder='big')
    return bin_packet_length + bin_packet_type + bin_message

def server_heartbeat_packet():
    return (1).to_bytes(2, byteorder='big') + "H".encode()

def end_of_session_packet():
    return (1).to_bytes(2, byteorder='big') + "Z".encode()

def decode_msg(bin_msg):
    length = int.from_bytes(bin_msg[0:2],byteorder='big')
    type = bin_msg[2].decode()
    payload = bin_msg[3:length]
    return(type, payload)

def decode_login_request_packet(bin_payload):
    username = bin_payload[3, 3+6].decode()
    password = bin_payload[9, 9+10].decode()
    requested_session = bin_payload[19, 19+10].decode()
    requested_sequence_number = bin_payload[29, 29+20].decode()
    return (username, password, requested_session, requested_sequence_number)

print(login_accepted_packet(1,2))
print(login_rejected_packet_not_authorized())
print(login_rejected_packet_session_not_available())
print(sequenced_data_packet("Abcdef 13"))