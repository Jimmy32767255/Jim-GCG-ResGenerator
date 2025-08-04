# Jim-GCG-ResGenerator

# JimGCG资源生成器

## 简介

这是一个用于生成[GCG](https://github.com/jie65535/GrasscutterCommandGenerator)的资源文件的项目

## 开始

1. 安装Python
2. 克隆仓库
```
git clone https://github.com/Jimmy32767255/Jim-GCG-ResGenerator.git
```
3. 安装依赖
```
python -m pip install -r requirements.txt
```
4. 运行项目
```
python Src/main.py
```

## 要求

- Grasscutter-Res-Origin
###### 大部分资源文件从这里生成（ExcelBinOutput和TextMap）
- GCG-Res-Origin（\Source\GrasscutterTools\Resources）
###### 暂时无法生成的资源文件从这里复制

## 命令行参数

请使用`--help`参数查看所有参数说明。

## 图形用户界面

如果没有指定`-C`或`--cli`参数，程序将以图形用户界面模式运行。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE 文件](LICENSE)。
