"""Birth-time conventions used for chart casting.

Three readings of the same birth record:

* ``stated``  – the benchmark default. If the source gives only a two-hour period (时辰), that
  period is used as written. If it gives a clock time, daylight saving time is removed, giving
  the local standard time in force at birth (Hong Kong 1941–1979, Taiwan 1945–1979 and mainland
  China 1986–1991 had summer time).
* ``clock``   – the clock time exactly as written (summer time not removed).
* ``true_solar`` – local apparent solar time: standard time + 4 min per degree east of the zone
  meridian + the equation of time. Only computed when the source gives a clock time and the
  birthplace has coordinates.

Time zones come from the IANA database (``zoneinfo``), so historical offsets such as Malaysia and
Singapore at UTC+7:30 before 1982 or Taiwan at UTC+9 before 1945 are applied automatically.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

PLACES = json.loads((Path(__file__).with_name('places.json')).read_text(encoding='utf-8'))
SHICHEN = '子丑寅卯辰巳午未申酉戌亥'


def place_info(place: str | None) -> dict:
    """Coordinates and IANA zone for a birthplace string used in the dataset."""
    if not place:
        return {'lon': None, 'lat': None, 'tz': None, 'precision': None}
    return PLACES.get(place, {'lon': None, 'lat': None, 'tz': None, 'precision': None})


def shichen_of(hour: int, minute: int = 0) -> str:
    """Two-hour period of a clock time: 23:00–00:59 子, 01:00–02:59 丑 …"""
    return SHICHEN[((hour + 1) % 24) // 2]


def equation_of_time(dt: datetime) -> float:
    """Equation of time in minutes (NOAA approximation, error < 1 min)."""
    doy = dt.timetuple().tm_yday
    g = 2 * math.pi / 365 * (doy - 1 + (dt.hour - 12) / 24)
    return 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                     - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))


def convert(birth: dict) -> dict:
    """Return the datetime and 时辰 under each convention for one ``profile.birth`` record."""
    info = place_info(birth.get('place'))
    tz = birth.get('timezone') or info.get('tz')
    out = {'place': birth.get('place'), 'lon': info.get('lon'), 'lat': info.get('lat'),
           'location_precision': info.get('precision'), 'timezone': tz}
    if birth.get('hour') is None:
        return {**out, 'stated': None, 'clock': None, 'true_solar': None}
    y, m, d, h, mi = birth['year'], birth['month'], birth['day'], birth['hour'], birth['minute'] or 0
    clock = datetime(y, m, d, h, mi)
    exact = not birth.get('approximate')
    dst_min = 0
    std_offset_min = None
    if tz:
        aware = clock.replace(tzinfo=ZoneInfo(tz))
        dst_min = int(aware.dst().total_seconds() // 60)
        std_offset_min = int(aware.utcoffset().total_seconds() // 60) - dst_min
    standard = clock - timedelta(minutes=dst_min)

    def pack(dt: datetime | None, basis: str):
        if dt is None:
            return None
        return {'datetime': dt.strftime('%Y-%m-%d %H:%M'), 'shichen': shichen_of(dt.hour, dt.minute), 'basis': basis}

    if exact:
        stated = pack(standard, 'clock time with summer time removed' if dst_min else 'clock time (no summer time in force)')
    else:
        stated = pack(clock, f"时辰 as written ({birth.get('time_raw')}); hour set to its midpoint")
    true_solar = None
    if exact and info.get('lon') is not None and std_offset_min is not None:
        meridian = std_offset_min / 4.0          # degrees east of Greenwich of the zone's meridian
        lon_corr = 4.0 * (info['lon'] - meridian)
        eot = equation_of_time(standard)
        dt = standard + timedelta(minutes=lon_corr + eot)
        true_solar = pack(dt, f'standard time {lon_corr:+.0f} min longitude {eot:+.1f} min equation of time')
        true_solar['correction_minutes'] = round(lon_corr + eot, 1)
    return {**out, 'dst_minutes': dst_min, 'standard_utc_offset_minutes': std_offset_min,
            'stated': stated, 'clock': pack(clock, 'as written') if exact else None, 'true_solar': true_solar}
