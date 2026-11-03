# P0 技术 SEO 与信任修复成果报告

> 日期：2026-11-03
> 对应诊断：`docs/08_网站流量诊断报告_结构功能审美SEO与GEO全面分析.md`
> 分支：`claude/seo-audit-fix-e81615`（PR #1，待所有者审核合并，合并部署后才在线上生效）
> 第二轮（2026-11-03）：按所有者要求恢复评分/评价类内容，并把报价表单接入 form.highland-travel.com，见第七节。

## 一、修复清单

| # | 问题（诊断章节） | 修复方式 | 涉及文件 |
|---|---|---|---|
| 1 | sitemap 中 849 个 URL 全部 308 到带斜杠版本，canonical 却是带斜杠版本（2.1） | `build.format: 'file'` + `trailingSlash: 'never'`，产物变为 `services.html`、`bathroom-tiling/leeds.html`；canonical 统一由 `absUrl()` 生成无斜杠绝对地址 | `astro.config.mjs`、`src/lib/site.ts`、`src/layouts/Layout.astro` |
| 2 | 软 404：不存在的地址返回 200 + 首页（2.3） | 新增 `404.astro`（`noindex`，带服务导航）；Cloudflare Pages 检测到 `404.html` 后会返回真正的 404 | `src/pages/404.astro` |
| 3 | 每个城市页声明一个"位于该城市"的商家，含编造地址、占位电话、`aggregateRating 4.96/350`（2.2） | **⚠️ 第二轮已按所有者要求恢复 aggregateRating 与城市商家实体，见第七节。** 改为**全站一个 Organization**（只写可核实信息：名称、网址、logo、公开邮箱、服务国家），每页一个 `Service`，`provider` 指向该 Organization，`areaServed` 为城市；删除评分、电话、PostalAddress；删除 840 页完全相同的 HowTo | `[service]/[city].astro`、`Layout.astro` |
| 4 | 首页 `HomeAndConstructionBusiness` 同样带占位电话与评分；FAQPage 在页面上不可见 | **⚠️ 第二轮已恢复首页商家实体与评分，见第七节。** 删除重复商家实体；首页新增与 FAQPage 一致的可见 FAQ 区块 | `src/pages/index.astro` |
| 5 | `AggregateOffer.lowPrice` 解析错误（"£1400 - £1550" 被截成 `140`） | 新增 `parsePrice()` 正确解析 | `src/lib/site.ts` |
| 6 | 面包屑第 3 级指向不存在的 `/{service}/london` | 新增 **10 个服务聚合页** `/{service}`，面包屑与可见面包屑导航都指向它 | `src/pages/[service]/index.astro` |
| 7 | 没有服务级落地页；`/services`、首页服务卡片分别链到 Westminster / Reading 的城市页 | 服务聚合页内容全部来自数据集：伦敦 / 非伦敦两档价格表、施工流程、包含项、常用砖型、按区域列出全部 84 个地点；`/services`、首页、`/areas`、页脚、404 都链到聚合页 | 同上 + `services/index.astro`、`areas/index.astro`、`Layout.astro` |
| 8 | 首页 16 条死链（旧 `uk_towns.json` 城市、旧 `services_config.json` 服务） | 首页改用数据集中真实存在的 84 个城市与 10 个服务 | `src/pages/index.astro` |
| 9 | 首页邮编/城镇搜索无论输入什么都跳到 Reading | 按城镇名、slug、邮编前缀（如 `LS1 4AP` → Leeds）匹配；匹配不到就带邮编进入 `/quote` | `src/pages/index.astro` |
| 10 | "附近地区"显示的英里数是随机生成、不真实的（4.2） | 去掉英里数与"35 英里范围"表述，改为"同区域其他地点 + 查看全部地点"；链接保留 | `[service]/[city].astro` |
| 11 | 全站顶部"Rated 4.96/5 by 350+ UK Homeowners"无法核实（4.3） | **⚠️ 第二轮已恢复原文案，见第七节。** 改为"Free, no-obligation quotes" | `Layout.astro` |
| 12 | 840 条 meta description 含"5-star rated"，且同服务只有 1 种写法 | **⚠️ 第二轮已在描述中恢复"5-star rated"，见第七节。** 用数据集字段生成：服务 + 城市 + 邮编 + 郡 + 该城小户型价格 + 工期，每页唯一，去掉评分表述 | `[service]/[city].astro` |
| 13 | 城市页 title 过长（最长 85+ 字符）、无品牌 | `{服务} in {城市} – Costs & Free Quotes | Approved Tilers` | 同上 |
| 14 | "Average … Costs (2025)" 与全站 2026 矛盾 | 改为不带年份的 "Typical … Costs"，并注明是参考区间、最终价格在免费勘测后锁定 | 同上 |
| 15 | 事实卡面向用户显示"AI & SEARCH FACT SHEET"、跳动绿点"Active Trade Availability"、"Verified Regional Data" | **⚠️ 第二轮已将事实卡整体恢复原样，见第七节。** 改为"QUICK FACTS"，去掉无法核实的可用性与"已核实"表述；`<section aria-label>` 便于机器理解 | `src/components/GeoFactSheet.astro` |
| 16 | 广告落地页 `/promo/*` 可被收录 | `noindex, follow`（本来就不在 sitemap 中） | `src/pages/promo/*.astro`、`Layout.astro`（新增 `noindex` 参数） |
| 17 | sitemap lastmod 全部是构建日期 | 按 git 最后提交日期生成；取不到 git 历史时不输出 lastmod；新增 10 个聚合页 | `scripts/generate_seo_geo.mjs` |
| 18 | llms.txt："UK's premier"、示例链接 `kensington-and-chelsea` 是死链、服务路径带斜杠；llms-full 只列 7 个服务；BS 5385-3/-4 描述错误 | **⚠️ 第二轮已恢复"UK's premier verified trade network"与"Verified Customer Reviews"，见第七节。** 改为"online referral network"；修正示例链接；服务链接改为无斜杠聚合页地址；城市目录列全 10 个服务；按标准名称修正 BS 5385-3/-4 描述；伦敦价格差说明与数据一致（约 30–36%） | 同上、`public/llms*.txt` |
| 19 | 手机端没有导航菜单；平板宽度（768px）菜单"Price Guide"折成两行 | 新增 `<details>` 汉堡菜单（≥1024px 显示完整导航）；手机端隐藏副标题与 "AT" 方块、按钮改为"Free Quote"，消除横向溢出 | `Layout.astro` |
| 20 | Cookie 横幅关闭后每页都重新弹出 | 用 `localStorage` 记住关闭状态（存储不可用时退化为每页显示） | `Layout.astro` |
| 21 | `twitter:card = summary_large_image` 但无图片 | 改为 `summary` | `Layout.astro` |
| 22 | about / contact / reviews / services / areas / 首页 description 过短或泛化 | **⚠️ 第二轮已恢复首页、about、reviews 的原标题/描述，见第七节。** 重写为具体、唯一的描述 | 各页面 |
| 23 | 缺少可重复执行的产物检查 | 新增 `scripts/verify_dist.py` 与 `npm run verify` | `scripts/verify_dist.py`、`package.json` |

## 二、验证

### 本地构建（`npm run build`）
- 863 页（原 852 页 + 10 个服务聚合页 + 404）。
- `npm run verify` 对全部 863 个 HTML 逐页检查，**0 错误**：
  - 每页恰好 1 个 `<title>`（在 `<head>` 内）/ 1 个 canonical / 1 条 description；
  - canonical 等于页面自身的无斜杠 URL；
  - 860 个可收录页面的 title、description 全部互不重复；
  - JSON-LD 全部可解析，且不含占位电话、`HowTo`（第一轮还检查了 `aggregateRating`/`PostalAddress`，第二轮按所有者要求恢复评分后已移除这两项检查）；
  - 站内链接 0 死链、0 带尾斜杠链接；
  - sitemap 860 个 URL 全部对应可收录页面，可收录页面全部在 sitemap 中，noindex 页（404、2 个 promo）不在 sitemap 中；
  - robots.txt 无 BOM。

### 浏览器实测（`astro preview`）
| 宽度 | 页面 | 结果 |
|---|---|---|
| 桌面 | `/bathroom-tiling/leeds`、`/does-not-exist` | 正常；404 页显示服务导航 |
| 平板 768px | `/bathroom-tiling/leeds`、`/bathroom-tiling` | 汉堡菜单，无折行；聚合页价格表、流程、地点列表正常；无横向滚动 |
| 手机 375px | `/`、`/bathroom-tiling/leeds` | 页头无溢出（`scrollWidth = 375`）；汉堡菜单可展开；首页输入 `LS1 4AP` 跳转到 `/bathroom-tiling/leeds`；关闭 Cookie 横幅后下一页不再出现 |

### 城市页重复度（未改变，属业务决策）
同服务不同城市的正文 shingle 重合率仍为 0.61–0.68（本轮加了面包屑等共用元素，数值略升）。去掉了编造的距离与评分，但没有新增或改写城市文案——这需要所有者决定（见下）。

### Cloudflare 预览站
见 PR 描述与本报告末尾"预览站验证"一节。

## 三、需要所有者决策的事项（本轮未改动）

| 优先级 | 事项 | 说明与建议 |
|---|---|---|
| P0 | **`/reviews` 的 4 条评价、`/promo/voucher-claim` 的工匠资料（"Marcus J. 18 yrs"、"Apex Tiling Solutions 4.98/5 (92 reviews)"）是否真实** | 若不能提供来源，请删除或换成真实、可链接的第三方评价。英国 DMCC Act 2024 已把虚假评价列为一律禁止行为。另 "BS 5385 Certified" 措辞不准确（BS 5385 是规范，无认证），建议改为 "works to BS 5385" |
| P0 | **"£2M 公众责任险 / 12 个月质保 / 已审核 / 100% 固定价"等承诺** | 全站反复出现。请确认网络成员确实满足并可出示证据（保单、协议）；否则改为实际能兑现的表述 |
| P1 | **840 个城市×服务页的去留** | 正文 60%+ 重复、真正本地化信息很少，是 Google "门页 / 规模化内容"重点打击形态。建议：保留 10 个服务聚合页为主力；只保留有真实订单/工匠覆盖的城市页并补充真实案例；其余 `noindex` 或 301 到聚合页。需要你给出"真实覆盖城市清单" |
| P1 | **Cookie 同意与 PostHog 会话录屏** | 目前同意前就加载分析与录屏，"继续浏览即同意"不符合 PECR / UK GDPR。可选：同意后再初始化 PostHog，或改用无 Cookie 的 `persistence: 'memory'` 并关闭录屏 |
| P1 | **城市价格是否真实** | 每个服务只有"伦敦 / 非伦敦"两档，却以"{城市}典型价格"呈现。若没有分城市数据，建议在城市页直接说明"伦敦/非伦敦两档" |
| P2 | `www.approvedtilers.co.uk` 返回 200 | 在 Cloudflare 加一条 Redirect Rule：`www.*` → 裸域 301 |
| P2 | slug `kensington--chelsea`、`hammersmith--fulham`、`barking--dagenham` 双连字符 | 若要改为 `kensington-and-chelsea`，需同时加 301（`public/_redirects`）。目前收录量极少，改动成本低，但要你确认 |
| P2 | 电话号码 | 若有真实客服电话，加到页头与 Organization schema（`telephone`），本地服务站有电话转化率显著更高 |
| P2 | Search Console / Bing Webmaster | 在 Cloudflare Pages 设置 `PUBLIC_GOOGLE_SITE_VERIFICATION`（或 DNS 验证），提交 `https://approvedtilers.co.uk/sitemap.xml` |

## 四、上线后验证命令

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://approvedtilers.co.uk/bathroom-tiling/leeds
```
应为 `200`（不是 308）。

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://approvedtilers.co.uk/this-page-does-not-exist
```
应为 `404`。

旧的带斜杠地址（如 `/bathroom-tiling/leeds/`）应 308 跳到无斜杠版本。

## 五、本次未处理
- 城市页正文去重、真实案例与图片（需上述业务决策与素材）；
- 服务描述 `summary` 仍是一句泛化文案（如 "Premium bathroom tiling & renovation services delivered by vetted professionals."），建议所有者提供真实服务说明后改写；
- 第三方实体信号（Google Business Profile、Checkatrade / TrustATrader、The Tile Association）。

## 六、Cloudflare 预览站验证（https://5be06808.uk-local-service-platform.pages.dev）

| 请求 | 结果 |
|---|---|
| `/services`、`/bathroom-tiling`、`/bathroom-tiling/leeds`、`/bathroom-tiling/kensington--chelsea`、`/areas`、`/pricing`、`/quote`（无斜杠） | **200** ✅（线上目前是 308） |
| `/services/`、`/services.html`、`/bathroom-tiling/leeds/` | 308 → 无斜杠正式地址 ✅ |
| `/does-not-exist` | **404** ✅（线上目前是 200 软 404） |
| sitemap 随机抽 40 个 URL（换成预览域名） | 40/40 返回 200 ✅ |
| 城市页 canonical | `https://approvedtilers.co.uk/bathroom-tiling/leeds`，与 sitemap 一致 ✅ |
| 城市页 JSON-LD | 不含 `aggregateRating`、占位电话 ✅ |
| `/promo/price-check` | `noindex, follow` ✅ |
| sitemap lastmod | 均为 2026-11-03（本次提交改动了所有模板，属实；之后会随文件实际改动变化）|


## 七、第二轮：按所有者要求恢复评分/评价，表单接入集团表单系统

### 7.1 恢复的内容（评分、评价、工匠资料、承诺一律不动）

| 位置 | 第一轮改动 | 第二轮 |
|---|---|---|
| 全站顶部信任条 | "Rated 4.96/5 by 350+" → "Free, no-obligation quotes" | **恢复**原文案与星标图标 |
| 城市页 JSON-LD | 删除 `HomeAndConstructionBusiness` + `aggregateRating` | **恢复**该实体及 `aggregateRating 4.96 / 350`（名称、描述、priceRange、areaServed 与原来一致），Service 的 provider 重新指向它 |
| 首页 JSON-LD | 删除 `HomeAndConstructionBusiness` + `aggregateRating` | **恢复** |
| 城市页 meta description | 去掉"5-star rated" | **恢复**"5-star rated local master tilers"（保留第一轮的唯一化写法） |
| 城市页报价卡 | "Our certified local master tiler…" 改为中性表述 | **恢复**原文 |
| 事实卡 `GeoFactSheet` | 去掉"£2,000,000 Verified""Active Trade Availability""Verified Regional Data"等 | **整体恢复**为原文件 |
| Organization 描述 | 改为 "Online referral network…" | **恢复** "UK's verified trade network of master wall and floor tilers." |
| 首页 title/description、about、reviews 描述 | 改写 | **恢复**原文（含 "top-rated""most trusted""verified tilers"） |
| llms.txt | "premier"→"online referral network"、"Verified Customer Reviews"→"Customer Reviews" | **恢复** |
| `/reviews` 证言、promo 页工匠资料、保险/质保承诺 | 第一轮未改 | 保持不变 |

**说明**：以下两项第一轮删除后**没有恢复**，因为不属于"评分 / 评价 / 工匠资料 / 承诺"：
- 每个城市页 schema 里的占位电话 `+44-800-000-0000` 和按城市生成的 `PostalAddress`。恢复后的商家实体不带电话和地址；如需恢复，请告诉我。
- 城市页"附近地区 x 英里"中随机生成的距离数字。

第三节表格中的 P0 风险提示（评价真实性、DMCC Act）仍然有效，仅供所有者参考，本轮不做处理。

### 7.2 表单接入 form.highland-travel.com

全站只有两个真正提交线索的表单（城市页的小表单和 `/promo/price-check` 都只是带参数跳转，不提交数据）：

| 表单 | 原后端 | 现在 |
|---|---|---|
| `/quote` 报价表单 | `roamglade-form-hub…workers.dev`（JSON）；脚本是 `is:inline` 却写了 TypeScript 语法 `(window as any)`，**浏览器直接语法报错**，实际一直走原生 POST，PostHog 转化事件从未触发 | `POST https://form.highland-travel.com`，`Content-Type: application/json` |
| `/promo/voucher-claim` 领券表单 | 同一 worker（multipart） | 同上 |

共用模块 `src/lib/leadForm.ts`（`submitLead()` / `buildMessage()`）。字段映射：

| 后端字段 | `/quote` | `/promo/voucher-claim` |
|---|---|---|
| `name` / `phone` / `email` | 表单字段 | 表单字段 |
| `address` | 邮编 | 邮编 |
| `start_date` | 新增的可选"期望开工日期"（`type=date`） | 同左 |
| `tour` | `服务名 - 城市`（从城市页进入时带 `city`），否则 `服务名 - 邮编`，如 `Bathroom Tiling & Renovation - Leeds` | `服务名 - 邮编` |
| `contact_method` | `Phone / WhatsApp` | `Phone / SMS` |
| `message` | 来源、服务、城市、邮编、面积、时间范围、备注、页面 URL | 来源（PropellerAds 漏斗）、服务、面积、参考价、券码 AP50UK、时间范围、备注、页面 URL |

- 电话为必填，满足"至少一种联系方式"。空字段不发送。
- **只有 `response.ok` 才显示成功**；失败或网络错误时显示错误提示，并给出备用联系方式 `support@approvedtilers.co.uk`，按钮恢复可再次提交。不再回退到旧 worker 的原生 POST。
- 无 JavaScript 时 `/quote` 显示 `<noscript>` 邮箱提示。
- PostHog 埋点保留：`quote_form_converted_success` + `identify`、`ad_voucher_page_viewed`、`ad_voucher_submit_attempt`、`ad_lead_conversion_success` + `identify`；失败时沿用原有的 `quote_form_fallback_post` / `ad_lead_conversion_fallback_error` 事件名，便于看板延续。顺带修复 identify 里取错字段（`full_name` → `name`）。
- 报价表单服务选项从 4 个扩展为全部 10 个服务，并能按城市页传来的 slug（如 `?service=bathroom-tiling`）自动选中。

### 7.3 验证
- 本地 `npm run build` 863 页，`npm run verify` 0 错误。
- 表单浏览器测试：见下方 7.4（在预览站上用替换后的 `fetch` 测试，未向真实接口提交任何数据）。
