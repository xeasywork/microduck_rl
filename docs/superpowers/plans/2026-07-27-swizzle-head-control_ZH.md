# Swizzle 头部控制实施计划

> 对应英文原文：[`2026-07-27-swizzle-head-control.md`](2026-07-27-swizzle-head-control.md)

## 约束

只修改 swizzle 环境所需部分，保持 61 维观测、现有滑行行为和 runtime head command 语义。策略负责头部，运行端不再额外叠加。

## Task 1：接入 head-pose

1. 在测试中断言 head command 存在、actor/critic 观测维度和 reward 配置；
2. 修改 `make_microduck_velocity_swizzle_env_cfg` 启用命令；
3. 设置 head pitch/yaw/roll 范围和 resampling；
4. 增加头部跟踪 reward；
5. 删除或调整与命令冲突的 neck-neutral reward；
6. 运行测试和短 play。

## 正式训练注意

先验证零头部命令不会破坏既有 swizzle，再逐步扩大命令范围。视频同时检查头部跟踪和身体是否用异常动作补偿。真机运行端只能把命令写入 obs 一次。

