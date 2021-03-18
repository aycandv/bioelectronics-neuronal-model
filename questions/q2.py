from neurosim import *

model = HHModel()

model.simulation(duration=20e-3)
model.stimulus_signal(amplitude=53e-6, duration=0.2e-3, start_time=0.1e-3)

model.run()

# Plotting Results

model.time_interval = model.time_interval*1000

plt.figure(figsize=(10, 12))
plt.suptitle("Question 2")

plt.subplot(4, 1, 1)
plt.plot(model.time_interval, model.I_stimulus*1e6, label="I_stimulus", color="green")
plt.ylabel("uA")
plt.legend()
plt.grid()

plt.subplot(4, 1, 2)
plt.plot(model.time_interval, model.V_membrane*1000, label="Membrane Potential")
plt.ylabel("mV")
plt.legend()
plt.grid()

plt.subplot(4, 1, 3)
plt.plot(model.time_interval, model.I_k*1000, label="K current")
plt.plot(model.time_interval, model.I_na*1000, label="Na current")
plt.plot(model.time_interval, model.I_membrane*1000, label="Membrane current")
plt.plot(model.time_interval, model.I_leak*1000, label="Leak current")
plt.ylabel("mA")
plt.legend()
plt.grid()

plt.subplot(4, 1, 4)
plt.plot(model.time_interval, model.m, label="m")
plt.plot(model.time_interval, model.n, label="n")
plt.plot(model.time_interval, model.h, label="h")
plt.ylabel("Probability")
plt.xlabel("Time Interval (ms)")
plt.legend()
plt.grid()

plt.show()

plt.plot(model.time_interval, model.conductance_na*1000, label="Conductivity Na")
plt.plot(model.time_interval, model.conductance_k*1000, label="Conductivity K")
plt.ylabel("Conductivity (mS * cm^-2)")
plt.xlabel("Time Interval (ms)")
plt.legend()
plt.grid()

plt.show()