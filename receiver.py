import numpy as np
from bchlib import BCH

def bpsk_demodulation(modulated_data, carrier_frequency, time_points):

    threshold = 0.0
    # Number of bits to be found
    info_length = int(np.ceil(time_points[len(time_points) - 1] * carrier_frequency))
    print("Info Length: ", info_length)

    # Create a carrier and shifted carrier and compare both to data values to determine binary
    for i in range(info_length):
        # Calculate the index for each bit
        index = int((i + 0.5) * len(time_points) / info_length)
        
        # Generate sinusoids for the current bit
        base_carrier = np.sin(2 * np.pi * carrier_frequency * time_points)
        shifted_carrier = np.sin(2 * np.pi * carrier_frequency * time_points + np.pi)

        # Compare with generated sinusoids
        if np.dot(modulated_data[index], base_carrier) > threshold:
            demodulated_data[i] = 0
        else:
            demodulated_data[i] = 1

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
print("Demod Data Length: ", len(demodulated_data))
print("Data: ", demodulated_data[0:])

# BCH Decoding
# bch = BCH(t=int(1), m=int(1))
# decoded_data = bch.decode(demodulated_data)

# Deserialize data
# final_message = deserialize_data(decoded_data)

# Print the final message
# Read message from file
with open('message.txt', 'r') as file:
    message = file.read()
print("Original Message:", message)
# print("Received Message:", final_message)
