# Spin 环境实施计划

> 对应英文原文：[`2026-08-04-spin-env.md`](2026-08-04-spin-env.md)

> 这是包含大量测试草案的历史实施计划，当前参数以源码为准。

## 全局约束

使用滑轮模型、统一 61 维观测和 14 动作。旋转方向固定时禁用左右镜像 symmetry；轮子按被动关节处理；phase 与部署端一致。

## Task 1：phase 包络

实现 4 秒梯形 yaw-rate 目标：加速约 0.5 s、恒速约 1.6 s、制动约 0.5 s、休息约 1.4 s。纯函数测试边界、连续、回绕和积分转角。

## Task 2：旋转和原地 reward

实现 yaw-rate tracking、L1 变体、平移惩罚和 recover 阶段。使用 fake env 验证包装、符号和 batch，不把高 yaw rate 错当姿态失败。

## Task 3：差动种子

奖励左右轮/腿差动和持续接地，为 PPO 提供可发现的物理方向。避免直接指定动作序列，让策略仍能适应随机化。

## Task 4：腿部剪切和头部

加入左右腿反对称 reward。颈部大多保持中性，但允许 head yaw 作为角动量工具。扩展 neck reward 的 pattern 参数并测试选择。

## Task 5：环境和注册

从 roller crouch/roller 基础继承 DR 和观测，允许静止或低速进入。删除速度命令 reward，加入 phase、spin reward、终止、PPO 和 registry。禁用 symmetry。

## Task 6：仿真验证

先 smoke，再进行短校准和长训。观察 yaw-rate、累计角度、x/y 漂移、制动、跌倒和视频。若策略绕圈，应提高 stay-in-place；若不启动，调整差动种子和目标尺度。

## 诊断记录

初始 500 iteration 表现用于估算角速度尺度与 reward 比例，这些是推导结果而非直接传感器测量。修改后重新做 smoke，不能直接沿用旧曲线结论。

