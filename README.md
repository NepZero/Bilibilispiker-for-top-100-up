# Bilibilispiker-for-top-100-up
爬取指定一年的百大up主的视频相关信息（日期，点赞量，投币数，播放量）并生成相关的统计图

## 项目介绍
本项目采用selenium用Chrome对B站的相关信息进行爬取，事先下好对应版本的Chrome驱动（详细见网上教程）。因每次B站返回的HTML文件有可能不同，报错就多试几次。本项目要手动输入每个up主的uid。

## 使用方法
1. 根据`requirements.txt`文件下载好相关库
```shell
pip install -r requirements.txt
```
2. 把想爬取的百大的uid写进`{year}.txt`中，如`2023.txt`所示
3. 运行`txt2json.py`将`{year}.txt`转化成`{year}.json`
4. 运行 `bilibilispiker.py`将`{year}.json`转化为记录详细信息的`{year}_top.json`。如果登入页面后过几秒报错，多试几次。
5. 运行`ranklist.py`绘制相关统计图
