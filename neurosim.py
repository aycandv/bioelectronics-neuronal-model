import numpy as np


def _alphas(v, v_r):
    """

    :param v:
    :param v_r:
    :return:
    """
    dv = (v - v_r) * 1000
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
        self.V_m_initial = -60e-3  # initial membrane potential
        self.V_thr = self. V_r + 15e-3

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
        pass

    def _initial_step(self):
        self.m = np.zeros(len(self.time_interval))
        self.m[0] = self.m_0
        self.h = np.zeros(len(self.time_interval))
        self.h[0] = self.h_0
        self.n = np.zeros(len(self.time_interval))
        self.n[0] = self.n_0

        conductance_na = np.zeros(len(time_interval))
        conductance_na[0] = max_conductivity_Na * m[0] ** 3 * h[0]
        I_na = np.zeros(len(time_interval))
        I_na[0] = conductance_na[0] * (V_membrane[0] - E_na)

        conductance_k = np.zeros(len(time_interval))
        conductance_k[0] = max_conductivity_K * n[0] ** 4
        I_k = np.zeros(len(time_interval))
        I_k[0] = conductance_k[0] * (V_membrane[0] - E_k)

        conductance_leak = np.repeat(max_conductivity_leak, len(time_interval))
        I_leak = np.zeros(len(time_interval))
        I_leak[0] = conductance_leak[0] * (V_membrane[0] - E_leak)

        I_stimulus = np.zeros(len(time_interval))
        I_stimulus[0:int(inject_time // dt)] = I_inj

        V_membrane[0] = V_r + (dt / cap_membrane) * (-I_k[0] - I_na[0] - I_leak[0] + I_stimulus[0])

        I_membrane = np.zeros(len(time_interval))
        I_membrane[0] = I_na[0] + I_k[0] + I_leak[0]

        pass

    def plot(self):
        pass

    def stimulus_signal(self, amplitude, duration, freq=None):
        """

        :param amplitude:
        :param duration:
        :param freq:
        :return:
        """
        self.I_stimulus = np.zeros(len(self.time_interval))
        self.I_stimulus[0:int(duration // self.dt)] = amplitude

    def _betas(self):
        pass
