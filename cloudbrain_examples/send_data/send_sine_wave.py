import sys
import time

from cloudbrain.publishers.rabbitmq import PikaPublisher
from cloudbrain.core.signal import sine_wave, signal_generator



def main():
    # Routing info
    user_id = "some_unique_id"
    device = 'openbci'
    base_routing_key = '%s:%s' % (user_id, device)

    # Metric info
    metric_name = 'eeg'
    num_channels = 8
    buffer_size = 10

    # Sine wave params
    alpha_amplitude = 10.0
    alpha_freq = 10.0
    beta_amplitude = 5.0
    beta_freq = 25.0

    # RabbitMQ options
    rabbitmq_address = 'localhost'
    rabbitmq_user = 'guest'
    rabbitmq_pwd = 'guest'

    # Mock data generator (sine wave)
    sampling_frequency = 250.0  # 1/250 = 0.004 s
    number_points = 249
    signal = sine_wave(number_points, sampling_frequency, alpha_amplitude, alpha_freq,
                       beta_amplitude, beta_freq)
    data = signal_generator(num_channels, number_points, sampling_frequency, signal)

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
