# 踢球姿态跟踪任务实施计划

> 对应英文/法文原文：[`2026-07-24-shoot-pose-following.md`](2026-07-24-shoot-pose-following.md)

> 文档记录的是 TDD 实施顺序和早期参数，当前实现可能不同。

## 全局约束和文件

新增 shoot env cfg、任务注册、`mdp.py` phase/pose 函数和测试。保持 61 维观测、14 动作、actor 不看球以及 all-collision 模型。

## Task 1：phase 随机化

扩展 phase command，使训练可从动作任意阶段 reset，play 可固定从起点开始。测试范围、批量 env 和关闭随机化。

## Task 2：`kick_pose_target`

实现 STAND、BACK、FORWARD、RECOVER 等姿态的分段插值。右腿为示例踢腿，左腿支撑；placeholder 最终需真机标定。

## Task 3：姿态 reward

实现 pose L2/L1 reward 和 helper，按名称选择 14 舵机。测试误差、phase 边界、左右腿和符号。

## Task 4：环境配置

加入球、reset、phase、姿态、球位移和支撑奖励；删除冲突继承项。平滑权重比慢速 ground-pick 更轻，允许快速出脚。

## Task 5：注册和集成测试

注册 `Mjlab-BallKick-Flat-MicroDuck` 类任务，测试环境构建、obs 61、球 asset、reward、终止和 PPO experiment。

## 实施后工作

64 env smoke 后进行长训，用视频验证不是摔倒撞球。调整姿态、球位置、支撑、速度和正则，再导出 ONNX 与真机增益测试。

