import matplotlib.pyplot as plt
import numpy as np
import json
import sys

from scipy import signal

from cloudbrain.subscribers.rabbitmq import PikaSubscriber

from cloudbrain_examples.settings import (base_routing_key, metric_name, num_channels, buffer_size,
                                          rabbitmq_address, rabbitmq_user, rabbitmq_pwd)

# A bunch of global variables to plot the data
extra = 0
count = 0
N_points = 200
data = [0 for i in range(N_points)]

plt.close("all")
fig = plt.figure()
ax = fig.add_subplot(111)

# Init X and Y data
x = np.arange(N_points)
y = data

li, = ax.plot(x, data)

# draw and show it
fig.canvas.draw()
plt.show(block=False)



def update_plot():
    global data, b, a

    li.set_ydata(data)

    ax.relim()
    ax.set_ylim([-15, 15])
    # ax.autoscale_view(True, True, True)
    fig.canvas.draw()

    plt.draw()

    plt.pause(0.0001)  # add this it will be OK.



def consume_metric(connection, deliver, properties, msg_s):
    global data

    msg = json.loads(msg_s)
    d = []
    for row in msg:
        d.append(float(row['channel_0']))
    data.extend(d)

    data = data[-N_points - extra:]
    update_plot()



def main():
    subscriber = PikaSubscriber(base_routing_key, rabbitmq_address, rabbitmq_user, rabbitmq_pwd)
    subscriber.connect()

    subscriber.register(metric_name, num_channels)

    print "Plotting %s ..." % metric_name
    subscriber.subscribe(metric_name, consume_metric)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
