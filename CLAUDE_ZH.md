# Microduck RL 开发规则

> 对应英文原文：[`CLAUDE.md`](CLAUDE.md)

本文是训练环境开发的经验手册。每条规则都来自真实 sim2real 或长训练故障。

## 常用命令

```bash
uv run list-envs
uv run train <TASK_ID> --env.scene.num-envs 4096
uv run train <TASK_ID> --env.scene.num-envs 64 --agent.max_iterations 5
uv run play <TASK_ID> --wandb-run-path <entity/project/run_id>
uv run scripts/export.py <TASK_ID> --wandb-run-path <...>
uv run scripts/infer_policy.py --walking out.onnx
uv run --with pytest pytest tests/
```

长训练前必须先做 64 env、5 iteration 冒烟测试。

## 仓库地图

- `tasks/mdp.py`：自定义奖励、事件、观测、命令和课程。
- `tasks/microduck_*_env_cfg.py`：任务环境配置。
- `tasks/__init__.py`：任务注册。
- `tasks/backlash.py`：齿隙变体包装。
- `robot/microduck_constants.py`：机器人和 BAM 配置。
- `actuator/friction_dr_bam.py`：舵机和摩擦随机化。
- `scripts/`：导出、推理和 sim2real 工具。
- `tests/`：CPU 配置和奖励回归测试。

## 不可破坏的不变量

1. actor 观测为 61 维，命令块顺序固定为 `twist(3) + head(4) + body(6)`。
2. 滑轮和齿隙模型有交错被动关节，MDP 函数不能硬编码关节索引，应按名称解析。
3. 所有不驱动关节以 `passive_` 开头；正则必须区分轮子和齿隙。
4. 独立环境必须注册 BAM 摩擦字段展开事件；普通 `dof_frictionloss` 随机化在 BAM 下可能无效。
5. actor 观测和对应 tracking reward 必须使用同一个传感器视图。
6. 观测归一化开启，必须通过官方 exporter 导出 ONNX。
7. 训练和部署都不使用动作低通；若新增过滤器必须两端匹配。
8. 自定义 domain randomization 不能在 reset 间累积。
9. Backlash 任务必须与原任务使用同类机器人模型。

## 新环境工作流

1. 选最近模板：移动用 velocity；两状态用 sitstand；终点姿态用 standup；动态技巧用 roulade。
2. 训练前验证物理假设：目标姿态要能稳定保持，目标高度从当前模型实测，不照抄旧值。
3. 在 cfg 顶部集中 `ENABLE_*` 和常量；提供 `make_..._env_cfg(play, rough)`；注册独立 experiment name。
4. 写 CPU cfg 测试，验证关节、奖励符号和 gate。
5. 运行冒烟训练，确认 61 维、无 NaN、所有 reward 可计算并能导出。
6. 正式训练并准备经历多轮 reward hacking 修正。

## 奖励设计

- 先确认符号：返回非负 cost 的函数通常配负 weight；内部已返回负值的 penalty 配正 weight。W&B 中 penalty episode reward 应为非正。
- RL 会钻所有未定义自由度。真正动作条件使用状态 gate、接触、方向和 latch，不靠很小的惩罚暗示。
- 避免到达后每 tick 领奖的 jackpot。使用速率限制、slew target 或一次性完成奖励。
- 动态技巧不要一直奖励 upright，否则策略会拒绝翻转。
- 发现动作前不要过早施加强平滑/低冲击惩罚，否则策略学会“不尝试”。后期通过 curriculum 加强。
- 接触任务必须区分合法接触、支撑接触和危险碰撞。
- 奖励每个阶段可达，必要时用 reverse curriculum 从动作中段重置。

## 命令和观测

不用的命令也要保留并补零。奖励不要依赖 actor 看不到且部署端不存在的信息，除非它只用于训练目标且策略被设计为固定动作。

删除 reward 项时确认没有 curriculum 仍引用；修改命令语义时同步运行端和推理脚本。

## 课程学习

课程应逐步增加扰动、摩擦、质量范围、目标难度和正则强度。课程过快会让刚学到的能力消失；中间状态保留少量采样以持续练习完成阶段。

## 训练运行与读图

- 先看 NaN、episode length 和终止原因。
- 确认每个 penalty 符号正确。
- 同时看任务进度指标和视频，单一总 reward 不足以证明动作正确。
- 定期导出/回放 checkpoint，避免只相信最后一个模型。
- 记录每轮配置、假设和失败模式。

## Sim2real 常见陷阱

- 目标高度偏几毫米就可能不可达。
- 关节索引在滑轮模型中交错。
- 编码器偏置的观测与 reward 视图不一致。
- 摩擦随机化作用到错误物理字段。
- 部署缺少训练时滤波或命令槽。
- 手工导出丢失归一化器。
- 只在 viewer 成功，不测电流、冲击和真实接触。

