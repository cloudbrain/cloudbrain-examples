# Routing info
user_id = "some_unique_id"
device = 'device_name'
base_routing_key = '%s:%s' % (user_id, device)

# Metric info
metric_name = 'eeg'
num_channels = 8
buffer_size = 2

# RabbitMQ options
rabbitmq_address = 'dev.getcloudbrain.com'
rabbitmq_user = 'cloudbrain'
rabbitmq_pwd = 'cloudbrain'