# 统计方案（三选一）

> 2026-10-27 更新：服务器为 2C2G 且已有多个容器，**放弃在服务器自托管 Umami**（Umami + PostgreSQL 约需 500~700MB 内存）。改为以下免服务器方案。

## 方案对比

| 方案 | 是否开源 | 服务器 | 免费额度 | 主题支持 | 推荐度 |
|---|---|---|---|---|---|
| **Umami Cloud** | 是（GitHub: umami-software/umami） | ❌ 不需要 | 10 万事件/月、1 站点、留存 6 个月 | ✅ 主题原生 `umami_analytics` | ⭐ 首选 |
| **GoatCounter 托管版** | 是（GitHub: arp242/goatcounter） | ❌ 不需要 | 个人站点免费（捐赠维持，无硬性套餐） | ❌ 需 inject 自定义脚本 | ⭐ 备选 |
| Cloudflare Web Analytics | ❌ 闭源 | ❌ 不需要 | 免费 | 主题原生支持 | 备选 |

## 方案 A：Umami Cloud（推荐）

1. 打开 https://umami.is → Sign up（可用 GitHub 账号登录）→ 选免费 Hobby 计划
2. 添加网站：名称「小🐟博客」，域名 `xiaoxiaoyu-123.github.io`
3. 复制 **Website ID**（UUID）
4. 交给 AI 写入主题：

```yaml
umami_analytics:
  enable: true
  serverURL: https://cloud.umami.is
  script_name: script.js
  website_id: <Website ID>
  option:
```

## 方案 B：GoatCounter（完全免费、无配额）

1. https://www.goatcounter.com/signup 注册子域（如 `xiaoxiaoyu.goatcounter.com`）
2. 主题 inject.head 加入（把子域换成你的）：

```html
<script data-goatcounter="https://xiaoxiaoyu.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
```

3. 注意：GoatCounter 不提供站内访问量数字展示，侧栏 UV/PV 需保留 busuanzi 或隐藏

## 服务器清理

本地 Umami 与 PostgreSQL 可卸载释放内存：1Panel → 应用 → umami → 卸载；1Panel → 数据库 → PostgreSQL → 卸载（确认无其他应用使用后）。

---

# 附：自托管 Umami 部署指南（已不采用，留档）

> 目标：把博客访问统计从 busuanzi 换到自托管 Umami。完成后把 **https 访问地址** 和 **Website ID** 发给 AI 接入主题。

## 为什么「数据库服务」下拉框是空的

1Panel 的 Umami 应用是「应用 + 外部数据库」模式：它要求你**先在 1Panel 里装好 PostgreSQL 服务**，安装页面的下拉框只是让你选一个已存在的数据库实例。服务器上还没装 PostgreSQL，所以显示「无数据」。

## 部署步骤

### 1. 先装 PostgreSQL

1Panel 左侧菜单 → **数据库** → **PostgreSQL** 标签 → **安装**：
- 版本选 16（或 17）
- 端口保持 5432，**不需要对外开放**
- 记下超级用户密码（自己设一个，存好）

### 2. 回到应用商店装 Umami（表单填写建议）

| 字段 | 值 | 说明 |
|---|---|---|
| 名称 | `umami` | 容器名 |
| 版本 | 3.4.1 | 最新版 |
| 数据库服务 | 选已安装的 PostgreSQL | 下拉仍为「无数据」= PostgreSQL 未装好/未启动 |
| 数据库名 / 用户 / 密码 | 保持自动生成 | 密码别改成含 `@ : / #` 的字符（会拼进 DATABASE_URL） |
| HTTP 端口 | `3000` | 宿主机端口（compose `${PANEL_APP_PORT_HTTP}:3000` 左侧）；被占用可换，但反代要同步改 |
| 应用端口外部访问 | **不勾选** | 只绑本机，反代仍可访问，更安全 |
| 内存限制 | 1024MB（最低 512MB） | Next.js 应用 |

`APP_SECRET`（`${HASH_SALT}`）由 1Panel 自动生成，无需填写。

安装后验证：

```bash
docker ps --format '{{.Names}}	{{.Ports}}' | grep -i umami   # 期望 127.0.0.1:3000->3000/tcp
curl -I http://127.0.0.1:3000                                  # 期望 200/302
```

### 3. 反向代理（不要用 1Panel 代理表单）

应用商店 → Umami → 安装：
- **数据库服务**：下拉选择刚装的 PostgreSQL（现在有选项了）
- 数据库名 / 用户名 / 密码：保持 1Panel 自动生成的值即可（它会自动建库建用户）
- **HTTP 端口**：保持 3000
- 高级设置里 **不要**「放开外部访问」——后面用反向代理 + HTTPS 访问，更安全

### 4. ⚠️ 必须配 HTTPS 域名（关键）

博客部署在 GitHub Pages（HTTPS），**如果 Umami 只有 `http://服务器IP:3000`，统计脚本会被浏览器当作"混合内容"直接拦截，统计完全失效**。所以必须给它一个 HTTPS 域名：

1Panel → **网站** → 创建网站 → **反向代理**：
- 域名：`umami.你的域名.com`（或任意子域）
- 代理地址：`http://127.0.0.1:3000`
- 创建后进入网站设置 → **HTTPS** → 申请 **Let's Encrypt** 免费证书，开启强制 HTTPS

然后在 **阿里云控制台 → 安全组** 放行 80、443（1Panel 面板的防火墙也要放行对应端口）。

> 没有域名怎么办：混合内容问题绕不过去，可选：① 用已有域名的子域；② 买个便宜域名（十几块一年）；③ 放弃自托管改用 Umami Cloud 免费版（有官方 https 域名）。告诉我你的选择，我按对应方案接入。

### 5. 初始化 Umami 并拿 Website ID

访问 `https://umami.你的域名.com`：
1. 用默认账号 `admin` / `umami` 登录，**第一件事改密码**
2. 设置 → 网站 → **添加网站**：名称填「小🐟博客」，域名填 `xiaoxiaoyu-123.github.io`
3. 复制该网站的 **Website ID**（形如 `a1b2c3d4-...` 的 UUID）

### 6. 把这两个值发给 AI

- Umami 的 https 访问地址（如 `https://umami.xxx.com`）
- Website ID

AI 会写入主题 `umami_analytics` 配置（serverURL / website_id），并**下线 busuanzi**（访问量改由 Umami 统计）。

## 常见报错

### `invalid port in upstream "http://127.0.0.1:3002"`

反向代理保存时报 nginx `[emerg] invalid port in upstream`。原因：代理地址带了 `http://` 协议头，而 nginx 在 upstream/server 解析时无法接受协议头——它把 `http:` 里的冒号当成端口分隔符，端口变成 `//127.0.0.1:3002` → 非数字 → 报错。

**解决**：代理地址字段只填纯 `host:port`（如 `127.0.0.1:3000`），不要带 `http://`。
同时确认端口与 Umami 实际映射端口一致（1Panel → 应用 → 已安装 → umami 查看端口映射），否则代理通了也会 502。

**不要填服务器公网 IP**：反向代理与 Umami 在同一台机器上，上游必须是 `127.0.0.1:端口`；填公网 IP 会走「发夹式」绕行，常直接失败。

若字段强制带协议或仍报错，手动改 `/www/sites/<域名>/proxy/root.conf`：

- 文件内有 `upstream { ... }` 块 → `server 127.0.0.1:3000;`（**无**协议头）
- 只有 `location` + `proxy_pass` → `proxy_pass http://127.0.0.1:3000;`（**有**协议头），推荐整段：

```nginx
#REWRITE-END
location ^~ / {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

**用终端直接写文件最保险**（避免编辑器/粘贴带入不可见字符）：

```bash
# 先查宿主机实际端口（compose 里 ${PANEL_APP_PORT_HTTP}:3000 的左边那个）
docker ps --format '{{.Names}}	{{.Ports}}' | grep -i umami
# 验证服务本身
curl -I http://127.0.0.1:3000

cat > /www/sites/umami.xiaoxiaoyu123.xyz/proxy/root.conf <<'EOF'
#REWRITE-END
location ^~ / {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
EOF
```

把 3000 换成 `docker ps` 查到的宿主机端口。保存后在该站点点「重载」。若改了仍报同样错误，删除地址**手动重新输入**，排除复制粘贴带入的不可见字符。改前先 `curl -I http://127.0.0.1:3000` 确认服务本身正常。

## 接入后验证

- 博客页面源码里出现 `umami` 脚本标签
- Umami 后台「实时」面板能看到自己的访问记录
- 主题侧栏的访问量数据改由 Umami 提供（需开启 `UV_PV` 选项，届时一并配置）
