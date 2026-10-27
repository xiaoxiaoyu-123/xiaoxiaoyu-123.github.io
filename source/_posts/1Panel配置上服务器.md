---
title: "1Panel配置上服务器"
date: 2026-04-24 21:00:00
description: 从零开始的使用shell脚本给服务器配置上1Panel完整入门指南，包含基础语法、常用标签详解和实战示例
categories: [部署运维]
tags: [Linux, 1Panel, 零基础指南, shell脚本]
cover: ../img/anime-tech-1panel-20260424.jpg
---
# 使用shell脚本给服务器配置上1Panel

## 前言
首先你的电脑上已经安装好了SSH客户端（如Xshell8），并且了解过Linux的基本操作。懂得使用SSH客户端连接上服务器。否则，你无法使用shell脚本给服务器配置1Panel。配置完成后，你可以Web界面登录1Panel来管理你的服务器。

## 1Panel安装
```bash
curl -sSL https://resource.fit2cloud.com/1panel/package/quick_start.sh -o quick_start.sh && bash quick_start.sh
```
在终端粘贴并运行上面的命令，即可安装1Panel。

## 备选方案
若遇到网络问题，一键安装1Panel的脚本无法正常安装，可通过如下步骤解决
官方脚本会自动安装 Docker，但网络问题可能导致失败，此时需要手动安装 Docker:
### Docker安装
- 1.安装必要的基础工具
```bash
sudo yum install -y yum-utils
```
这个命令是安装 yum-utils，它提供了后面需要用到的 yum-config-manager 工具。

- 2.添加阿里云的Docker镜像源
```bash
sudo yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```
这条命令会从阿里云的镜像服务器上下载 Docker 的安装源配置文件，并添加到你的系统中。

- 3.正式安装Docker
```bash
sudo yum install -y docker-ce docker-ce-cli containerd.io
```
运行这个命令，直接从阿里云的镜像源安装 Docker 社区版。

- 4.启动Docker并设为开机自启
```bash
sudo systemctl start docker && sudo systemctl enable docker
```
安装完成后，启动 Docker 服务，并让它在你每次重启服务器时自动运行。

- 5.验证安装
```bash
sudo docker version
```
运行这个命令来检查 Docker 是否安装成功。如果屏幕上显示了 Docker 的版本信息，就说明大功告成了。

### 1Panel安装
Docker成功安装后，运行1Panel的安装脚本
```bash
curl -sSL https://resource.fit2cloud.com/1panel/package/quick_start.sh -o quick_start.sh && bash quick_start.sh
```

## 1Panel配置
运行安装命令后，脚本会交互式地引导你完成以下初始设置
- 1.设置面板端口，可直接回车键使用默认的(或者是自定义4~5位数的)
- 2.设置安全入口，可直接回车使用默认的(或者是自定义)
- 3.设置面板用户和密码，设置你用来登录 Web 界面的用户名和密码
- 4.所有信息设置完后，终端会输出包含外网访问地址、用户名、密码的完整信息，记得截图保存

## 1Panel可视化管理
在浏览器输入外网访问地址，输入你的用户名、密码即可登录你的1Panel账号了，这样就可以进行服务器的可视化操作，不再需要Linux的命令行操作了！
后续操作主要围绕安全加固、环境部署、网站搭建和维护管理这四条线展开。


