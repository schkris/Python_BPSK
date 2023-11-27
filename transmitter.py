import random
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from bchlib import BCH

print("CWD:", os.getcwd())

def serialize_data(message):
    return message.encode()

def add_noise(data, error_percentage):
    num_bits_to_flip = int(len(bin(int.from_bytes(data, "big"))) * error_percentage)
    noisy_data = bytearray(data)
    
    for _ in range(num_bits_to_flip):
        bit_index = random.randint(0, len(data) - 1)
        noisy_data[bit_index] ^= 1  # Flip the bit
    
    return bytes(noisy_data)


def bpsk_modulation(data, carrier_frequency, points_per_bit=100):

    # Time Duration: Sample Rate * data length
    time_duration = (len(bin(int.from_bytes(noisy_data, "big"))) - 2) / carrier_frequency
    time_points = np.linspace(0, time_duration, points_per_bit * (len(bin(int.from_bytes(noisy_data, "big"))) - 2), endpoint=False)
    
    # Convert binary data to a list of integers (0 or 1)
    bits = [int(bit) for byte in data for bit in f"{byte:08b}"]
    time_per_bit = time_duration / len(bits)

    # Modulate the data onto the carrier signal
    # Amplitude of 1
    modulated_signal = np.zeros_like(time_points, dtype=float)
    for i, bit in enumerate(bits):
        modulated_signal[i * points_per_bit: (i + 1) * points_per_bit] = \
            np.sin(2 * np.pi * carrier_frequency * time_points[i * points_per_bit: (i + 1) * points_per_bit] +
                   np.pi * (2 * bit - 1))
        
    square_wave = np.repeat(bits, 2)
    square_time = np.repeat(np.arange(0, time_duration, time_per_bit), 2)
        
    return modulated_signal, time_points, square_wave, square_time


# Read message from file
with open('message.txt', 'r') as file:
    message = file.read()

# Serialize data
serialized_data = serialize_data(message)
binary_int = int.from_bytes(serialized_data, "big")
binary_string = bin(binary_int)
print("Data Serialized")
print("Length of Serialized Data:", len(binary_string))
print("Serialized Data:", serialized_data)
print("Binary String:", binary_string)

# Error Correction Parameters
length = len(binary_string)
num_errors = math.ceil(length * 0.1)
m = math.ceil(math.log2(length + 1))
print("Code Order: ", m)
print("Error Correction: ", num_errors)

# BCH Encoding
bch = BCH(t=int(num_errors), m=int(m))
bch_encoded_data = bch.encode(serialized_data)
print("Length of Serialized Data:", len(bin(int.from_bytes(serialized_data, "big"))))
print("Length of Encoded Data:", len(bin(int.from_bytes(bch_encoded_data, "big"))))
print("Serialized Data:", binary_string)
print("Encoded Data:", bin(int.from_bytes(bch_encoded_data, "big")))


# Add Noise
noisy_data = add_noise(bch_encoded_data, 0.1)  # 10% noise as an example
print("Noise Introduced")
print("Length of Noisy Encoded Data:", len(bin(int.from_bytes(noisy_data, "big"))))
print("Noisy Encoded Data:", bin(int.from_bytes(noisy_data, "big")))

# BPSK Modulation
modulated_data, time_data, square_wave, square_time = bpsk_modulation(noisy_data, 6e2, points_per_bit=100)  # 6 GHz carrier frequency
print("Data modulated")

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


# Plot the modulated signal
plt.plot(time_data, modulated_data)
plt.step(square_time, square_wave)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('BPSK Modulated Signal')
plt.show()
