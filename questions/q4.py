from neurosim import *
import matplotlib.pyplot as plt

model = HHModel()

model.simulation(duration=6e-3)

model.stimulus_signal(amplitude=50e-6, duration=0.15e-3, start_time=0.1e-3)

model.run()
model.time_interval = model.time_interval*1000
plt.figure(figsize=(10, 7))
plt.plot(model.time_interval, model.V_membrane*1000, label="50uA Stimulus Current Amplitude")

model.stimulus_signal(amplitude=200e-6, duration=0.15e-3)
model.run()
plt.plot(model.time_interval, model.V_membrane*1000, label="200uA Stimulus Current Amplitude")

model.stimulus_signal(amplitude=500e-6, duration=0.15e-3)
model.run()
plt.plot(model.time_interval, model.V_membrane*1000, label="500uA Stimulus Current Amplitude")

plt.ylabel("mV")
plt.xlabel("Time Interval (ms)")
plt.title("Question 4")
plt.legend()
plt.grid()

plt.show()
