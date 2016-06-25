import time

from cloudbrain.subscribers.rabbitmq import PikaSubscriber


from cloudbrain_examples.settings import (base_routing_key, metric_name, num_channels, buffer_size,
                                          rabbitmq_address, rabbitmq_user, rabbitmq_pwd)


def _print_callback(unsed_ch, unsed_method, unsed_properties, body):
    print "==> %s" % body



def main():

    # Setup the subscriber
    subscriber = PikaSubscriber(base_routing_key=base_routing_key,
                                rabbitmq_address=rabbitmq_address,
                                rabbitmq_user=rabbitmq_user,
                                rabbitmq_pwd=rabbitmq_pwd)
    subscriber.connect()
    subscriber.register(metric_name, num_channels)
    time.sleep(1)  # Leave it some time to register

    # Get one message at a time
    one_message = subscriber.get_one_message(metric_name)
    print "\n==> Got one message: %s\n" % one_message
    time.sleep(2)  # Give people time to read the message

    # Get message continuously
    print "==> Subscribing ..."
    try:
        subscriber.subscribe(metric_name, _print_callback)
    except KeyboardInterrupt:
        subscriber.disconnect()



if __name__ == '__main__':
    main()
