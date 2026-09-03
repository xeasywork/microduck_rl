"""Calm full-body command training for MicroDuck pet interactions.

One 61D-compatible policy learns low-speed approach/retreat while tracking
head and body pose commands. Runtime composite behaviors choose command
sequences for approach, a left/right nuzzle lean, and a small excitement bob;
person distance remains an external perception/safety concern and is not part
of the policy observation.
"""

from copy import deepcopy

from mjlab.envs import ManagerBasedRlEnvCfg

from mjlab_microduck.tasks import mdp as microduck_mdp
from mjlab_microduck.tasks.microduck_velocity_env_cfg import (
    MicroduckRlCfg,
    make_microduck_velocity_env_cfg,
)


def make_microduck_pet_motion_env_cfg(
    play: bool = False,
    rough: bool = False,
) -> ManagerBasedRlEnvCfg:
    """Create the calm command-following policy used by pet behaviors."""

    cfg = make_microduck_velocity_env_cfg(play=play, rough=rough)

    twist = cfg.commands["twist"]
    twist.ranges.lin_vel_x = (-0.16, 0.22)
    twist.ranges.lin_vel_y = (-0.12, 0.12)
    twist.ranges.ang_vel_z = (-0.50, 0.50)
    twist.rel_standing_envs = 0.35
    twist.rel_turn_in_place_envs = 0.10

    # Keep a large stationary bucket: nuzzle/head gestures must be stable
    # without stepping, while the non-zero bucket still trains approach/retreat.
    cfg.curriculum["standing_envs"].params["standing_stages"] = [
        {"step": 0, "rel_standing_envs": 0.35},
    ]

    body_ranges = (
        (-0.012, 0.012),  # trunk fore/aft relative to support polygon
        (-0.018, 0.018),  # left/right lean for nuzzle commands
        (-0.012, 0.018),  # gentle crouch/rise for excitement bob
        (-0.16, 0.16),  # roll
        (-0.12, 0.12),  # pitch
        (-0.12, 0.12),  # yaw relative to feet
    )
    cfg.commands["body_pose"].ranges = body_ranges
    cfg.curriculum["body_pose_range"].params["range_stages"] = [
        {
            "step": 0,
            "ranges": tuple((low * 0.25, high * 0.25) for low, high in body_ranges),
        },
        {
            "step": 600 * 24,
            "ranges": tuple((low * 0.60, high * 0.60) for low, high in body_ranges),
        },
        {"step": 1200 * 24, "ranges": body_ranges},
    ]

    cfg.rewards["body_pose_tracking"].func = microduck_mdp.body_pose_tracking_locomotion
    cfg.rewards["body_pose_tracking"].weight = 2.5
    cfg.rewards["body_pose_tracking"].params = {
        "command_name": "body_pose",
        "nominal_height": 0.105,
        "xy_std": 0.025,
        "z_std": 0.025,
        "angle_std": 0.25,
        "axis_weights": (0.7, 1.0, 1.0, 1.0, 0.8, 0.6),
        "vel_gate_command_name": None,
    }

    # Pet motions favor smoothness and planted feet over peak travel speed.
    cfg.rewards["foot_slip"].weight = -0.25
    cfg.rewards["action_rate_l2"].weight = -0.20
    cfg.curriculum["action_rate_weight"].params["weight_stages"] = [
        {"step": 0, "weight": -0.20},
        {"step": 600 * 24, "weight": -0.50},
        {"step": 1200 * 24, "weight": -0.90},
        {"step": 1800 * 24, "weight": -1.20},
    ]

    return cfg


MicroduckPetMotionRlCfg = deepcopy(MicroduckRlCfg)
MicroduckPetMotionRlCfg.experiment_name = "microduck_pet_motion"
MicroduckPetMotionRlCfg.run_name = "pet_motion"
MicroduckPetMotionRlCfg.max_iterations = 6000
