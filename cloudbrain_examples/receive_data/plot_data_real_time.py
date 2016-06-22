#!/usr/bin/env python2

import matplotlib.pyplot as plt
import numpy as np
import json
import sys

from scipy import signal

from cloudbrain.subscribers.rabbitmq import PikaSubscriber


# A bunch of global variables to plot the data
plt.close("all")
fig = plt.figure()
ax = fig.add_subplot(111)

N_points = 1024
extra = 0

data = [0 for i in range(N_points)]

count = 0

b1, a1 = signal.iirfilter(1, [59.0 / 125.0, 61.0 / 125.0], btype='bandstop')
b2, a2 = signal.iirfilter(1, 3.0 / 125.0, btype='highpass')

# some X and Y data
x = np.arange(N_points)
y = data

li, = ax.plot(x, data)

# draw and show it
fig.canvas.draw()
plt.show(block=False)



def update_plot():
    global data, b, a

    # set the new data
    data_f = data
    data_f = signal.lfilter(b1, a1, data_f)
    data_f = signal.lfilter(b2, a2, data_f)
    #data_f = data_f[-N_points:]

    li.set_ydata(data_f)

    ax.relim()
    ax.autoscale_view(True, True, True)
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
    device_id = "amsterdam"
    device_name = "openbci"
    base_routing_key = "%s:%s" % (device_id, device_name)

    metric_name = 'eeg'
    num_channels = 8

    rabbitmq_address = "localhost"
    rabbitmq_user = "guest"
    rabbitmq_pwd = "guest"

    subscriber = PikaSubscriber(base_routing_key, rabbitmq_address, rabbitmq_user, rabbitmq_pwd)
    subscriber.connect()

    subscriber.register(metric_name, num_channels)
    subscriber.subscribe(metric_name, consume_metric)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

