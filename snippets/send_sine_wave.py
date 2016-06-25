import sys
import time

from cloudbrain.publishers.rabbitmq import PikaPublisher
from cloudbrain.core.signal import sine_wave, signal_generator

from cloudbrain_examples.settings import (base_routing_key, metric_name, num_channels, buffer_size,
                                          rabbitmq_address, rabbitmq_user, rabbitmq_pwd)


def main():

    # Sine wave params
    alpha_amplitude = 10.0
    alpha_freq = 10.0
    beta_amplitude = 5.0
    beta_freq = 25.0
    notch_amplitude = 10.0
    notch_freq = 60.0 # Simulate ambiant electrical noise

    # Mock data generator (sine wave)
    sampling_frequency = 250.0  # 1/250 = 0.004 s
    number_points = 250
    signal = sine_wave(number_points, sampling_frequency, alpha_amplitude, alpha_freq,
                       beta_amplitude, beta_freq, notch_amplitude, notch_freq)
    data = signal_generator(num_channels, sampling_frequency, signal)

    # Setup the publisher
    publisher = PikaPublisher(base_routing_key=base_routing_key,
                              rabbitmq_address=rabbitmq_address,
                              rabbitmq_user=rabbitmq_user,
                              rabbitmq_pwd=rabbitmq_pwd)
    publisher.connect()
    publisher.register(metric_name, num_channels, buffer_size)

    # Publish data
    print "Publishing data ..."
    try:
        for datapoint in data:
            publisher.publish(metric_name, datapoint)
    except KeyboardInterrupt:
        publisher.disconnect()
        time.sleep(0.1)
        sys.exit(0)



if __name__ == '__main__':
    main()
