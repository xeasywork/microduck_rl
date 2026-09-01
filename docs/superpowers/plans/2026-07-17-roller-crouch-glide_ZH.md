# Roller Crouch-Glide 实施计划

> 对应英文/法文原文：[`2026-07-17-roller-crouch-glide.md`](2026-07-17-roller-crouch-glide.md)

> 这是带日期的实施记录。代码可能已继续演进；当前事实以源码和测试为准。

## 全局约束

- 保持 actor 61 维、动作 14 维；
- 复用 roller 模型、BAM、观测和 DR；
- 被动轮按名称排除；
- phase 和运行端严格一致；
- 先测试纯函数，再建立完整环境。

## 文件结构

计划涉及 `tasks/mdp.py`、`microduck_roller_crouch_env_cfg.py`、任务注册、测试、`infer_policy.py` 和导出/部署配置。

## Task 1：梯形高度目标

先为 phase → 目标高度编写纯函数和边界测试，覆盖下降、低位、上升、休息、周期回绕和错误参数。纯函数通过后再接入环境。

## Task 2：奖励

实现高度跟踪和前向速度奖励，使用最小 fake env 验证数值、符号和批量行为。增加防摔、接触和平滑项，并确认不会通过停下或坐地刷分。

## Task 3：环境和注册

从 roller env 继承物理和随机化，删除冲突奖励，加入 phase 命令、目标高度、任务专属 PPO 配置和 registry ID。测试观测宽度、被动轮排除、奖励权重和 play 配置。

## Task 4：Smoke run

```bash
uv run train Mjlab-RollerCrouch-Flat-MicroDuck \
  --env.scene.num-envs 64 --agent.max_iterations 5
```

检查构建、无 NaN、所有 reward 计算和 episode 正常结束。

## Task 5：正式训练和 Play

扩大到 4096 env，观察高度跟踪、速度保持和视频。若策略只会减速，应提高速度要求或随机进入速度；若动作过猛，后期逐步增加平滑正则。

## Task 6：ONNX 与部署

用 `scripts/export.py` 导出归一化 ONNX，在 roller 场景中以正确 CLI/按键和 phase 周期复现，再装入真机对应策略槽。

## 自检重点

测试不能只验证函数存在，还要锁定符号、命令布局、被动关节、运行端周期和导出形状。

