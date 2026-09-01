# Hugging Face Jobs 训练

> 对应英文原文：[`README.md`](README.md)

通过 Hugging Face 托管 GPU 训练 Microduck。认证使用缓存的 HF token 或 `HF_TOKEN`，W&B 凭据从本机配置转发。

## 一次性准备

```bash
hf auth login
wandb login
```

## 提交任务

在普通训练命令后加入 `--hf-jobs`：

```bash
uv run train <TASK_ID> \
  --env.scene.num-envs 4096 \
  --agent.max_iterations 4000 \
  --hf-jobs
```

常用参数：

- `--namespace <name>`：个人或组织命名空间；
- `--flavor l4x1`、`a10g-large`、`a100-large`：GPU 类型；
- `--timeout 12h`：最长运行时间；
- `--detach`：提交后立即返回；
- `--dry-run`：只打包和显示任务；
- `--run-name <tag>`：自定义运行名；
- `--no-uv-cache`：不挂载持久 uv 缓存；
- `--no-wandb`：不转发 W&B 密钥。

## 后台流程

1. 根据 Git tracked + uncommitted 文件制作源码 tarball；
2. 上传到私有 dataset；
3. 创建私有模型仓库存 checkpoint；
4. 挂载持久 uv 缓存；
5. Job 安装 uv、解压、`uv sync` 并训练；
6. 后台 uploader 定期上传 `model_*.pt`；
7. 退出时执行最终上传。

## Checkpoint 和管理

提交器打印模型仓库和 job URL。可用 `HfApi.list_jobs()`、`fetch_job_logs()` 和 `cancel_job()` 查询、跟随或取消任务。

先提交 64 env、5 iteration 冒烟任务，再承担正式 GPU 成本。

