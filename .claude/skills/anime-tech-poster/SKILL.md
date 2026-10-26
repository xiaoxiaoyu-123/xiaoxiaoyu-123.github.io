---
name: anime-tech-poster
description: 为技术博客文章生成「二次元角色 × 技术科普」的 PC 横屏海报（1920×1080），并自动存入 source/img、把文章 front-matter 的 cover 接上。当用户说「生成海报」「做张封面图」「把这篇博客的封面换掉」「配一张 anime tech 海报」「批量给博客换封面」时使用。内置完整视觉规范（5 级信息层级、左信息右角色、底部信息条）与本项目已跑通的流水线（角色垫图生成底图 → 排版 → 截图 → 接入 cover），内置 20 个角色原型库（.claude/poster-work/characters/），底图默认由火山方舟 Seedream 5.0 flash 垫图生成。
---

# Anime Tech Blog Visual System Skill
## 「二次元角色 × 技术科普 × 推荐宣传」PC 横屏统一视觉系统

---

> **本项目已实现自动化流水线，不要手写 HTML 或手工调坐标。** 脚本、配置样板和踩过的坑
> 都在 `.claude/poster-work/`，用法与坑位见文末**第 28 节**。以下第 1–26 节定义视觉规范，
> 脚本按规范实现。

## 0. Skill 定位

你是一名负责「技术内容视觉化 + 二次元角色视觉设计 + 信息图海报设计」的视觉设计师。

目标不是单独生成一张漂亮的动漫图，而是建立一套可以持续用于技术博客的**系列化视觉系统**。

用户的技术博客主要通过 PC 端访问，因此：

- 所有主视觉默认采用 **16:9 横屏**
- 推荐成品尺寸：**1920 × 1080**
- 也可使用 2560 × 1440、1600 × 900
- 不采用传统手机海报/竖版招新海报的构图比例
- 需要保证在 PC 浏览器作为博客 Hero Background / Banner / Header 时仍然清晰
- 同一系列不同技术文章必须拥有明显的统一品牌感，同时允许技术主题、角色、配色、图标和代码发生变化

核心视觉关键词：

> **Anime Character + Developer Culture + Technical Infographic + Editorial Poster + Tech Education + Recommendation Campaign + Clean UI + Premium Illustration**

---

# 1. 核心视觉目标

最终画面应让用户第一眼感受到：

> 「这是一套属于程序员 / 技术博客的二次元技术知识海报。」

而不是：

> 「一张普通动漫壁纸上随便加了一些代码。」

因此必须同时满足三个层次：

### 第一层：角色视觉吸引力

- 原创二次元角色
- 角色必须与技术主题产生视觉联系
- 角色占画面约 35%～45%
- 角色是视觉焦点之一，但不能遮挡主要文字
- 人物姿态自然、具有轻微动态
- 避免纯站桩证件照式人物

### 第二层：技术主题识别

用户必须快速知道当前主题是什么：

- JavaScript
- Vue 3
- TypeScript
- MySQL
- MyBatis
- Linux
- Docker
- Git
- Spring Boot
- React
- Node.js
- Redis
- Kubernetes
- Kafka
- Elasticsearch
- Python
- C/C++
- AI / LLM
- 等等

技术名称应该成为画面的第二核心视觉。

### 第三层：知识科普

不能只有 Logo 和技术名称。

需要用少量高价值信息表达：

- 技术是什么
- 核心特性
- 常见能力
- 使用场景
- 技术生态
- 为什么值得学习
- 与博客主题对应的知识关键词

---

# 2. 统一横屏母版

默认使用：

> **1920 × 1080 / 16:9**

推荐采用以下空间结构：

```text
┌─────────────────────────────────────────────────────────────┐
│  顶部：系列标签 / 推荐标签 / Blog Category                 │
│                                                             │
│  ┌──────────────────────┐       ┌────────────────────────┐ │
│  │                      │       │                        │ │
│  │  技术主题区域         │       │                        │ │
│  │                      │       │       二次元角色        │ │
│  │   TECH NAME          │       │                        │ │
│  │   技术中文标题        │       │   与技术主题融合        │ │
│  │                      │       │                        │ │
│  │   技术关键词          │       │                        │ │
│  │                      │       │                        │ │
│  ├──────────────────────┤       │                        │ │
│  │ 核心特性  核心能力    │       │                        │ │
│  │ 应用场景  技术生态    │       │                        │ │
│  └──────────────────────┘       └────────────────────────┘ │
│                                                             │
│  ┌───────────────────────┐    ┌──────────────────────────┐ │
│  │   Code Editor          │    │ 为什么选择 / 核心知识点   │ │
│  │   代码示例             │    │ ✓ xxx                    │ │
│  │   技术关键词           │    │ ✓ xxx                    │ │
│  └───────────────────────┘    └──────────────────────────┘ │
│                                                             │
│  底部：应用领域 / 技术生态 / 技术关键词 / 博客系列标识      │
└─────────────────────────────────────────────────────────────┘
```

---

# 3. 横屏构图原则

## 3.1 左右分区

默认：

### 左侧 50%～55%

负责信息：

- 推荐标签
- 技术名称
- 中文标题
- Slogan
- 核心特性
- 技术简介
- Code Editor
- 知识卡片

### 右侧 45%～50%

负责：

- 二次元角色
- 技术相关道具
- 技术视觉符号
- 大型 Logo / 抽象图形
- 氛围光效

人物可以轻微突破右侧边界，但不能影响主要文字阅读。

---

# 4. PC 阅读安全区

因为最终用于技术博客网页背景，需要特别注意：

### 左侧安全区

保证：

- 博客标题
- 技术名称
- 主要摘要

不会贴近边缘。

建议左右至少保留：

> 70～100 px

### 上方安全区

至少：

> 50～70 px

### 下方安全区

至少：

> 60 px

### 重要文字不要放在：

- 人物脸部
- 人物头发高对比区域
- 复杂背景纹理
- 强光区域

---

# 5. 视觉层级

必须建立明确的 5 级层级：

### Level 1：技术名称

最大文字。

例如：

> JavaScript

> VUE 3

> TYPESCRIPT

> MYSQL

> DOCKER

> SPRING BOOT

推荐占左侧视觉区域约 20%～30%。

---

### Level 2：文章主题

例如：

> Vue 3 响应式原理

> TypeScript 类型系统

> MySQL 索引与查询优化

> Spring Boot 自动配置原理

字体明显小于技术名称。

---

### Level 3：核心关键词

例如：

> Composition API · Reactivity · Proxy

> Type Safety · Generic · Utility Types

> Index · B+Tree · Transaction · MVCC

---

### Level 4：知识模块

使用 3～5 个卡片：

- 核心能力
- 技术特点
- 应用场景
- 工程实践
- 技术生态

---

### Level 5：装饰信息

例如：

- 代码窗口
- Terminal
- Git Branch
- Database Schema
- API Route
- Docker Container
- Cloud Nodes
- JSON
- CLI
- UI Components

这些元素只能作为辅助。

---

# 6. 「推荐宣传」视觉语言

参考海报中的：

> 「某角色 推荐」

不要机械复制。

技术博客可以转换为：

### 推荐型

> 「XX 推荐」

> 「本期推荐」

> 「技术专题」

> 「开发者必读」

> 「技术入门」

### 知识型

> 「深入理解」

> 「原理解析」

> 「从入门到实践」

> 「源码探秘」

### 系列型

> 「TECH NOTE 01」

> 「BACKEND SERIES」

> 「FRONTEND SERIES」

> 「DATABASE SERIES」

这样可以保留原参考海报的「推荐宣传」气质，同时更适合技术博客。

---

# 7. 二次元角色设计系统

## 7.1 角色必须原创

默认生成：

> original anime-style character

不要要求直接复制已有动漫角色。

角色应该根据技术主题进行设计。

---

## 7.2 角色与技术绑定

### JavaScript

视觉：

- 青绿色
- Web UI
- 浏览器
- JS 图标
- 动态代码
- 前端开发者气质

角色：

> 活泼、灵动、现代前端工程师风格

---

### Vue 3

视觉：

- Vue Green
- Composition API
- Reactive nodes
- Component tree

角色：

> 清新、轻盈、现代 UI 工程师

---

### TypeScript

视觉：

- 蓝色
- 类型系统
- Interface
- Generic
- Type Graph

角色：

> 理性、专业、工程师气质

---

### MySQL

视觉：

- 蓝色 / 深蓝
- Database
- Table
- SQL
- Index
- Query

角色：

> 数据库工程师 / 数据分析师

可加入：

- 数据表
- SQL 查询窗口
- 数据节点

---

### MyBatis

视觉：

- 深蓝
- Java
- XML
- Mapper
- SQL

角色：

> Java 后端开发者

视觉道具：

- XML 文件
- Mapper
- SQL
- Java Bean

---

### Linux

视觉：

- 深色
- Terminal
- Shell
- Command Line
- File System

角色：

> 冷静、专业的系统工程师

---

### Docker

视觉：

- 蓝色
- Container
- Docker whale
- Image
- Container
- Kubernetes nodes

角色：

> 云原生 / DevOps 工程师

---

### Git

视觉：

- 橙红色 / 深色
- Branch
- Commit
- Merge
- Repository

角色：

> 版本控制 / 软件工程主题角色

可以加入：

```text
main
dev
feature/login
commit
merge
```

---

### Spring Boot

视觉：

- Spring Green
- Java
- REST API
- Microservice
- Dependency Injection

角色：

> 企业级后端工程师

---

# 8. 角色动作

避免：

> 正面站立 + 双手自然垂下

优先：

- 手持平板
- 手持笔记本
- 操作电脑
- 查看代码
- 操作终端
- 指向技术图表
- 手持数据库结构
- 与代码窗口互动
- 坐在开发桌旁
- 轻微回头
- 向画面另一侧伸手

动作应该服务于技术主题。

---

# 9. 技术道具系统

根据主题自动生成：

### Frontend

- Browser
- UI Components
- DOM Tree
- CSS Grid
- API
- Code Editor

### Backend

- Server
- API
- Database
- Microservices
- Request / Response

### Database

- Tables
- SQL
- Index
- Query
- ER Diagram
- Data Nodes

### DevOps

- Terminal
- Docker Container
- Cloud
- Pipeline
- Git Branch

### AI

- Neural Network
- Token
- Transformer
- Embedding
- Vector Database
- Model Architecture

---

# 10. Code Editor 模块

参考海报必须保留：

> 一个视觉化代码编辑器窗口

但代码必须服务于当前博客。

例如 Vue：

```vue
<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>

<template>
  <button @click="count++">
    {{ count }}
  </button>
</template>
```

MySQL：

```sql
SELECT *
FROM user
WHERE status = 1
ORDER BY created_at DESC;
```

Git：

```bash
git checkout -b feature/login
git add .
git commit -m "feat: add login"
git merge main
```

Docker：

```dockerfile
FROM node:20

WORKDIR /app
COPY . .

RUN npm install
CMD ["npm", "run", "dev"]
```

注意：

> AI 图片生成模型容易生成错误代码，因此代码窗口主要承担「程序员视觉符号」作用；如果需要真正可读的代码，应在后期排版时叠加真实代码。

---

# 11. 技术科普卡片

每张图推荐 3～5 个卡片。

统一结构：

```text
ICON

核心能力
一句简洁说明
```

例如 Vue 3：

```text
⚡ 响应式
基于 Proxy 构建现代响应式系统

🧩 组件化
通过组件复用构建复杂界面

🚀 Composition API
更灵活地组织业务逻辑

🌐 生态完善
Router / Pinia / Vite 等工具链
```

不要堆大量正文。

原则：

> **背景图负责「认识主题」，博客正文负责「深入学习」。**

---

# 12. 底部信息条

底部建议设置一个完整的技术应用导航条。

例如 Vue：

```text
Vue 3

Component      Router       Pinia       Vite       SSR
组件化          路由          状态管理      构建工具      服务端渲染
```

例如 MySQL：

```text
MySQL

Storage Engine · Index · Transaction · MVCC · Replication
```

例如 Docker：

```text
Docker

Image · Container · Volume · Network · Registry
```

底部区域必须保持统一高度和结构。

这会成为整个博客系列的重要识别元素。

---

# 13. 背景设计

不要使用纯白背景。

推荐：

> 柔和浅色背景 + 技术主题色 + 半透明 UI 图形

可以使用：

- 大型技术 Logo
- 网格
- 点阵
- 线路
- 数据节点
- 几何图形
- 代码字符
- 半透明窗口
- 光晕
- 粒子
- 抽象流线

但背景必须低对比。

原则：

> **背景负责氛围，文字负责信息，人物负责吸引力。**

---

# 14. 配色系统

每一种技术拥有自己的主题色，但整体饱和度控制一致。

推荐：

| 技术 | 主色方向 |
|---|---|
| JavaScript | 黄色 + 黑色 |
| Vue | 绿色 + 深灰 |
| TypeScript | 蓝色 + 深蓝 |
| MySQL | 蓝色 + 深蓝 |
| MyBatis | 蓝紫 / 深蓝 |
| Linux | 深灰 + 蓝紫 |
| Docker | 天蓝 + 深蓝 |
| Git | 橙红 + 深灰 |
| Spring Boot | 绿色 + 深灰 |
| React | 青蓝 |
| Node.js | 绿色 |
| Python | 蓝黄 |
| Redis | 红色 |
| Kubernetes | 蓝色 |
| Kafka | 深灰 / 红色 |
| Elasticsearch | 黄色 / 黑色 |
| AI / LLM | 紫蓝渐变 |

注意：

> 主色不同，但明度、背景亮度、卡片透明度、边框处理应该保持统一。

---

# 15. 字体系统

中文：

- 思源黑体
- HarmonyOS Sans
- 阿里巴巴普惠体
- Noto Sans CJK
- 现代无衬线字体

英文技术名称：

- Inter
- Helvetica Neue
- Montserrat
- DIN
- Space Grotesk
- IBM Plex Sans

代码：

- JetBrains Mono
- Fira Code
- Source Code Pro

技术名称允许使用：

> 超大英文无衬线字体 / 半衬线字体

但必须保证 PC 阅读清晰。

---

# 16. UI 卡片设计

统一采用：

> 白色 / 半透明白色 + 轻边框 + 轻阴影 + 圆角

避免：

- 大面积厚重阴影
- 过度玻璃拟态
- 太多渐变
- 卡片全部漂浮
- 每个模块形状完全不同

统一组件语言比单张图片的花哨程度更重要。

---

# 17. 装饰元素

可以使用：

- ✦ 星星
- 小圆点
- 心形
- 几何线
- 技术图标
- 花瓣
- 光点
- 数据节点
- 代码符号
- `{ }`
- `</>`
- `#`
- `<>`
- `[]`
- `//`
- `git branch`
- `SQL`
- `API`

但是：

> 装饰元素数量控制在「丰富但不嘈杂」。

二次元风格可以可爱，但整体仍然要具有：

> **技术博客 / 开发者文化 / 专业信息设计**

而不是纯萌系壁纸。

---

# 18. 博客背景的特殊规则

这是本 Skill 与普通招新海报最大的区别。

因为图片最终用于：

> PC 技术博客背景图

所以必须遵守：

### 不要

- 把所有文字塞满
- 使用过长正文
- 人物覆盖标题
- 角色脸部处于文字区
- 底部放过多小字
- 使用手机海报式超高信息密度
- 让背景比博客正文更抢眼

### 要

- 大标题
- 少量核心信息
- 大面积留白
- 明确视觉焦点
- 技术元素
- 二次元角色
- 统一 UI 卡片
- 可作为网页 Hero Background

---

# 19. 推荐信息密度

一张图建议：

### 大标题

1 个

### 副标题

1～2 个

### 技术关键词

3～5 个

### 科普卡片

3～5 个

### Code Editor

1 个

### Why / 核心知识

3～5 条

### 底部应用领域

4～6 个

不要超过这个范围。

---

# 20. 系列统一规则

无论技术是什么，都保持：

```text
统一：
├── 16:9
├── 左信息 / 右人物
├── 超大技术名称
├── 推荐标签
├── 技术关键词
├── 科普卡片
├── Code Editor
├── Why / 核心知识
├── 底部应用领域
├── 二次元角色
├── 技术主题色
└── 轻量科技背景

变化：
├── 角色
├── 服装
├── 动作
├── 主色
├── 技术 Logo
├── 技术道具
├── 代码
├── 知识点
└── 应用场景
```

---

# 21. 单篇博客生成流程

当用户提供一篇技术博客时：

## Step 1：识别技术

提取：

- 技术名称
- 技术分类
- 版本
- 文章主题

例如：

> Vue 3 响应式原理

识别为：

```text
Technology: Vue 3
Category: Frontend
Topic: Reactivity
```

---

## Step 2：提取知识点

从文章中提取：

- 3～5 个核心知识点
- 3～5 个技术关键词
- 3～5 个应用场景

---

## Step 3：生成视觉主题

确定：

- 主色
- 辅色
- 背景元素
- 技术 Logo
- 技术道具
- UI 风格

---

## Step 4：生成原创角色

角色必须：

- 符合技术主题
- 有明确职业属性
- 与技术道具互动
- 具有青春、轻快、专业的气质
- 保持二次元商业插画质感

---

## Step 5：生成横屏构图

必须采用：

> 16:9 horizontal composition

推荐：

> 左侧信息 + 右侧角色

---

## Step 6：生成文字系统

自动生成：

```text
[推荐标签]

TECHNOLOGY

中文文章标题

核心 Slogan

关键词

核心特性

技术科普

代码窗口

为什么值得学习

应用领域
```

---

## Step 7：最终检查

检查：

- 是否横屏
- 是否 16:9
- 是否适合 PC
- 文字是否有安全边距
- 人物是否遮挡文字
- 技术主题是否明确
- 配色是否统一
- 信息是否过载
- 是否具有系列感
- 是否像技术博客，而不是普通动漫壁纸

---

## Step 8：产出图片与自动接入博客（必做）

终检通过后，必须完成两步交付（详细规范见第 27 节）：

1. 将成品图片保存到博客图片目录 `source/img`
2. 打开对应的博客文档（`source/_posts` 下的 .md），把 front-matter 中的 `cover` 字段更新为该图片的相对路径

只有这两步都完成，本任务才算结束。

---

# 22. 图像生成 Prompt 母版

生成图像时可以基于以下模板：

```text
Create a premium 16:9 horizontal anime-style technology editorial poster
for a modern developer technical blog.

Theme:
[TECHNOLOGY]

Article topic:
[ARTICLE TOPIC]

Visual identity:
anime character + developer culture + technical education +
technology recommendation campaign + modern editorial infographic.

Composition:
1920x1080 landscape.
Left side contains the information hierarchy.
Right side contains one original anime-style character.
Strong visual balance between typography, technical UI elements,
and character illustration.

Left information area:
- recommendation badge
- huge technology name "[TECH NAME]"
- Chinese article title "[TITLE]"
- short technical slogan
- 3-5 technical keywords
- 3-5 concise technical feature cards
- one code editor window
- one "Why choose / Core knowledge" card

Right character:
one original anime-style character designed specifically
around [TECHNOLOGY].
The character should interact with technology-related objects,
such as [TECH OBJECTS].
Dynamic but elegant pose.
High-quality anime illustration.
Clean line art.
Detailed hair and clothing.
Professional developer aesthetic.

Technology visual language:
[TECH VISUAL ELEMENTS]

Color palette:
primary [COLOR]
secondary [COLOR]
background [COLOR]

Background:
soft editorial technology background,
subtle grid,
abstract data lines,
small nodes,
floating UI panels,
technology symbols,
soft glow,
light particles,
low-contrast geometric shapes.

Typography:
large clean modern sans-serif typography,
strong hierarchy,
high readability,
premium editorial layout,
Chinese and English typography integrated naturally.

Bottom:
a clean technology ecosystem strip containing
[APPLICATIONS / ECOSYSTEM].

Style:
high-end anime technology magazine,
modern developer poster,
clean infographic,
professional technical blog hero image,
premium Japanese-inspired editorial design,
balanced whitespace,
soft lighting,
sharp details,
cohesive visual system.

Avoid:
vertical poster,
mobile composition,
excessive text,
crowded layout,
photorealistic character,
random unrelated objects,
low-quality anatomy,
text covering the face,
overly dark background,
excessive decoration,
generic anime wallpaper,
visual clutter.
```

---

# 23. 重要：AI 生成文字的处理策略

图像模型对中文和代码文字的准确率可能不足。

因此生成时：

### 第一阶段

重点生成：

- 人物
- 构图
- 背景
- 卡片
- 技术视觉元素
- Logo 位置
- Code Editor 位置

### 第二阶段

使用设计软件 / HTML / CSS / Figma / Photoshop 等：

- 重新排版标题
- 添加真实代码
- 添加中文
- 添加技术图标
- 调整字体
- 调整间距

这样可以得到比「一次性让模型生成全部文字」更稳定的结果。

---

# 24. 建议的系列命名

整个博客可以建立一个统一视觉系列：

### 中文

> **TECH · 二次元技术志**

> **开发者技术图鉴**

> **二次元技术科普计划**

> **TECH ANIME SERIES**

### 英文

> **ANIME × TECH**

> **DEVELOPER VISUAL NOTES**

> **TECH CULTURE SERIES**

推荐在每张图片的角落保持一个固定的小型系列 Logo：

```text
ANIME × TECH
TECH NOTE / 2026
```

这样几十篇文章组成一个完整系列后，会形成非常明显的个人博客视觉品牌。

---

# 25. 使用示例

用户输入：

```text
主题：Vue 3
文章：Vue3 响应式原理详解
```

自动输出设计方向：

```text
Technology:
Vue 3

Topic:
Reactivity

Primary:
Vue Green

Character:
清新、现代的前端开发少女

Visual Objects:
Proxy
Reactive Graph
Component Tree
Browser UI
Code Editor

Keywords:
Proxy
Reactive
ref
computed
watch

Cards:
响应式
组件化
Composition API
高性能
生态系统

Bottom:
Vite
Pinia
Vue Router
Nuxt
Vitest
```

---

用户输入：

```text
主题：MySQL
文章：MySQL 索引与 B+Tree 原理
```

自动输出：

```text
Technology:
MySQL

Topic:
Index / B+Tree

Primary:
Database Blue

Character:
数据工程师风格二次元角色

Visual Objects:
Database
Table
B+Tree
Index
SQL Query

Keywords:
B+Tree
Index
Clustered Index
Query
MVCC

Cards:
高效查询
索引结构
事务机制
数据一致性
高并发

Bottom:
SQL
InnoDB
Transaction
Replication
Performance
```

---

# 26. 最终设计原则

始终遵循以下一句话：

> **让人物负责吸引目光，让技术名称负责建立认知，让信息卡片负责解释知识，让代码负责建立开发者氛围，让统一版式负责建立品牌。**

最终不是：

> 「动漫 + 代码」

而应该是：

> **「二次元角色驱动的技术科普视觉系统」**

并且：

> **同一博客系列，即使从 JavaScript 换到 MySQL、从 Linux 换到 Docker，用户仍然应该一眼看出它们属于同一个视觉品牌。**

---

# 27. 产出目录与 Cover 自动接入（项目级规范）

本 Skill 在本博客项目中的固定产出规则。任何一次海报生成任务，都必须遵守本节。

## 27.1 产出目录

所有生成的海报成品图，统一保存到：

> `C:\Users\xinan\my-blog\source\img`

- 成品尺寸 1920 × 1080
- 格式优先 PNG；单张体积超过 2 MB 时可转 JPG / WebP
- 不写入其他任何目录
- 博客中引用时一律使用相对路径，不使用绝对路径

## 27.2 文件命名

统一命名格式：

```text
anime-tech-<技术名小写>-<生成日期 yyyyMMdd>.png
```

示例：

```text
anime-tech-1panel-20260424.png
anime-tech-mysql-20260501.png
anime-tech-docker-20260518.png
```

规则：

- 文件名全部小写，单词之间用 `-` 连接
- 不含空格、不含中文
- 同一技术多篇文章用日期区分
- 文件扩展名必须与实际保存的格式一致（.png / .jpg / .webp）

## 27.3 Cover 自动接入

博客文章统一位于：

> `C:\Users\xinan\my-blog\source\_posts`

每篇文章的 front-matter 中，`cover` 字段负责声明文章封面，例如：

```yaml
---
title: "1Panel配置上服务器"
date: 2026-04-24 21:00:00
description: 从零开始的使用shell脚本给服务器配置上1Panel完整入门指南，包含基础语法、常用标签详解和实战示例
categories: [Linux,shell脚本,1Panel]
tags: [Linux,1Panel,零基础指南]
cover: ../img/anime-tech-1panel-20260424.png
---
```

接入规则：

1. 文章在 `source/_posts` 下，图片在 `source/img` 下，因此 cover 固定使用相对路径前缀 `../img/`
2. 生成海报后，自动把对应文章的 `cover` 更新为 `../img/<新文件名>`
3. 只修改 `cover` 这一行；`title`、`date`、`description`、`categories`、`tags` 等其他字段一律不动
4. 若原文档没有 `cover` 字段，在 front-matter 末尾新增一行
5. 若原 `cover` 已指向其他图片，替换后必须在完成汇报中注明原值，便于回滚
6. 顺序固定：先确认图片已实际写入 `source/img`，再修改 cover，避免出现指向不存在文件的死链
7. 若用户同时提供多篇文章，逐一处理，每篇文章的 cover 必须与「技术主题匹配的那张图」对应，不能张冠李戴

## 27.4 单篇文章的完整交付定义

一篇博客的海报任务，只有同时满足以下条件才算完成：

- [ ] 图片已保存到 `source/img`，命名符合 27.2
- [ ] 图片为 16:9 横屏，已通过第 21 节 Step 7 终检
- [ ] 对应文章的 `cover` 已指向新图
- [ ] 完成汇报中列出：图片完整路径、文件名、cover 变更（含原值）

# 28. 本项目执行流水线（落地实现，必读）

第 1–26 节定义的是**视觉规范**；本节是本博客项目里已经跑通的**执行方式**。
接到生成任务时照本节做，不要从零手写 HTML、不要手工调坐标。

## 28.1 脚本位置

全部在 `C:\Users\xinan\my-blog\.claude\poster-work\`：

| 文件 | 作用 |
|---|---|
| `gen_bases_seedream.py` | **当前主力**：调火山方舟 Seedream 5.0（默认 flash-260915）以角色垫图生成底图（右侧角色 + 左侧留空），候选图落 `bases-seedream/` |
| `characters/<en>/` | 角色原型库：`prototype.png`（垫图参考）+ `profile.json`（外观/性格/色板/适用主题）；总目录 `characters/index.json` |
| `build_characters.py` | 从用户图库（`~/Pictures/二次元高清图`）登记角色的工具，图库加新图后往 CATALOG 加条目重跑 |
| `clean.py` | 抹掉 AI 底图自带的乱码英文标题（Seedream 时代偶尔还用得上） |
| `build_poster.py` | 读 JSON 配置 → 生成 1920×1080 的 HTML 海报 |
| `render.py` | Playwright + Chrome 截图 HTML → PNG |
| `configs/<slug>.json` | 每篇文章的文案配置（标题/关键词/卡片/代码/底栏） |
| `gen_bases.py` / `clean_base.py` | 旧 SenseNova 流水线，**已退役**，留作存档 |

依赖：环境变量 `ARK_API_KEY`（火山方舟，备份在 `~/.ark_key`，勿写入项目）、`Pillow`（预览缩图）、
`opencv-python`（clean.py）、`playwright`（用系统 Chrome，`channel="chrome"`）。

## 28.2 单篇流程

```bash
cd .claude/poster-work
python gen_bases_seedream.py <slug> --char <角色en名> --count 2   # 1. 垫图底图 -> bases-seedream/<slug>-<模型>-<n>.png
# 1.5 挑一张候选（必看：角色一致性 / 左侧留白 / 有无乱码字）；有乱码才需要 clean.py
python build_poster.py configs/<slug>.json poster-<slug>.html    # 2. 配置 -> HTML（config 的 bg 填选中候选路径）
python render.py poster-<slug>.html poster-<slug>.png            # 3. 截图成品
```

然后按第 27 节交付：存 `source/img/anime-tech-<技术>-<文章日期>.png` → 改文章 cover。
`configs/1panel.json` 是字段样板，新增文章只需写一个新的 config。

## 28.3 底图 prompt 的硬要求

`gen_bases_seedream.py` 的 `PROMPT_TMPL` 已经调好，这几条**不能删**：

- `keep her EXACT hairstyle, hair color, eye color, face, outfit`（垫图保角色一致性的关键）
- `LEFT HALF: keep mostly empty ... no objects and no character on the left third`
- `Strictly avoid: any text, letters, numbers, watermark ...`

Seedream 5.0 + API 参数 `watermark:false` 出图无第三方水印，但 **flash 偶发小面积乱码字**
（实测出过 "AFI"），挑图时留意，中招就换候选或补跑一张；pro 基本不出。

## 28.4 clean.py 的三个坑（都踩过，别再重走）

1. **不是所有底图都有乱码文字**，输出 `(no text detected)` 是正常结果而非失败。
2. **人眼对「成形」的低对比图案极其敏感。** 逐像素填充统计上只差 1–2 个色阶，字形却依然
   清晰可辨；必须整块填掉（当前做法是逐列纵向插值）。
3. **填充锚点行必须真的干净，且判据要用大尺度背景（301 中值）而不是局部中值。** 标题下方
   常有一块宽软阴影，它大到让局部中值窗口整体落在阴影内、`diff` 塌缩到阈值以下，于是被
   当成背景，锚点又落回墨迹上，填充就从墨色开始渐隐、拖出竖条残影。框还要按「词间距」
   切断，否则会一路扩张到角色身上。

## 28.5 水印由版式解决，不要在图上抹

（SenseNova 时代靠信息条遮水印的旧方案已作废：Seedream 走 API 参数 `watermark:false`，出图无水印。
底部信息条仍保留——它是统一视觉系统的一部分，不再承担遮水印职责。）

## 28.6 批量执行注意

- flash ≈ 15 秒/张、pro ≈ 3 分钟/张（2026-10 实测）；默认 flash，重点封面才用 `--model` 指定 pro。
- 角色按文章气质从 `characters/index.json` 挑（看色板/适用主题字段）；5 个 IP 角色（温迪/初音未来/
  平泽唯/阿斯托尔福/雪之下雪乃）谨慎使用，见各 profile.json 的 note。
- 每张底图必须**单独目视确认**再交付：底图构图（角色是否在右、左侧是否够干净）无法
  靠脚本判断。
- 中途 Chrome 截图偶发超时（内存压力），重跑 `render.py` 即可；建议逐张打印成功/失败。
- API 参数坑：Seedream 5.0 **不支持** `sequential_image_generation`（4.0 的参数），传了报 400。
