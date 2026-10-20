# 出处存档（sources）

`data/` 下全部 17 年的真题（`hkjfma_2010.json` – `hkjfma_2020.json`、`contest8_2021.json` – `contest8_2026.json`）都是从下面这些原始来源整理出来的。
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
| 2021 第12届 | 9 张题目图 [hkjfma.org/?p=10036](https://hkjfma.org/?p=10036) → `images/2021_questions_*.jpg`；转载站转录 → `pages/2021_questions_feiyuntiegui_2494.txt`（逐张对照原图核对） | 官网未存答案表；原始发布版（v1.0.0）与转载站答案一致 | 转载 |
| 2022 第13届 | 官网未存题目原图；转载站转录 → `pages/2022_questions_feiyuntiegui_2495.txt`，与知乎重打稿 → `pages/2022_questions_zhihu_1894883708294635772.txt` 交叉核对 | 手写答案表 [hkjfma.org/?p=10070](https://hkjfma.org/?p=10070) → `images/2022_answer_key.jpg` | 官方 |
| 2023 第14届 | 官网题目原文 [hkjfma.org/?p=10091](https://hkjfma.org/?p=10091) → `pages/2023_hkjfma_official.txt` | 手写答案表 [hkjfma.org/?p=10105](https://hkjfma.org/?p=10105) → `images/2023_answer_key.jpg` | 官方 |
| 2024 第15届 | 官网未存题目原图；转载站转录 → `pages/2024_questions_feiyuntiegui_2556.txt`，分歧处对照知乎转载的 8 张题目图 [zhuanlan.zhihu.com/p/713492772](https://zhuanlan.zhihu.com/p/713492772) | 手写答案表 [hkjfma.org/?p=10885](https://hkjfma.org/?p=10885) → `images/2024_answer_key.jpg` | 官方 |
| 2025 第16届 | 8 张题目图 [hkjfma.org/?p=11465](https://hkjfma.org/?p=11465) → `images/2025_questions_*.jpg`（逐张核对） | 手写答案表 → `images/2025_answer_key.jpg` | 官方 |
| 2026 第17届 | 8 张题目图 [hkjfma.org/?p=13618](https://hkjfma.org/?p=13618) → `images/2026_questions_*.jpg`（2026-07-08 录入，2026-10-20 逐张重读） | 手写答案表 → `images/2026_answer_key.jpg` | 官方 |

## 转载站答案为什么可信

转载站 feiyuntiegui.com（「紫微星語」，2023-02-23 发布）汇总了 2010–2023 年的全部答案。
把它和本仓库手上所有的官方答案逐题比对，**10 个有官方答案的年份共 283 题，283 题完全一致**：

| 年份 | 2010 | 2011 | 2012 | 2013 | 2015 | 2016 | 2018 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| 一致 / 可比题数 | 9/9 | 15/15 | 15/15 | 16/16 | 34/34 | 34/34 | 40/40 | 40/40 | 40/40 | 40/40 |

（2015 年第 18 题官方接受 B 或 D、2016 年第 13 题转载站漏写，这两题不计入比对。）
所以 2014、2017、2019、2020 四年共 150 题采用该站答案；2021 年官网没有存档答案表，采用与原始发布版、该站都一致的答案。这五年共 190 题在 JSON 里标为 `"answer_source": "secondary"`。
如果你只想用官方答案，按这个字段过滤即可。

## 2015 年题目只有转载来源

官方题目帖没有被存档，2015 年题目全部来自转载站。这个站点的题目也能和其他年份的官方原文逐字比对：2018 年 200/200 个题干和选项完全一致，2014、2016、2017 年只差几个字，差异主要是它把「西曆」统一改写成「公历」，另有个别错字和一处漏题。所以 2015 年的题意可靠，个别用字可能和官方原帖有出入。年柱、命例顺序与官方答案帖（「1957丁酉年坤命 台灣 張評」等）全部吻合。

## 转写时做过的处理

- **简体化**：JSON 里的文字用 OpenCC（繁简转换库）转成简体；「乾命」「乾造」受保护，不会被转成「干」。
- **明显笔误**：只改了不影响题意的错别字（如「蓬了幾針」→「縫了幾針」），每一处都写在该年 JSON 的 `corrections` 字段里，原文保留在 `pages/`。
- **删去英文译文**：2013、2014、2018 年题目附有英文翻译，JSON 只收中文。
- **2018 年第 5 命例的生辰**：官网原文和 2018-06 的 Wayback 存档都漏印了出生资料。采用转载站 [ziweicn.com/show/3487.html](http://www.ziweicn.com/show/3487.html) 给出的「1940-10-13 未時，台灣」；排盘为庚辰年 丙戌月 己丑日 辛未時，四支正是辰戌丑未，与第 25 题题干「此辰戌丑未之女命」吻合。
- **2020 年答案**：转载站把 6–10 题写成「BCAAAA」（多了一个 A），去掉多余的 A 只有一种读法：6B 7C 8A 9A 10A。
- **出生时间**：原文只给时辰（或时间区间）的，`hour` 取中点（子=0、丑=2……亥=22），原写法留在 `time_raw`。时区、出生时刻的 UTC 偏移和夏令时按 IANA 时区数据库计算：117 个出生资料中，21 个处于香港或中国大陆的夏令时（UTC+9），12 个是 1982 年前的马来西亚、新加坡（UTC+7:30），1940 年的台湾（日治时期）和日本出生的各 1 个为 UTC+9。

## 2021–2025 年的重新转写（v2）

原始发布版（git 标签 `v1.0.0`，论文实验所用）的 2021–2025 年题目经过改写，并有转写错误。v2 按上表来源逐字重新转写，再与 v1 逐题对齐比较：

| 年份 | 与 v1 不同的题干/选项 | 其中改变题意的 | 命例更正 |
|---|---|---|---|
| 2021 | 53 | 0 | 第 8 命例 10:31 → 原文「10:30 左右」 |
| 2022 | 27 | 1（Q36 A「家境错误」→「家境贫穷」） | — |
| 2023 | 52 | 1（Q14 题干「婚前情状」→「命主目前婚姻感情状况」） | — |
| 2024 | 35 | 11 | 第 4 命例「午时」→「丑时」；第 5 命例「男命」→「坤命」（女） |
| 2025 | 52 | 19 | — |

判定依据：
- 2025 年的每一处都对照官方题图确认；2023 年以官网原文为准。
- 2024 年 v1 与转载站有分歧的地方，都用知乎转载的题目图裁定，结果全部支持转载站。例如第 6 题 v1 的「寡黙／慷慨／爱蟋蟀书画」，原题是「忧郁／戆直／爱虫鱼书画」；第 26、28 题有两个选项 v1 的整句内容与原题不同。第 4、5 命例的时辰和性别，转载站文字与知乎题目图一致，西历和农历两处写法也互相吻合。
- 2022 年 v1 的措辞与知乎重打稿一致，说明 v1 取自那篇；本版改用转载站的逐字转录，两份只在 Q36 A 有实质差异。
- 9 处改变题意的错误落在正确答案选项或题干上：2023 Q14 题干，2024 Q26 B、Q28 B、Q29 D，2025 Q17 D、Q22 A、Q25 B、Q36 C、Q39 C。

v1 的答案键全部正确（2022–2025 年对照官方答案表）。命主 ID 与题目 ID 沿用 v1，只有 2024 年第 5 命例因性别更正改名为 `female_19710412_P005`。

## 自查脚本

`python tools/verify.py` 会做三项检查。当前结果：

- **文字**：2010–2024 年每个题干和选项（共 2400 多个字符串）放回原文查找。差异都是 `corrections` 登记过的笔误更正，或已核实的转载站误差（2020 Q15、2021 Q23、2024 Q26）。
- **顺序**：每个选项都按 A→E 落在本题题干与下一题题干之间。
- **命例**：日期、性别与原文一致；原文印出的四柱、农历日期、「此X年男命」提示、题目里的大运及起运年份，与排盘库重算的结果全部吻合。

2025、2026 年只有图片来源，不在文字检查范围内，已对照原图逐字重读。
