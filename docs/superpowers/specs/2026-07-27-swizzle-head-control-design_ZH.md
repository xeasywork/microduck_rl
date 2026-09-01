# 设计：Swizzle 头部控制

> 对应英文原文：[`2026-07-27-swizzle-head-control-design.md`](2026-07-27-swizzle-head-control-design.md)

## 目标

让 swizzle 滑行策略在保持平衡和步态的同时响应头部姿态命令，运行端可用按键或 API 控制头部。

## 选定方案

采用方案 A：策略通过 61 维观测中的 4 维 head command 自己管理头部，不在策略输出之后额外叠加关节偏移。

## 环境修改

- 在 swizzle cfg 中启用 head-pose command；
- actor/critic 观测保留正确命令顺序；
- 增加头部姿态跟踪奖励；
- 对命令加入合理范围、重采样和噪声；
- 确保继承的 neck neutral 奖励不会抵消命令。

## 运行端

运行端把 head target 写入命令块。不能同时 post-hoc 添加同一偏移，否则头部会移动两倍。

## 测试

验证观测仍为 61 维、命令存在、奖励引用正确关节、零命令保持中性。play 中分别测试 pitch/yaw/roll 极值和滑行稳定性。

