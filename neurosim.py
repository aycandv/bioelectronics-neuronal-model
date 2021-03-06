import numpy as np
import matplotlib.pyplot as plt


def _alphas(v, v_r):
    """
    Calculates alpha parameters using current membrane potential
    and resting potential in units of milli volts.
    :param v: Membrane potential in milli volts. float.
    :param v_r: Membrane potential in milli volts. float.
    :return: A tuple of three alpha parameters.
    """
    dv = (v - v_r) * 1000
    mul = 1000
    alpha_m = 0.1 * (25 - dv) / ((np.exp((25 - dv) / 10)) - 1) * mul
    alpha_h = 0.07 * np.exp(-dv / 20) * mul
    alpha_n = 0.01 * (10 - dv) / ((np.exp((10 - dv) / 10)) - 1) * mul
    return alpha_m, alpha_h, alpha_n


def _betas(v, v_r):
    """
    Calculates beta parameters using current membrane potential
    and resting potential in units of milli volts.
    :param v: Membrane potential in milli volts. float.
    :param v_r: Membrane potential in milli volts. float.
    :return: A tuple of three beta parameters.
    """
    dv = (v - v_r) * 1000
    mul = 1000
    beta_m = 4 * np.exp(-dv / 18) * mul
    beta_h = 1 / ((np.exp((30 - dv) / 10)) + 1) * mul
    beta_n = 0.125 * np.exp(-dv / 80) * mul
    return beta_m, beta_h, beta_n


class HHModel:
    def __init__(self, membrane_potential=-60e-3):
        """
        Initializes HHModel and all required parameters will be used
        in simulation.
        :param membrane_potential: Membrane potential of the cell.
        Default value is -60e-3 V.
        """
        self.max_conductivity_K = 36e-3
        self.max_conductivity_Na = 120e-3
        self.max_conductivity_leak = 0.3e-3

        self.cap_membrane = 1e-6
        self.R = 10e+3

        self.E_k = -72.1e-3
        self.E_na = 52.4e-3
        self.E_leak = -49.2e-3

        self.V_r = -60e-3  # Resting potential
        self.V_m_initial = membrane_potential  # initial membrane potential
        self.V_thr = self.V_r + 15e-3

        self.I_s = 0  # Stimulus current
        self.I_m = 0  # total membrane current for patch if no stimulus

        self.I_inj = 53e-6  # step current density peak

        self.dt = 1e-5

        self.m_0 = 0.0393
        self.h_0 = 0.6798
        self.n_0 = 0.2803

        self.T = 6.3

        self.time_interval = None

        self.V_membrane = None

        self.m = None
        self.h = None
        self.n = None

        self.conductance_na = None
        self.conductance_k = None
        self.conductance_leak = None

        self.I_na = None
        self.I_k = None
        self.I_leak = None
        self.I_stimulus = None
        self.I_membrane = None

    def simulation(self, duration):
        """
        After initializing HHModel, this function should be called.
        :param duration: duration of simulation in seconds.
        :return:
        """
        self.time_interval = np.arange(0, duration + self.dt, self.dt)

    def run(self):
        """
        In an iterative approach, it calculates conductivities of ions,
        m,n and h particles, ionic currents and membrane potential at
        each time step so that it can be plotted to observe results.
        Before stepping into for loop, it initializes parameters such as
        maximum conductivity before simulation starts.
        :return:
        """

        # Initializing all variables. Setting initial parameters
        # such as m, n, h, Vm to be able to run simulation.
        self._initial_step()
        for t in range(1, len(self.time_interval)):
            # Getting alpha and beta variables.
            alpha_m, alpha_h, alpha_n = _alphas(self.V_membrane[t - 1], self.V_r)
            beta_m, beta_h, beta_n = _betas(self.V_membrane[t - 1], self.V_r)

            # Calculation of m, n, h particles at time t.
            self.m[t] = self.m[t - 1] + self.dt * (alpha_m * (1 - self.m[t - 1]) - beta_m * self.m[t - 1])
            self.h[t] = self.h[t - 1] + self.dt * (alpha_h * (1 - self.h[t - 1]) - beta_h * self.h[t - 1])
            self.n[t] = self.n[t - 1] + self.dt * (alpha_n * (1 - self.n[t - 1]) - beta_n * self.n[t - 1])

            # Calculating conductance of Sodium and Potassium at time t.
            self.conductance_k[t] = self.n[t] ** 4 * self.max_conductivity_K
            self.conductance_na[t] = self.m[t] ** 3 * self.h[t] * self.max_conductivity_Na

            # Calculating currents at time t.
            self.I_k[t] = self.conductance_k[t] * (self.V_membrane[t - 1] - self.E_k)
            self.I_na[t] = self.conductance_na[t] * (self.V_membrane[t - 1] - self.E_na)
            self.I_leak[t] = self.conductance_leak[t] * (self.V_membrane[t - 1] - self.E_leak)
            self.I_membrane[t] = self.I_k[t] + self.I_na[t] + self.I_leak[t]

            # Calculating membrane potential at time t.
            self.V_membrane[t] = self.V_membrane[t - 1] + (self.dt / self.cap_membrane) * (
                    self.I_stimulus[t] - self.I_k[t] - self.I_na[t] - self.I_leak[t])

    def _initial_step(self):
        """
        It creates arrays of membrane potential, conductivity of ions,
        ionic currents and m, n and h particles. It also sets initial
        values of those arrays since it will be an iterative approach
        to calculate all those values.
        :return:
        """
        self.V_membrane = np.zeros(len(self.time_interval), dtype=np.float128)
        self.V_membrane[0] = self.V_m_initial

        self.m = np.zeros(len(self.time_interval))
        self.m[0] = self.m_0
        self.h = np.zeros(len(self.time_interval))
        self.h[0] = self.h_0
        self.n = np.zeros(len(self.time_interval))
        self.n[0] = self.n_0

        self.conductance_na = np.zeros(len(self.time_interval))
        self.conductance_na[0] = self.max_conductivity_Na * self.m[0] ** 3 * self.h[0]
        self.I_na = np.zeros(len(self.time_interval))
        self.I_na[0] = self.conductance_na[0] * (self.V_membrane[0] - self.E_na)

        self.conductance_k = np.zeros(len(self.time_interval))
        self.conductance_k[0] = self.max_conductivity_K * self.n[0] ** 4
        self.I_k = np.zeros(len(self.time_interval))
        self.I_k[0] = self.conductance_k[0] * (self.V_membrane[0] - self.E_k)

        self.conductance_leak = np.repeat(self.max_conductivity_leak, len(self.time_interval))
        self.I_leak = np.zeros(len(self.time_interval))
        self.I_leak[0] = self.conductance_leak[0] * (self.V_membrane[0] - self.E_leak)

        self.V_membrane[0] = self.V_r + (self.dt / self.cap_membrane) * (
                self.I_stimulus[0] - self.I_k[0] - self.I_na[0] - self.I_leak[0])

        self.I_membrane = np.zeros(len(self.time_interval))
        self.I_membrane[0] = self.I_na[0] + self.I_k[0] + self.I_leak[0]

    def plot(self):
        """
        For ease of use, it plots general properties of the neuron
        such as membrane potential, conductivity of ions, currents etc.
        """
        plt.plot(self.time_interval, self.m, label="m")
        plt.plot(self.time_interval, self.n, label="n")
        plt.plot(self.time_interval, self.h, label="h")
        plt.grid()
        plt.legend()
        plt.show()

        plt.plot(self.time_interval, self.conductance_k, label="g_K")
        plt.plot(self.time_interval, self.conductance_na, label="g_Na")
        plt.grid()
        plt.legend()
        plt.show()

        plt.plot(self.time_interval, self.I_k, label="J_K")
        plt.plot(self.time_interval, self.I_na, label="J_Na")
        # plt.plot(self.time_interval, self.I_leak, label="J_leak")
        plt.plot(self.time_interval, self.I_membrane, label="J_membrane")
        plt.plot(self.time_interval, self.I_stimulus, label="J_Stimulus")
        plt.grid()
        plt.legend()
        plt.show()

        plt.plot(self.time_interval, self.V_membrane, label="V_membrane")
        plt.grid()
        plt.legend()
        plt.show()

    def stimulus_signal(self, amplitude, duration, start_time=0, freq=None):
        """
        After simulation is initialized and simulation duration is set, this
        function creates stimulus current to be applied to the neuron.
        :param amplitude: Amplitude of stimulus current in Amps.
        :param duration: Stimulus current duration in seconds.
        :param start_time: Starting time of stimulus current in seconds.
        :param freq: Frequency of stimulus current. Default value is None.
        :return: time interval and stimulus signal arrays as a tuple of two elements.
        """
        if self.I_stimulus is None:
            self.I_stimulus = np.zeros(len(self.time_interval))
        if freq is None:
            self.I_stimulus[int(start_time / self.dt):int((duration + start_time) / self.dt)] = amplitude
            print(int(start_time / self.dt))
            print(int((duration + start_time) / self.dt))
        else:
            self.I_stimulus[int(start_time / self.dt):int((duration + start_time) / self.dt)] = amplitude * np.sin(
                2 * np.pi * freq * self.time_interval[int(start_time / self.dt):int((duration + start_time) / self.dt)])

        return self.time_interval, self.I_stimulus


class CSModel(HHModel):

    def __init__(self, membrane_potential=-74.5e-3):
        """
        Initializes Connor and Steven's HHModel and all required parameters will be used
        in simulation.
        :param membrane_potential: Membrane potential of the cell.
        Default value is -74.5e-3 V.
        """
        super().__init__(membrane_potential=-74.5e-3)
        self.max_conductivity_A = 0.477e-3
        self.a_0 = 0.5079
        self.b_0 = 0.4332
        self.E_a = -75e-3

        self.a = None
        self.b = None
        self.I_a = None

        self.tau_a = None
        self.tau_b = None

    def _initial_step(self):
        super()._initial_step()
        self.a = np.zeros(len(self.time_interval))
        self.a[0] = self.a_0
        self.b = np.zeros(len(self.time_interval))
        self.b[0] = self.b_0

        mul = 1

        self.conductance_A = np.zeros(len(self.time_interval))
        self.conductance_A[0] = self.max_conductivity_A * self.a[0] ** 3 * self.b[0]
        self.I_a = np.zeros(len(self.time_interval))
        self.I_a[0] = self.conductance_A[0] * (self.V_membrane[0] - self.E_a) #* 1e3

        self.a_inf = np.zeros(len(self.time_interval))
        self.a_inf[0] = ((0.0761 * np.exp(0.0314 * (self.V_membrane[0]*1e3 + 94.22))) /
                         (1 + np.exp(0.0346 * (self.V_membrane[0]*1e3 + 1.17)))) ** (1 / 3)

        self.b_inf = np.zeros(len(self.time_interval))
        self.b_inf[0] = (1 + np.exp(0.0688 * (self.V_membrane[0]*1e3 + 53.3))) ** -4

        self.tau_a = np.zeros(len(self.time_interval))
        self.tau_a[0] = 0.3632 + 1.158 / (1 + np.exp(0.0497 * (self.V_membrane[0]*1e3 + 55.96))) * 1000

        self.tau_b = np.zeros(len(self.time_interval))
        self.tau_b[0] = 1.24 + 2.678 / (1 + np.exp(0.0624 * (self.V_membrane[0] * 1e3 + 50))) * 1000

    def run(self):
        """
        In an iterative approach, it calculates conductivities of ions,
        a, b, m, n and h particles, ionic currents and membrane potential
        at each time step so that it can be plotted to observe results.
        Before stepping into for loop, it initializes parameters such as
        maximum conductivity before simulation starts.
        :return:
        """

        # Initializing all variables. Setting initial parameters
        # such as m, n, h, Vm to be able to run simulation.
        mul = 1000
        self._initial_step()
        for t in range(1, len(self.time_interval)):
            # Getting alpha and beta variables.

            dv = (self.V_membrane[t - 1] - self.V_r) * 1000

            alpha_m = 0.38 * (dv + 29.7) / (1 - np.exp(-(dv + 29.7) / 10)) * mul
            alpha_h = 0.266 * np.exp(-(dv + 48) / 20) * mul
            alpha_n = 0.02 * (45.7 + dv) / (-(np.exp((-45.7 - dv) / 10)) + 1) * mul

            beta_m = 15.2 * np.exp(-0.0556 * (dv + 54.7)) * mul
            beta_h = 3.8 / ((np.exp((-18 - dv) / 10)) + 1) * mul
            beta_n = 0.25 * np.exp(-(dv - 55.7) / 80) * mul

            # Calculation of m, n, h particles at time t.
            self.m[t] = self.m[t - 1] + self.dt * (alpha_m * (1 - self.m[t - 1]) - beta_m * self.m[t - 1])
            self.h[t] = self.h[t - 1] + self.dt * (alpha_h * (1 - self.h[t - 1]) - beta_h * self.h[t - 1])
            self.n[t] = self.n[t - 1] + self.dt * (alpha_n * (1 - self.n[t - 1]) - beta_n * self.n[t - 1])

            self.a_inf[t-1] = ((0.0761 * np.exp(0.0314 * (dv + 94.22))) /
                             (1 + np.exp(0.0346 * (dv + 1.17)))) ** (1 / 3)
            self.b_inf[t-1] = (1 + np.exp(0.0688 * (dv + 53.3))) ** -4

            self.tau_a[t-1] = 0.3632 + 1.158 / (1 + np.exp(0.0497 * (dv + 55.96))) * 1000
            self.tau_b[t-1] = 1.24 + 2.678 / (1 + np.exp(0.0624 * (dv + 50))) * 1000

            self.a[t] = self.a[t-1] + ((self.a_inf[t-1] - self.a[t-1]) / self.tau_a[t-1])
            self.b[t] = self.b[t-1] + ((self.b_inf[t-1] - self.b[t-1]) / self.tau_b[t-1])

            # Calculating conductance of Sodium and Potassium at time t.
            self.conductance_k[t] = self.n[t] ** 4 * self.max_conductivity_K
            self.conductance_na[t] = self.m[t] ** 3 * self.h[t] * self.max_conductivity_Na
            self.conductance_A[t] = self.max_conductivity_A * self.a[t] ** 3 * self.b[t]

            # Calculating currents at time t.

            self.I_k[t] = self.conductance_k[t] * (self.V_membrane[t - 1] - self.E_k)
            self.I_na[t] = self.conductance_na[t] * (self.V_membrane[t - 1] - self.E_na)
            self.I_leak[t] = self.conductance_leak[t] * (self.V_membrane[t - 1] - self.E_leak)
            self.I_a[t] = self.conductance_A[t] * (self.V_membrane[t - 1] - self.E_a)

            self.I_membrane[t] = self.I_k[t] + self.I_na[t] + self.I_leak[t] + self.I_a[t]

            # Calculating membrane potential at time t.
            self.V_membrane[t] = self.V_membrane[t - 1] + (self.dt / self.cap_membrane) * (
                    self.I_stimulus[t] - self.I_membrane[t])
