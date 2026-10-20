"""Build BaziQA JSON files from the hand-checked markup in src/YYYY.md.

Output keeps the layout of the original contest8_*.json files (element 0 = contest metadata,
then one object per chart) and adds provenance fields. Text is converted to Simplified Chinese
with OpenCC so every year reads the same way; the Traditional originals stay in sources/.

usage: pip install opencc && python tools/build.py data
"""
import json
import re
import sys
from pathlib import Path

import opencc

HERE = Path(__file__).parent
CC = opencc.OpenCC('t2s')
PROTECT = {'乾命': '命', '乾造': '造', '乾坤': '坤'}
SHICHEN_MID = {z: (i * 2) % 24 for i, z in enumerate('子丑寅卯辰巳午未申酉戌亥')}  # 子=0, 丑=2 … 亥=22


def s(text):
    if text is None:
        return None
    for k, v in PROTECT.items():
        text = text.replace(k, v)
    out = CC.convert(text)
    return out.replace('', '乾')


def parse(path):
    meta, cases, cur, q = {}, [], None, None
    for raw in path.read_text(encoding='utf-8').split('\n'):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith('@case'):
            parts = [p.strip() for p in line[len('@case'):].split('|')]
            attrs = dict(p.split('=', 1) for p in parts[1:])
            cur = {'case': parts[0], **attrs, 'raw': '', 'info': [], 'note': [], 'questions': []}
            cases.append(cur)
            q = None
            continue
        key, _, val = line.partition(': ')
        if cur is None:
            meta.setdefault(key.strip(), []).append(val.strip())
            continue
        if key in ('raw',):
            cur['raw'] = val
        elif key in ('info', 'note'):
            cur[key].append(val)
        elif key == 'Q':
            q = {'stem': val, 'options': []}
            cur['questions'].append(q)
        elif re.fullmatch(r'[A-E]', key):
            assert q is not None, line
            assert len(q['options']) == 'ABCDE'.index(key), f'{path.name}: option order at {line!r}'
            q['options'].append(val)
        else:
            raise ValueError(f'{path.name}: cannot parse {line!r}')
    return {k: v if len(v) > 1 else v[0] for k, v in meta.items()}, cases


def birth(c, year):
    y, m, d = (int(x) for x in c['date'].split('-'))
    t = c.get('time', '')
    out = {'year': y, 'month': m, 'day': d, 'hour': None, 'minute': None,
           'place': s(c.get('place', '')) or None, 'approximate': None, 'time_raw': s(t) or None,
           'raw': s(c['raw'])}
    if re.fullmatch(r'\d{1,2}:\d{2}', t):
        out['hour'], out['minute'] = (int(x) for x in t.split(':'))
        out['approximate'] = bool(c.get('approx'))
    elif re.fullmatch(r'[子丑寅卯辰巳午未申酉戌亥][時时]', t):
        out['hour'], out['minute'] = SHICHEN_MID[t[0]], 0
        out['approximate'] = True  # only the two-hour 时辰 is known; hour is its midpoint
    elif t:
        raise ValueError(f'{year} case {c["case"]}: unknown time {t!r}')
    return out


def build(year, out_dir):
    meta, cases = parse(HERE / 'src' / f'{year}.md')
    key = meta['key'].replace(' ', '')
    accept = {}
    for a in ([meta['accept']] if isinstance(meta.get('accept'), str) else meta.get('accept', [])):
        m = re.match(r'Q(\d+)=([A-E|]+)\s*(.*)', a)
        accept[int(m.group(1))] = (m.group(2).split('|'), m.group(3))
    nq = sum(len(c['questions']) for c in cases)
    assert nq == len(key), f'{year}: {nq} questions but key has {len(key)} letters'
    fixes = meta.get('fix', [])
    fixes = [fixes] if isinstance(fixes, str) else fixes

    persons, n = [], 0
    for c in cases:
        b = birth(c, year)
        g = c['gender']
        pid = f"{year}_C{c['case']}_{g}_{c['date'].replace('-', '')}"
        place = b['place'] or '出生地不详'
        person = {
            'person_id': pid,
            'name': f"{b['year']}年{place}出生{'男性' if g == 'male' else '女性'}",
            'case_no': c['case'],
            'profile': {'birth': b, 'gender': g},
            'setter': {'name': s(c.get('provider')) or None, 'method': s(c.get('method')) or None},
            'context': [s(x) for x in c['info']],
            'notes': [s(x) for x in c['note']],
            'categories': {'感情': [], '财富': [], '六亲': [], '事业': [], '健康': []},
            'questions': [],
        }
        for q in c['questions']:
            n += 1
            ans = key[n - 1]
            labels = 'ABCDE'[:len(q['options'])]
            assert ans in labels, f'{year} Q{n}: answer {ans} not among {labels}'
            item = {
                'question_id': f'{pid}-Q{n}',
                'question_no': n,
                'question': s(q['stem']),
                'options': [f'{l}. {s(o)}' for l, o in zip(labels, q['options'])],
                'answer': ans,
            }
            if n in accept:
                item['accepted_answers'] = accept[n][0]
                item['answer_note'] = s(accept[n][1])
                assert ans in item['accepted_answers']
            person['questions'].append(item)
        persons.append(person)

    head = {
        'contest_id': f'hkjfma_{year}',
        'current_year': str(year),
        'edition': int(meta['edition']),
        'title': s(meta['title']),
        'description': s(f"香港青年术数家协会「全球算命师大赛」第{meta['edition']}届真题。"
                         f"{meta['format']}。参赛者根据命主的出生资料选择最符合其命运情况的答案。"),
        'total_questions': nq,
        'num_charts': len(persons),
        'scoring': s(meta['scoring']),
        'answer_source': meta['answer_source'],
        'sources': {'questions': s(meta['questions_source']), 'answers': s(meta['answers_source'])},
        'corrections': [s(f) for f in fixes],
    }
    out = Path(out_dir) / (f'contest8_{year}.json' if year >= 2021 else f'hkjfma_{year}.json')
    out.write_text(json.dumps([head] + persons, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return out, nq, len(persons)


if __name__ == '__main__':
    out_dir = sys.argv[1]
    years = [int(p.stem) for p in sorted((HERE / 'src').glob('*.md')) if re.fullmatch(r'\d{4}', p.stem)]
    for y in years:
        print(*build(y, out_dir))
