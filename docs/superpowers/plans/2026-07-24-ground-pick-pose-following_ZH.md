# Ground-pick 姿态跟踪实施计划

> 对应英文/法文原文：[`2026-07-24-ground-pick-pose-following.md`](2026-07-24-ground-pick-pose-following.md)

> 这是带代码草案的历史计划，合并后的实现以源码为准。

## 约束

保持现有任务 ID、61 维观测、运行端 phase 周期和 sim2real 随机化；姿态按关节名称定义，不硬编码滑轮式索引。

## Task 1：`phase_pose_blend`

实现四段姿态插值纯函数，覆盖下降、低位保持、上升和站立保持。测试 segment 边界、连续性、回绕、批量输入和目标姿态维度。

## Task 2：姿态跟踪奖励

实现 L2/L1 pose tracking 和统一误差 helper。测试 HOME 零误差、单关节偏差、权重/关节选择和 self-negating 符号。

## Task 3：随机 phase

给 GroundPick phase command 增加 `randomize_phase`，训练 reset 时覆盖所有动作阶段，play 默认从周期起点开始。测试随机范围和确定性模式。

## Task 4：重写 env reward/pose

配置 STAND 与 DOWN 姿态、周期各段比例和 reward。STAND 直接使用 HOME，DOWN 初值来自 FOLD keyframe，真机数据可用后替换。删除会抵消姿态轨迹的旧高度项。

## Task 5：端到端验证

运行任务构建、CPU tests、64 env smoke、play 和 ONNX export。检查下降/保持/上升时序、嘴部接触、恢复站立和运行端按键一致性。

## 自检

重点确认 phase 命令真的进入 actor、未使用槽补零、姿态顺序与模型一致、奖励不会鼓励摔倒，并且 exporter 包含归一化器。

