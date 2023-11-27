from bchlib import BCH
import random
import os
import math
import numpy as np
import matplotlib.pyplot as plt

print("CWD:", os.getcwd())

def serialize_data(message):
    return message.encode()

'''
def encode_bytes_with_bch(data, bch, chunk_size=8):
    encoded_chunks = []

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        # Pad the last chunk with zeros if needed
        chunk += b'\x00' * (chunk_size - len(chunk))
        # BCH Encoding
        encoded_chunk = bch.encode(chunk)
        # Append the encoded chunk to the result
        encoded_chunks.append(encoded_chunk)

    return encoded_chunks


def decode_bytes_with_bch(encoded_chunks, bch):
    decoded_chunks = []

    for encoded_chunk in encoded_chunks:
        # BCH Decoding
        decoded_chunk = bch.decode(encoded_chunk)
        # Append the decoded chunk to the result
        decoded_chunks.append(decoded_chunk)

    return decoded_chunks


def add_noise(data, percentage):
    num_bytes_to_flip = int(len(data) * percentage / 8)
    noisy_data = bytearray(data)
    
    for _ in range(num_bytes_to_flip):
        byte_index = random.randint(0, len(data) - 1)
        bit_index = random.randint(0, 7)
        noisy_data[byte_index] ^= (1 << bit_index)
    
    return bytes(noisy_data)

def bpsk_modulation(data, carrier_frequency):

    # Sample Rate: 100MHz
    # Time Duration: Sample Rate * data length
    time_duration = len(data) / 100e6
    time_points = np.linspace(0, time_duration, int(100e6 * time_duration), endpoint=False)
    
    # Convert bytes to integers (0 or 1)
    numeric_data = np.frombuffer(data, dtype=np.uint8) - ord('0')

    # Modulate the data onto the carrier signal
    # Amplitude of 1
    modulated_signal = np.sin(2 * np.pi * carrier_frequency * time_points + np.pi * (2 * numeric_data - 1))

    return modulated_signal, time_points
'''
# Read message from file
with open('message.txt', 'r') as file:
    message = file.read()

# Serialize data
serialized_data = serialize_data(message)
binary_int = int.from_bytes(serialized_data, "big")
binary_string = bin(binary_int)
print("Data Serialized")
print("Length of Serialized Data:", len(serialized_data))
print(serialized_data)
print(binary_string)
chunks = [serialized_data[i:i+8] for i in range(0, len(serialized_data), 8)]

num_errors = math.ceil(len(serialized_data) * 0.1)
m = len(serialized_data)
t = m - math.log2(len(serialized_data) + num_errors + 1)
t = max(1, int(t))

# BCH Encoding
bch = BCH(t=int(t), m=int(m))
bch_encoded_data = bch.encode(serialized_data)
print("Length of Serialized Data:", len(bch_encoded_data))
'''
# Encode each 8-bit chunk using BCH
encoded_chunks = encode_bytes_with_bch(serialized_data, bch)

# Print or use the encoded chunks as needed

for encoded_chunk in encoded_chunks:
    print(encoded_chunk)
print("Data Encoded")

# Decode each set of bytes using BCH
decoded_chunks = decode_bytes_with_bch(encoded_chunks, bch)

# Print or use the decoded chunks as needed
for decoded_chunk in decoded_chunks:
    print(decoded_chunk)

# Add Noise
noisy_data = add_noise(encoded_data, 0.1)  # 10% noise as an example
print("Noise Introduced")

# BPSK Modulation
modulated_data, time_data = bpsk_modulation(noisy_data, 6e9)  # 6 GHz carrier frequency
print("Data modulated")
'''
# Write to file
try:
    with open('transmitter.txt', 'wb') as file:
        file.write(serialized_data)
        file.flush()
except Exception as e:
    print("Error:", e)

with open('transmitter.txt', 'rb') as file:
    file_content = file.read()
    print("File Content:", file_content)

'''
# Plot the modulated signal
plt.plot(time_data, modulated_data)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('BPSK Modulated Signal')
plt.show()
'''
