# P0 技术 SEO 与信任修复成果报告

> 日期：2026-11-03
> 对应诊断：`docs/08_网站流量诊断报告_结构功能审美SEO与GEO全面分析.md`
> 分支：`claude/seo-audit-fix-e81615`（PR 待所有者审核合并，合并部署后才在线上生效）

## 一、修复清单

| # | 问题（诊断章节） | 修复方式 | 涉及文件 |
|---|---|---|---|
| 1 | sitemap 中 849 个 URL 全部 308 到带斜杠版本，canonical 却是带斜杠版本（2.1） | `build.format: 'file'` + `trailingSlash: 'never'`，产物变为 `services.html`、`bathroom-tiling/leeds.html`；canonical 统一由 `absUrl()` 生成无斜杠绝对地址 | `astro.config.mjs`、`src/lib/site.ts`、`src/layouts/Layout.astro` |
| 2 | 软 404：不存在的地址返回 200 + 首页（2.3） | 新增 `404.astro`（`noindex`，带服务导航）；Cloudflare Pages 检测到 `404.html` 后会返回真正的 404 | `src/pages/404.astro` |
| 3 | 每个城市页声明一个"位于该城市"的商家，含编造地址、占位电话、`aggregateRating 4.96/350`（2.2） | 改为**全站一个 Organization**（只写可核实信息：名称、网址、logo、公开邮箱、服务国家），每页一个 `Service`，`provider` 指向该 Organization，`areaServed` 为城市；删除评分、电话、PostalAddress；删除 840 页完全相同的 HowTo | `[service]/[city].astro`、`Layout.astro` |
| 4 | 首页 `HomeAndConstructionBusiness` 同样带占位电话与评分；FAQPage 在页面上不可见 | 删除重复商家实体；首页新增与 FAQPage 一致的可见 FAQ 区块 | `src/pages/index.astro` |
| 5 | `AggregateOffer.lowPrice` 解析错误（"£1400 - £1550" 被截成 `140`） | 新增 `parsePrice()` 正确解析 | `src/lib/site.ts` |
| 6 | 面包屑第 3 级指向不存在的 `/{service}/london` | 新增 **10 个服务聚合页** `/{service}`，面包屑与可见面包屑导航都指向它 | `src/pages/[service]/index.astro` |
| 7 | 没有服务级落地页；`/services`、首页服务卡片分别链到 Westminster / Reading 的城市页 | 服务聚合页内容全部来自数据集：伦敦 / 非伦敦两档价格表、施工流程、包含项、常用砖型、按区域列出全部 84 个地点；`/services`、首页、`/areas`、页脚、404 都链到聚合页 | 同上 + `services/index.astro`、`areas/index.astro`、`Layout.astro` |
| 8 | 首页 16 条死链（旧 `uk_towns.json` 城市、旧 `services_config.json` 服务） | 首页改用数据集中真实存在的 84 个城市与 10 个服务 | `src/pages/index.astro` |
| 9 | 首页邮编/城镇搜索无论输入什么都跳到 Reading | 按城镇名、slug、邮编前缀（如 `LS1 4AP` → Leeds）匹配；匹配不到就带邮编进入 `/quote` | `src/pages/index.astro` |
| 10 | "附近地区"显示的英里数是随机生成、不真实的（4.2） | 去掉英里数与"35 英里范围"表述，改为"同区域其他地点 + 查看全部地点"；链接保留 | `[service]/[city].astro` |
| 11 | 全站顶部"Rated 4.96/5 by 350+ UK Homeowners"无法核实（4.3） | 改为"Free, no-obligation quotes" | `Layout.astro` |
| 12 | 840 条 meta description 含"5-star rated"，且同服务只有 1 种写法 | 用数据集字段生成：服务 + 城市 + 邮编 + 郡 + 该城小户型价格 + 工期，每页唯一，去掉评分表述 | `[service]/[city].astro` |
| 13 | 城市页 title 过长（最长 85+ 字符）、无品牌 | `{服务} in {城市} – Costs & Free Quotes | Approved Tilers` | 同上 |
| 14 | "Average … Costs (2025)" 与全站 2026 矛盾 | 改为不带年份的 "Typical … Costs"，并注明是参考区间、最终价格在免费勘测后锁定 | 同上 |
| 15 | 事实卡面向用户显示"AI & SEARCH FACT SHEET"、跳动绿点"Active Trade Availability"、"Verified Regional Data" | 改为"QUICK FACTS"，去掉无法核实的可用性与"已核实"表述；`<section aria-label>` 便于机器理解 | `src/components/GeoFactSheet.astro` |
| 16 | 广告落地页 `/promo/*` 可被收录 | `noindex, follow`（本来就不在 sitemap 中） | `src/pages/promo/*.astro`、`Layout.astro`（新增 `noindex` 参数） |
| 17 | sitemap lastmod 全部是构建日期 | 按 git 最后提交日期生成；取不到 git 历史时不输出 lastmod；新增 10 个聚合页 | `scripts/generate_seo_geo.mjs` |
| 18 | llms.txt："UK's premier"、示例链接 `kensington-and-chelsea` 是死链、服务路径带斜杠；llms-full 只列 7 个服务；BS 5385-3/-4 描述错误 | 改为"online referral network"；修正示例链接；服务链接改为无斜杠聚合页地址；城市目录列全 10 个服务；按标准名称修正 BS 5385-3/-4 描述；伦敦价格差说明与数据一致（约 30–36%） | 同上、`public/llms*.txt` |
| 19 | 手机端没有导航菜单；平板宽度（768px）菜单"Price Guide"折成两行 | 新增 `<details>` 汉堡菜单（≥1024px 显示完整导航）；手机端隐藏副标题与 "AT" 方块、按钮改为"Free Quote"，消除横向溢出 | `Layout.astro` |
| 20 | Cookie 横幅关闭后每页都重新弹出 | 用 `localStorage` 记住关闭状态（存储不可用时退化为每页显示） | `Layout.astro` |
| 21 | `twitter:card = summary_large_image` 但无图片 | 改为 `summary` | `Layout.astro` |
| 22 | about / contact / reviews / services / areas / 首页 description 过短或泛化 | 重写为具体、唯一的描述 | 各页面 |
| 23 | 缺少可重复执行的产物检查 | 新增 `scripts/verify_dist.py` 与 `npm run verify` | `scripts/verify_dist.py`、`package.json` |

## 二、验证

### 本地构建（`npm run build`）
- 863 页（原 852 页 + 10 个服务聚合页 + 404）。
- `npm run verify` 对全部 863 个 HTML 逐页检查，**0 错误**：
  - 每页恰好 1 个 `<title>`（在 `<head>` 内）/ 1 个 canonical / 1 条 description；
  - canonical 等于页面自身的无斜杠 URL；
  - 860 个可收录页面的 title、description 全部互不重复；
  - JSON-LD 全部可解析，且不含 `aggregateRating`、占位电话、`PostalAddress`、`HowTo`；
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
