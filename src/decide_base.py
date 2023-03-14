import numpy as np
from pyqubo import Array, Constraint, Placeholder, Binary
from openjij import SQASampler
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib

from utils.utils import load_yaml
from utils.stop_watch import stop_watch
from model.model import QuboModel
from src.common.setting_parameter import Parameter
from model.sampler import select_sampler


def make_plot(data_list, x, save_path, labels, x_label, y_label):
    fig = plt.figure()
    plt.rcParams["font.size"] = 16
    for data, label in zip(data_list, labels):
        plt.plot(x, data, marker="o", label=label)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    plt.axvline(1.3, ls="--", c="black", lw=1)
    plt.axvline(1.4, ls="--", c="black", lw=1)
    plt.axvline(1.5, ls="--", c="black", lw=1)
    plt.legend()
    fig.savefig(save_path)


@stop_watch
def main():

    # ======= 問題の設定
    parameter = Parameter()

    qubo_model = QuboModel(
        parameter.A,
        parameter.D,
        parameter.T,
        parameter.S_dt,
        parameter.R_a,
        parameter.G_ga,
        parameter.r_adt
    )
    model = qubo_model.create_model()

    base_test = [round(i * 0.05, 2) for i in range(1, 41)]
    w_desire = parameter.config["coeff"]["w_desire"]["ratio"]
    w_group = parameter.config["coeff"]["w_group"]["ratio"]

    result_list = []
    min_energy_list = []
    mean_energy_list = []
    max_energy_list = []

    for base in base_test:
        w_desire_test = w_desire * base
        w_group_test = w_group * base
        feed_dict = {"w_desire": w_desire_test, "w_group": w_group_test}
        qubo, offset = model.to_qubo(feed_dict=feed_dict)

        sampler = select_sampler(parameter.config["algorithm"])
        sampleset = sampler.sample_qubo(qubo, num_reads=parameter.config["num_reads"])

        decode_samples = model.decode_sampleset(sampleset=sampleset, feed_dict=feed_dict)
        success_num = 0
        for sample in decode_samples:
            if len(sample.constraints(only_broken=True)) == 0:
                success_num += 1
        result_list.append(success_num)
        min_energy_list.append(np.min(sampleset.energies))
        mean_energy_list.append(np.mean(sampleset.energies))
        max_energy_list.append(np.max(sampleset.energies))

    result_list_percent = [i / parameter.config["num_reads"] for i in result_list]
    

    make_plot(
        [result_list_percent],
        base_test,
        parameter.config["output"]["base_test"],
        ["solution rate"],
        x_label="base",
        y_label="solution rate"
    )
    make_plot(
        [min_energy_list, mean_energy_list, max_energy_list],
        base_test,
        parameter.config["output"]["enegry"],
        ["min", "mean", "max"],
        x_label="base",
        y_label="enegry"
    )
    


if __name__ == "__main__":
    main()