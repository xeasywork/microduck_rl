# Roller StandUp 实施计划

> 对应英文/法文原文：[`2026-08-04-roller-standup.md`](2026-08-04-roller-standup.md)

> 这是详细历史计划，包含代码草案与当时测量。当前真值以源码、测试和策略总结为准。

## 全局约束

- 使用带轮 all-collision 模型；
- actor 61 维、动作 14 维；
- 被动轮按名称排除；
- 起点在地面，不能保留 `fell_over`；
- 目标高度必须实测；
- 先 TDD，再 GPU。

## 文件结构

新增 roller standup env cfg、cfg/reward/reset 测试、任务注册和交接总结。复用 standup MDP 函数，但 remap 关节和物理。

## Task 1：环境骨架

从 roller env 继承 BAM、观测和 DR，命令中性化，删除速度、feet-flat、髋中性和其他滑行 reward。加入独立 PPO 配置和任务 ID。

文档记录的带轮模型实际 joint 顺序显示四个被动轮交错在 14 舵机之间；测试必须锁定。

## Task 2：起身奖励

移植躯干高度、upright、姿态、完成保持等 standup reward，所有 joint selection 按名称。测试 reward 符号、gate、目标高度和正趴/仰躺样本。

## Task 3：地面 reset

混合正趴、仰躺和部分起身状态；随机姿态、关节和噪声；删除正常步态的跌倒终止。reverse curriculum 保证后半段技能从早期就有样本。

## Task 4：课程

早期提高滚动阻力，帮助策略找到支点；随后降低到真实摩擦。逐步加入推动、动作速率、冲击和更宽 DR，避免初期正则冻结。

## Task 5：GPU 与交接

先 64 env、5 iteration smoke，再正式训练。play 要分别强制正趴和仰躺。记录实测高度、关节映射、课程、失败模式和部署命令。

## 计划后的真机经验

策略可能用头部暴力支撑。直接加入很强头部冲击惩罚曾使策略完全不动，应改成阈值/gate/后期课程，并由硬性真机电流限制兜底。

