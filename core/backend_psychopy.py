from rewardgym.psychopy_render import (
    FeedBackStimulus,
    ImageStimulus,
    StimuliWithResponse,
    ActionStimulus,
    BaseStimulus
)
from rewardgym.stimuli import fixation_cross, posner_cue, posner_target
from rewardgym.render.passive_routines import PresentationRoutine, FeedBackRoutine
from rewardgym.render import ImageDefinition


def get_psychopy_info(
    random_state=111,
    key_dict={"left": 0, "right": 1},
    external_stimuli=None,
    fullpoints=None,
    **kwargs,
):

    reward_feedback = FeedBackRoutine(
        duration=1.0, name="reward", bar_total=fullpoints, rl_label="reward"
    )

    fix = PresentationRoutine(
        stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=True)], duration=0.5, name="fixation"
    )

    fix_isi = PresentationRoutine(
                stimulus_definitions=[ImageDefinition(image=fixation_cross(), name="fixation", autoDraw=True)],
                duration=0.4, name="isi"
    )

    def first_step(img):
        return [
            fix,
            PresentationRoutine(
                stimulus_definitions=[ImageDefinition(
                    image=img,
                    pos=(0, 0),
                    name="cue",
                )],
                duration=0.4,
                name="cue",
                rl_label="obs",
            ),
            fix_isi,
            ActionStimulus(
                duration=0.0,
                key_dict={"space": 0},
                timeout_action=0,
                name="dummy",
                name_timeout="dummy",
                rl_label="action",
            ),
        ]

    def second_step(img1, img2, image_shift, to=1):
        return [
            BaseStimulus(name="second-stage", duration=None, flip=False, rl_label="reward"),
            StimuliWithResponse(
                duration=2.0,
                key_dict=key_dict,
                name="response",
                target_name="target",
                target_duration=0.35,
                timeout_action=None,
                positions=((-image_shift, 0), (image_shift, 0)),
                images=[img1, img2],
                flip_probability=0.5,
                random_state=random_state,
                rl_label="action",
                target_rl_label="obs",
            )
        ]

    final_step = [
        reward_feedback,
        ImageStimulus(
            image_paths=[fixation_cross()], duration=0.4, name="iti", autodraw=False,
            rl_label="obs",
        ),
    ]

    info_dict = {
        0: {"psychopy": []},
        1: {"psychopy": first_step(posner_cue(left=True))},
        2: {"psychopy": first_step(posner_cue(left=False))},
        3: {
            "psychopy": second_step(
                posner_target(target=True),
                posner_target(target=False),
                image_shift=550,
                to=None,
            )
        },
        4: {
            "psychopy": second_step(
                posner_target(target=False),
                posner_target(target=True),
                image_shift=550,
                to=None,
            )
        },
        5: {"psychopy": final_step},
        6: {"psychopy": final_step},
    }

    return info_dict, None
