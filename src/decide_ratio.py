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


def make_heatmap(map, axis_list, save_path):
    fig = plt.figure(figsize=(14, 14))
    sns.heatmap(map, annot=True)
    plt.xticks([i+0.5 for i in range(len(axis_list))], axis_list)
    plt.yticks([i+0.5 for i in range(len(axis_list))], axis_list)
    plt.xlabel("w_group")
    plt.ylabel("w_desire")
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

    test_case = [i * 0.5 for i in range(1, 20)]
    test_num = len(test_case)
    result_map = np.zeros(shape=(test_num, test_num))

    for w_desire in range(test_num):
        for w_group in range(test_num):
            feed_dict = {"w_desire": test_case[w_desire], "w_group": test_case[w_group]}
            qubo, offset = model.to_qubo(feed_dict=feed_dict)

            sampler = select_sampler(parameter.config["algorithm"])
            sampleset = sampler.sample_qubo(qubo, num_reads=parameter.config["num_reads"])

            decode_samples = model.decode_sampleset(sampleset=sampleset, feed_dict=feed_dict)
            success_num = 0
            for sample in decode_samples:
                if len(sample.constraints(only_broken=True)) == 0:
                    success_num += 1
            result_map[w_desire, w_group] = success_num

    result_map_percent = result_map / parameter.config["num_reads"]

    make_heatmap(result_map_percent, test_case, parameter.config["output"]["coeff_test"])


if __name__ == "__main__":
    main()