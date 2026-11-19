import pathlib
from typing import Literal

import numpy as np

from rewardgym import check_random_state
from rewardgym.reward_classes import BaseReward
from rewardgym.tasks.yaml_tools import load_task_from_yaml
from rewardgym.runner.plugins import AddRemainder

def get_task(
    render_backend: Literal["pygame", "psychopy"] | None = None,
    random_state: int | np.random.Generator = 1000,
    key_dict=None,
    **kwargs,
):
    random_state = check_random_state(random_state)
    yaml_file = pathlib.Path(__file__).parents[1].resolve() / "task.yaml"
    info_dict, environment_graph = load_task_from_yaml(yaml_file)

    reward_structure = {
        5: BaseReward([1]),
        6: BaseReward([0]),
    }

    info_dict.update(
        {
            "position": {
                0: "selection",
                1: "cue-left",
                2: "cue-right",
                3: "target-left",
                4: "target-right",
                5: "win",
                6: "lose",
            }
        }
    )


    if render_backend is not None:
        from .render import get_render_info

        if key_dict is None:
            key_dict = {"left": 0, "right": 1}

        render_dict, _ = get_render_info(
            random_state=random_state, key_dict=key_dict, fullpoints=info_dict["meta"]["fullpoints"]
        )
        info_dict.update(render_dict)

    info_dict.update({"plugins": {"post-trial": [AddRemainder()]}})

    return environment_graph, reward_structure, info_dict
