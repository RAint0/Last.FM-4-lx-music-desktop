<p align="center"><a href="https://github.com/RAint0/Last.FM-4-lx-music-desktop"><img width="200" src="https://github.com/RAint0/Last.FM-4-lx-music-desktop/blob/main/logo.png" alt="lx-music logo"></a></p>
<p align="center">
  <a href="https://github.com/RAint0/Last.FM-4-lx-music-desktop"><img src="https://img.shields.io/github/release/RAint0/Last.FM-4-lx-music-desktop" alt="Release version"></a>
  <a href="https://github.com/pylast/pylast"><img src="https://img.shields.io/badge/pyLast-v5.2.0%2B-blue" alt="pyLast version"></a>
  <a href="https://github.com/lyswhut/lx-music-desktop/releases"><img src="https://img.shields.io/badge/LX_Music-v2.7.0%2B-blue" alt="LX version"></a>
  <a href="https://github.com/RAint0/Last.FM-4-lx-music-desktop/"><img src="https://img.shields.io/github/downloads/RAint0/Last.FM-4-lx-music-desktop/latest/total" alt="Downloads"></a>
  <a href="https://github.com/RAint0/Last.FM-4-lx-music-desktop/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green" alt="License"></a>
</p>

# Last.FM 4 lx-music-desktop
一个将洛雪的听歌记录（scrobble）到last.fm上的Python脚本,写得很随意。
last.FM是一个强大的音乐网站，可以为你记录听过的音乐并和自己的数据库匹配，在任意时刻————但最主要是当朋友圈都在晒某云音乐或者是企鹅音乐的年终总结时，它可以为你生成一份类似的总结报表。last.FM的网站上还可以根据你听过的音乐为你推荐音乐，请时不时去逛逛。

## 介绍
1. 使用了pyLast(last.FM API的python接口)和LX_Music v2.7.0+的SSM订阅接口
2. 这个logo真好看


## 开始
1. 创建一个Last.Fm账号。
2. 申请API_KEY和API_SECRET，申请地址：[https://www.last.fm/api/account/create](https://www.last.fm/api/account/create) 
3. 替换LastFM4LX.pyw中的API_KEY和API_SECRET。
4. 通过pip install 按照所需要的环境
5. 先启动洛雪音乐助手，再运行pyw脚本（python的无窗口运行，需要用pythonw）

## 进阶 
1. 使用VBS脚本一键启动洛雪音乐助手并运行脚本，例子在start.vbs
2. 可以为vbs脚本创建快捷方式，编辑名称并替换ico图标（仓库中有可用的ico文件）。
3. win11toast为win11的通知包，其他系统用户可以删除toast或者自行修改。
