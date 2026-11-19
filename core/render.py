from rewardgym.render import ImageDefinition
from rewardgym.render.routines import (
    DynamicRoutine,
    FeedBackRoutine,
    PresentationRoutine,
)
from rewardgym.render.routines import ActionRoutine, AutoAction
from rewardgym.render.stimuli import fixation_cross, posner_cue, posner_target


def get_render_info(
    random_state=111,
    key_dict=None,
    external_stimuli=None,
    fullpoints=None,
    **kwargs,
):

    if key_dict is None:
        key_dict = {"left": 0, "right": 1}
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
            AutoAction(
                name="auto-transition",
                key_dict={"space": 0},
                rl_label="action",
            )
        ]

    def flip_horizontal_callback(routine, context):
        routine.draw_list = []
        probability = 0.5
        flip = context.env_context.random_state.random() < probability

        for ii in routine.stimuli:
            if hasattr(ii, "flip"):
                ii.flip = [False, flip]

            routine.draw_list.append(ii)

        return {"extra_infos": {"misc": f"flip-{flip}"}}

    def unflip(routine, context, state):
        for ii in routine.stimuli:
            if hasattr(ii, "flip"):
                ii.flip = [False, False]


    def second_step(img1, img2, image_shift):
        return [
            PresentationRoutine(name="second-stage", duration=None, flip=False, rl_label="reward"),
            DynamicRoutine(
                duration=0.35,
                name="target",
                stimulus_definitions=[
                    ImageDefinition(
                        name="img-left",
                        pos=(-image_shift, 0),
                        image=img1
                    ),
                    ImageDefinition(
                        name="img-right",
                        pos=(image_shift, 0),
                        image=img2
                    )
                ],
                rl_label="obs",
                callback_before_draw=flip_horizontal_callback,
                callback_after_draw=unflip
            ),
            ActionRoutine(
                duration=2.0,
                key_dict=key_dict,
                name="response",
                timeout_action=None,
                rl_label="action",
            )
        ]

    final_step = [
        reward_feedback,
        PresentationRoutine(
            stimulus_definitions=[
                ImageDefinition(
                    image=fixation_cross(),
                    name="fix",
                    pos=(0, 0)
                )
            ],
            duration=0.4, name="iti",
            rl_label="obs",
        ),
    ]

    info_dict = {
        0: {"render": []},
        1: {"render": first_step(posner_cue(left=True))},
        2: {"render": first_step(posner_cue(left=False))},
        3: {
            "render": second_step(
                posner_target(target=True),
                posner_target(target=False),
                image_shift=550,
            )
        },
        4: {
            "render": second_step(
                posner_target(target=False),
                posner_target(target=True),
                image_shift=550,
            )
        },
        5: {"render": final_step},
        6: {"render": final_step},
    }

    return info_dict, None
