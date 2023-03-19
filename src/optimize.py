import numpy as np
from pyqubo import Array, Constraint, Placeholder, Binary
from openjij import SQASampler
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
from loguru import logger
import time

from utils.utils import load_yaml
from utils.stop_watch import stop_watch
from model.model import QuboModel
from src.common.setting_parameter import Parameter
from model.sampler import select_sampler


def make_schedule(data, save_path, x_label, y_label, no_d, no_t, A, D, T):
    fig = plt.figure(figsize=(15, 15))
    plt.xticks([i for i in range(no_d * no_t)], [f"{d}_{t}" for d in D for t in T])
    plt.xlim(-2, no_d * no_t + 1)
    plt.xlabel(x_label)

    plt.yticks([0, 2, 4, 6, 8, 10], A)
    plt.ylim(-1, 12)
    plt.ylabel(y_label)

    plt.imshow(data, cmap="GnBu")

    for j in range(0, no_d * no_t + 1):
        plt.axvline(j - 0.5, ls="--", c="black", lw="1")
    fig.savefig(save_path)


@stop_watch
def main():
    # ======= logの設定
    dt_now = time.strftime("%Y%m%d_%H-%M-%S")
    logger.add(f"logs/{dt_now}.log", rotation="500MB")

    # ======= 問題の設定
    parameter = Parameter()

    w_desire = (
        parameter.config["coeff"]["w_desire"]["ratio"]
        * parameter.config["coeff"]["base"]
    )
    w_group = (
        parameter.config["coeff"]["w_group"]["ratio"]
        * parameter.config["coeff"]["base"]
    )

    qubo_model = QuboModel(
        parameter.A,
        parameter.D,
        parameter.T,
        parameter.S_dt,
        parameter.R_a,
        parameter.G_ga,
        parameter.r_adt,
    )
    model = qubo_model.create_model()
    feed_dict = {"w_desire": w_desire, "w_group": w_group}
    qubo, offset = model.to_qubo(feed_dict=feed_dict)

    logger.info(f"setting Sampler: Sampler = {parameter.config['algorithm']}")
    sampler = select_sampler(parameter.config["algorithm"])
    sampleset = sampler.sample_qubo(qubo, num_reads=parameter.config["num_reads"])

    energies = sampleset.energies

    decode_samples = model.decode_sampleset(sampleset=sampleset, feed_dict=feed_dict)
    pass_constraint = []
    for i, sample in enumerate(decode_samples):
        if len(sample.constraints(only_broken=True)) == 0:
            pass_constraint.append(i)

    # 制約が満たされた解で最もエネルギーが小さいsampleを抽出
    use_idx = pass_constraint[np.argmin(energies[pass_constraint])]
    logger.info(f"Min Enegry = {energies[use_idx]}, idx = {use_idx}")

    target_sample = sampleset.record[use_idx][0].reshape(
        parameter.no_a, parameter.no_d * parameter.no_t
    )
    base_schedule = np.zeros(
        shape=(parameter.no_a * 2 - 1, parameter.no_d * parameter.no_t)
    )
    for i, schedule in enumerate(target_sample):
        base_schedule[2 * i, :] = schedule

    make_schedule(
        base_schedule,
        parameter.config["output"]["schedule"],
        "日にちと各ターム",
        "作業員",
        parameter.no_d,
        parameter.no_t,
        parameter.A,
        parameter.D,
        parameter.T,
    )


if __name__ == "__main__":
    main()
