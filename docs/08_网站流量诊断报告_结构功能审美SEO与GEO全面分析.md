# ApprovedTilers.co.uk 网站流量诊断报告：结构 / 功能 / 审美 / SEO / GEO

> 诊断日期：2026-11-03
> 诊断对象：https://approvedtilers.co.uk（线上实测）+ 本仓库源码（`master` @ f91ccb4）
> 方法：沿用 oulutrip 项目的诊断模板——线上 `curl` 抓取（状态码、跳转、meta、JSON-LD、多种爬虫 UA）、sitemap 抽样、本地 `astro build` 后对全部 852 个 HTML 逐页脚本检查、页面间文本重复度计算（5 词 shingle Jaccard）、数据集字段模板化统计、品牌词搜索。
> 部署方式：Cloudflare Pages（响应头 `server: cloudflare`），Astro 4 静态输出，`npm run build` = 生成 robots/sitemap/llms → `astro build`。

---

## 0. 一句话结论

**与 oulutrip 同一类问题：技术层把收录卡死 + 内容层是高度模板化的"城市×服务"门页 + 信任信号与结构化数据存在编造。**

1. **技术 P0**：除首页外，sitemap 里的 **849/850 个 URL 全部 308 跳转**到带斜杠版本，而页面 canonical 又指向带斜杠版本——sitemap 与 canonical 互相矛盾；不存在的地址返回 **200 + 首页内容**（软 404）；首页 16 条内链是死链；首页"搜索"按钮无论输入什么都跳到 Reading。
2. **结构化数据 P0**：840 个城市页每页都声明一个"位于该城市"的 `HomeAndConstructionBusiness`，带**编造的邮编地址**、**占位电话 `+44-800-000-0000`**、以及全站统一的 **`aggregateRating 4.96 / 350 条评价`**（站内只有 4 条无来源的评价）。这是 Google 结构化数据垃圾政策明令禁止的写法，有被人工处罚的风险。
3. **内容 P1**：840 个城市页由 10 个服务 × 84 个城市模板生成，同服务不同城市的页面**正文 58%–64% 完全重复**，`summary`/`h1`/`meta_description`/流程/清单在同一服务下只有 1 种写法；"附近地区 X 英里"的距离数字是**随机生成的、不真实**（例：伊斯灵顿到卡姆登写成 14 英里，实际相邻）。这正是 Google "Doorway pages / Scaled content abuse" 打击的形态。
4. **渠道/品牌**：搜索 `"approvedtilers.co.uk"` 与品牌+服务词，**均找不到本站任何页面**；只有 PostHog，没有 Search Console 验证（环境变量支持但未见配置）。

---

## 1. 现状快照（实测数据）

| 指标 | 实测值 | 评价 |
|---|---|---|
| sitemap URL 数 | 850（10 静态页 + 840 城市×服务页） | — |
| sitemap URL 访问结果 | 随机抽 30 个：**30/30 返回 308** → 带 `/` 版本；首页除外 | ❌ 严重 |
| 带斜杠 URL | 随机抽 30 个：30/30 返回 200 | — |
| 页面 canonical | `https://approvedtilers.co.uk/services/`（**带斜杠**，与 sitemap 不一致） | ❌ |
| 不存在的页面 `/nonexistent`、`/services.html` | **200**，返回首页 HTML（30,962 字节） | ❌ 软 404 |
| `www.` 子域 | 200（不跳转），canonical 指向裸域 | ⚠️ 应 301 |
| `http://` | 301 → https | ✅ |
| title / canonical / description 每页数量 | 852 页全部恰好 1 个，且互不重复 | ✅ |
| meta description 内容 | 10 种模板×城市名替换；含"5-star rated"无法证实 | ⚠️ |
| 内部死链（本地构建全站扫描） | **16 条**：首页 15 个城市卡片（`/bathroom-tiling/slough` 等）+ `/wet-room-installation/reading` | ❌ |
| 面包屑第 3 级 | 指向 `/{service}/london`，**该页面不存在** | ❌ |
| JSON-LD | 语法合法，但内容编造（见 2.2） | ❌ |
| 城市页正文重复度（同服务不同城市） | Reading vs Leeds 0.58、Westminster vs Camden 0.64、Glasgow vs Cardiff 0.58 | ❌ |
| 城市页正文重复度（同城市不同服务） | Leeds 浴室 vs 厨房 0.52 | ❌ |
| 页面体积 | HTML 中位数 35 KB，CSS 29 KB，无图片 | ✅ 很轻 |
| robots.txt | 无 BOM，允许全部爬虫，指向 sitemap | ✅ |
| sitemap lastmod | 850 条全部为同一天（构建日期 2026-10-23） | ⚠️ 不可信 |
| AI 爬虫（GPTBot / ClaudeBot / PerplexityBot / Googlebot / Bingbot） | 全部 200 | ✅ |
| llms.txt / llms-full.txt | 存在（5.7 KB / 68 KB）；含"UK's premier"等无法证实表述 | ⚠️ |
| 统计 | PostHog（EU）已装，含会话录屏 | ✅（但同意机制有合规问题，见 5） |
| 品牌词搜索 | `"approvedtilers.co.uk"`、"Approved Tilers UK bathroom tiling Westminster" 均无本站结果 | ❌ |

---

## 2. SEO 技术层

### 2.1 ❌ P0：URL 尾斜杠 308 与 sitemap / canonical 冲突（与 oulutrip 同源）

- 证据：`curl -I https://approvedtilers.co.uk/bathroom-tiling/westminster` → `308 Location: .../westminster/`；sitemap 里写的是无斜杠版本；页面 canonical 写的是带斜杠版本（`src/layouts/Layout.astro` 用 `Astro.url.pathname` 生成，目录式输出下带 `/`）。
- 后果：Google 抓 sitemap → 全是"网页会自动重定向"；sitemap 与 canonical 信号相反，抓取预算浪费。
- 修复：`astro.config.mjs` 加 `build.format: 'file'`、`trailingSlash: 'never'`，canonical 统一去掉尾斜杠。

### 2.2 ❌ P0：结构化数据编造（LocalBusiness / 评分 / 电话 / 地址）

`src/pages/[service]/[city].astro` 每页输出：

```json
"@type": "HomeAndConstructionBusiness",
"telephone": "+44-800-000-0000",
"address": { "addressLocality": "Westminster", "postalCode": "W1", ... },
"aggregateRating": { "ratingValue": "4.96", "reviewCount": "350" }
```

- 本业务是**撮合平台**，在 84 个城市并没有 840 个实体门店；按城市声明 `PostalAddress` 等于编造营业地址。
- `+44-800-000-0000` 是占位号码；全站其他地方没有公布任何电话。
- `4.96 / 350` 无任何来源；`/reviews` 页只有 4 条无日期、无来源的评价；且 Google 规定**自己网站给自己打的评分（self-serving reviews）不能用于 LocalBusiness/Organization 星级**。
- 首页 `src/pages/index.astro` 与 `Layout.astro` 的 Organization 也带同样的电话和评分。
- 面包屑第 3 级指向不存在的 `/{service}/london`。

### 2.3 ❌ P1：软 404

站点没有 `404.astro`，Cloudflare Pages 找不到 404.html 时会把首页当成 SPA 回退并返回 200。任何拼错的地址都变成"首页的重复页"。

### 2.4 ⚠️ P2：其他

- sitemap `lastmod` 是构建日期（`scripts/generate_seo_geo.mjs` 中 `today`），850 条全一样；
- `twitter:card = summary_large_image` 但全站没有任何图片；
- 城市页 title 形如 `Expert Bathroom Tiling & Renovation in Kensington and Chelsea | 100% Fixed Price Quotes`（85 字符），过长且无品牌；
- 城市页标题写 "Average … Costs in {city} (2025)"，而价格页、事实卡写 2026，年份自相矛盾；
- slug `kensington--chelsea`、`hammersmith--fulham` 带双连字符（不影响收录，改动需加 301，暂不动）。

---

## 3. 结构与信息架构

| 问题 | 证据 | 影响 |
|---|---|---|
| **没有服务聚合页** | `/services` 的 10 张卡片全部链到 `/{service}/westminster`；首页服务卡片链到 `/{slug}/reading`；面包屑链到不存在的 `/london` | "浴室瓷砖"这类最有价值的非地域词没有落地页；84 个城市页之间没有一个"父页面" |
| `/areas` 只链浴室服务 | 84 个城市全部链到 `/bathroom-tiling/{city}` | 其他 9 个服务的城市页只能靠城市页内的交叉链接发现 |
| 首页数据源错误 | 首页城市列表用 `uk_towns.json`（34 个旧城市，其中 15 个已无页面），服务列表用 `services_config.json`（4 个服务，`wet-room-installation` 已不存在） | 16 条死链 |
| 推广页可被收录 | `/promo/price-check`、`/promo/voucher-claim` 为广告落地页，`robots: index` | 薄内容、与广告着陆体验混淆 |
| 移动端无导航 | `Layout.astro` 中 `<nav class="hidden md:flex">`，`md` 以下没有任何菜单 | 手机用户无法进入 Services / Price Guide / Areas / Reviews |

---

## 4. 内容质量（排名的决定性因素）

### 4.1 ❌ "城市×服务"页面是换地名的模板页

对数据集 `src/data/tiling_pseo_dataset.json` 统计（把城市名/郡/邮编/区域/房屋类型替换为占位符后）：

| 字段 | 840 页中不同写法数 | 含义 |
|---|---|---|
| `h1` | 10 | 每个服务 1 种 |
| `meta_description` | 10 | 每个服务 1 种 |
| `summary` | 10 | 每个服务 1 句话 |
| `service_process`、`checklist` | 10 | 每个服务 1 套 |
| `local_pain_points` | 90 | 每服务约 9 个模板 |
| `estimated_price_range` | 20 | 例：浴室只有 £500–650（52 城）与 £680–830（32 城）两档 |
| `house_type_context` | 84 | 唯一真正按城市变化的字段（一句话） |

页面正文实测 5 词 shingle 重合率 58%–64%（加上城市名替换后实际更高）。**真正"本地化"的信息只有：城市名、邮编前缀、一句房屋类型、价格档位。**

### 4.2 ❌ "附近地区"距离是编造的

`nearby_areas` 中的 `dist_miles` 随机生成且互不对称：

- Islington → Camden **14.0 英里**（两区相邻）；
- Kensington and Chelsea → Barking and Dagenham **4.9 英里**（实际约 15 英里）；
- Westminster → Croydon **4.1 英里**（实际约 10 英里）；
- 页面文字还写"neighbouring districts within 35 miles"。

数据集中没有经纬度，无法重新计算。页面把这些数字当成事实展示，对用户和 AI 都是错误信息。

### 4.3 ❌ 无法核实的信任表述（E-E-A-T）

| 表述 | 位置 | 问题 |
|---|---|---|
| "Rated 4.96/5 by 350+ UK Homeowners" | 全站顶部信任条 | 无来源；与 `/reviews` 仅 4 条评价矛盾 |
| "5-star rated local master tilers" | 840 条 meta description | 同上 |
| 4 条评价（Sarah M.、James T.…） | `/reviews` | 无日期、无平台来源 |
| "Marcus J. 18 yrs exp"、"Apex Tiling Solutions 4.98/5 (92 reviews)" | `/promo/voucher-claim` | 无法核实是否真实存在 |
| "BS 5385 Certified" | 同上 | BS 5385 是施工规范，不存在"认证" |
| "£2M insured / 12-month guarantee / vetted / BS 5385 compliant" | 全站 | 业务承诺，需所有者确认能兑现并可出示证据 |
| "UK's premier verified trade network" | llms.txt | 最高级宣称，无依据 |

> 英国 **《2024 数字市场、竞争和消费者法》（DMCC Act）** 自 2025 年 4 月起将"发布或委托发布虚假评价、隐瞒激励评价"列为一律禁止的不公平商业行为，由 CMA 直接执法，可处全球营业额 10% 罚款。若上述评价/评分不能证明真实，这是法律风险而不只是 SEO 风险。

---

## 5. 功能与转化路径

| 问题 | 证据 | 建议 |
|---|---|---|
| 首页邮编搜索无效 | `index.astro`：输入任何内容都 `location.href = '/bathroom-tiling/reading'` | 按输入匹配城市，匹配不到则带邮编进入报价页 |
| Cookie 横幅每页都弹 | 关闭只是 `style.display='none'`，无持久化 | 记住关闭状态 |
| Cookie 同意不合规 | 横幅写"继续使用即同意"，PostHog（含会话录屏）在同意前即加载 | 英国 PECR/UK GDPR 要求分析类 Cookie 事先同意——**需所有者决定**是否改为"同意后再加载"或改用无 Cookie 模式 |
| 表单提交端点 | 报价表单提交到 `roamglade-form-hub…workers.dev`（与其他项目共用） | 功能正常；建议确认邮件通知已测试 |
| 无电话 | 页面没有公布电话，schema 却有占位电话 | 有真实号码就加上，没有就不在 schema 里写 |

---

## 6. 审美与视觉

整体为标准的"建材/装修平台"风格（深色 hero + 琥珀色 CTA + 白色卡片），干净、加载快，**没有图片**是最大的短板：

1. 一个靠"手艺"卖服务的站点没有任何作品照片、工匠照片，信任感完全依赖文字徽章；
2. 城市页的"AI & SEARCH FACT SHEET"标签、跳动绿点"Active Trade Availability"、"Verified Regional Data"直接面向用户显示，像开发者遗留文字，也属于无法核实的表述；
3. 徽章重复：顶部信任条、hero 徽章、TrustBadges、事实卡、页脚各重复一遍"£2M / 12 个月 / 固定价"，信息密度高但显得用力过猛；
4. 移动端：顶部信任条在手机上换成两行，且无导航菜单（见 3）。

---

## 7. GEO（ChatGPT / Perplexity / Google AI Overview 等）

### 已经做对的
- robots 显式放行主流 AI 爬虫，实测全部 200；
- 有 llms.txt / llms-full.txt；每个城市页有事实卡（价格档、工期、保险）和 FAQ，服务端渲染、AI 可直接读取。

### 问题
1. **AI 推荐的前提是"被第三方提到"**：品牌在搜索中查不到，没有 Checkatrade / TrustATrader / Google Business Profile / Tile Association 等第三方实体信号，模型没有理由推荐。
2. **事实卡里有错误事实**（编造的距离、评分），一旦被 AI 引用，会损害实体可信度。
3. **实体定义不清**：页面一会儿是"本地工匠（Local Master Tiler Serving Westminster）"，一会儿是"全国网络"；schema 每页一个不同名称的 Business。AI 无法确定"Approved Tilers"是一家公司还是 840 家。
4. llms.txt 中 URL 与 sitemap 一致（无斜杠），但线上都会 308（随 2.1 一起修复）。

---

## 8. 整改路线图

### 第 1 周：止血（本轮已修，见修复报告）
1. `build.format: 'file'` 修 308；canonical 无斜杠；
2. 增加 404 页消除软 404；
3. 结构化数据去掉编造的评分、电话、城市地址；改为"一个 Organization + 每页一个 Service（areaServed=城市）"；
4. 修首页死链、首页搜索、面包屑死链；
5. 推广页 `noindex`；sitemap lastmod 改为真实修改时间；
6. 删除无法核实的"4.96/350+""5-star rated"、编造的距离数字；
7. 新增 10 个服务聚合页作为城市页的父页面；移动端导航；Cookie 横幅持久化。

### 需要所有者决策（本轮不动）
见修复报告"待决策事项"：城市页 noindex/合并策略、评价页真实性、保险/保修/审核承诺的证据、Cookie 同意与 PostHog、www 跳转、`--` slug。

### 第 2–3 个月：增长
- 把 840 页收敛为"10 个服务页 + 少量真有订单城市的深度页"，其余 noindex 或合并到区域页；
- 在真实完成的项目基础上写案例（照片、地点、面积、价格、工期），这是本地服务站最强的原创内容；
- 注册 Google Business Profile（若有服务区域型实体）、Checkatrade / TrustATrader / The Tile Association，积累可验证评价；
- 在 Search Console / Bing Webmaster 验证并提交 sitemap，观察"已编入索引"变化。

---

## 附录：关键证据位置

- 尾斜杠与 canonical：`astro.config.mjs`、`src/layouts/Layout.astro`（`canonicalUrl`）
- 编造 schema：`src/pages/[service]/[city].astro`（`pageSchema`）、`src/pages/index.astro`（`homeSchema`）、`src/layouts/Layout.astro`（`baseOrgSchema`）
- 首页死链与搜索：`src/pages/index.astro`（`uk_towns.json`、`services_config.json`、`home-search-btn`）
- 距离数据：`src/data/tiling_pseo_dataset.json`（`nearby_areas[].dist_miles`）
- 信任条：`src/layouts/Layout.astro`（"Rated 4.96/5"）
- 推广页：`src/pages/promo/*.astro`
- sitemap / llms 生成：`scripts/generate_seo_geo.mjs`
