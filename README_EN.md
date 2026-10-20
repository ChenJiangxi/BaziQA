# BaziQA: 17 Years of Real Fortune-Telling Contest Questions

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Paper](https://img.shields.io/badge/arXiv-2602.12889-b31b1b.svg)](https://arxiv.org/abs/2602.12889)

[中文](README.md) | **English**

BaziQA is a benchmark for Chinese fortune-telling reasoning (mainly BaZi / Four Pillars, plus Zi Wei Dou Shu and Qi Men Dun Jia). It contains **all 555 questions from the 17 editions (2010–2026) of the Global Fortune Teller Contest** run by the Hong Kong Junior Fengshui Master Association.

Each question was written by a practising fortune-teller about a real person. The correct answer is what actually happened in that person's life. The organiser publishes the answer key and the champion's score every year, so a model can be scored and also compared directly with the best human practitioners.

The dataset and paper ([arXiv:2602.12889](https://arxiv.org/abs/2602.12889)) power the [AuraMate](https://auramate.net/) app.

## Highlights

- **Real people, real outcomes**: 117 birth charts, 555 multiple-choice questions, about 70 question setters. Answers are life events, not annotator opinions.
- **Human baseline**: contest champions answered 43%–78% correctly; random guessing gives 25%.
- **Traceable**: every file records where its questions and answers came from; the original pages, question images and answer sheets are archived in [`sources/`](sources/). Years whose official key is lost are marked `answer_source: "secondary"` so they can be excluded.
- **Chart-ready birth data**: place, the time as written, the two-hour period (shichen), and the UTC offset and daylight-saving status at the moment of birth. 35 of the 117 charts are not at plain UTC+8 (Hong Kong and mainland summer time, Malaysia and Singapore at UTC+7:30 before 1982).
- **Reproducible and self-checking**: `tools/build.py` rebuilds every JSON file from hand-checked transcriptions; `tools/verify.py` checks each question against its source text and each chart against a computed BaZi chart.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/human_champion_accuracy_dark.png">
  <img alt="Champion accuracy in the Global Fortune Teller Contest, 2010–2026: between 43% and 78%; random guessing is 20–25%" src="docs/human_champion_accuracy_light.png">
</picture>

## Quick start

```python
import json, glob
for f in sorted(glob.glob('data/hkjfma_*.json')) + sorted(glob.glob('data/contest8_*.json')):
    data = json.load(open(f, encoding='utf-8'))
    meta, persons = data[0], data[1:]
    print(meta['current_year'], meta['answer_source'], meta['total_questions'])
```

Each file is a JSON array: element 0 is contest metadata, the rest are birth charts, each with its questions (`question`, `options`, `answer`). Text is in Simplified Chinese; the Traditional originals are kept in `tools/src/`.

## What is inside

| Part | Charts | Questions |
|---|---|---|
| Contest editions 1–17 (2010–2026) | 117 | 555 |
| Celebrity50 | 50 | 488 |

- 365 contest questions use the organiser's official answer key; 190 (2014, 2017, 2019–2021) use a repost whose answers match every official key we could check (283 of 283 questions).
- 2010, 2011 and the first case of 2020 have five options per question; all others have four.
- Several cases were set with Zi Wei Dou Shu or Qi Men Dun Jia; filter on `setter.method` for BaZi-only evaluation.

## Charts and evaluation

- [`charts/`](charts/): BaZi and Zi Wei Dou Shu charts for all 117 birth records, cast with [lunar-python](https://github.com/6tail/lunar-python) and [iztro](https://github.com/SylarLong/iztro) (both MIT); engine and time conventions in [`paipan/`](paipan/README.md). The default reading uses the written two-hour period, or the clock time minus summer time; clock-time and apparent-solar-time pillars are included, and the 12 charts whose hour pillar depends on the choice are flagged.
- [`eval/`](eval/README.md): `score.py` (per-year accuracy, the contest's trimmed score, majority vote, macro average), the paper's multi-turn baseline `run_baseline.py` for any OpenAI-compatible API, and the reporting rules (data version, track, number of runs, time convention).

```bash
pip install -r requirements.txt
python eval/run_baseline.py --files contest8_2026 --model <model> --base-url <url> --runs 3 --out preds.jsonl
python eval/score.py preds.jsonl
```

## Versions

Version 2 re-transcribed every question from the earliest source available (official question images and web pages first). Against the 2021–2025 data used in the paper (tag [`v1.0.0`](https://github.com/ChenJiangxi/BaziQA/tree/v1.0.0/data)), it fixes 32 wording errors that changed a question's meaning (9 of them in the correct option or the question stem) and 2 wrong birth charts (one wrong hour, one wrong gender). Answer keys were correct. Use `v1.0.0` to reproduce the paper; use the current data for new work. Details: [`sources/README.md`](sources/README.md).

## Citation

```bibtex
@dataset{bazi_QA,
  title={BaZi Fortune-Telling QA Dataset},
  author={Jiangxi Chen},
  year={2025},
  publisher={GitHub},
  url={https://github.com/ChenJiangxi/BaziQA}
}
```

## License and disclaimer

Transcriptions, metadata and code are MIT-licensed. The contest questions belong to the Hong Kong Junior Fengshui Master Association and the individual setters; they are included with attribution for research. This dataset is for research and AI evaluation only and is not fortune-telling advice.
