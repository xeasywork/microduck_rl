from mjlab_microduck.tasks import mdp as microduck_mdp
from mjlab_microduck.tasks.microduck_pet_motion_env_cfg import (
    MicroduckPetMotionRlCfg,
    make_microduck_pet_motion_env_cfg,
)


def test_pet_motion_keeps_shared_command_layout_and_safe_training_stack():
    cfg = make_microduck_pet_motion_env_cfg()

    assert tuple(cfg.commands) == ("twist", "head_pose", "body_pose")
    assert len(cfg.commands["head_pose"].ranges) == 4
    assert len(cfg.commands["body_pose"].ranges) == 6
    assert cfg.commands["twist"].rel_standing_envs == 0.35
    assert (
        cfg.rewards["body_pose_tracking"].func
        is microduck_mdp.body_pose_tracking_locomotion
    )
    assert cfg.rewards["body_pose_tracking"].weight > 0
    assert cfg.rewards["foot_slip"].weight < 0
    assert cfg.rewards["action_rate_l2"].weight < 0
    assert "expand_bam_friction_fields" in cfg.events
    assert "nan_state" in cfg.terminations


def test_pet_motion_play_and_rough_variants_build():
    assert (
        make_microduck_pet_motion_env_cfg(play=True).scene.terrain.terrain_type
        == "plane"
    )
    assert (
        make_microduck_pet_motion_env_cfg(rough=True).scene.terrain.terrain_type
        == "generator"
    )
    assert MicroduckPetMotionRlCfg.experiment_name == "microduck_pet_motion"
