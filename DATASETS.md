# 数据集获取与许可说明

本项目使用 Git 子模块保存上游代码、公开数据和标注。由于 GitHub 文件限制与数据集许可不同，**并非所有图像都能合法地复制进本仓库**。

## 一键准备

```bash
git clone --recurse-submodules https://github.com/th9rain/smart-ac.git
cd smart-ac
python scripts/prepare_datasets.py
```

已经普通克隆过仓库时也可以直接运行脚本；脚本会初始化子模块、拉取 Git LFS 文件并检查校验和。

## 当前状态

| 数据集 | 图像 | 标签 | 克隆后状态 | 许可/限制 |
|---|---:|---:|---|---|
| Fashion-MNIST | 70,000 | 10 类分类标签 | 完整可用 | MIT；数据已包含在子模块 |
| DeepFashion2 | 491,895 | 类别、框、关键点、分割、属性、配对 | 仅代码与示例；数据需申请 | 官方要求填表获取解压密码，不在此再分发 |
| ModaNet | 原图来自 PaperDoll/Chictopia | 55,176 张图像对应的 13 类 COCO 多边形标注 | 标注完整；原图不在仓库 | 标注 CC BY-NC 4.0；仅非商业用途 |

## Fashion-MNIST

位置：`datasets/fashion-mnist/data/fashion/`

递归克隆后会获得四个压缩文件：

| 文件 | 内容 | MD5 |
|---|---|---|
| `train-images-idx3-ubyte.gz` | 60,000 张训练图像 | `8d4fb7e6c68d591d4c3dfef9ec88bf0d` |
| `train-labels-idx1-ubyte.gz` | 60,000 个训练标签 | `25c81989df183df01b3e8a0aad5dffbe` |
| `t10k-images-idx3-ubyte.gz` | 10,000 张测试图像 | `bef4ecab320f06d8554ea6380940ec79` |
| `t10k-labels-idx1-ubyte.gz` | 10,000 个测试标签 | `bb300cfdad3c16e7a12a480ee83cd310` |

标签为：T-shirt/top、Trouser、Pullover、Dress、Coat、Sandal、Shirt、Sneaker、Bag、Ankle boot。

官方项目：https://github.com/zalandoresearch/fashion-mnist

## DeepFashion2

子模块 `datasets/DeepFashion2/` 包含官方说明、转换和评估代码，但不包含 491K 张图像及 JSON 标注。

官方流程：

> 压缩包合计约 15.8 GB，解压后约 16.7 GB；如同时保留压缩包和解压内容，建议预留至少 35 GB。

1. 填写[官方申请表](https://docs.google.com/forms/d/e/1FAIpQLSeIoGaFfCQILrtIZPykkr8q_h9qQ5BoTYbjvf95aXbid0v2Bw/viewform)获取解压密码。
2. 从[官方 Google Drive](https://drive.google.com/drive/folders/125F48fsMBz2EF0Cpqk6aaHet5VH399Ok)下载训练、验证和测试压缩包。
3. 解压到 `data/deepfashion2/`，形成：

```text
data/deepfashion2/
├── train/
│   ├── image/
│   └── annos/
├── validation/
│   ├── image/
│   └── annos/
└── test/
    └── image/
```

此目录已被 `.gitignore` 排除。不要提交解压密码、申请信息或数据文件。协作者需各自接受官方条款并获取数据。

官方项目：https://github.com/switchablenorms/DeepFashion2

## ModaNet

位置：`datasets/modanet/annotations/`

子模块通过 Git LFS 提供 COCO 格式标注：

| 文件 | MD5 |
|---|---|
| `modanet2018_instances_train.json` | `96478657d20e322e9d3282c6d73c0c4c` |
| `modanet2018_instances_val.json` | `900b24b7d6c0c48203e6244f45d65499` |

安装 [Git LFS](https://git-lfs.com/) 后运行：

```bash
git -C datasets/modanet lfs pull
```

这些 JSON 是**标注**，不是 RGB 原图。官方说明称标注对应 PaperDoll/Chictopia 图像集；历史原图下载约 40 GB，但官方 PaperDoll 仓库和下载端点目前均不可用，且没有核实到这些用户照片的统一再分发许可。本项目不会从非官方镜像自动下载或重新打包上传。

官方项目：https://github.com/eBay/modanet

## 为什么不把全部数据直接提交到 Git

- 普通 GitHub 单文件硬限制为 100 MiB；大图像集会让仓库克隆、历史维护和配额管理失控。
- Git LFS 解决的是传输方式，不会自动获得数据再分发权，而且存在存储和流量配额。
- DeepFashion2 的官方申请和密码流程不能由公开镜像绕过。
- ModaNet 标注的许可不等于底层 PaperDoll/Chictopia 原图的许可。

因此，本项目采用“公开小数据随子模块 + 大型/受限数据官方获取 + 自动校验”的方式，既方便复现，也不会把无法确认再分发权的数据公开上传。
