"""Score model predictions against the BaziQA answer keys.

Predictions: JSONL, one line per question: {"question_id": "...", "answer": "B", "run": 1}
``answer`` is the option letter (``B``, ``b``, ``(B)`` and ``B.`` are accepted; anything else, such
as ``答案：B``, counts as no answer). Lines with the same ``run`` number form one run, across all
files given. A file whose lines have no ``run`` field is one run of its own, so
``score.py a.jsonl b.jsonl`` scores two runs. Questions with no prediction or no valid letter count
as wrong and are reported in the ``no answer`` column (summed over runs).

usage:
  python eval/score.py preds.jsonl                         # default track: contest8 (2021–2026)
  python eval/score.py preds.jsonl --track full            # 2010–2026, all 555 questions
  python eval/score.py preds.jsonl --track official        # official answer keys only (365)
  python eval/score.py preds.jsonl --bazi-only --json report.json

Reported per year: accuracy (mean ± sd over runs), the contest's own trimmed score (drop the best
and/or worst case as that year's rules did), and majority-vote accuracy when there are several
runs (blank answers do not vote; a tie earns fractional credit). The headline number is the macro
average: mean over years of each year's mean over runs. Years with no predictions at all are left
out with a warning, so a partial run never turns into a full-track number.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = {
    'contest8': 'contest years 2021–2026, eight setters × five questions (240 questions)',
    'full': 'all 17 editions 2010–2026 (555 questions)',
    'official': 'only questions whose answer key is the organiser\'s own (365 questions)',
}


LETTER = re.compile(r'[(（]?([A-Ea-e])[)）.。、]?')


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


def dropped(year: int, n_cases: int) -> int:
    """How many cases the contest's own scoring drops: 2014 the best one, from 2015 the best and worst."""
    if year >= 2015 and n_cases > 2:
        return 2
    if year == 2014 and n_cases > 1:
        return 1
    return 0


def trimmed(year: int, per_case: dict) -> int:
    """The contest's own score, computed on the cases in scope."""
    s = sorted(per_case.values())
    d = dropped(year, len(s))
    if d == 2:
        return sum(s[1:-1])
    if d == 1:
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
    unknown = duplicates = invalid = 0
    for i, path in enumerate(args.predictions, 1):
        for line in open(path, encoding='utf-8'):
            if not line.strip():
                continue
            r = json.loads(line)
            if r['question_id'] not in keys:
                unknown += 1
                continue
            # explicit run numbers are shared across files; a file without them is its own run
            run = f"run {r['run']}" if 'run' in r else f'file {i}'
            m = LETTER.fullmatch(str(r.get('answer') or '').strip())
            invalid += m is None and bool(str(r.get('answer') or '').strip())
            duplicates += r['question_id'] in runs[run]
            runs[run][r['question_id']] = m.group(1).upper() if m else ''

    by_year = defaultdict(list)
    for qid, k in qset.items():
        by_year[k['year']].append(qid)
    # a run counts for a year only if it has at least one prediction in that year
    present = {(run, keys[q]['year']) for run, pred in runs.items() for q in pred}
    absent = sorted(y for y in by_year if not any((r, y) in present for r in runs))
    for y in absent:
        del by_year[y]
    report = {'track': args.track, 'bazi_only': args.bazi_only, 'runs': sorted(runs), 'per_year': {}}
    print(f"track: {args.track} — {TRACKS[args.track]}{' — BaZi charts only' if args.bazi_only else ''}")
    print(f"questions: {sum(len(v) for v in by_year.values())}   runs: {len(runs)} ({', '.join(sorted(runs))})"
          + (f"   ignored unknown ids: {unknown}" if unknown else ''))
    if duplicates:
        print(f"WARNING: {duplicates} repeated (run, question) lines; the last one was kept")
    if invalid:
        print(f"WARNING: {invalid} answers are not a bare option letter and were scored as no answer")
    if absent:
        print(f"WARNING: no predictions for {', '.join(map(str, absent))}; those years are left out, "
              f"so the macro average below is NOT a full-track number")
    report['years_without_predictions'] = absent
    print(f"{'year':>5} {'n':>4} {'accuracy':>16} {'trimmed score':>16} {'majority vote':>14} {'no answer':>10}")
    year_means = []
    for year in sorted(by_year):
        qids = by_year[year]
        accs, trims, missing = [], [], 0
        year_runs = [r for r in sorted(runs) if (r, year) in present]
        for run in year_runs:
            pred = runs[run]
            per_case = defaultdict(int)
            correct = 0
            for qid in qids:
                ok = pred.get(qid, '') in qset[qid]['accepted']
                correct += ok
                per_case[qset[qid]['case']] += ok
                missing += not pred.get(qid)
            accs.append(correct / len(qids))
            # full marks of the trimmed score (every case has five questions from 2014 on)
            out_of = len(qids) - 5 * dropped(year, len(per_case))
            trims.append((trimmed(year, per_case), out_of))
        mean = st.mean(accs) if accs else 0.0
        sd = st.pstdev(accs) if len(accs) > 1 else 0.0
        vote = None
        if len(year_runs) > 1:
            votes = 0.0
            for qid in qids:
                c = Counter(a for a in (runs[r].get(qid, '') for r in year_runs) if a).most_common()
                if not c:
                    continue
                tied = [a for a, n in c if n == c[0][1]]
                # a tie gets fractional credit instead of an arbitrary winner
                votes += sum(a in qset[qid]['accepted'] for a in tied) / len(tied)
            vote = votes / len(qids)
        tmean = st.mean(t for t, _ in trims) if trims else 0
        year_means.append(mean)
        report['per_year'][year] = {'n': len(qids), 'accuracy_mean': mean, 'accuracy_sd': sd,
                                    'per_run': accs, 'trimmed_mean': tmean,
                                    'trimmed_out_of': trims[0][1] if trims else None,
                                    'majority_vote': vote, 'no_answer': missing}
        print(f"{year:>5} {len(qids):>4} {100 * mean:>9.1f}% ±{100 * sd:>4.1f} "
              f"{tmean:>9.1f}/{trims[0][1] if trims else 0:<5} "
              f"{'' if vote is None else f'{100 * vote:.1f}%':>14} {missing:>10}")
    macro = st.mean(year_means) if year_means else 0.0
    report['macro_accuracy'] = macro
    print(f"macro-average accuracy over {len(year_means)} years: {100 * macro:.1f}%"
          "   (random guessing ≈ 25%; 2010, 2011 and 2020 Q1–5 have five options)")
    if args.json:
        Path(args.json).write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
