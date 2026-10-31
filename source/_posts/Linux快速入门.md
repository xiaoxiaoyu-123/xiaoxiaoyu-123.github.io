---
title: "Linux快速入门"
date: 2026-04-19 19:00
description: 从零开始的 Linux 完整入门指南，包含环境安装、远程连接、系统管理和常用命令详解，附实战示例
categories: [部署运维]
tags: [Linux, 零基础教程]
cover: ../img/anime-tech-linux-20260419.jpg
---
# Linux快速入门

## 1. 前言
此博客将介绍 Linux 的基础操作、常用命令详解和实战示例，帮助初学者快速入门 Linux，也是为自己记录下学习 Linux 的过程。

我自己是从虚拟机开始摸索的，一路踩了不少坑，所以这篇会尽量把每一步都写细一点，你跟着敲就能跑起来 💪

## 2. 安装Linux
- 2.1 首先，我们需要下载一个虚拟机软件，如VirtualBox、VMware等。这里推荐VMware，下载地址：[VMware下载地址](https://www.vmware.com/zh.cn/virtualization.html)
- 2.2 其次，我们需要下载一个Linux镜像文件，这里推荐下载Ubuntu 25.10版本。可通过清华大学镜像网站下载，地址为：[Ubuntu下载地址](https://mirrors.tuna.tsinghua.edu.cn/ubuntu-releases/)
- 2.3 最后，我们需要在VMware中创建一个新的虚拟机，选择Ubuntu镜像文件，安装即可。

> 💡 小提示：清华镜像站下载速度比官网快很多，建议优先用它～

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
   > ⚠️ 注意：关防火墙只建议在自己 learning 用的虚拟机里操作，正式服务器请按需放行端口，别一关了之～

### 4.2 关机重启操作
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
- 5.1.1 man——查看手册说明文档的方式
  ```bash
  man man  # 查看man命令的说明文档
  man ls   # 查看 ls 命令的说明文档
  ```
- 5.1.2 help 获取 shell 内建命令的帮助信息
  ```bash
  help 命令名
  ```
- 5.1.3 常用快捷键
```sh
ctrl+c    # 停止进程
ctrl+l    # 清屏
ctrl+q    # 退出
tab键     # 自动补全(提示)
上下键     # 查找执行过的命令
ctrl+u    # 清除当前敲的命令
```

### 5.2 文件目录的查看和切换
- 5.2.1 pwd——显示当前工作目录的绝对路径
  ```bash
      pwd   # 显示当前工作目录的绝对路径
  ```
- 5.2.2 cd——切换
   ```bash
      cd /  # 进入根目录，cd可切换到绝对路径也可以相对路径
   ```
- 5.2.3 ls——查看当前目录下的文件夹
   ```bash
      ls    # 查看当前目录下的文件夹
      ls -l # 查看当前目录下的文件夹和文件的详细信息
   ```
- 5.2.4 回到上一级路径
   ```bash
      cd ..  # 回到当前目录的上一级路径
      cd -   # 回到上一次所在路径
   ```

### 5.3 创建目录及文件
- 5.3.1 mkdir——创建一个新的目录
  ```bash
      mkdir ...   # ...为要创建的目录
      mkdir -p /.../...    # 创建多层目录，可用命令行无限递归创建文件夹
  ```
- 5.3.2 touch——创建空文件
  ```bash
      touch 文件名称 # 基础语法
  ```
- 5.3.3 cp 复制文件或目录
  ```bash
   cp source dest   # 复制 source 到 dest
   cp -r source dest # 复制目录时记得加 -r 递归
  ```

### 5.4 删除移动目录文件
- 5.4.1 rm——删除文件或目录
  ```bash
   rm 文件名或目录名   # 删除文件或目录
   rm -r 目录名      # 递归删除目录
   rm -f 文件名      # 强制删除文件
   rm -v         # 显示指令的详细执行过程
  ```
  > ⚠️ 注意：`rm -rf` 属于「删库跑路」级命令，敲之前**先看三遍路径**，Linux 下没有回收站后悔药！
- 5.4.2 mv——移动文件或目录
  ```bash
   mv source dest    # 将source移动到dest
   mv ~/桌面/文件名 ~/回收站     # 将文件移动到回收站
   mv ~/桌面/文件名 ~/桌面/新文件名  # 修改文件名称
  ```

### 5.5 查看文件
- 5.5.1 cat——查看文件内容，从第一行开始显示
```bash
      cat 文件名        # 查看文件内容
      cat -n 文件名     # 显示所有行的行号，包括空行
```
- 5.5.2 more——分页查看大文件，空格翻页、q 退出
```bash
      more 文件名       # 内容太长一屏放不下时用它
```
- 5.5.3 less——和 more 类似，但支持上下键回看（推荐）
```bash
      less 文件名       # 功能比 more 更强，看完按 q 退出
```
- 5.5.4 head / tail——只看开头或结尾
```bash
      head -n 10 文件名   # 只看前 10 行
      tail -n 10 文件名   # 只看后 10 行
      tail -f 日志文件名   # 实时追踪日志新增内容，运维必备
```

### 5.6 搜索查找
- 5.6.1 find——按名字或范围查找文件
```bash
      find /home -name "*.txt"   # 在 /home 下查找所有 .txt 文件
      find . -name "关键字*"      # 在当前目录模糊查找
```
- 5.6.2 grep——在文件内容里筛选关键字
```bash
      grep 关键字 文件名          # 在文件中查找包含关键字的行
      grep -n 关键字 文件名       # 顺便显示行号
      cat 文件名 | grep 关键字    # 管道写法，效果一样
```

### 5.7 压缩解压
- 5.7.1 tar——打包与解压（最常用）
```bash
      tar -zxvf 压缩包.tar.gz    # 解压 .tar.gz 压缩包
      tar -zcvf 打包名.tar.gz 目录  # 把目录打包压缩
```
- 5.7.2 zip / unzip
```bash
      zip 压缩包.zip 文件名        # 压缩成 zip
      unzip 压缩包.zip           # 解压 zip
```

## 6. 总结
✅ 最后梳理一下入门路线：**装好虚拟机 → 用 xshell 远程连接 → 学会系统管理的基础操作 → 把文件目录、查看、搜索、压缩这几组常用命令敲熟**。

Linux 入门没有捷径，就是多敲多练。刚开始记不住命令很正常，我到现在也还会忘，忘了就 `man` 一下，用着用着就熟了。

希望这篇教程对你有所帮助！如果有写错的地方或者更好的命令推荐，欢迎在评论区留言 💬 我们下一篇博客见！
