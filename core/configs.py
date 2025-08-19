try:
    from rewardgym.utils import check_random_state
    from rewardgym.tasks.utils import check_conditions_not_following
except ImportError:
    from ....utils import check_random_state
    from ...utils import check_conditions_not_following


def get_configs(stimulus_set: str = "1"):
    random_state = check_random_state(int(stimulus_set))

    condition_dict = {
        "cue-left-target-left": {0: {0: 1}, 1: {0: 3}},
        "cue-left-target-right": {0: {0: 1}, 1: {0: 4}},
        "cue-right-target-right": {0: {0: 2}, 2: {0: 4}},
        "cue-right-target-left": {0: {0: 2}, 2: {0: 3}},
    }

    # 20 trials in each condition template
    condition_template_80_20 = (
        ["cue-left-target-left"] * 8
        + ["cue-left-target-right"] * 2
        + ["cue-right-target-right"] * 8
        + ["cue-right-target-left"] * 2
    )

    condition_template_90_10 = (
        ["cue-left-target-left"] * 9
        + ["cue-left-target-right"] * 1
        + ["cue-right-target-right"] * 9
        + ["cue-right-target-left"] * 1
    )

    condition_template_70_30 = (
        ["cue-left-target-left"] * 7
        + ["cue-left-target-right"] * 3
        + ["cue-right-target-right"] * 7
        + ["cue-right-target-left"] * 3
    )

    condition_template_60_40 = (
        ["cue-left-target-left"] * 6
        + ["cue-left-target-right"] * 4
        + ["cue-right-target-right"] * 6
        + ["cue-right-target-left"] * 4
    )

    iti_template = [0.5, 0.75, 1.0, 1.25] * 10
    isi_template = [0.4, 0.6] * 20

    n_blocks_condition = 4

    condition_template_sets = random_state.choice(
        [
            condition_template_60_40 * 2,
            condition_template_70_30 * 2,
            condition_template_80_20 * 2,
            condition_template_90_10 * 2,
        ],
        size=n_blocks_condition,
        replace=False,
    )

    dont_follow = ["cue-left-target-right", "cue-right-target-left"]

    conditions, isi, iti = [], [], []

    for cn in range(n_blocks_condition):
        reject = True

        while reject:
            condition_template = random_state.choice(
                a=condition_template_sets[cn], size=40, replace=False
            ).tolist()

            check = check_conditions_not_following(condition_template, dont_follow, 1)

            if check and (
                len(conditions) == 0 or conditions[-1] != condition_template[0]
            ):
                conditions.extend(condition_template)
                isi.extend(random_state.permutation(isi_template).tolist())
                iti.extend(random_state.permutation(iti_template).tolist())
                reject = False

    config = {
        "name": "posner",
        "stimulus_set": stimulus_set,
        "isi": isi,
        "iti": iti,
        "condition": conditions,
        "condition_dict": condition_dict,
        "ntrials": len(conditions),
        "update": ["isi", "iti"],
        "add_remainder": True,
        "breakpoints": [79],
        "break_duration": 45,
    }

    return config
