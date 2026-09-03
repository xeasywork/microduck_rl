# Pet Motion Training Task

`Mjlab-PetMotion-Flat-MicroDuck` preserves the shared 61-dimensional observation interface while training calm full-body command following. It reuses the proven walking task's BAM actuator, observation noise, delays, domain randomization, disturbance recovery, and NaN guard, then narrows locomotion speeds and increases body-pose and smoothness rewards.

The policy supplies low-speed forward/reverse motion, stable left/right body lean, and a small crouch/rise range. Runtime composite behaviors use them as follows:

- `approach_person`: external vision/ToF supplies direction and distance before every short motion segment;
- `shy_retreat`: a short low-speed reverse segment followed by another observation;
- `nuzzle_left/right`: stop walking, then command a lateral body offset and roll near a safe distance;
- `happy_bounce`: command a small crouch, rise, and return to neutral without optimizing for jump height.

Person position and contact force are not policy observations. App/Brain owns person localization; duck-side ToF, IMU, and control timeout own the final stop. MicroDuck has no touch or pressure sensor, so a nuzzle cannot be interpreted as sensing petting.

Run the configuration test and the required low-cost smoke training before a long run:

```bash
uv run --with pytest pytest tests/test_pet_motion_cfg.py
uv run train Mjlab-PetMotion-Flat-MicroDuck --env.scene.num-envs 64 --agent.max_iterations 5
```

After the smoke succeeds, train and export only through the repository script so the observation normalizer is embedded in ONNX:

```bash
uv run train Mjlab-PetMotion-Flat-MicroDuck --env.scene.num-envs 4096
uv run scripts/export.py Mjlab-PetMotion-Flat-MicroDuck --wandb-run-path <entity/project/run_id>
uv run scripts/infer_policy.py --walking out.onnx
```

Do not set `hardware_ready` until the exported policy passes MuJoCo disturbance recovery, domain-randomization regression, CPU deployment rehearsal, and hardware-in-the-loop tests.
