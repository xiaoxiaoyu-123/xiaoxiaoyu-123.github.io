# 变更记录（CHANGELOG）

记录博客项目的所有结构变动、配置修改、内容发布与 skill 调整。**新条目追加在文件顶部**，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

## [2026-10-27] 🚀 首次自动部署成功——重构成果全量上线

- push `source` → Actions 构建 → Pages 部署，全链路 success
- 线上验证通过：本地搜索索引、鲸鱼娘看板娘、Umami 统计、文章页 Giscus、玫红主色、12 篇新封面、16:9 卡片、最新文章《AI全栈心理健康助手项目》
- 本机网络注意：GitHub 直连不通，git 已配置 github.com 专用代理（`http.https://github.com.proxy=127.0.0.1:33210`），**推送前需开启代理工具**

## [2026-10-27] GitHub Actions 自动部署配置完成

### 新增
- `.github/workflows/deploy.yml`：push `source` 分支 → Node 20 + npm ci + hexo generate → peaceiris/actions-gh-pages 推 main 分支
- 使用内置 `GITHUB_TOKEN`（permissions: contents: write），**无需在 GitHub 配置任何 Secret/Deploy Key**
- Pages 保持「main 分支 / root」构建方式不变，内置 token 的推送会正常触发 Pages 构建
- 本地主分支 `main` 改名为 `source`（源码分支），远程 `origin` 已配置

### 新的发布方式
```
git add -A && git commit -m "..." && git push
```
push 即发布；任何电脑无需本地 Hexo 环境即可更新博客。旧的手动 `hexo deploy` 保留为备用通道。

### 待办
- ⚠️ 首次 `git push -u origin source` 因本机当前无法直连 GitHub（代理工具未开）暂未执行；开代理后推送即触发首次自动部署

## [2026-10-27] 统计接入 Umami Cloud（免服务器方案）

### 背景
- 服务器 2C2G 且已跑多个容器，自托管 Umami + PostgreSQL 内存不足（安装失败），改用官方云托管

### 变更
- 主题启用 `umami_analytics`：`serverURL` 留空走 Umami Cloud（`https://cloud.umami.is/script.js`），website_id `215130f2-7efc-4218-b160-8df1a92d1906`
- `data-domains: xiaoxiaoyu-123.github.io`：只统计正式域名，本地预览不污染数据
- 站内 UV/PV 数字暂不展示（需要 API 密钥且会暴露在前端）；busuanzi 暂时保留用于页面数字展示
- 验证：生成页面包含脚本地址、website_id、域名白名单、手动 track；Umami Cloud 脚本 HTTP 200
- 服务器侧可卸载自托管的 umami 与 PostgreSQL 释放内存（待用户操作）

## [2026-10-27] Giscus 评论区上线

### 新增
- 主题 `comments.use: Giscus`：repo `xiaoxiaoyu-123/xiaoxiaoyu-123.github.io`、repo_id `R_kgDOP_riHQ`、General 类别 id `DIC_kwDOP_riHc4DJubq`（经 giscus 官方 API 查询确认）
- 配置项：中文界面（data-lang: zh-CN）、reactions 开启、懒加载（滚到评论区才加载）、明暗主题自动切换
- 验证：文章页 giscus-wrap 容器与全部参数在位；`comments: false` 的关于页正确不渲染评论

## [2026-10-27] 看板娘更换：miku Live2d → 开源鲸鱼娘（dsh-whale-musume）

### 变更
- 接入 [dsh-whale-musume](https://github.com/Sutera-Diffusus/dsh-whale-musume)（MIT）：`assets/` 三件套 + 92 张立绘自托管至 `source/assets/`（13MB），Butterfly inject 挂载 `whale-moe-core.js` + `dsh-whale-moe.js`
- 下线 miku Live2d 注入块（git 历史可回滚）；L2Dwidget 外链依赖清零

### 移植要点（DSH 宿主 → Hexo）
- 该桌宠的核心（状态机+表现层）**零宿主依赖**，立绘根路径 `/assets/generated/` 与 Hexo 根路径部署天然匹配，无需改它一行代码
- DSH 专属功能自动降级：工作姿态联动、设置面板、TTS 语音在博客上不可用；保留：立绘/空闲动作/点击台词/拖拽/贴边探头/视线跟随鼠标/养成数据（localStorage）
- 已验证：脚本挂载 3 处、L2Dwidget 残留 0、立绘 HTTP 200、`[data-dsh-whale-root]` 成功渲染且图片加载成功

## [2026-10-27] 阶段三：性能选项 + 主题深度定制完成

### 性能
- 原生 lazyload（`native: true`）：全站图片 `loading='lazy'`，首屏不再全量加载
- fancybox 灯箱：文章图片可点击放大
- instantpage：悬停预加载下一页
- **CDN 全本地化**：安装 hexo-butterfly-extjs 1.5.8，`third_party_provider: local`，fancybox/instantpage/fontawesome 等主题资源全部走 `/pluginsSrc/`——代理软件没开时页面加载慢的问题顺带解决（仅剩 Live2d 模型与 typed.js 两处外链）

### 主题
- `theme_color` 启用玫红主色系（#ff7c9c）：链接/分页/滚动条/引用等与粉色站点底色统一，替换默认蓝
- 暗色模式配色适配：页面底色 #1f1a20 暗玫瑰、卡片阴影加深，夜间不再粉底刺眼

### 验证
- 302 文件生成；首页/文章页 HTML 确认 lazy 属性、fancybox 本地资源、暗色 CSS、玫红主色（css/index.css）
- 预览服务已重启（HTTP 200）

## [2026-10-27] 阶段二决策记录：Giscus + Umami 自托管 + 保持 permalink

### 决策
- 评论系统选定 **Giscus**（GitHub Discussions，零成本）；待用户在 GitHub 开启 Discussions、安装 giscus App 后提供 repo_id/category_id
- 站点统计选定 **Umami 自托管**（1Panel 应用商店部署）；待用户提供 serverURL + website_id 后接入并下线 busuanzi
- permalink 评估结论：**保持日期式 URL 不变**（避免断链，收益不值得）

## [2026-10-27] 阶段二第一批：本地搜索 + 占位符清零 + 分类规范化

### 新增
- 本地搜索：hexo-generator-searchdb 1.5.0，主题启用 `local_search`，生成 search.json（27 条全站索引）；Butterfly 搜索弹窗对 json 格式自动兼容

### 修正
- 占位符全部清零：社交邮箱（原 xxxxxx@gmail.com）、侧栏 Follow Me 按钮（原 github.com/xxxxxx）、公告文案（原 "This is my Blog"）
- 友链数据 `_data/link.yml`：Hexo 模板默认内容（繁体示例站）→ 真实建站工具条目 + 友链添加模板注释
- 音乐页：补上介绍内容，修复 front-matter `descriptiao` 拼写错误
- 分类规范化 8 处：错挂修正（《Agent开发实习》→[前端,求职]）、空分类补齐（《关于暑假的计划》→[学习]）、近义合并（电脑清理/电脑系统→[电脑技巧]，生活随想→[随笔]）、命名规范（去括号空格、lucky-canves→lucky-canvas）
- SEO：keywords 中文逗号 → 英文逗号

### 环境注意
- 本机系统环境变量残留死代理 `127.0.0.1:33210`（代理软件未开时），会拖慢 npm/浏览器外链请求；npm 操作需临时置空 `HTTP_PROXY/HTTPS_PROXY`

## [2026-10-27] 首页卡片封面框锁定 16:9

### 变更
- `_config.butterfly.yml` inject.head 新增 CSS：首页卡片封面框 `aspect-ratio: 16/9` 与海报同比例（桌面端封面占宽 42%→47%，移动端全宽），`object-fit: cover` 不再裁掉海报两侧标题
- 已在本地 1400px 桌面与 480px 移动端实测：封面框均为 1.78（16:9），整张海报完整显示；其他卡片布局不受影响

## [2026-10-27] 全站封面铺开完成：12 篇文章换上新海报

### 新增
- `.claude/poster-work/gen_posters_seedream.py`：**整张海报一次生成**流水线（角色垫图 + 图库海报风格参考双输入，文案读 configs/*.json），不再依赖 HTML 排版层

### 变更
- 11 篇旧 SenseNova 封面 + 1 篇错挂封面全部替换为 Seedream flash 整张海报（1920×1080 JPG，276~337KB）
- 角色按主题分配（12 个角色全部出场）：1Panel→leo、CSS→libra、Git→gemini、HTML→aries、Linux→sagittarius、Markdown→virgo、MySQL→aquarius、Hexo→asahi-shio、评教→komazawa-noi、部署→taurus、前端项目→cancer、AI全栈→osawa-mahiro
- 《AI全栈心理健康助手项目》cover 从错挂的 linux 海报改为专属新图

### 质检经验（沉淀在 03 方案 §5）
- flash 文字准确率约 80%/张；底部信息条与带文字气泡是乱码重灾区（已从模板移除）
- 角色锁定必须把 profile 的 appearance 外貌描述写进 prompt，仅靠垫图+一句 same hairstyle 不够
- 三轮迭代共生成 22 张（含重做），全部逐张目检后交付

## [2026-10-27] 阶段一「地基治理」完成（6 个 git 提交）

### 版本控制
- `git init`（main 分支），改造前原状先做基线提交，之后每项改动独立提交可回滚
- 新增 `.gitignore`（public、node_modules、.deploy_git、db.json、海报产物）

### 清理
- 删除 `source/_posts/test.vue`、`_config.landscape.yml`
- 移除 `symbols_count_time` 死配置、`_config.yml` 与 `_config.butterfly.yml` 两处失效 live2d 配置
- 卸载 11 个依赖：hexo-theme-landscape、hexo-helper-live2d、9 个 live2d 模型包
- **Live2d 收敛为唯一配置源**：`_config.butterfly.yml` inject.bottom 的 L2Dwidget 脚本（miku，右侧）

### 图片
- 11 张 anime-tech 封面 PNG→JPG：18MB→2MB（单张 ≤244KB）；`source/img` 总体积 33MB→15MB
- 首页横幅、2 篇文章 cover、2 张正文截图同步压缩；16 篇文章引用路径已同步
- 补齐主题缺失图片：favicon（头像裁切）、bg03~06 横幅、404.jpg、friend_404.gif
- 修复文章内失效引用：HTML速通补 `.png` 后缀、纠正 `post-html03` 笔误、每周总结三移除丢失的 zj03、搭载之旅示例图转行内代码

### 验证结果（hexo clean && generate）
- 247 文件 / 130 页生成成功；最新文章《AI全栈心理健康助手项目》已在 `public/2026/10/19/`
- 页面引用图片无缺失（代码块内示例路径除外）；L2Dwidget / typed.js / favicon 全部正常
- 待用户确认后执行 `hexo deploy`

### 遗留
- `source/img/zj01.jpg`（818KB）、`preview.jpg`（717KB）无任何引用，待用户决定是否删除

## [2026-10-27] 改造完成：全量角色库建成，流水线正式切换 Seedream 5.0 flash

### 角色库（.claude/poster-work/characters/）
- 用户图库 21 张图全部登记：**20 个角色**（11 星座原创 + 4 编程海报原创 + 5 个 IP 角色）+ 1 张十二星座合照参考图（`ref-zodiac-group.png`）
- 每个角色：prototype.png（垫图）+ profile.json（外观/性格/色板/适用主题）；总目录 index.json
- IP 角色（温迪/初音未来/平泽唯/阿斯托尔福/雪之下雪乃）在 profile 中标注版权风险提示，谨慎使用
- 图库缺摩羯座单卡（合照里有），以后补图可用 build_characters.py 登记

### 流水线切换
- `gen_bases_seedream.py` 默认模型改为 **doubao-seedream-5-0-flash-260915**（15s/张）；pro 留作重点封面
- `anime-tech-poster` skill 第 28 节执行流水线整体重写：脚本表、单篇流程（候选图挑选环节）、prompt 硬要求、水印方案（API watermark:false 取代版式遮挡）、批量注意事项
- 旧 SenseNova 流水线（gen_bases.py）标记退役留档

### 待办
- 全站封面铺开（03 方案 §5）：27 篇逐篇垫图生成 → 挑图 → 换 cover → 压缩 → 清理旧大图

## [2026-10-27] 路线 A 实施启动：垫图流水线跑通，试产封面完成

### 新增（.claude/poster-work/）
- `characters/asahi-shio/`、`characters/leo/`：角色原型库（原型图已从用户图库拷贝入项目 + profile.json 角色档案）
- `gen_bases_seedream.py`：火山方舟 Seedream 5.0 垫图生成脚本（替代 SenseNova 后端；含重试、THEMES 主题注册表、候选图机制）
- `configs/vue3springboot.json` + `poster-vue3springboot.png`：《AI全栈心理健康助手项目》试产完整封面（1920×1080）

### 决策与验证
- 开通并验证 Seedream 5.0 双模型：**flash（15s/张）定为默认主力，pro（3min/张）留给重点封面**；两者角色一致性均达标
- 踩坑记录：5.0 不支持 `sequential_image_generation` 参数（4.0 的），报 400
- 全部调用细节沉淀在 [03-封面图生成改造方案.md](03-封面图生成改造方案.md) §4.5

### 试产结果
- 底图 2560×1440 约 250KB/张，角色与原型库人物可辨识为同一人
- 完整封面：左侧排版信息 + 右侧角色，文字全部清晰无乱码
- 待用户验收后：《AI全栈心理健康助手项目》cover 替换（现为错用的 Linux 海报），随后按 §5 计划全站铺开

## [2026-10-27] 封面图生成改造方案定稿（路线 A）

### 决策
- 确定封面底图方案为**路线 A：垫图生成**——用「参考图垫图」能力把用户角色原型（`C:\Users\xinan\Pictures\二次元高清图`，21 张高质量 AI 人设卡）作为固定角色生成封面，替换现有 SenseNova 纯文生图后端
- 模型选型查证结论：**Seedream 4.0/5.0（火山方舟）** 为唯一胜任选项（CogView-4 不支持垫图；GLM/DeepSeek 为文本模型无生图能力）

### 新增
- `docs/03-封面图生成改造方案.md`：改造设计（角色原型库、gen_bases_seedream.py、候选图机制）、存量 27 篇文章批量换封面计划、验收标准

### 待办
- 用户开通火山方舟并配置 `ARK_API_KEY` 后开始实施
- 实施完成后全站封面统一重建

## [2026-10-26] 文档体系建立

### 新增
- 建立 `docs/` 维护文档目录（不参与 Hexo 构建，不会被发布）
- `docs/01-项目结构分析.md`：首次全项目结构扫描报告（技术栈、目录、依赖、内容、问题清单 P0/P1/P2）
- `docs/02-重构优化方案.md`：三阶段重构任务清单（地基治理 → 功能补全 → 视觉与架构升级）
- `docs/CHANGELOG.md`：本变更记录

### 重要发现（待处理，详见 02-重构优化方案.md）
- 最新文章《vue3+SpringBoot全栈项目》(2026-10-19) 尚未生成部署
- 项目根目录无 git 版本控制
- Live2d 存在三处互相矛盾的配置
- 6 处主题图片引用指向不存在的文件（favicon、bg03~06、404 占位图）
- 封面图 PNG 单张约 1.8MB，首页加载体积过大
