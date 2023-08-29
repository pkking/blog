---
title: stable-diffusion-webui使用和配置
tags: 
- stable-diffusion-webui
- AIGC
date: 2023-08-29 22:24
---

## WHY
随着 [`stable-diffusion-SDXL-1.0`](https://stablediffusionxl.com/)发布，`text2img`的效果越来越好了，加上正好买了`2080Ti 22G`，于是准备实施SD

## 硬件
| 硬件| 型号|
| --| -- |
| 显卡|  2080Ti 22G (魔改)|
| CPU| i7-10070 |
| 内存| 32G|

## 安装 & 启动

当前我是在windows上安装，需要先安装[`python 3.10`](https://www.python.org/downloads/release/python-3106/)
```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui
.\webui-user.bat
```

执行后，会看到一些打印，当看到`Running on local URL:  http://0.0.0.0:7860` 就算启动成功了，通过浏览器访问`http://ip:7860` 即可
```
(venv) PS D:\projs\stable-diffusion-webui> .\webui-user.bat    
venv "D:\projs\stable-diffusion-webui\venv\Scripts\Python.exe"
Python 3.10.6 (tags/v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)]
Version: v1.5.2
Commit hash: c9c8485bc1e8720aba70f029d25cba1c4abf2b5c
Launching Web UI with arguments: --listen --xformers --no-half-vae
Loading weights [31e35c80fc] from D:\projs\stable-diffusion-webui\models\Stable-diffusion\sd_xl_base_1.0.safetensors
Creating model from config: D:\projs\stable-diffusion-webui\repositories\generative-models\configs\inference\sd_xl_base.yaml
Running on local URL:  http://0.0.0.0:7860
```

## 模型配置

### 配置SDXL 1.0
参考[这个回复](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/11685#discussioncomment-6574915)
1. 下载[模型](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors)
1. 将模型放到` models/Stable-diffusion `目录
1. 在`webui-user.bat`中的`COMMANDLINE_ARGS=`后增加`--no-half-vae`参数，例如
    ```
    set COMMANDLINE_ARGS=--listen --xformers --no-half-vae
    ```

*注意：SDXL 1.0 需要32G内存*

## 配置style
参考[这个讨论](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/10129)

将[style.csv](https://github.com/AUTOMATIC1111/stable-diffusion-webui/files/11423539/styles.csv)放到代码根目录，然后重启项目即可

这样在style下拉菜单就能看到各种`style`了

![Alt text](./image.png)

## TODO
- 收集一些`Prompt`和插件
- 调试`refine`