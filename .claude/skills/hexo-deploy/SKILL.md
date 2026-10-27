---
name: hexo-deploy
description: >
  Hexo 博客部署助手（显式触发，绝不自动执行）。仅当用户明确说「部署」「发布博客」
  「更新博客网站」「hexo deploy」「把博客发上去」「我写了新文章，发布一下」时使用。
  流程：先跑 hexo clean + hexo generate 生成本地站点并汇报生成了多少页、哪些文章，
  停下等用户确认；只有用户明确说「发布」「推上去」才执行 hexo deploy 推送到 GitHub Pages。
  绝不在用户没有明确要求时自动生成或部署。
user-invocable: true
---

# Hexo 博客部署助手

> **⚡ 2026-10-27 起主发布通道已更换为 GitHub Actions**：push `source` 分支即自动构建发布
> （workflow 见 `.github/workflows/deploy.yml`，本地主分支已改名 `source`）。
> 用户说「发布」时优先执行：`git add -A && git commit && git push`（推 source 分支，push 即发布）。
> 下方的手动 `hexo deploy` 流程仅作为 Actions 故障时的备用方案。
> ⚠️ 本机直连 GitHub 经常不通，推送前先确认代理工具已开启（系统环境变量指向 127.0.0.1:33210）。

把 `source/` 里的内容发布到公网。核心原则：**只有你明确说「发布」，才会真的推到线上。**

## 为什么必须分两步

`hexo deploy` 会把整个 `public/` 推到 GitHub Pages 的 `main` 分支，**内容立刻对公网可见**，
搜索引擎和 RSS 订阅者都能看到。推错了只能再发一次覆盖——没有「撤销」。

所以本技能把两件事严格拆开：

| 阶段 | 命令 | 影响范围 | 可逆 |
|---|---|---|---|
| **生成** | `hexo clean && hexo generate` | 只动本地 `public/`、`db.json` | ✅ 随便重跑 |
| **部署** | `hexo deploy` | 推送到公网仓库 | ❌ 不可撤销 |

## 触发条件

**使用**（用户明确要求时）：
- 「部署」「发布博客」「更新博客网站」「把博客发上去」
- 「hexo deploy」「我写了新文章，发布一下」

**不使用**（绝不自动触发）：
- 用户只是在写文章、改样式、调主题，没提部署
- 用户问的是 Hexo 的用法或配置（回答问题即可）
- 任何没有明确部署指令的情况

## 本项目固定信息

| 项 | 值 |
|---|---|
| 项目根 | `C:\Users\xinan\my-blog` |
| Hexo 版本 | 7.3.0（`hexo` 已全局可用，无需 npx） |
| 部署目标 | `https://github.com/xiaoxiaoyu-123/xiaoxiaoyu-123.github.io.git` 的 `main` 分支 |
| 线上地址 | https://xiaoxiaoyu-123.github.io/ |
| 部署暂存库 | `.deploy_git/` —— hexo-deployer-git 自己维护，**不要手动进去改** |

> ⚠️ **本项目的 `source/` 不在 git 仓库里**（项目根不是 git 仓库，也没有 `.gitignore`）。
> 也就是说文章内容**没有版本控制、没有 diff、无法回滚**。这更加说明不能跳过下面的检查点。

## 执行流程

### 1. 确认在项目根目录

```bash
pwd && ls _config.yml package.json
```

不是 `C:\Users\xinan\my-blog` → 切过去再继续。缺 `_config.yml` → 说明不在 Hexo 站点，
告诉用户并停止。

### 2. 部署前检查（生成本身安全，但先把问题挡在生成之前）

**a) 列出「自上次部署以来改动了什么」**（`source/` 没有 git，所以用上次部署时间当基准）：

```bash
LAST=$(git -C .deploy_git log -1 --format=%ci)
echo "上次部署: $LAST"
find source/_posts source/img -newermt "$LAST" -type f 2>/dev/null | sort
```

把这些文件列给用户，让他确认「这次就是要发这些」。数量多的话按 `_posts` / `img` 分组汇总，
不要刷屏。

**a2) 找出从未部署过的文章**（`db.json` 是上一次构建留下的记录，**必须在 `hexo clean` 之前跑**，
clean 会把 db.json 删掉）：

```bash
python -c "
import json,os,glob
d=json.load(open('db.json',encoding='utf-8'))
inb={p['source'].replace('_posts/','') for p in d['models']['Post'] if isinstance(p,dict)}
for f in sorted(glob.glob('source/_posts/*.md')):
    b=os.path.basename(f)
    if b not in inb: print('  从未部署:', b, os.path.getsize(f), '字节')
"
```

**这一步很关键**——它会把「新写了但一直没发出去的文章」揪出来。本项目 2026-09-16 实测就查出
`MySQL基础速通.md`（45KB）从上线过。数据库不存在时跳过并说明即可。

**b) 检查未来日期的文章** —— Hexo **会静默跳过**未来日期的文章，页面上直接没有，且不报错。
这是最常见的「我明明写了却没发出去」：

```bash
python -c "
import re,io,glob,datetime
today=datetime.date.today(); print('今天:',today)
for fn in sorted(glob.glob('source/_posts/*.md')):
    s=io.open(fn,encoding='utf-8',errors='replace').read()
    m=re.search(r'^date:\s*(\d{4})-(\d{2})-(\d{2})', s, re.M)
    if m and datetime.date(*map(int,m.groups()))>today:
        print('  未来日期(不会发布):', fn, m.group(0))
"
```

有输出 → **停下**，问用户是不是故意的（草稿可以先留着），不要擅自改他的日期。

**c) 检查空文件和草稿**：

```bash
find source/_posts -size 0          # 0 字节文章
ls source/_drafts 2>/dev/null        # 草稿目录（hexo g 默认不生成草稿）
```

0 字节文章会生成一个空页面，草稿不会发布但会让人以为「写的东西不见了」——都提醒一下。

### 3. 生成站点

```bash
hexo clean && hexo generate
```

- `hexo clean` 会删掉 `public/` 和 `db.json`，强制全量重建。**默认就要 clean**：
  不 clean 时 `public/` 里残留的旧页面会被一起推上线。
- 跑完汇报：**生成了多少个页面 / 用了多少秒 / 有没有 warning**。

### 4. 🛑 停下，等用户确认

把这一步的结果摊给用户：

> ✅ 站点已生成（本地 `public/`，**还没发布**）
> - 生成页面：N 个，耗时 X 秒
> - 文章：`source/_posts` 共 M 篇，其中本次新改动的有：…
> - 报错/警告：无（或列出）
>
> 你可以先本地看一眼：`hexo server` → http://localhost:4000
> 确认没问题就说「发布」，我再执行 `hexo deploy` 推到线上。

**这一步必须停下来等用户回复，不得直接部署。**

### 5. 用户明确说「发布」后，执行部署

```bash
hexo deploy
```

`hexo deploy` 会在 `.deploy_git` 里提交一个 `Site updated: <时间>` 并 push 到远端 `main`。
这一步需要网络和 git 凭据。

### 6. 汇报结果

```bash
git -C .deploy_git log --oneline -1
```

告诉用户：

> 🚀 已部署
> - 提交：`Site updated: …`（<短 hash>）
> - 线上地址：https://xiaoxiaoyu-123.github.io/
> - GitHub Pages 通常 1–2 分钟生效，强制刷新（Ctrl+F5）看最新的

## 常见问题

| 现象 | 原因 / 处理 |
|---|---|
| 部署成功但线上没变 | GitHub Pages 还在构建，等 1–2 分钟；再强制刷新。仍不对就去仓库的 Actions/Pages 看构建状态 |
| 部署报认证失败 | git 凭据问题，**停下**把错误给用户，不要擅自改成 SSH 或换 remote |
| 某篇文章线上没有 | 先查日期是不是未来时间（见步骤 2b），再查是不是在 `_drafts/` 里 |
| 改了东西但线上还是旧的 | 大概率是没 clean，`public/` 里混了旧文件。重跑 `hexo clean && hexo generate` |
| `hexo d` 卡住/超时 | 网络问题。重试；连续失败就把错误交给用户 |

## 铁律

1. **绝不自动触发**：没有用户明确的部署指令，一律不跑 `hexo generate` 之外的任何东西，
   更不碰 `hexo deploy`。
2. **生成和部署必须分开**：跑完 `hexo generate` 一定停下来给用户看，得到明确确认才 deploy。
3. **确认词要明确**：用户说「发布」「推上去」「deploy」才算确认；「嗯」「还行」不算。
4. **不擅自改用户内容**：未来日期、空文件、草稿都只**报告**，要不要动由用户决定。
5. **不碰 `.deploy_git`**：那是部署器的暂存库，手动改会让状态错乱。
6. **部署失败不擅自处理**：报错就停下，把原始错误交给用户，不要自作主张换 remote、
   改分支或强推。
