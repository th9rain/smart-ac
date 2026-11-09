# 智能空调 - Smart AC Clothing Recognition

> 基于衣服识别的智能空调控制系统

## 项目概述

本项目旨在通过图像识别技术检测舱内人员的衣着类型，实现空调的智能化控制。

## 项目架构

```
智能空调/
├── datasets/                    # 数据集
│   ├── fashion-mnist/          # Fashion-MNIST 服装基准数据集 (70K张)
│   ├── DeepFashion2/           # DeepFashion2 服装数据集 (491K张) ⭐推荐
│   └── modanet/                # ModaNet 街拍服装分割数据集 (55K张)
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
  - 每件衣服都有 **边界框、关键点、分割Mask**
  - 包含遮挡、视角、缩放等标注
  - 商家-消费者匹配对（适合跨域学习）
- **推荐场景**: 衣服分类、分割、虚拟试穿训练

### 3. ModaNet
- **规模**: 55,000+ 张街拍图片，~800,000 多边形标注
- **类别**: 13 类（包、腰带、靴子、外套、连衣裙、裤子等）
- **特点**: COCO 格式分割标注，适合分割任务
- **推荐场景**: 语义分割、实例分割

## 下一步计划

- [ ] 采集舱内场景图片（自采 200-500 张）
- [ ] 基于 DeepFashion2 训练衣服分类模型
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

各数据集 License 详见对应子模块目录。
