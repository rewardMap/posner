try:
    from ....pygame_render import BaseText, BaseDisplay, feedback_block, BaseAction
except ImportError:
    from rewardgym.pygame_render import (
        BaseText,
        BaseDisplay,
        feedback_block,
        BaseAction,
    )


def get_pygame_info(action_map, window_size=256):
    base_position = (window_size // 2, window_size // 2)

    final_display = BaseText("+", 500, textposition=base_position)
    base_position = (window_size // 2, window_size // 2)
    left_position = (window_size // 2 - window_size // 4, window_size // 2)
    right_position = (window_size // 2 + window_size // 4, window_size // 2)

    reward_disp, earnings_text = feedback_block(base_position)

    def first_step(img1, pos):
        return [
            BaseDisplay(None, 1),
            BaseText("+", 1000, textposition=base_position),
            BaseDisplay(None, 1),
            BaseText(img1, 500, textposition=base_position),
            BaseDisplay(None, 1),
            BaseText("x", 500, textposition=pos),
            BaseAction(),
        ]

    final_display = [
        BaseDisplay(None, 1),
        reward_disp,
        earnings_text,
    ]

    pygame_dict = {
        0: {"pygame": first_step("<", left_position)},
        1: {"pygame": first_step("<", right_position)},
        2: {"pygame": first_step(">", left_position)},
        3: {"pygame": first_step(">", right_position)},
        4: {"pygame": final_display},
        5: {"pygame": final_display},
    }

    return pygame_dict
