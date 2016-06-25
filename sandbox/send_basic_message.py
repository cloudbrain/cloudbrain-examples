import time

from cloudbrain.publishers.rabbitmq import PikaPublisher

from cloudbrain_examples.settings import (base_routing_key, metric_name, num_channels, buffer_size,
                                          rabbitmq_address, rabbitmq_user, rabbitmq_pwd)



def main():
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
