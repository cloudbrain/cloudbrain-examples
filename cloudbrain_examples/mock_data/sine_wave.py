import numpy as np
import time



def sine_wave(number_points, sampling_frequency, alpha_amplitude, alpha_freq,
              beta_amplitude, beta_freq):
    sample_spacing = 1.0 / sampling_frequency
    x = np.linspace(start=0.0, stop=number_points * sample_spacing, num=number_points)

    alpha = alpha_amplitude * np.sin(alpha_freq * 2.0 * np.pi * x)
    beta = beta_amplitude * np.sin(beta_freq * 2.0 * np.pi * x)

    import random

    y = alpha + beta + min(alpha_amplitude, beta_amplitude) / 2.0 * random.random()

    return y



def signal_generator(num_channels, number_points, sampling_frequency, signal):
    num_points_generated = 0
    t0 = 0

    sample_spacing = 1.0 / sampling_frequency
    while True:

        timestamp_in_s = t0 + num_points_generated * sample_spacing
        timestamp = int(timestamp_in_s * 1000000)
        datapoint = {'timestamp': timestamp}

        channel_data = signal[num_points_generated % number_points]
        for i in range(num_channels):
            datapoint['channel_%s' % i] = channel_data

        num_points_generated += 1
        time.sleep(sample_spacing)
        yield datapoint
