from neurosim import *
import matplotlib.pyplot as plt

model = HHModel(membrane_potential=-105e-3)

model.simulation(duration=20e-3)

model.stimulus_signal(amplitude=-11.7e-6, duration=2e-3, start_time=0.1e-3)

model.run()
model.time_interval = model.time_interval*1000

plt.figure(figsize=(11, 9))
plt.suptitle("Question 6\nAnode Break Excitation")

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
