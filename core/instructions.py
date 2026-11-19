import json
import pathlib

from rewardgym.render.stimuli import fixation_cross, posner_cue, posner_target
from rewardgym.render.routines.passive_routines import InstructionRoutine
from rewardgym.render.stimulus_definitions import ImageDefinition, TextDefinition

instructions_path = (
    pathlib.Path(__file__).parent.resolve() / "assets" / "instructions_en.json"
)
instructions = json.loads(instructions_path.read_text())


def get_instructions(instructions=instructions):

    fix = fixation_cross()
    cue_left = posner_cue(left=True)
    cue_right = posner_cue(left=False)
    pt_true = posner_target(target=True)
    pt_false = posner_target(target=False)

    slide_0 = InstructionRoutine(
        name="slide-1",
        stimulus_definitions=[
            TextDefinition(
                name="text1",
                text=instructions["0.0"],
                height=28,
                pos=(0, 200)
            ),
            ImageDefinition(
                name="image1",
                image=fix,
                size=fix.shape[:2]
            )
        ]
    )

    slide_1 = InstructionRoutine(
        name="slide2",
        stimulus_definitions=[
        TextDefinition(
            name="1",
            text=instructions["1.0"],
            height=28,
            pos=(0, 250),
        ),
        ImageDefinition(
            name="2",
            image=cue_left,
            pos=(-200, 0)
        ),
        ImageDefinition(
            name="3",
            image=cue_right,
            pos=(200, 0)
        ),
        ]
    )

    slide_2 = InstructionRoutine(
        name="slide2",
        stimulus_definitions=[
            ImageDefinition(
                pos=(-300, 100),
                image=pt_true,
                name="a"
            ),
            ImageDefinition(
                pos=(300, 100),
                image=pt_true[::-1],
                name="b"
            ),
            ImageDefinition(
                pos=(0, -125),
                image=pt_false,
                name="c"
            ),
            TextDefinition(
                text=instructions["2.0"],
                height=28,
                pos=(0, 250),
                name="d",
            ),
            TextDefinition(
                text=instructions["2.1"],
                height=28,
                pos=(0, -10),
                name="e"
            ),
            TextDefinition(
                text=instructions["2.2"],
                height=28,
                pos=(0, -250),
                name="f"
            )
        ]
    )

    slide_3 = InstructionRoutine(
        name="slide3",
        stimulus_definitions=[
            TextDefinition(
                text=instructions["3.0"],
                height=28,
                pos=(0,0),
                name="a",
            )
        ]
    )
    slide_3 = InstructionRoutine(
        name="slide4",
        stimulus_definitions=[
            TextDefinition(
                text=instructions["4.0"],
                height=28,
                pos=(0,0),
                name="a",
                alignText="center"
            )
        ]
    )

    return [slide_0, slide_1, slide_2, slide_3], instructions
