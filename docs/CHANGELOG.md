# 变更记录（CHANGELOG）

记录博客项目的所有结构变动、配置修改、内容发布与 skill 调整。**新条目追加在文件顶部**，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

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
