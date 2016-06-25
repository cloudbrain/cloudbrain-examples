import pylab as plt
import numpy as np
from scipy import signal

number_points = 200
sampling_frequency = 250.0
sample_spacing = 1.0 / sampling_frequency
x = np.linspace(start=0.0, stop=number_points * sample_spacing, num=number_points)

frequency_to_filter = 60.0
f_nyquist = 0.5 * sampling_frequency
f_start = (frequency_to_filter - 5.0) / f_nyquist
f_stop = (frequency_to_filter + 5.0) / f_nyquist
a0, b0 = signal.butter(2, [f_start, f_stop], 'bandstop')

y = np.sin(2 * np.pi * frequency_to_filter * x)
fy0 = signal.lfilter(a0, b0, y)

b1, a1 = signal.iirfilter(1, 3.0 / 125.0, btype='highpass')
b2, a2 = signal.iirfilter(1, [f_start, f_stop], btype='bandstop')
fy1 = signal.lfilter(b1, a1, y)
fy2 = signal.lfilter(b2, a2, fy1)


plt.plot(y[50:], label='Original signal', color='pink')
plt.plot(fy0[50:], label='Butterworth filter', color='black')
plt.plot(fy1[50:], label='High pass', color='blue')
plt.plot(fy2[50:], label='Band Stop', color='green')
plt.legend()
plt.show()

