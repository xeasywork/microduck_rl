# Ground-pick：按 phase 插值跟踪姿态

> 对应英文/法文原文：[`2026-07-24-ground-pick-pose-following-design.md`](2026-07-24-ground-pick-pose-following-design.md)

## 目标

把捡拾动作从模糊的高度/接触奖励改为明确姿态轨迹：站立 → 下探 → 低位保持 → 回升 → 站立。

## 目标姿态

用关节名称定义 STAND、DOWN 等关键姿态。STAND 使用模型 HOME；DOWN 初值来自折叠 keyframe，后续应由真机或 pose editor 实测替换。

## Phase 曲线

周期分四段，目标姿态在关键点间插值。phase 由命令生成；训练可随机 phase reset，使每个阶段都得到样本并避免只会从起点执行。

## 新 MDP 函数

- `phase_pose_blend` 计算阶段目标；
- pose tracking / L1 reward 按名称比较舵机关节；
- helper 统一处理 HOME、被动关节和批量 env。

## 奖励

姿态跟踪为主，辅以嘴部接近/接触、平衡、平滑、能量和完成后稳定。避免奖励只靠降低躯干或摔倒获得。

## Sim2real

运行端与训练端必须使用相同周期、phase 含义和 61 维命令布局。未使用头部/身体槽保持补零。

## 测试和训练

纯函数测试四段边界和连续性；cfg 测试关节解析和奖励；随机 phase smoke 检查各阶段。正式训练后同时看 pose error、接触、站立恢复和视频。

