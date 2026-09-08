# lifeos-media-pack · 中文社媒内容闭环技能包

> **English:** AI Agent Skills for a Chinese social-media content pipeline (WeChat Official Account / Channels / Xiaohongshu): voice profile → topic matrix → drafting → video script / cover cards → pre-publish gate → weekly review. Built for non-technical creators — each user builds their own voice profile first. MIT licensed.

多用户中文社媒内容流水线，7 个 SKILL.md 技能串成闭环，面向**公众号 → 视频号 → 小红书**三平台。改造自 [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills)（MIT），针对中文平台做了本地化。**技能是公共的，声线是私人的**：每个用户跑一次 `building-voice-base` 建自己的声音基座，一人一声，禁止共用。

## 闭环图

```
building-voice-base（声音基座，建一次用全年）
        │
        ▼
picking-topics（选题矩阵 4×8）◄──────────────┐
        │ 点格                                │
        ▼                                    │
writing-gongzhonggao（公众号成稿）            │
        │                                    │
   ┌────┴─────┐                              │
   ▼          ▼                              │
writing-    making-xhs-cards                 │
koubogao    （小红书图卡）                    │
（口播稿）    │                              │
   │          │      reviewing-weekly（周复盘）
   └────┬─────┘              │
        ▼                    │
checking-before-publish ──发布──► 数据回流 ─┘
（十二项自查，唯一否决权）
```

## 安装

```bash
# Claude Code
cp -r skills/* ~/.claude/skills/

# Codex / Gemini CLI / Copilot CLI（跨运行时别名目录）
cp -r skills/* ~/.agents/skills/
```

也可以试试技能市场命令（每个技能单独装）：`npx skills add wlkerwong-boop/lifeos-media-pack`

装完第一步永远是：对 AI 说「**帮我建声音基座**」。新手请看《安装指南.html》（浏览器打开，傻瓜式）。

## 与现有系统的关系
- Hermes 每晚 21:00 cron 往 `草稿池/` 写草稿：本包的 writing-gongzhonggao 负责把它抬成终稿
- 《自媒体系列化清单》管连载排期：picking-topics 管日常选题，互为补充
- 「视频合成」技能（ffmpeg+edge-tts）：writing-koubogao 的下游

## 工作区与路径（v0.2 多用户机制）
- 每个用户的工作区默认 `~/media-hub/`，内含三件套：`about-me.md` + `voice.md` + `paths.md`
- `paths.md` 由 building-voice-base 首次运行时生成，记录该用户的成稿/草稿/复盘目录与命名规范
- 其余 6 个技能全部从 `paths.md` 取路径，不写死任何人的目录
- 普光师兄的既有工作区：`~/Projects/media-hub/`（paths.md 已补齐）；LifeOS 产出在 `20-29 工作事业/24.02 自媒体运营/`，文件名守宪法 `YYYY-MM-DD-HHMMSS-主题.md`

## 给新用户安装
发整个文件夹给对方（或压缩包），看《安装指南.html》，三步装好 + 第一次跑「建声音基座」。指南面向技术小白，可直接转发。

## 状态
**v0.2 多用户版**（2026-09-08）。v0.1→v0.2：7 技能去个人化（称呼/路径/红线来源改为读用户自己的 about-me.md 与 paths.md），新增工作区机制与转发用安装指南。测试记录：第一轮为实测驱动（charlie947 原版包 9 项汉化缺口为基线）；v0.2 的多用户改造为结构化改动（未新增规则），沿用既有测试基线，后续两轮计划：真实周复盘一轮、新用户首跑一轮。按《宪法规则》第 1 条，满三轮测试方可转正。

## License
MIT（继承上游）。guizang 等中文同类仓库为 AGPL，本包未引用其任何代码。
