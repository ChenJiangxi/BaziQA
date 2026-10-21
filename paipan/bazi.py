"""BaZi (Four Pillars) chart casting with lunar-python (https://github.com/6tail/lunar-python, MIT).

Conventions (the library defaults, the same family of algorithms as lunar-javascript):
* year pillar changes at 立春, month pillar at each solar term (节);
* the day pillar changes at 23:00 (子初换日, lunar-python EightChar sect 1): a birth between 23:00 and
  23:59 takes the next day's day pillar, matching the hour pillar, which already starts the next day.
  Pass ``sect=2`` for the other school (晚子时日柱算当天); the library's default is 2, and with it the
  day stem and the 子-hour stem come from different days;
* luck-pillar start age by the 3-days-per-year rule (yun sect 1).
"""
from __future__ import annotations

from datetime import datetime

from lunar_python import Solar

GAN = '甲乙丙丁戊己庚辛壬癸'
ZHI = '子丑寅卯辰巳午未申酉戌亥'


def year_ganzhi(year: int) -> str:
    """干支 label of a Gregorian year (as used for 流年, counted from 立春)."""
    return GAN[(year - 4) % 10] + ZHI[(year - 4) % 12]


def cast(dt_str: str, gender: str, liunian_until: int | None = None, sect: int = 1) -> dict:
    """Cast a chart for 'YYYY-MM-DD HH:MM' local time; gender 'male' / 'female'.

    sect 1 (default): the day changes at 23:00. sect 2: a 23:00–23:59 birth keeps the same day."""
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    lunar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, 0).getLunar()
    ec = lunar.getEightChar()
    ec.setSect(sect)

    def pillar(name: str) -> dict:
        g = getattr(ec, f'get{name}')
        gz = g()
        return {
            'ganzhi': gz,
            'gan_shishen': getattr(ec, f'get{name}ShiShenGan')(),
            'zhi_canggan': [{'gan': h, 'shishen': s} for h, s in zip(getattr(ec, f'get{name}HideGan')(),
                                                                   getattr(ec, f'get{name}ShiShenZhi')())],
            'nayin': getattr(ec, f'get{name}NaYin')(),
            'dishi': getattr(ec, f'get{name}DiShi')(),       # 日干在该支的十二长生
            'xunkong': getattr(ec, f'get{name}XunKong')(),
        }

    yun = ec.getYun(1 if gender == 'male' else 0)
    dayun = [{'index': d.getIndex(), 'ganzhi': d.getGanZhi(), 'start_year': d.getStartYear(),
              'end_year': d.getEndYear(), 'start_age': d.getStartAge(), 'end_age': d.getEndAge()}
             for d in yun.getDaYun()[1:10]]
    out = {
        'datetime': dt_str,
        'lunar_date': lunar.toString(),
        'pillars': {k: pillar(n) for k, n in (('year', 'Year'), ('month', 'Month'), ('day', 'Day'), ('hour', 'Time'))},
        'day_master': ec.getDayGan(),
        'taiyuan': ec.getTaiYuan(), 'minggong': ec.getMingGong(), 'shengong': ec.getShenGong(),
        'qiyun': {'after_years': yun.getStartYear(), 'after_months': yun.getStartMonth(),
                  'after_days': yun.getStartDay(), 'start_date': yun.getStartSolar().toYmd(),
                  # 阳年男、阴年女顺行，反之逆行（年干按立春）
                  'direction': 'forward' if (GAN.index(ec.getYearGan()) % 2 == 0) == (gender == 'male') else 'backward'},
        'dayun': dayun,
    }
    if liunian_until:
        out['liunian'] = {str(y): year_ganzhi(y) for y in range(dt.year, liunian_until + 1)}
    return out
