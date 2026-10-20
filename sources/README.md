# 出处存档（sources）

`data/hkjfma_2010.json` – `hkjfma_2020.json` 和 `data/contest8_2026.json` 都是从下面这些原始页面整理出来的。
主办方香港青年術數家協會的旧论坛（forum.hkjfma.org）已经下线，所以论坛内容只能依赖 Wayback Machine（archive.org 的网页存档）。
这里保留原文（繁体，按发布时的样子）和关键图片，方便以后核对转写和答案。

- `pages/`：网页正文的纯文本导出（繁体原文，未改字）
- `images/`：只以图片形式发布的题目、答案表和得奖名单
- 逐题转写稿在 `../tools/src/YYYY.md`，由 `../tools/build.py` 转成 `data/` 下的 JSON

## 逐年出处

| 年份 | 题目来源 | 答案来源 | 答案可信度 |
|---|---|---|---|
| 2010 第1届 | [hkjfma.org/?p=109](https://hkjfma.org/?p=109) → `pages/2010_hkjfma_official.txt` | 同页答案段 | 官方 |
| 2011 第2届 | [hkjfma.org/?p=124](https://hkjfma.org/?p=124) → `pages/2011_hkjfma_official.txt` | 同页答案段 | 官方 |
| 2012 第3届 | [hkjfma.org/?p=131](https://hkjfma.org/?p=131) → `pages/2012_hkjfma_official.txt` | 同页答案段 | 官方 |
| 2013 第4届 | [hkjfma.org/?p=412](https://hkjfma.org/?p=412) → `pages/2013_hkjfma_official.txt` | 同页「答案公報」 | 官方 |
| 2014 第5届 | [hkjfma.org/?p=477](https://hkjfma.org/?p=477) → `pages/2014_hkjfma_official.txt`；论坛原帖 [Wayback](https://web.archive.org/web/20190921022814/http://forum.hkjfma.org/discuz/forum.php?mod=viewthread&tid=32668&extra=page%3D1) → `pages/2014_questions_forum_tid32668.txt` | 官方答案帖未被存档；用转载站 → `pages/answers_2010-2023_feiyuntiegui_2496.txt` | 转载 |
| 2015 第6届 | 官方题目帖未被存档；用转载站 [feiyuntiegui.com/?id=2488](http://www.feiyuntiegui.com/?id=2488) → `pages/2015_questions_feiyuntiegui_2488.txt` | 论坛「正確答案」帖 [Wayback](https://web.archive.org/web/20191020082554/http://forum.hkjfma.org/discuz/forum.php?mod=viewthread&tid=32957&extra=page%3D1) → `pages/2015_answers_forum_tid32957.txt` | 官方 |
| 2016 第7届 | 论坛题目帖 [Wayback](https://web.archive.org/web/20190923160006/http://www.forum.hkjfma.org/discuz/forum.php?mod=viewthread&tid=33126&extra=page%3D1) → `pages/2016_questions_forum_tid33126.txt` | 论坛答案帖第 2 楼 [Wayback](https://web.archive.org/web/20191022213457/http://www.forum.hkjfma.org/discuz/forum.php?mod=viewthread&tid=33155) → `pages/2016_answers_forum_tid33155.txt` | 官方 |
| 2017 第8届 | [hkjfma.org/?page_id=7657](https://hkjfma.org/?page_id=7657) → `pages/2017_hkjfma_official.txt` | 官网只公布得奖者；用转载站 | 转载 |
| 2018 第9届 | [hkjfma.org/?page_id=9264](https://hkjfma.org/?page_id=9264) → `pages/2018_hkjfma_official.txt` | 手写答案表 [hkjfma.org/?page_id=9290](https://hkjfma.org/?page_id=9290) → `images/2018_answer_key.jpg` | 官方 |
| 2019 第10届 | 10 张题目图 [hkjfma.org/?page_id=9345](https://hkjfma.org/?page_id=9345) → `images/2019_questions_*.png`；转载站的文字转录 → `pages/2019_questions_feiyuntiegui_2492.txt`（仅作交叉核对） | 官网答案页只有得奖名单和作答分布截图；用转载站 | 转载 |
| 2020 第11届 | 8 张题目图 [hkjfma.org/?p=10007](https://hkjfma.org/?p=10007) → `images/2020_questions_*.jpg`；转载站的文字转录 → `pages/2020_questions_feiyuntiegui_2493.txt`（仅作交叉核对） | 官网答案页只有得奖名单；用转载站 | 转载 |
| 2026 第17届 | 8 张题目图 [hkjfma.org/?p=13618](https://hkjfma.org/?p=13618)（2026-07-08 录入） | 手写答案表 → `images/2026_answer_key.jpg` | 官方 |

## 转载站答案为什么可信

转载站 feiyuntiegui.com（「紫微星語」，2023-02-23 发布）汇总了 2010–2023 年的全部答案。
把它和本仓库手上所有的官方答案逐题比对，**10 个有官方答案的年份共 283 题，283 题完全一致**：

| 年份 | 2010 | 2011 | 2012 | 2013 | 2015 | 2016 | 2018 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| 一致 / 可比题数 | 9/9 | 15/15 | 15/15 | 16/16 | 34/34 | 34/34 | 40/40 | 40/40 | 40/40 | 40/40 |

（2015 年第 18 题官方接受 B 或 D、2016 年第 13 题转载站漏写，这两题不计入比对。）
所以 2014、2017、2019、2020 四年共 150 题采用该站答案，并在 JSON 里标为 `"answer_source": "secondary"`。
如果你只想用官方答案，按这个字段过滤即可。

## 2015 年题目只有转载来源

官方题目帖没有被存档，2015 年题目全部来自转载站。这个站点的题目也能和其他年份的官方原文逐字比对：2018 年 200/200 个题干和选项完全一致，2014、2016、2017 年只差几个字，差异主要是它把「西曆」统一改写成「公历」，另有个别错字和一处漏题。所以 2015 年的题意可靠，个别用字可能和官方原帖有出入。年柱、命例顺序与官方答案帖（「1957丁酉年坤命 台灣 張評」等）全部吻合。

## 转写时做过的处理

- **简体化**：JSON 里的文字用 OpenCC（繁简转换库）转成简体，和 2021–2025 年的原有文件一致；「乾命」「乾造」受保护，不会被转成「干」。
- **明显笔误**：只改了不影响题意的错别字（如「蓬了幾針」→「縫了幾針」），每一处都写在该年 JSON 的 `corrections` 字段里，原文保留在 `pages/`。
- **删去英文译文**：2013、2014、2018 年题目附有英文翻译，JSON 只收中文。
- **2018 年第 5 命例的生辰**：官网原文和 2018-06 的 Wayback 存档都漏印了出生资料。采用转载站 [ziweicn.com/show/3487.html](http://www.ziweicn.com/show/3487.html) 给出的「1940-10-13 未時，台灣」；排盘为庚辰年 丙戌月 己丑日 辛未時，四支正是辰戌丑未，与第 25 题题干「此辰戌丑未之女命」吻合。
- **2020 年答案**：转载站把 6–10 题写成「BCAAAA」（多了一个 A），去掉多余的 A 只有一种读法：6B 7C 8A 9A 10A。
