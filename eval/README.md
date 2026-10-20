# 评测口径与工具（eval）

这里规定 BaziQA 的成绩怎么算、怎么报告，并提供一个可直接运行的基线。不同团队只要按这里的口径报告，数字就能直接比较。

## 1. 预测文件格式

JSONL，每行一道题：

```json
{"question_id": "female_19831028_P004-Q16", "answer": "B", "run": 1}
```

- `question_id` 取自 `data/*.json`；`answer` 是选项字母；`run` 是第几次运行（不写默认为 1）。
- 漏答按答错计，`score.py` 会单独列出漏答数。

## 2. 计分

```bash
python eval/score.py preds.jsonl                       # 默认赛道 contest8
python eval/score.py preds.jsonl --track full          # 全部 17 届
python eval/score.py preds.jsonl --track official      # 只用官方答案
python eval/score.py preds.jsonl --bazi-only           # 只算八字命例
python eval/score.py run1.jsonl run2.jsonl --json report.json
```

| 赛道 | 范围 | 题数 | 用途 |
|---|---|---|---|
| `contest8`（默认） | 2021–2026 | 240 | 主榜。格式统一：每年 8 位老师 × 5 题，4 选 1 |
| `full` | 2010–2026 | 555 | 全量。早年题量少，2010、2011 年为 5 选 1 |
| `official` | 只含官方答案的年份 | 365 | 排除转载答案（2014、2017、2019–2021） |

每年输出：
- 正确率：多次运行时给出均值 ± 标准差；
- 官方式成绩：按当年规则去掉最好、最差命例；
- 多数票正确率：有多次运行时给出。

**头条数字是宏平均**：先对每年的各次运行取均值，再对年份取均值。这和论文的统计口径相同。

`--bazi-only` 只保留出题老师注明用八字的命例。注明紫微、奇门和未注明术数的命例都会被排除。

## 3. 报告成绩时必须写明

1. **数据版本**：git 标签，如 `v2.2.0`；论文数字对应 `v1.0.0`。
2. **赛道与筛选**：`contest8` / `full` / `official`，是否 `--bazi-only`。
3. **运行次数与汇总方式**：建议至少 3 次。单次运行同一套题的波动可达 ±3 题（约 ±7.5 个百分点）。
4. **排盘口径**：默认 `stated`；改用 `clock` 或 `true_solar` 要注明。见 [`../paipan/README.md`](../paipan/README.md)。
5. **是否给模型看紫微盘**：`--ziwei auto/always/never`。
6. **模型名称、版本和解码参数**（temperature 等）。

## 4. 基线：多轮问答

`run_baseline.py` 就是论文里的 Multi-turn 基线，适用于任何 OpenAI 兼容接口：

1. 每个命例开一段独立对话；
2. 第一轮把排盘交给模型，请它做一般性的命盘分析；
3. 之后逐题提问，每题最后一行写「答案：X」；
4. 解析不到答案时追问一次。

提示词全部写在脚本里，没有针对答案调过。

```bash
pip install openai
export OPENAI_API_KEY=...
python eval/run_baseline.py --files contest8_2021 contest8_2022 contest8_2023 contest8_2024 contest8_2025 contest8_2026 \
    --model <模型名> --base-url <接口地址> --runs 3 --out preds/<模型名>.jsonl
python eval/score.py preds/<模型名>.jsonl
python eval/run_baseline.py --files contest8_2026 --dry-run    # 只打印提示词，不调用接口
```

模型看到的内容：
- 命主资料：性别、出生时间与原文写法、出生地；
- 出题老师给的已知信息；
- 八字盘；
- 出题老师注明用紫微的命例，另附紫微盘（`--ziwei auto`）。

不会看到答案和整理者备注 `notes`。原文出生行照原样给出，其中有些带着出题老师的署名。

论文当年用的排盘工具是 xuan-utils-pro（Java）。它底层用的也是 6tail 的 lunar 历法库，和这里的 lunar-python 同源，所以四柱算法一致。不过两者的输出字段不同（例如这里没有神煞），出生时间口径和 v1 数据也不同，所以用本基线复现的数字会和论文有出入。

## 5. 建议的盲测赛道

题目和答案公开后，新模型可能在训练时见过它们。每届比赛在截止日前不公布答案，那时提交的预测天然没有这个问题。建议每年在截止日前把模型预测存档（带时间戳的提交或 PR），赛后用官方答案打分，并与当届人类冠军并列报告。
