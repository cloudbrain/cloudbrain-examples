import time

from cloudbrain.publishers.rabbitmq import PikaPublisher



def main():
    # Routing info
    user_id = "some_unique_id"
    device = 'openbci'
    base_routing_key = '%s:%s' % (user_id, device)

    # Metric info
    metric_name = 'eeg'
    num_channels = 8
    buffer_size = 2

    # RabbitMQ options
    rabbitmq_address = 'localhost'
    rabbitmq_user = 'guest'
    rabbitmq_pwd = 'guest'

    # Message to send
    message = {'timestamp': 100}
    for i in range(num_channels):
        message['channel_%s' % i] = i

    # Setup the publisher
    publisher = PikaPublisher(base_routing_key=base_routing_key,
                              rabbitmq_address=rabbitmq_address,
                              rabbitmq_user=rabbitmq_user,
                              rabbitmq_pwd=rabbitmq_pwd)
    publisher.connect()
    publisher.register(metric_name, num_channels, buffer_size)

    # Publish data
    print "Publishing data ..."
    publish = True
    while publish:
        try:
            publisher.publish(metric_name, message)
            time.sleep(0.001)
        except KeyboardInterrupt:
            publish = False
            publisher.disconnect()



if __name__ == '__main__':
    main()
