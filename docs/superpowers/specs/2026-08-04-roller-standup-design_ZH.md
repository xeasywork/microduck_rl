# 设计：`roller_standup` 穿滑轮起身

> 对应英文/法文原文：[`2026-08-04-roller-standup-design.md`](2026-08-04-roller-standup-design.md)

## 已确定方向

创建独立起身策略，从带轮 all-collision 模型的正趴/仰躺状态恢复到轮上站立。复用普通 standup 的核心结构，但不能照搬关节索引和摩擦课程。

## 架构

从 roller env 派生 BAM、观测和 DR，删除滑行速度、feet-flat 等与起身冲突的奖励。命令保持中性，注册独立任务、PPO experiment 和测试。

## 实测常量

站立、趴地和仰躺高度由当前碰撞几何实测。目标高度需要考虑负载下压缩，模型改变后重测。

## 关节索引

被动轮关节交错在左右腿和头部之间。所有 reward 按名称解析，并由测试锁定实际 joint id。无轮模型的固定索引在这里错误。

## 奖励

删除 roller locomotion 的速度、feet-flat、髋部中性和旧 pose 高度项；保留通用平滑、能量、碰撞和 sim2real 项；加入躯干高度、upright、站立姿态和完成保持。

## 观测和命令

actor 仍为 61 维，排除被动轮。命令槽补零，不给策略添加部署端不存在的信息。

## Reset

正趴和仰躺混合，随机 orientation、关节和物理；移除 `fell_over` 终止。可使用 reverse curriculum 从部分起身姿态开始。

## 摩擦课程

轮子是难点：早期使用较高滚动阻力帮助发现起身，之后逐步降低到真实范围。课程方向与普通滑行训练相反。

## PPO、测试和风险

网络与 standup 相近。测试高度、索引、奖励删除、终止和 reset；GPU smoke 后再长训。风险是轮子滑走、头部暴力支撑、目标高度错误和过早正则冻结策略。

