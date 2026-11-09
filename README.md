# 智能空调 - Smart AC Clothing Recognition

> 基于衣服识别的智能空调控制系统

## 项目概述

本项目旨在通过图像识别技术检测舱内人员的衣着类型，实现空调的智能化控制。

## 获取项目与数据

```bash
git clone --recurse-submodules https://github.com/th9rain/smart-ac.git
cd smart-ac
python scripts/prepare_datasets.py
```

- **Fashion-MNIST**：递归克隆后完整可用（图像和标签均包含）。
- **ModaNet**：递归克隆后可获得 Git LFS 标注；底层 RGB 原图不在仓库。
- **DeepFashion2**：官方要求填表获取解压密码，因此不能公开镜像；准备脚本会给出申请、下载及目录提示。

完整的下载步骤、校验和与许可边界见 [DATASETS.md](DATASETS.md)。

## 项目架构

```text
smart-ac/
├── datasets/                    # 官方项目子模块
│   ├── fashion-mnist/          # 完整 Fashion-MNIST 数据（70K 张）
│   ├── DeepFashion2/           # 官方代码、说明与示例（数据需申请）
│   └── modanet/                # ModaNet 标注（Git LFS）
├── data/
│   ├── deepfashion2/           # 本地放置受限数据，不提交 Git
│   └── cabin/                  # 本地舱内自采数据，不提交 Git
├── scripts/
│   └── prepare_datasets.py     # 初始化与校验脚本
├── DATASETS.md                 # 数据来源、获取方法和许可
└── README.md
```

## 数据集说明

### 1. Fashion-MNIST
- **规模**: 70,000 张 (28x28 灰度图)
- **类别**: 10 类（T恤、裤子、连衣裙、鞋等）
- **特点**: 简单易用，MIT 许可证，完全开源
- **推荐场景**: 快速原型验证、基准测试

### 2. DeepFashion2（推荐用于训练）
- **规模**: ~491,000 张图片，801,000+ 衣服标注
- **类别**: 13 类（短袖/长袖上衣、外套、裤子、裙子、连衣裙等）
- **特点**:
  - 每件衣服都有 **边界框、关键点、分割 Mask**
  - 包含遮挡、视角、缩放等标注
  - 商家-消费者匹配对（适合跨域学习）
- **获取限制**: 子模块不包含实际数据；必须通过官方表单申请解压密码
- **推荐场景**: 衣服分类、分割、虚拟试穿训练

### 3. ModaNet
- **规模**: 55,176 张街拍图片对应的标注，265,705 个训练集多边形实例
- **类别**: 13 类（包、腰带、靴子、外套、连衣裙、裤子等）
- **特点**: COCO 格式分割标注，适合分割任务
- **获取限制**: 子模块包含 Git LFS 标注，不包含对应的 PaperDoll/Chictopia RGB 原图
- **推荐场景**: 语义分割、实例分割

## 下一步计划

- [ ] 采集舱内场景图片（自采 200-500 张）
- [ ] 按官方流程申请并下载 DeepFashion2
- [ ] 结合 CARLA 生成合成舱内数据
- [ ] 实现虚拟试穿功能
- [ ] 集成到空调控制系统

## 相关工具

| 工具 | 用途 |
|------|------|
| [CARLA](https://carla.org/) | 自动驾驶仿真器，可生成合成舱内数据 |
| [SAM](https://segment-anything.com/) | Segment Anything 分割模型 |
| [OOTDiffusion](https://github.com/levihaibo/ootd) | 虚拟试穿扩散模型 |
| [DeepFashion3D](https://github.com/GAP-LAB-CUHK-SZ/deepFashion3D) | 3D 服装重建数据集 |

## License

主项目内容的许可证将单独确定。各第三方数据集保留各自许可证和使用条款；详见 [DATASETS.md](DATASETS.md) 以及对应子模块。不要把子模块的许可证理解为所有底层图像都可任意再分发。
