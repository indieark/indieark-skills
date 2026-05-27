# landing-cyberpunk-game

**路线**：`style-mockup` → landing 变体
**风格**：cyberpunk · Low-life High-tech 废土反乌托邦
**Extension 调用**：`ui-ux-pro-max`（默认分支 / 67 styles 库）
**生成日期**：2026-05-27
**Skill 版本**：v0.2.0 router-alpha + taste-skill 融合后

## S3 锁定的美学方向（注意，这是这条产物的灵魂）

- 气质：Low-life High-tech 废土反乌托邦 cyberpunk
- 受众：极客 / 玩家 / 独立游戏关注者
- 子流派：废墟感重 + CRT 残影 + 故障 / glitch / chromatic aberration
- 内容类型：独立游戏 launch landing（虚构游戏 NULL // RUN）
- 一句话差异化：**「整页核心叙事是一台 4:3 红框 CCTV 监视器播放着无脸 runner 的最后镜头」**——不是 hero 大字 + 三列卡片，而是把「被抹除身份」的 game lore 物化成监视器画面；CTA 包装成「上传 payload 警告框」

## ui-ux-pro-max 67 styles 库调用

- `#41 Cyberpunk UI` — 主风格立场
- `#7 Dark Mode (OLED)` — 深色基底
- `#51 HUD / Sci-Fi FUI` — 监视器 overlay 元素
- `#67 Chromatic Aberration / RGB Split` — 故障美学

**注意**：默认 67 styles 库里的 cyberpunk 配色是 matrix 绿 `#00FF00`，本产物刻意拒绝默认套路，改用「深紫 + 品红 + 青 + 警示红」四色 palette。这是 S3 美学方向门拍板的具体落地——不是 extension 默认推荐。

## 选用的 palette + font pairing

- Palette：BG `#0A0010` / Surface `#16002A` / Text `#E9CBFF` / Cyan `#00F0FF` / Magenta `#FF2E9C` / Red CTA `#FF003C`
- Fonts：Major Mono Display（display）+ IBM Plex Mono（body）+ Space Mono（terminal）

## 五维 critique 摘要

- 视觉冲击：Pass — CCTV 红框 + phosphor glow + 全页 CRT 扫描线 + 9s 节奏故障跳一次的 hero 标题
- 信息层级：Pass — kicker → title → subtitle → 4 项 stats → 双 CTA 节奏标准但 stats 是叙事道具
- 交互细节：**Partial** — hover 走 `skewX + chromatic-aberration`（替代禁用的 `translateY(-4px)`）已落地；遗憾点是未引入 IntersectionObserver 做 sector 卡逐张揭示
- 工程质量：Pass — CSS 变量化 / `prefers-reduced-motion` 全覆盖 / `:focus-visible` 键盘可达 / `aria-labelledby` / `role="img"` / 4 档断点 / 无外链 JS
- **差异化记忆点：Pass** — 「红框 CCTV + 无脸 runner + 终端 cat profile + Wishlist 警示框」是元素级具体钩子，能一句话讲清「这是台监视器，被你看到的人是被抹除身份的玩家角色」

## 反 AI slop 黑名单核查

| 项 | 状态 |
|---|---|
| Inter / Roboto / Arial / system-ui | ✅ 0 命中 |
| 白底 + 紫渐变 + 灰卡片 | ✅ 0 命中（深紫黑 + 品红警示） |
| hero + 3 列卡 + CTA + footer 套版 | ✅ 替换为 CCTV hero + 非对称 5 卡 sector board |
| `translateY(-4px)` + 软阴影 hover | ✅ 替换为 `skewX + chromatic-aberration` |
| 「Build, Ship, Scale」「Future of X」文案 | ✅ 替换为 `< NO_FACE > // last seen: SECTOR_7` / `we don't phone home` 等 hacker terminal 路子 |

## 残余风险

- Google Fonts CDN 依赖，离线场景气质缩水约 30%
- CCTV 监视器场景是纯 CSS shape art，若有概念原画建议替换 + 保留 CRT overlay
- 故障节奏 9s 一次是刻意低频，marketing 要求强 hook 时可调到 5s
- CTA `href="#"` 占位，真 Steam wishlist 链上线需替换

## 预览

```bash
cd skills/html-gen-pro/skills/html-gen-pro/examples/landing-cyberpunk-game/
python -m http.server 8088
# 访问 http://localhost:8088
```

或直接 `file://` 打开 [index.html](index.html)（注意 Google Fonts 在 file:// 下可能被 CORS 拦截）。
