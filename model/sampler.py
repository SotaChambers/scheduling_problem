from openjij import SQASampler
from dwave.system import DWaveSampler, EmbeddingComposite

from utils.utils import load_yaml

def select_sampler(algorithm):
    if algorithm == "SQA":
        sampler = SQASampler()
    elif algorithm == "QA":
        credential_cfg = load_yaml("config/d-wave_credential.yml")
        token = credential_cfg["TOKEN"]
        endpoint = credential_cfg["ENDPOINT"]
        # ソルバーの定義
        dw_sampler = DWaveSampler(
            solver="DW_2000Q_6",
            token=token,
            endpoint=endpoint
        )
        sampler = EmbeddingComposite(dw_sampler)
    else:
        raise NotImplementedError("only SQA and QA are supported")
    return sampler