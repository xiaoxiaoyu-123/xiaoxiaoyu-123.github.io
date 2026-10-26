---
title: "📝 我的Hexo博客搭建之旅：从零到一的全记录"
date: 2025-10-11 13:30:00
categories: [博客搭建]
tags: [Hexo, GitHub,Butterfly主题]
description: 详细记录使用Hexo+Butterfly主题搭建个人博客的完整过程、遇到的问题及解决方案
cover: ../img/anime-tech-hexo-20251011.jpg

---
# 🚀 Hexo博客搭建全记录



## 📊 技术选型：为什么选择Hexo？
在评估了多个静态博客生成器（包括Jekyll、Hugo、VuePress等）后，我最终选择了Hexo，以下是详细的对比分析：
### ✅ Hexo的核心优势
- **生成速度：**⚡️ 极快，基于Node.js，千篇文章秒级生成
- **主题生态：**🎨 丰富美观，Butterfly、NexT等主题设计优秀
- **部署便捷性：**🚀 一键部署，原生支持Git/GitHub Pages
- **学习曲线：**📚 简单易学，纯Markdown写作，无后端负担
- **社区活跃度：**🌟 非常活跃，中文文档完善，问题易解决

<br>
<br>

经过对比，我选择了**Hexo**作为博客框架，原因如下：

### 🔍 决策因素
- **技术栈匹配**：作为前端学习者，Node.js环境更熟悉
- **写作体验**：专注Markdown内容，无需关注渲染细节
- **自定义灵活**：主题可深度定制，CSS/JS可自由修改
- **免费托管**：GitHub Pages完全免费，适合学生党


## 🛠️ 详细搭建流程

### 第一阶段：环境准备https://nodejs.org/zh-cn
- 1.安装Node.js（建议LTS版本），访问 nodejs.org 下载安装  [@Node.js官网](https://nodejs.org/zh-cn)
- 2. 2. 安装Git，访问 git-scm.com 下载  [@git官网](https://git-scm.com/)
- 3. **验证安装：**
```
  node -v    # 显示版本号表示成功  
  npm -v     # 显示版本号表示成功  
  git --version
```
### 第二阶段：Hexo初始化
- 1. 全局安装Hexo cli
```
 npm install -g hexo-cli
``` 

- 2. 创建博客目录
``` 
   hexo init my-blog  
   cd my-blog
```

- 3. 安装依赖
```
npm install
```

- 4.本地预览
```
hexo clean && hexo s
```


### 第三阶段：主题配置
- 1. 安装Butterfly主题
```
npm install hexo-theme-butterfly
```
- 2. 修改站点配置 _config.yml
```
theme: butterfly
```
- 3. 复制主题配置文件
```
cp node_modules/hexo-theme-butterfly/_config.yml _config.butterfly.yml
```


### 第四阶段：基础优化
- 1.config.yml 关键配置示例
  **站点信息：**
```
title: 我的技术博客
subtitle: 记录学习与成长
description: 前端开发 | 技术分享 | 学习笔记
keywords: [前端, JavaScript, CSS, 学习]
```

- 2.部署配置
```
deploy:
  type: git
  repo: https://github.com/用户名/仓库名.git
  branch: main
```



## 🧩遇到的问题与解决方案


### 🚨 常见问题汇总
- 1.端口占用
   - 具体表现：Error: listen EADDRINUSE: address already in use :::4000
   - 解决方案：hexo s -p 5000 或结束占用进程
- 2.图片路径
   - 具体表现：本地显示正常，部署后图片丢失
   - 解决方案：使用相对路径 `![](../img/xxx.jpg)`
- 3.主题不生效
   - 具体表现：修改配置后无变化
   - 解决方案：执行 hexo clean && hexo g 清理缓存
- 4.Git部署失败	
   - 具体表现：权限错误或分支冲突
   - 解决方案：检查SSH密钥或强制推送 git push -f


### 🛠️ 详细问题解析
- 问题1：端口4000被占用
```
# 解决方案A：更换端口
hexo s -p 5000  # 使用5000端口

# 解决方案B：查找并终止占用进程
# Windows
netstat -ano | findstr :4000
taskkill /PID [进程号] /F

# macOS/Linux
lsof -i :4000
kill -9 [进程号]
```
- 问题2：图片资源管理
推荐的文件结构：
```
source/
├── _posts/          # 文章目录
│   └── 2024-10-11-hexo-tutorial.md
└── img/             # 图片目录
    ├── bg14.jpg     # 封面图
    └── screenshots/ # 截图目录
```
图片引用方式：
```
<!-- 相对路径引用（推荐） -->
![描述文字](../img/bg14.jpg)

<!-- 绝对路径引用 -->
![描述文字](/img/bg14.jpg)
```



## 📚 学习资源推荐


### 🎥 视频教程
**推荐教程：**[@Hexo+Butterfly完整搭建 ](https://www.bilibili.com/video/BV1Ko4y1S7mv)
- 时长：2~3个小时
- 特点：教学视频详细
- 适合人群：完全新手
**补充学习：**
[@Hexo官方入门指南](https://hexo.io/zh-cn/docs/)
[@Butterfly主题配置](https://butterfly.js.org/posts/21cfbf15/)


### 📖 文档资源
1.**官方文档**（必读）
- [@Hexo中文文档](https://hexo.io/zh-cn/docs/)
- [@Butterfly主题文档](https://butterfly.js.org/posts/21cfbf15/)
2.**问题解决平台**
- GitHub Issues：搜索类似问题
- Stack Overflow：技术问题解答
- CSDN/博客园：中文社区分享
3. **AI助手**（强烈推荐）
遇到问题时的提问模板：
- 1. 问题描述：清晰说明现象
- 2. 错误信息：完整复制报错
- 3. 尝试步骤：已做的解决尝试
- 4. 相关代码：配置文件或代码片段
推荐工具：DeepSeek、ChatGPT等



## 💎 实用技巧分享


### ✨ 写作效率提升
```
# 使用VS Code插件
1. Markdown All in One：增强写作体验
2. Paste Image：直接粘贴截图到文章
3. Hexo Utils：快速生成文章模板

# 文章模板示例
title: "{{ 标题 }}"
date: {{ date }}
tags: [标签1, 标签2]
categories: [分类]
description: {{ 描述 }}
cover: ../img/{{ 封面图 }}

```


### 🚀 自动化部署脚本
```
#!/bin/bash
# deploy.sh - 一键部署脚本

echo "开始清理缓存..."
hexo clean

echo "生成静态文件..."
hexo g

echo "部署到GitHub..."
hexo d

echo "✅ 部署完成！"
```


### 📊 数据备份策略
```
# 需要备份的重要文件：
# 1. source/              # 所有文章和图片
# 2. _config.yml          # 站点配置
# 3. _config.butterfly.yml # 主题配置
# 4. package.json         # 依赖列表
```


## 🎯 总结与建议


### 给新手的建议
- 1.循序渐进：先跑通基础流程，再深度定制
- 2.及时备份：修改配置前先备份原文件
- 3.善用搜索：90%的问题已有解决方案
- 4.参与社区：在GitHub上Star和Follow优秀项目


### Hexo适合谁？
- ✅ 技术写作者：专注内容，无需关心渲染
- ✅ 前端学习者：可深入学习主题定制
- ✅ 学生/个人博主：零成本搭建个人品牌
- ✅ 文档维护者：多文章、多分类管理便捷


### 最终效果
经过一周的搭建和优化，我的博客已具备：
- 📱 响应式设计（手机/平板/电脑全适配）
- 🎨 美观的Butterfly主题界面
- ⚡️ 秒级加载速度（GitHub Pages + CDN）
- 🔍 SEO优化（自动生成sitemap）
- 📈 访问统计（Google Analytics集成）



## 🌟 写在最后
博客不仅是技术记录，更是思考的延伸和成长的见证。Hexo给了我一个简单却强大的起点，让我能专注于写作本身，而非技术实现。
<br>

资源汇总：
[@🔗Hexo官网](https://hexo.io/zh-cn/)
[@🔗Butterfly主题文档](https://butterfly.js.org/)
[@🔗Hexo+Butterfly完整搭建视频教学 ](https://www.bilibili.com/video/BV1Ko4y1S7mv)
[@🔗我的博客GitHub网页](https://github.com/xiaoxiaoyu-123/xiaoxiaoyu-123.github.io)
希望这篇记录能帮助到同样想搭建个人博客的你。如果有任何问题，欢迎分享交流！💬

