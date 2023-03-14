import pyqubo
from pyqubo import Array, Constraint, Placeholder, Binary, cpp_pyqubo
import numpy as np


class QuboModel:
    def __init__(self, A, D, T, S_dt, R_a, G_ga, r_adt) -> None:
        self.A = A
        self.D = D
        self.T = T
        self.S_dt = S_dt
        self.R_a = R_a
        self.G_ga = G_ga
        self.r_adt = r_adt
        self.no_a = len(self.A)
        self.no_d = len(self.D)
        self.no_t = len(self.T)
        self.no_g = len(self.G_ga)
        self.x = Array.create(
            "x",
            shape=(self.no_a, self.no_d, self.no_t),
            vartype="BINARY"
        )

    def create_obj_need_people(self) -> cpp_pyqubo.Add:
        cost = 0
        for t in range(self.no_t):
            for d in range(self.no_d):
                cost += (np.sum(self.x.T[t][d]) - self.S_dt[d][t]) ** 2
        return cost

    def create_obj_hope_day(self) -> cpp_pyqubo.Add:
        cost = 0
        for a in range(self.no_a):
            cost += (np.sum(self.x[a]) - self.R_a[a]) ** 2
        return cost

    def create_constraint_non_available(self) -> cpp_pyqubo.Add:
        costraint = 0
        for a in range(self.no_a):
            for d in range(self.no_d):
                for t in range(self.no_t):
                    # if self.r_adt[a][d][t] == 0:
                    costraint += (1 - self.r_adt[a][d][t]) * self.x[a][d][t]
        return costraint

    def create_constraint_group(self) -> cpp_pyqubo.Add:
        costraint = 0
        for d in range(self.no_d):
            for t in range(self.no_t):
                for g in range(self.no_g):
                    costraint += (
                            (np.sum(self.G_ga[g]) - np.sum(self.x.T[t][d] * self.G_ga[g]))
                            *
                            np.sum(self.x.T[t][d] * self.G_ga[g])
                    )
        return costraint

    def create_cost_function(self) -> cpp_pyqubo.Add:
        cost_function = (
            self.create_obj_need_people()
            +
            self.create_obj_hope_day()
            +
            Placeholder("w_desire") * Constraint(self.create_constraint_non_available(), label="constraint_1")
            +
            Placeholder("w_group") * Constraint(self.create_constraint_group(), label="constraint_1")
        )
        return cost_function

    def create_model(self) -> cpp_pyqubo.Model:
        cost_function = self.create_cost_function()
        model = cost_function.compile()
        return model