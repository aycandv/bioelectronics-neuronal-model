import numpy as np
import matplotlib.pyplot as plt


def _alphas(v, v_r):
    """

    :param v:
    :param v_r:
    :return:
    """
    dv = (v - v_r) * 1000
    print(v, v_r)
    mul = 1000
    alpha_m = 0.1 * (25 - dv) / ((np.exp((25 - dv) / 10)) - 1) * mul
    alpha_h = 0.07 * np.exp(-dv / 20) * mul
    alpha_n = 0.01 * (10 - dv) / ((np.exp((10 - dv) / 10)) - 1) * mul
    return alpha_m, alpha_h, alpha_n


def _betas(v, v_r):
    """

    :param v:
    :param v_r:
    :return:
    """
    dv = (v - v_r) * 1000
    mul = 1000
    beta_m = 4 * np.exp(-dv / 18) * mul
    beta_h = 1 / ((np.exp((30 - dv) / 10)) + 1) * mul
    beta_n = 0.125 * np.exp(-dv / 80) * mul
    return beta_m, beta_h, beta_n


class HHModel:
    def __init__(self, membrane_potential=-60e-3):
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

        pass

    def simulation(self, duration):
        """

        :param duration:
        :return:
        """
        self.time_interval = np.arange(0, duration + self.dt, self.dt)

    def run(self):
        self._initial_step()
        print(len(self.time_interval))
        for t in range(1, len(self.time_interval)):
            alpha_m, alpha_h, alpha_n = _alphas(self.V_membrane[t - 1], self.V_r)
            beta_m, beta_h, beta_n = _betas(self.V_membrane[t - 1], self.V_r)

            self.m[t] = self.m[t - 1] + self.dt * (alpha_m * (1 - self.m[t - 1]) - beta_m * self.m[t - 1])
            self.h[t] = self.h[t - 1] + self.dt * (alpha_h * (1 - self.h[t - 1]) - beta_h * self.h[t - 1])
            self.n[t] = self.n[t - 1] + self.dt * (alpha_n * (1 - self.n[t - 1]) - beta_n * self.n[t - 1])

            self.conductance_k[t] = self.n[t] ** 4 * self.max_conductivity_K
            self.conductance_na[t] = self.m[t] ** 3 * self.h[t] * self.max_conductivity_Na

            self.I_k[t] = self.conductance_k[t] * (self.V_membrane[t - 1] - self.E_k)
            self.I_na[t] = self.conductance_na[t] * (self.V_membrane[t - 1] - self.E_na)
            self.I_leak[t] = self.conductance_leak[t] * (self.V_membrane[t - 1] - self.E_leak)
            self.I_membrane[t] = self.I_k[t] + self.I_na[t] + self.I_leak[t]

            self.V_membrane[t] = self.V_membrane[t - 1] + (self.dt / self.cap_membrane) * (
                    self.I_stimulus[t] - self.I_k[t] - self.I_na[t] - self.I_leak[t])
        pass

    def _initial_step(self):
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

        pass

    def plot(self):
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
        # plt.plot(self.time_interval, self.I_membrane, label="J_membrane")
        # plt.plot(self.time_interval, self.I_stimulus, label="J_Stimulus")
        plt.grid()
        plt.legend()
        plt.show()

        plt.plot(self.time_interval, self.V_membrane, label="V_membrane")
        plt.grid()
        plt.legend()
        plt.show()

    def stimulus_signal(self, amplitude, duration, freq=None):
        """

        :param amplitude:
        :param duration:
        :param freq:
        :return:
        """
        self.I_stimulus = np.zeros(len(self.time_interval))
        if freq is None:
            self.I_stimulus[:int(duration / self.dt)] = amplitude
        else:
            self.I_stimulus[:int(duration / self.dt)] = amplitude * np.sin(2*np.pi*freq*self.time_interval[:int(duration / self.dt)])

        return self.time_interval, self.I_stimulus
