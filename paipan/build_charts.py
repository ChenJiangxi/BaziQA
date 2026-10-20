"""Cast BaZi and Zi Wei charts for every contest chart in data/ and write charts/.

usage:  pip install lunar-python && (cd paipan/ziwei && npm install) && python paipan/build_charts.py

Output (one file per contest year, keyed by person_id):
  charts/bazi/<file>.json   full chart under the default ``stated`` time convention, plus the four
                            pillars under ``clock`` and ``true_solar`` when those can be computed
  charts/ziwei/<file>.json  iztro chart cast from the ``stated`` 时辰

Self-check printed at the end: iztro computes its own day and hour pillars; they must equal the
BaZi engine's. (Year and month pillars may differ by design: Zi Wei turns the year at lunar New
Year and counts lunar months, BaZi turns at 立春 and counts solar terms.)
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bazi import cast  # noqa: E402
from timeconv import convert  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ZIWEI_DIR = Path(__file__).resolve().parent / 'ziwei'


def time_index(hhmm: str) -> int:
    h = int(hhmm[11:13])
    if h == 23:
        return 12            # 晚子
    if h == 0:
        return 0             # 早子
    return (h + 1) // 2


def pillars_only(chart: dict) -> list[str]:
    return [chart['pillars'][k]['ganzhi'] for k in ('year', 'month', 'day', 'hour')]


def main() -> None:
    files = sorted((ROOT / 'data').glob('hkjfma_*.json')) + sorted((ROOT / 'data').glob('contest8_*.json'))
    (ROOT / 'charts' / 'bazi').mkdir(parents=True, exist_ok=True)
    (ROOT / 'charts' / 'ziwei').mkdir(parents=True, exist_ok=True)
    engines = {'bazi': f"lunar-python {version('lunar-python')}",
               'ziwei': f"iztro {json.loads((ZIWEI_DIR / 'node_modules/iztro/package.json').read_text())['version']}"}
    mismatches, varies, late_zi, total = [], [], [], 0
    for f in files:
        data = json.loads(f.read_text(encoding='utf-8'))
        year = int(data[0]['current_year'])
        bazi_out, requests = {}, []
        for p in data[1:]:
            pid, birth, gender = p['person_id'], p['profile']['birth'], p['profile']['gender']
            conv = convert(birth)
            entry = {'case_no': p.get('case_no'), 'gender': gender, 'time': conv}
            if conv['stated'] is None:
                # birth hour unknown (the 2013 question asks for it): three pillars only
                noon = cast(f"{birth['year']:04d}-{birth['month']:02d}-{birth['day']:02d} 12:00", gender, year + 2)
                noon['pillars']['hour'] = None
                noon['note'] = 'birth hour unknown; year/month/day pillars and luck pillars cast at 12:00'
                entry['chart'] = noon
                entry['alternatives'] = {}
            else:
                entry['chart'] = cast(conv['stated']['datetime'], gender, year + 2)
                alts = {}
                for name in ('clock', 'true_solar'):
                    if conv[name]:
                        alts[name] = {'datetime': conv[name]['datetime'],
                                      'pillars': pillars_only(cast(conv[name]['datetime'], gender))}
                entry['alternatives'] = alts
                if conv['stated']['datetime'][11:13] == '23':
                    # 晚子时: schools that change the day at 23:00 use the next day's pillar
                    d1 = (datetime.strptime(conv['stated']['datetime'], '%Y-%m-%d %H:%M') + timedelta(days=1))
                    alts['day_changes_at_23h'] = {'datetime': conv['stated']['datetime'],
                                                  'day_pillar': pillars_only(cast(d1.strftime('%Y-%m-%d') + ' 00:30', gender))[2],
                                                  'note': '晚子时：若按 23:00 换日，日柱取次日'}
                base = pillars_only(entry['chart'])
                entry['hour_pillar_varies'] = any(a['pillars'][3] != base[3] for a in alts.values() if 'pillars' in a)
                entry['day_pillar_varies'] = any(a['pillars'][2] != base[2] for a in alts.values() if 'pillars' in a)
                if entry['hour_pillar_varies']:
                    varies.append(f"{year} {p.get('case_no')}")
                requests.append({'id': pid, 'date': conv['stated']['datetime'][:10],
                                 'timeIndex': time_index(conv['stated']['datetime']),
                                 'gender': '男' if gender == 'male' else '女'})
            bazi_out[pid] = entry
            total += 1
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
            json.dump(requests, tmp, ensure_ascii=False)
        ziwei = json.loads(subprocess.run(['node', str(ZIWEI_DIR / 'ziwei.mjs'), tmp.name],
                                          capture_output=True, text=True, check=True).stdout)
        Path(tmp.name).unlink()
        ziwei_out = {z['id']: z for z in ziwei}
        for pid, z in ziwei_out.items():
            zi = z['chinese_date'].split()
            bz = pillars_only(bazi_out[pid]['chart'])
            late = bazi_out[pid]['alternatives'].get('day_changes_at_23h')
            if zi[3] != bz[3] or zi[2] != (late['day_pillar'] if late else bz[2]):
                mismatches.append(f"{f.stem} {pid}: iztro {zi} vs bazi {bz}")
            elif late:
                late_zi.append(f"{f.stem} {pid}")
        meta = {'contest_id': data[0]['contest_id'], 'engine': engines, 'default_time_convention': 'stated'}
        (ROOT / 'charts' / 'bazi' / f.name).write_text(
            json.dumps({**meta, 'charts': bazi_out}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        (ROOT / 'charts' / 'ziwei' / f.name).write_text(
            json.dumps({**meta, 'charts': ziwei_out}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{total} charts cast with {engines}')
    print(f'hour pillar differs between time conventions in {len(varies)} charts: {", ".join(varies)}')
    print(f'晚子时 births (iztro changes the day at 23:00, BaZi default keeps it): {len(late_zi)}')
    print(f'unexpected iztro vs BaZi day/hour pillar mismatches: {len(mismatches)}')
    for m in mismatches:
        print('  ', m)


if __name__ == '__main__':
    main()
