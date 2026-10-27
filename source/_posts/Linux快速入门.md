---
title: "Linux快速入门"
date: 2026-04-19 19:00
description: 从零开始的Linux完整入门指南，包含基础语法、常用标签详解和实战示例
categories: [部署运维]
tags: [Linux, 零基础教程]
cover: ../img/anime-tech-linux-20260419.jpg
---
# Linux快速入门

## 1. 前言
此博客将介绍Linux的基础语法、常用标签详解和实战示例，帮助初学者快速入门Linux操作，也是为自己记录下学习 Linux 的过程。

## 2. 安装Linux
- 2.1 首先，我们需要下载一个虚拟机软件，如VirtualBox、VMware等。这里推荐VMware.下载地址：[VMware下载地址](https://www.vmware.com/zh.cn/virtualization.html)
- 2.2 其次，，我们需要下载一个Linux镜像文件，这里推荐下载Ubuntu 25.10版本。可通过清华大学镜像网站下载，地址为：[Ubuntu下载地址](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/)
- 2.3 最后，我们需要在VMware中创建一个新的虚拟机，选择Ubuntu镜像文件，安装即可。

## 3. xshell和xftp
xshell和xftp是两个常用的Linux客户端工具，用于连接和管理Linux服务器。
- 3.1 首先，我们需要下载xshell和xftp。下载地址：[xshell和xftp下载地址](https://www.xshell.com/zh/xshell/)
- 3.2 安装完成后，先注册一个账号，登录后，我们需要在xshell中配置一个新的连接，连接类型选择SSH，主机地址输入虚拟机的IP地址，端口输入22，用户名输入自定义用户名，密码输入自定义密码。
- 3.3 最后，我们需要在xshell中连接到虚拟机，即可开始使用Linux了。
- 3.4 xftp的连接类似xshell，只是连接类型选择FTP，主机地址输入虚拟机的IP地址，端口输入21，用户名输入自定义用户名，密码输入自定义密码。
- 3.5 最后，我们需要在xftp中连接到虚拟机，即可开始使用xftp了。

## 4. 系统管理
### 4.1 关闭防火墙
   - 4.1.1 在xshell中，输入以下命令关闭防火墙：
   ```bash
   sudo ufw disable
   ```
   - 4.1.2 确认关闭防火墙，输入以下命令：
   ```bash
   sudo ufw status
   ```
   - 4.1.3 如果防火墙已关闭，会显示以下信息：
   ```bash
   Status: inactive
   ```
### 4.2关机重启操作
   - 4.2.1 在xshell中，输入以下命令关机：
   ```bash
   sudo shutdown -h now
   ```
   - 4.2.2 在xshell中，输入以下命令重启：
   ```bash
   sudo reboot
   ```
### 4.3 修改主机名
   - 4.3.1 在xshell中，输入以下命令修改主机名：
   ```bash
   sudo hostnamectl set-hostname 新主机名
   ```
   - 4.3.2 确认修改主机名，输入以下命令：
   ```bash
   hostnamectl status
   ```
   - 4.3.3 如果主机名已修改，会显示以下信息：
   ```bash
   Hostname: 新主机名
   ```
### 4.4 软件管理_apt软件包管理器
   - 4.4.1 在xshell中，输入以下命令更新软件源：
   ```bash
   sudo apt update
   ```
   - 4.4.2 在xshell中，输入以下命令安装软件：
   ```bash
   sudo apt install 软件名
   ```
   - 4.4.3 在xshell中，输入以下命令卸载软件：
   ```bash
   sudo apt remove 软件名
   ```

## 5. 操作使用
### 5.1 常用帮助
- 5.1.1 man man——查看手册说明文档的方式
  ```bash
  man man  #查看man命令的说明文档
  man ls  # 查看ls命令的说明文档
  ```
- 5.1.2 help获取shell内建命令的帮助信息
  ```bash
  help 命令名  <!-- 获得shell内建命令的帮助信息 -->
  ```
- 5.1.3 常用快捷键
```sh
ctrl+c    #停止进程
ctrl+l    # 清屏
ctrl+q    # 退出
tab键     # 自动补全(提示)
上下键     #查找执行过的命令
ctrl+u    #清除当前敲的命令
```

### 5.2 文件目录的查看和切换
- 5.2.1 pwd——显示当前工作目录的绝对路径
  ```bash
      pwd   #显示当前工作目录的绝对路径
  ```
- 5.2.2 cd——切换
   ```bash
      cd /  #进入根目录，cd可切换到绝对路径也可以相对路径
   ```
- 5.2.3 ls——查看当前目录下的文件夹
   ```bash
      ls    #查看当前目录下的文件夹
      ls -l #查看当前目录下的文件夹和文件的详细信息
   ```
- 5.2.4 回到上一级路径
   ```bash
      cd ..  #回到当前目录的上一级路径
      cd -  #回到上一次所在路径
   ```

### 5.3 创建目录及文件
- 5.3.1 mkdir——创建一个新的目录
  ```bash
      mkdir ...   #...为要创建的目录
      mkdir -p /.../...    #创建多层目录，可用命令行无限递归创建文件夹
  ```
- 5.3.2 touch——创建空文件
  ```bash
      touch 文件名称 #基础语法
  ```
- 5.3.3 cp复制文件或目录
  ```bash
   cp source dest（复制source到dest）
  ```

### 5.4 删除移动目录文件
- 5.4.1 rm——删除文件或目录
  ```bash
   rm 文件名或目录名   #删除文件或目录
   rm -r 目录名      #递归删除目录
   rm -f 文件名      #强制删除文件
   rm -v         #显示指令的详细执行过程
  ```
- 5.4.2 mv——移动文件或目录
  ```bash
   mv source dest    #将source移动到dest
   mv ~/桌面/文件名 ~/回收站     #将文件移动到回收站
   mv ~/桌面/文件名 ~/桌面/新文件名 #修改文件名称
  ``` 

### 5.5 查看文件
- 5.5.1 cat——查看文件内容，从第一行开始显示
```bash
      cat #要查看的文件
      cat n #显示所有行的行号，包括空行
```
- 5.5.2 





