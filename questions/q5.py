from neurosim import *
import matplotlib.pyplot as plt

model = HHModel()

model.simulation(duration=20e-3)

first_start = 0.1e-3
second_start = 6.5e-3
stimulus_amplitude = 500e-6
model.stimulus_signal(amplitude=stimulus_amplitude, duration=0.15e-3, start_time=first_start)
model.stimulus_signal(amplitude=stimulus_amplitude, duration=0.15e-3, start_time=second_start)

model.run()
model.time_interval = model.time_interval*1000

plt.figure(figsize=(11, 9))
plt.suptitle(f"Waiting Time Between Two Stimulus: {(second_start*1000 - first_start*1000)} msec \nStimulus: {stimulus_amplitude*1e6} uA")

plt.subplot(3, 1, 1)
plt.plot(model.time_interval, model.I_stimulus*1e6, label="Stimulus Current", color="green")
plt.ylabel("uA")
plt.legend()
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(model.time_interval, model.V_membrane*1000, label="Membrane Potential")
plt.ylabel("mV")
plt.grid()
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(model.time_interval, model.m, label="m")
plt.plot(model.time_interval, model.n, label="n")
plt.plot(model.time_interval, model.h, label="h")
plt.xlabel("Time Interval (ms)")
plt.ylabel("Probability")
plt.grid()
plt.legend()

plt.show()
