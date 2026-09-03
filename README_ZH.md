# Microduck RL

> 对应英文原文：[`README.md`](README.md)

本仓库为 Microduck 提供强化学习环境，基于 mjlab、MuJoCo Warp 和 PPO。策略以 50 Hz 训练，导出 ONNX 后由相邻 `microduck` 运行仓库部署到真机。

训练重点不是只在仿真中表现好，而是通过 BAM 舵机模型、延迟、摩擦、质量、电池和齿隙随机化缩小 sim2real 差距。

## 快速开始

本地训练需要 CUDA GPU 和 `uv`：

```bash
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096
```

观看 W&B 训练结果：

```bash
uv run play Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <entity/project/run_id>
```

导出 ONNX：

```bash
uv run scripts/export.py Mjlab-Velocity-Flat-MicroDuck --wandb-run-path <...>
```

CPU MuJoCo 键盘推理：

```bash
uv run scripts/infer_policy.py --walking output.onnx
```

从 checkpoint 继续训练：

```bash
uv run train <TASK_ID> --env.scene.num-envs 4096 \
  --agent.load-checkpoint model_29999.pt --agent.resume True
```

没有 CUDA 时在训练命令末尾加入 `--hf-jobs`，提交到 Hugging Face Jobs。

## 任务

| 任务族 | 作用 |
|---|---|
| `Velocity` | 平地/崎岖地形速度跟踪和头部命令 |
| `VelStand` | 行走、跌倒恢复和身体姿态 |
| `StandUp` | 从正趴、仰躺或坐姿起身 |
| `SitStand` | 命令式坐下与站起 |
| `GroundPick` | 嘴部接触地面再恢复站立 |
| `BallKick` | 固定区域球的踢击，actor 看不到球 |
| `Roulade` | 前滚翻并回到双脚 |
| `PetMotion` | 低速靠近/后退、左右贴近倾斜和兴奋起伏命令 |
| `Velocity ... Rollers` | 被动轮滑移动 |
| `Swizzle` | 对称 swizzle 滑行 |
| `RollerCrouch` | 滑行中下蹲 |
| `RollerSlope` | 斜坡被动下滑 |
| `RollerStandUp` | 穿滑轮起身 |
| `Spin` | 滑轮原地快速旋转 |

使用 `uv run list-envs` 查看实际注册表。

## Backlash 版本

主要任务都有 `-Backlash-` 变体，在 14 个舵机关节串联 ±1° 齿隙。编码器、BAM 反馈和观测从齿隙输出侧读取，保持 61 维观测和 14 维动作不变。

## 舵机模型

任务使用 BAM 的 XL330 电压控制模型，包括反电动势、摩擦、电池压降、命令延迟和 per-env 随机化。理想 PD 模型对这种小型机器人不足以支持可靠 sim2real。

## 机器人模型

- `robot_walk.xml`：行走与 PetMotion 模型，减少躯干/头部碰撞。
- `robot_allcollisions.xml`：起身、坐站、捡拾、踢球和翻滚。
- `robot_allcollisions_rollers.xml`：滑轮任务。
- `*_backlash.xml`：齿隙版本。

## 关键约定

- actor 观测固定 61 维：48 本体 + 13 命令。
- 未使用命令槽补零，不能删除。
- 被动关节统一以 `passive_` 开头。
- ONNX 必须由 `scripts/export.py` 导出，归一化器要写进图。
- 14 舵机顺序保持统一，嘴部不在策略中。

## 测试

```bash
uv run --with pytest pytest tests/
```

CPU 测试锁定关节映射、奖励符号、配置不变量和 NaN 保护。
