"""Re-run the consistency checks on data/hkjfma_*.json and data/contest8_2026.json.

1. text   - every stem and option, normalised (simplified script, no spaces/punctuation),
            must occur verbatim in the archived source text under sources/pages/.
            Expected misses are exactly the typo fixes listed in each file's `corrections`.
2. order  - walking through the source, each question's options must appear in A→E order
            between its own stem and the next question's stem.
3. birth  - date / gender in each chart must match its raw birth line; printed four pillars,
            lunar dates, "此X X男命" year clues and 大運 names/start years quoted in the
            questions must agree with a lunar-python chart computed from the stored fields.

2025 and 2026 are not covered by 1–2: their only sources are images (checked by reading them).

usage: pip install opencc lunar-python && python tools/verify.py
"""
import json
import re
import unicodedata
from pathlib import Path

import opencc
from lunar_python import Solar

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'sources' / 'pages'
CC = opencc.OpenCC('t2s')
PUNCT = re.compile(r'[\s　\xa0,，.。、:：;；?？!！()（）\[\]【】「」『』"“”\'‘’\-—–_~～·…/|＊*]+')
GZ = '[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
SOURCES = {
    2010: ['2010_hkjfma_official.txt'], 2011: ['2011_hkjfma_official.txt'],
    2012: ['2012_hkjfma_official.txt'], 2013: ['2013_hkjfma_official.txt'],
    2014: ['2014_hkjfma_official.txt', '2014_questions_forum_tid32668.txt'],
    2015: ['2015_questions_feiyuntiegui_2488.txt'], 2016: ['2016_questions_forum_tid33126.txt'],
    2017: ['2017_hkjfma_official.txt'], 2018: ['2018_hkjfma_official.txt'],
    2019: ['2019_questions_feiyuntiegui_2492.txt'], 2020: ['2020_questions_feiyuntiegui_2493.txt'],
    2021: ['2021_questions_feiyuntiegui_2494.txt'], 2022: ['2022_questions_feiyuntiegui_2495.txt'],
    2023: ['2023_hkjfma_official.txt'], 2024: ['2024_questions_feiyuntiegui_2556.txt'],
}


def norm(t):
    return PUNCT.sub('', CC.convert(unicodedata.normalize('NFKC', t)).lower())


def cn_num(t):
    digits = {'正': 1, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
              '冬': 11, '腊': 12, '臘': 12}
    t = t.replace('廿', '二十')
    if t.isdigit():
        return int(t)
    if t in digits:
        return digits[t]
    if '十' in t:
        hi, _, lo = t.partition('十')
        return (digits[hi] if hi else 1) * 10 + (digits[lo] if lo else 0)
    return None


def load(year):
    name = f'contest8_{year}.json' if year >= 2021 else f'hkjfma_{year}.json'
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))


def check_text_and_order():
    misses, order = [], []
    for y, files in SOURCES.items():
        src = norm('\n'.join((P / f).read_text(encoding='utf-8') for f in files))
        qs = [q for p in load(y)[1:] for q in p['questions']]
        cur = 0
        for k, q in enumerate(qs):
            for lab, txt in [('stem', q['question'])] + [(o[0], o[3:]) for o in q['options']]:
                if norm(txt) not in src:
                    misses.append(f'{y} Q{q["question_no"]} {lab}: {txt}')
            s = src.find(norm(q['question']), cur)
            if s < 0:
                continue
            nxt = src.find(norm(qs[k + 1]['question']), s + 1) if k + 1 < len(qs) else len(src)
            nxt = len(src) if nxt < 0 else nxt
            pos = s
            for o in q['options']:
                j = src.find(norm(o[3:]), pos + 1)
                if 0 <= j <= nxt:
                    pos = j
                elif norm(o[3:]) in src:      # present, but not where it belongs
                    order.append(f'{y} Q{q["question_no"]} option {o[0]} out of place: {o}')
            cur = s + 1
    return misses, order


def check_birth():
    issues = []
    years = list(SOURCES) + [2025, 2026]
    for y in years:
        for p in load(y)[1:]:
            b, g, raw = p['profile']['birth'], p['profile']['gender'], p['profile']['birth']['raw'] or ''
            tag = f"{y} C{p['case_no']}"
            m = re.search(r'(\d{4})\s*年\s*(?:生|[陽阳][曆历])?\s*(?:男命)?\s*[、,\-—]*\s*(\d{1,2})\s*月\s*[、,\-—]*\s*(\d{1,2})\s*日', raw)
            m2 = re.search(r'(?<!\d)(\d{2})-(\d{2})-(\d{4})', raw)
            m3 = re.search(r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})', raw)
            ymd = (tuple(map(int, m.groups())) if m else
                   (int(m2.group(3)), int(m2.group(2)), int(m2.group(1))) if m2 else
                   tuple(map(int, m3.groups())) if m3 else None)
            if ymd != (b['year'], b['month'], b['day']):
                issues.append(f'{tag}: stored date differs from raw line ({ymd})')
            says_m, says_f = bool(re.search('男|乾', raw)), bool(re.search('女|坤', raw))
            if says_m != says_f and (g == 'male') != says_m:
                issues.append(f'{tag}: gender {g} contradicts raw line')
            if b['hour'] is None:
                continue
            lunar = Solar.fromYmdHms(b['year'], b['month'], b['day'], b['hour'], b['minute'] or 0, 0).getLunar()
            ec = lunar.getEightChar()
            pillars = [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]
            text = ' '.join([raw] + p['context'] + [q['question'] + ' '.join(q['options']) for q in p['questions']])
            pm = re.search(rf'({GZ})年\s*[、,]?\s*({GZ})月\s*[、,]?\s*({GZ})日\s*[、,]?\s*({GZ})[时時]', raw)
            if pm and list(pm.groups()) != pillars:
                issues.append(f'{tag}: printed pillars {pm.groups()} ≠ computed {pillars}')
            lm = re.search(r'[农農][历曆][:：\s]*(?:[一二三四五六七八九〇零\d]{4}年|' + GZ + r'年)?\s*'
                           r'([正一二三四五六七八九十冬腊臘\d]{1,3})\s*月\s*初?([一二三四五六七八九十廿\d]{1,3})', raw)
            if lm:
                want = (cn_num(lm.group(1)), cn_num(lm.group(2)))
                got = (abs(lunar.getMonth()), lunar.getDay())
                nxt = Solar.fromYmd(b['year'], b['month'], b['day']).next(1).getLunar()
                if want != got and not (b['hour'] >= 23 and want == (abs(nxt.getMonth()), nxt.getDay())):
                    issues.append(f'{tag}: printed lunar date {lm.group(0)} ≠ computed {got}')
            for yc in re.findall(rf'此({GZ})[男女]命', text):
                if yc != pillars[0]:
                    issues.append(f'{tag}: text calls it a {yc} year, computed {pillars[0]}')
            if '紫微' in (p['setter']['method'] or ''):
                continue                    # 紫微 大限 names are palace stems, not 八字 大運
            dys = {d.getGanZhi(): d.getStartYear() for d in ec.getYun(1 if g == 'male' else 0).getDaYun()[1:]}
            for gz in set(re.findall(rf'({GZ})\s*大?[运運]', text)):
                if gz not in dys:
                    issues.append(f'{tag}: text names a {gz}运, computed 大运 are {list(dys)}')
            for m in re.finditer(rf'({GZ})\s*大?[运運]\s*的?\s*[（(]\s*(\d{{4}})', text):
                gz, yr = m.groups()
                if text[max(0, m.start() - 1)] == '至':   # "甲午至乙未運(1974-1994)": the year belongs to 甲午
                    continue
                if gz not in dys or abs(int(yr) - dys[gz]) > 1:
                    issues.append(f'{tag}: text puts {gz}运 at {yr}, computed {dys.get(gz)}')
    return issues


if __name__ == '__main__':
    misses, order = check_text_and_order()
    # A miss is expected when the year's `corrections` names that question, or when the source
    # itself is a second-hand transcription that was overruled by the original image.
    KNOWN = {(2020, 15): 'repost reads 慨; the original image has 嘅',
             (2024, 26): 'repost truncates 分手原因 to 分手原; the Zhihu copy has the full word',
             (2021, 23): 'repost reads 以及; the original image has 與及'}
    unexplained = []
    for x in misses:
        y, q = int(x[:4]), int(re.search(r'Q(\d+)', x).group(1))
        listed = re.search(rf'Q{q}(?!\d)', ' '.join(load(y)[0]['corrections']))
        if not listed and (y, q) not in KNOWN:
            unexplained.append(x)
    print(f'[text] {len(misses)} strings differ from source; {len(misses) - len(unexplained)} are listed corrections '
          f'or known source errors; {len(unexplained)} unexplained:')
    for x in unexplained:
        print('   ', x)
    order = [o for o in order if not re.search(rf'Q{re.search(r"Q(\d+)", o).group(1)}(?!\d)',
                                                 ' '.join(load(int(o[:4]))[0]['corrections']))]
    print(f'[order] {len(order)} options out of place (corrected options excluded):')
    for x in order:
        print('   ', x)
    issues = check_birth()
    print(f'[birth] {len(issues)} issues:')
    for x in issues:
        print('   ', x)
