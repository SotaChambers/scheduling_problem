import numpy as np
from utils.utils import load_yaml


class Parameter:
    config = load_yaml("config/config.yml")

    A = config["A"]
    D = config["D"]
    T = config["T"]
    S_dt = config["S_dt"]
    R_a = config["R_a"]
    G_ga = np.array(config["G_ga"])
    r_adt = config["r_adt"]

    no_a = len(A)
    no_d = len(D)
    no_t = len(T)
    no_g = len(G_ga)