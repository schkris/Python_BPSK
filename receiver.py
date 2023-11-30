import numpy as np
import math
import struct
from bchlib import BCH

def bpsk_demodulation(modulated_data, carrier_frequency, time_points):

    threshold = 0.0
    # Number of bits to be found
    info_length = int(np.ceil(time_points[len(time_points) - 1] * carrier_frequency))
    # print("Info Length: ", info_length)

    # Create a carrier and shifted carrier and compare both to data values to determine binary
    base_carrier = np.sin(2 * np.pi * carrier_frequency * time_points)
    shifted_carrier = np.sin(2 * np.pi * carrier_frequency * time_points + np.pi)
    # print("Base Carrier Length: ", len(base_carrier))
    # print("Base Carrier: ", base_carrier)
    # print("Shifted Carrier Length: ", len(shifted_carrier))
    # print("Shifted Carrier: ", shifted_carrier)

    # Initialize demodulated_data array
    demodulated_data = np.zeros(info_length, dtype=int)

    for i in range(info_length):
        # Calculate the index for each bit
        index = int((i + 0.33) * len(time_points) / info_length)

        # print("Index: ", index, "Time: ", time_points[index], "Value: ", modulated_data[index])

        # Calculate distances from both carriers
        distance_base = np.abs(modulated_data[index] - base_carrier[index])
        distance_shifted = np.abs(modulated_data[index] - shifted_carrier[index])
        # print("Base: ", distance_base, "Shifted: ", distance_shifted)

        # Determine the demodulated bit based on minimum distance
        if distance_base < distance_shifted:
            demodulated_data[i] = 0
        else:
            demodulated_data[i] = 1

    # print("Demodulated Data Length: ", len(demodulated_data))
    # print("Demodulated Data:", demodulated_data)

    return demodulated_data

def deserialize_data(binary_data):
    # Implementation required
    pass

# Read from file
with open('transmitter.txt', 'rb') as file:
    transmission_data = np.loadtxt(file)
# Extract time points and modulated signal
time_points = transmission_data[:, 0]
modulated_signal = transmission_data[:, 1]

# BPSK Demodulation
threshold_value = 0.0  # Adjust the threshold as needed
demodulated_data = bpsk_demodulation(modulated_signal, 6e9, time_points)
# print("Demod Data Length: ", len(demodulated_data))
# print("Data: ", demodulated_data[0:])
integer_value = int(''.join(map(str, demodulated_data)), 2)
byte_data = integer_value.to_bytes((len(demodulated_data) + 7) // 8, byteorder='big')
print("Data Length: ", len(bin(int.from_bytes(byte_data, "big"))))
print("Demod Data: ", bin(int.from_bytes(byte_data, "big")))

# BCH Decoding
with open('parity_num.txt', 'r') as file:
    parity_num_str = file.read().strip()
    parity_num = int(parity_num_str)
print("Parity Num:", parity_num)
byte_string = ''.join(map(str, demodulated_data))
received_data = byte_string[:parity_num]
parity = byte_string[parity_num:]
parity_int = int(parity, 2)
print("Parity Int: ", parity_int)
received_int = int(received_data, 2)
print("Received Int: ", received_int)
parity_bytes = parity_int.to_bytes((len(parity) + 7) // 8, byteorder='big')
received_bytes = received_int.to_bytes((len(received_data) + 7) // 8, byteorder='big')
print("Parity Length: ", len(bin(int.from_bytes(parity_bytes, "big"))))
print("Received Length: ", len(bin(int.from_bytes(received_bytes, "big"))))
print("Parity Bits: ", bin(int.from_bytes(parity_bytes, "big")))
print("Received Data: ", bin(int.from_bytes(received_bytes, "big")))
t = math.ceil(len(bin(int.from_bytes(received_bytes, "big"))) * 0.1)
m = math.ceil(math.log2(len(bin(int.from_bytes(received_bytes, "big"))) + t + 1))
print("Num Errors:", t)
print("Code Order (m):", m)
print("Length", len(bin(int.from_bytes(received_bytes, "big"))))
bch = BCH(t=int(t), m=int(m))
decoded_data = bch.decode(received_bytes, parity_bytes)
print("Decoded Data: ", bin(int.from_bytes(decoded_data, "big")))

# Deserialize data
# final_message = deserialize_data(decoded_data)

# Print the final message
# Read message from file
with open('message.txt', 'r') as file:
    message = file.read()
print("Original Message:", message)
# print("Received Message:", final_message)
