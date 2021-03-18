from neurosim import *
import matplotlib.pyplot as plt

model = HHModel()
model.simulation(duration=1)

frequencies = [1, 2, 5, 10, 20, 50, 100]

for f in frequencies:
    print(f)
    model.stimulus_signal(amplitude=15e-6, duration=1, start_time=0.1e-3, freq=f)
    model.run()

    plt.figure(figsize=(9, 10))
    plt.suptitle(f"Stimulation w/ Frequency={f} Hz")

    plt.subplot(3, 1, 1)
    plt.plot(model.time_interval, model.I_stimulus * 1e6, label="Stimulus Current", color="green")
    plt.ylabel("uA")
    plt.legend()
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(model.time_interval, model.V_membrane * 1000, label="Membrane Potential")
    plt.ylabel("mV")
    plt.grid()
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(model.time_interval, model.m, label="m")
    plt.plot(model.time_interval, model.n, label="n")
    plt.plot(model.time_interval, model.h, label="h")
    plt.xlabel("Time Interval (s)")
    plt.ylabel("Probability")
    plt.grid()
    plt.legend()

    plt.show()
