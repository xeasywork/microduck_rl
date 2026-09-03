# 宠物动作训练任务

`Mjlab-PetMotion-Flat-MicroDuck` 是一套保持 61 维观测协议不变的全身动作策略。它复用已经验证过的步态、BAM 执行器、观测噪声、延迟、域随机化和 NaN 防护，同时缩小移动速度，强化身体姿态跟踪和动作平滑。

这套策略提供三个底层能力：低速前进/后退、稳定的左右身体倾斜、轻微的下蹲/抬升。运行时复合行为据此组织：

- `approach_person`：外部视觉/ToF 每一步给出方向和距离，策略只执行短时低速移动；
- `shy_retreat`：执行短时低速后退，然后重新观察；
- `nuzzle_left/right`：停止走动后给出左右偏移和 roll 指令，靠近安全距离后保持；
- `happy_bounce`：按“轻微下蹲—抬升—回中”下发身体高度指令，不追求离地高度。

人物和接触力不进入策略观测。App/Brain 负责人物定位，鸭端 ToF、IMU 和控制超时负责停止；当前没有触摸或压力传感器，因此不能把贴近解释成检测到了抚摸。

先运行配置测试和低成本烟雾训练：

```bash
uv run --with pytest pytest tests/test_pet_motion_cfg.py
uv run train Mjlab-PetMotion-Flat-MicroDuck --env.scene.num-envs 64 --agent.max_iterations 5
```

烟雾训练通过后再启动长训练。只能使用仓库的导出脚本，以确保观测归一化器写入 ONNX：

```bash
uv run train Mjlab-PetMotion-Flat-MicroDuck --env.scene.num-envs 4096
uv run scripts/export.py Mjlab-PetMotion-Flat-MicroDuck --wandb-run-path <entity/project/run_id>
uv run scripts/infer_policy.py --walking out.onnx
```

新的 ONNX 在完成 MuJoCo 扰动恢复、域随机化回归、CPU 推理演练和真鸭硬件在环测试之前，不得标记为 `hardware_ready`。
