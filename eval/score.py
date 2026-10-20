"""Score model predictions against the BaziQA answer keys.

Predictions: JSONL, one line per question: {"question_id": "...", "answer": "B", "run": 1}
(``run`` is optional; lines with the same run number form one run). Missing questions count as
wrong and are reported as missing.

usage:
  python eval/score.py preds.jsonl                         # default track: contest8 (2021–2026)
  python eval/score.py preds.jsonl --track full            # 2010–2026, all 555 questions
  python eval/score.py preds.jsonl --track official        # official answer keys only (365)
  python eval/score.py preds.jsonl --bazi-only --json report.json

Reported per year: accuracy (mean ± sd over runs), the contest's own trimmed score (drop the best
and/or worst case as that year's rules did), and majority-vote accuracy when there are several
runs. The headline number is the macro average: mean over years of each year's mean over runs.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = {
    'contest8': 'contest years 2021–2026, eight setters × five questions (240 questions)',
    'full': 'all 17 editions 2010–2026 (555 questions)',
    'official': 'only questions whose answer key is the organiser\'s own (365 questions)',
}


def load_keys() -> dict:
    keys = {}
    files = sorted((ROOT / 'data').glob('hkjfma_*.json')) + sorted((ROOT / 'data').glob('contest8_*.json'))
    for f in files:
        data = json.loads(f.read_text(encoding='utf-8'))
        meta, year = data[0], int(data[0]['current_year'])
        for p in data[1:]:
            method = (p.get('setter') or {}).get('method') or ''
            for q in p['questions']:
                qid = q['question_id']
                assert qid not in keys, f'duplicate question_id {qid}'
                keys[qid] = {'year': year, 'case': str(p.get('case_no', p['person_id'])).rstrip('ab'),
                             'accepted': q.get('accepted_answers', [q['answer']]),
                             'answer_source': meta.get('answer_source', 'official'),
                             'bazi': '八字' in method}
    return keys


def trimmed(year: int, per_case: dict) -> int:
    """The contest's own score: 2014 dropped the best case; from 2015 the best and the worst."""
    s = sorted(per_case.values())
    if year >= 2015 and len(s) > 2:
        return sum(s[1:-1])
    if year == 2014 and len(s) > 1:
        return sum(s[:-1])
    return sum(s)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('predictions', nargs='+')
    ap.add_argument('--track', choices=TRACKS, default='contest8')
    ap.add_argument('--years', default=None, help='override the track years, e.g. 2018-2026 or 2021,2023')
    ap.add_argument('--bazi-only', action='store_true', help='keep only charts whose setter used BaZi')
    ap.add_argument('--json', default=None, help='also write a machine-readable report')
    args = ap.parse_args()

    keys = load_keys()
    if args.years:
        years = set()
        for part in args.years.split(','):
            a, _, b = part.partition('-')
            years |= set(range(int(a), int(b or a) + 1))
    else:
        years = set(range(2021, 2027)) if args.track == 'contest8' else set(range(2010, 2027))
    qset = {qid: k for qid, k in keys.items() if k['year'] in years
            and (args.track != 'official' or k['answer_source'] == 'official')
            and (not args.bazi_only or k['bazi'])}

    runs = defaultdict(dict)                       # run -> {qid: answer}
    unknown = 0
    for path in args.predictions:
        for line in open(path, encoding='utf-8'):
            if not line.strip():
                continue
            r = json.loads(line)
            if r['question_id'] not in keys:
                unknown += 1
                continue
            runs[r.get('run', 1)][r['question_id']] = (r.get('answer') or '').strip().upper()[:1]

    by_year = defaultdict(list)
    for qid, k in qset.items():
        by_year[k['year']].append(qid)
    report = {'track': args.track, 'bazi_only': args.bazi_only, 'years': sorted(by_year),
              'questions': len(qset), 'runs': len(runs), 'per_year': {}}
    print(f"track: {args.track} — {TRACKS[args.track]}{' — BaZi charts only' if args.bazi_only else ''}")
    print(f"questions: {len(qset)}   runs: {len(runs)}" + (f"   ignored unknown ids: {unknown}" if unknown else ''))
    print(f"{'year':>5} {'n':>4} {'accuracy':>16} {'trimmed score':>16} {'majority vote':>14} {'missing':>8}")
    year_means = []
    for year in sorted(by_year):
        qids = by_year[year]
        accs, trims, missing = [], [], 0
        for run in sorted(runs):
            pred = runs[run]
            per_case = defaultdict(int)
            correct = 0
            for qid in qids:
                ok = pred.get(qid, '') in qset[qid]['accepted']
                correct += ok
                per_case[qset[qid]['case']] += ok
                missing += qid not in pred
            accs.append(correct / len(qids))
            # full marks of the trimmed score: every case has five questions from 2014 on
            out_of = len(qids) - (10 if year >= 2015 else 5 if year == 2014 else 0)
            trims.append((trimmed(year, per_case), out_of))
        mean = st.mean(accs) if accs else 0.0
        sd = st.pstdev(accs) if len(accs) > 1 else 0.0
        vote = None
        if len(runs) > 1:
            votes = 0
            for qid in qids:
                c = Counter(runs[r].get(qid, '') for r in runs).most_common()
                top = c[0][1]
                tied = sorted(a for a, n in c if n == top)
                votes += tied[0] in qset[qid]['accepted']      # ties broken alphabetically
            vote = votes / len(qids)
        tmean = st.mean(t for t, _ in trims) if trims else 0
        year_means.append(mean)
        report['per_year'][year] = {'n': len(qids), 'accuracy_mean': mean, 'accuracy_sd': sd,
                                    'per_run': accs, 'trimmed_mean': tmean,
                                    'trimmed_out_of': trims[0][1] if trims else None,
                                    'majority_vote': vote, 'missing_predictions': missing}
        print(f"{year:>5} {len(qids):>4} {100 * mean:>9.1f}% ±{100 * sd:>4.1f} "
              f"{tmean:>9.1f}/{trims[0][1] if trims else 0:<5} "
              f"{'' if vote is None else f'{100 * vote:.1f}%':>14} {missing:>8}")
    macro = st.mean(year_means) if year_means else 0.0
    report['macro_accuracy'] = macro
    print(f"macro-average accuracy over {len(year_means)} years: {100 * macro:.1f}%"
          "   (random guessing ≈ 25%; 2010, 2011 and 2020 Q1–5 have five options)")
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
