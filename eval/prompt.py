"""Turn a chart from charts/ into plain text for a model prompt.

The text contains only what is on the chart and what the question setter gave; it never contains
answers. Person names are not used (the contest data is anonymous).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PILLAR_NAMES = {'year': '年柱', 'month': '月柱', 'day': '日柱', 'hour': '时柱'}


def load_year(file_stem: str) -> tuple[dict, list, dict, dict]:
    """Return (meta, persons, bazi_charts, ziwei_charts) for e.g. 'contest8_2024' or 'hkjfma_2015'."""
    data = json.loads((ROOT / 'data' / f'{file_stem}.json').read_text(encoding='utf-8'))
    bazi = json.loads((ROOT / 'charts' / 'bazi' / f'{file_stem}.json').read_text(encoding='utf-8'))['charts']
    ziwei = json.loads((ROOT / 'charts' / 'ziwei' / f'{file_stem}.json').read_text(encoding='utf-8'))['charts']
    return data[0], data[1:], bazi, ziwei


def wants_ziwei(person: dict, mode: str) -> bool:
    if mode == 'always':
        return True
    if mode == 'never':
        return False
    return '紫微' in (person['setter'].get('method') or '')      # auto: the setter used Zi Wei


def bazi_text(entry: dict) -> str:
    c = entry['chart']
    lines = ['【八字排盘】']
    for k, name in PILLAR_NAMES.items():
        p = c['pillars'][k]
        if p is None:
            lines.append(f'{name}：未知')
            continue
        hidden = '、'.join(f"{h['gan']}（{h['shishen']}）" for h in p['zhi_canggan'])
        lines.append(f"{name}：{p['ganzhi']}　天干十神 {p['gan_shishen']}　藏干 {hidden}　纳音 {p['nayin']}　长生 {p['dishi']}")
    lines.append(f"日主：{c['day_master']}　日柱旬空：{c['pillars']['day']['xunkong']}　胎元 {c['taiyuan']}　命宫 {c['minggong']}　身宫 {c['shengong']}")
    q = c['qiyun']
    lines.append(f"起运：出生后 {q['after_years']} 年 {q['after_months']} 个月 {q['after_days']} 天起运（{q['start_date']}），{'顺行' if q['direction'] == 'forward' else '逆行'}")
    lines.append('大运：' + '；'.join(f"{d['ganzhi']}（{d['start_year']}–{d['end_year']}，虚岁 {d['start_age']}–{d['end_age']}）" for d in c['dayun']))
    if c.get('liunian'):
        lines.append('流年：' + '，'.join(f'{y}{gz}' for y, gz in c['liunian'].items()))
    return '\n'.join(lines)


def ziwei_text(z: dict) -> str:
    lines = ['【紫微斗数排盘】',
             f"农历 {z['lunar_date']}，{z['time']}（{z['time_range']}）；五行局 {z['five_elements_class']}；命主 {z['soul']}；身主 {z['body']}；"
             f"命宫在{z['soul_palace_branch']}，身宫在{z['body_palace_branch']}"]
    palaces = z['palaces']
    start = next((i for i, p in enumerate(palaces) if p['name'] in ('命宫', '命')), 0)
    for p in palaces[start:] + palaces[:start]:                    # 从命宫起排
        def fmt(stars):
            return '、'.join(s['name'] + (s.get('brightness') or '') + (f"（化{s['mutagen']}）" if s.get('mutagen') else '') for s in stars) or '无'
        dec = p.get('decadal') or {}
        rng = dec.get('range')
        name = p['name'] if p['name'].endswith('宫') else p['name'] + '宫'
        lines.append(f"{name}（{p['stem']}{p['branch']}{'，身宫' if p['is_body_palace'] else ''}）：主星 {fmt(p['major_stars'])}；"
                     f"辅星 {fmt(p['minor_stars'])}；杂曜 {'、'.join(p['adjective_stars']) or '无'}；长生 {p['changsheng12']}"
                     + (f"；大限 {rng[0]}–{rng[1]} 岁" if rng else ''))
    return '\n'.join(lines)


def chart_text(meta: dict, person: dict, bazi: dict, ziwei: dict, ziwei_mode: str = 'auto') -> str:
    """Everything a model may see about one chart, before any question."""
    b = person['profile']['birth']
    entry = bazi[person['person_id']]
    t = entry['time']
    used = t['stated']['datetime'] if t['stated'] else f"{b['year']}-{b['month']:02d}-{b['day']:02d}（时辰不详）"
    lines = [f"当前年份：{meta['current_year']} 年",
             '【命主资料】',
             f"性别：{'男' if person['profile']['gender'] == 'male' else '女'}",
             f"出生（公历）：{used}" + (f"（原文：{b['raw']}）" if b.get('raw') else ''),
             f"出生地：{b.get('place') or '原文未写'}"]
    if person.get('context'):
        lines.append('出题老师提供的已知信息：' + '；'.join(person['context']))
    lines.append('')
    lines.append(bazi_text(entry))
    z = ziwei.get(person['person_id'])
    if z and wants_ziwei(person, ziwei_mode):
        lines.append('')
        lines.append(ziwei_text(z))
    return '\n'.join(lines)
