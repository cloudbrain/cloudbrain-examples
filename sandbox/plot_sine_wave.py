import sys

import matplotlib.pyplot as plt

from cloudbrain.core.signal import sine_wave, signal_generator



def plot_data(num_channels, data):
    f, axarr = plt.subplots(num_channels)
    for i in range(num_channels):
        channel_name = 'channel_%s' % i
        data_to_plot = []
        for datapoint in data:
            data_to_plot.append(datapoint[channel_name])
        axarr[i].plot(data_to_plot)
        axarr[i].set_title(channel_name)
    plt.show()



def main():
    # Params
    sampling_frequency = 250.0  # i.e. 0.004 seconds (=1/250.0)
    alpha_amplitude = 1.0
    alpha_freq = 10.0
    beta_amplitude = 1.0
    beta_freq = 25.0
    notch_amplitude = 10.0
    notch_freq = 60.0
    num_channels = 8
    number_points = 249
    buffer_size = 10
    num_buffers_to_plot = 20

    # Sine wave data
    signal = sine_wave(number_points, sampling_frequency, alpha_amplitude,
                       alpha_freq, beta_amplitude, beta_freq, notch_amplitude, notch_freq)
    data = signal_generator(num_channels, sampling_frequency, signal)

    # plot data
    data_to_plot = []
    buffer = []
    for datapoint in data:
        buffer.append(datapoint)
        data_to_plot.append(datapoint)

        if len(buffer) == buffer_size:
            print buffer
            buffer = []

        if len(data_to_plot) == num_buffers_to_plot * buffer_size:
            plot_data(num_channels, data_to_plot)
            sys.exit(0)



if __name__ == '__main__':
    main()
