# lifeos-media-pack · 中文社媒内容闭环技能包

普光师兄专属的中文社媒内容流水线，7 个 SKILL.md 技能串成闭环，面向**公众号 → 视频号 → 小红书**三平台。改造自 [charlie947/social-media-skills](https://github.com/charlie947/social-media-skills)（MIT），针对中文平台与 LifeOS 规则做了本地化。

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

## 与现有系统的关系
- Hermes 每晚 21:00 cron 往 `草稿池/` 写草稿：本包的 writing-gongzhonggao 负责把它抬成终稿
- 《自媒体系列化清单》管连载排期：picking-topics 管日常选题，互为补充
- 「视频合成」技能（ffmpeg+edge-tts）：writing-koubogao 的下游

## 固定路径约定
- 声音基座：`~/Projects/media-hub/about-me.md` + `voice.md`
- LifeOS 产出：`20-29 工作事业/24.02 自媒体运营/`（草稿池/成稿区/发布复盘），文件名守宪法 `YYYY-MM-DD-HHMMSS-主题.md`

## 状态
**v0.1 试用版**（2026-09-08）。测试记录：第一轮为实测驱动（charlie947 原版包在真实项目中的 9 项汉化缺口为基线，写作参数来自当日实测跑通值）；后续两轮测试计划见 `docs` 待补。按《宪法规则》第 1 条，满三轮测试方可转正。

## License
MIT（继承上游）。guizang 等中文同类仓库为 AGPL，本包未引用其任何代码。
