# 设计：按姿态序列踢球

> 对应英文/法文原文：[`2026-07-24-shoot-pose-following-design.md`](2026-07-24-shoot-pose-following-design.md)

## 目标

通过 phase 驱动的姿态序列训练稳定踢球：站立、蓄力、向前踢、收回。球用于奖励，actor 不观察球。

## 非目标

不做视觉找球、任意球位条件化、移动球预测或完整足球导航。

## 架构

新增 shoot env cfg、任务注册和 phase 命令。14 关节姿态初始为 placeholder，最终应通过真机 `read_pose.py` 或可靠 pose 编辑器标定。

## Phase、reset 和继承

phase 可随机化，reset 从稳定站姿开始，无额外前进动量。继承 all-collision 环境的 BAM、DR、观测和安全项，但删除与踢球冲突的旧奖励。

## 奖励

- 跟踪插值姿态；
- 支撑腿平衡和双脚/单脚合理接触；
- 踢脚速度和球向前位移；
- 限制躯干倾倒、横向漂移和过大冲击；
- 平滑正则比 ground-pick 更轻，允许快速 kick snap。

训练后曾发现直接迁移某些权重会压制踢腿，必须根据视频和 per-term reward 调整，而不是照搬。

## 观测和部署

保持 61 维输入，运行端产生相同 phase。球状态不进入 actor，因此上层负责把球放入有效区域。

## 测试和开放项

测试 phase 边界、姿态、传感器重命名、关节选择和 reward 符号。开放项包括最终姿态、踢球方向、冲击和真机增益。

