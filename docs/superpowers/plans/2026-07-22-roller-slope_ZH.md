# `roller_slope` 斜坡模式实施计划

> 对应英文/法文原文：[`2026-07-22-roller-slope.md`](2026-07-22-roller-slope.md)

> 这是历史实施计划，实际状态以当前代码和测试为准。

## 全局约束和文件

任务使用带轮模型、统一 61 维观测和无主动轮驱动的物理。新增 `slope_terrain.py`、roller slope env cfg、地形/课程/cfg 测试、任务注册和推理入口。

## Task 1：难度到坡角

先写纯函数，把离散或连续难度映射到坡度。测试最小/最大、单调性、裁剪和无效参数。

## Task 2：平地 + 坡道地形

实现 `FlatRampTerrainCfg`：reset 区域保持平地，前方连续连接斜坡，避免初始碰撞和几何断层。测试顶点、三角形、边界和坡角。

## Task 3：坡度课程

根据成功或进度调整 terrain level。测试升级、降级、上下限和批量 env，不让偶然高速滑落误判成功。

## Task 4：环境和注册

从 roller 基础继承 BAM/DR/观测，命令补零，reset 给小幅前向速度。奖励 upright、沿坡位移、接触和低横移；删除普通速度命令跟踪。注册独立任务与 PPO。

## Task 5：部署

在 `infer_policy.py` 增加 slope 标志和触发按键，使用斜坡 MJCF/terrain。运行端只在物理坡度位于训练范围时触发。

## 验证

运行 CPU 测试、64 env smoke、长训和 play。观察机器人是否真正靠重力下坡、是否横向漂移、摔倒刷位移或在坡前停住。

