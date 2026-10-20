"""Draw docs/human_champion_accuracy_{light,dark}.png for the README.

Data = the champion's raw score (questions right / questions asked) as published by the
organiser each year; years whose winners' table was not archived are left out.
Sources: sources/pages/*winners*, sources/images/*winners*, sources/images/*answer_key*.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
# year: (champion correct, questions, options per question)
DATA = {2010: (6, 9, 5), 2011: (8, 15, 5), 2012: (8, 15, 4), 2015: (15, 35, 4), 2016: (23, 35, 4),
        2018: (19, 40, 4), 2019: (20, 40, 4), 2020: (17, 40, 4), 2022: (19, 40, 4), 2023: (21, 40, 4),
        2024: (26, 40, 4), 2026: (31, 40, 4)}
THEMES = {
    'light': dict(surface='#fcfcfb', text='#0b0b0b', muted='#52514e', grid='#e4e3df', series='#2a78d6'),
    'dark': dict(surface='#1a1a19', text='#ffffff', muted='#c3c2b7', grid='#383835', series='#3987e5'),
}
plt.rcParams['font.family'] = ['PingFang SC', 'Heiti SC', 'Arial Unicode MS']


def draw(mode):
    c = THEMES[mode]
    years = list(DATA)
    pct = [100 * a / b for a, b, _ in DATA.values()]
    chance = [100 / k for _, _, k in DATA.values()]
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
    fig.patch.set_facecolor(c['surface']); ax.set_facecolor(c['surface'])
    xs = range(len(years))
    w = 0.56
    for x, v in zip(xs, pct):            # bars with a rounded data-end, square at the baseline
        ax.add_patch(FancyBboxPatch((x - w / 2, 0), w, v, boxstyle='round,pad=0,rounding_size=0.08',
                                    mutation_aspect=12, linewidth=0, facecolor=c['series']))
        ax.add_patch(plt.Rectangle((x - w / 2, 0), w, min(v, 3), linewidth=0, facecolor=c['series']))
    # chance level: 20% in the 5-option years, 25% otherwise
    for x, ch in zip(xs, chance):
        ax.plot([x - 0.45, x + 0.45], [ch, ch], color=c['muted'], linewidth=1.6, linestyle=(0, (3, 2)))
    hi, lo = max(pct), min(pct)           # label only the extremes; the README table has every year
    for x, v, (a, b, _) in zip(xs, pct, DATA.values()):
        if v in (hi, lo):
            ax.text(x, v + 1.6, f'{a}/{b}', color=c['text'], fontsize=9, ha='center', va='bottom')
    ax.set_xticks(list(xs), [str(y) for y in years], color=c['muted'], fontsize=9)
    ax.set_xlim(-0.6, len(years) - 0.4); ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'], color=c['muted'], fontsize=9)
    ax.yaxis.grid(True, color=c['grid'], linewidth=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right', 'left'):
        ax.spines[s].set_visible(False)
    ax.spines['bottom'].set_color(c['grid'])
    ax.tick_params(length=0)
    fig.text(0.06, 0.95, '全球算命師大賽 历届冠军的正确率', color=c['text'], fontsize=13, fontweight='bold', va='top')
    fig.text(0.06, 0.885, '虚线为随机猜测（4 选 1 为 25%，2010–2011 年 5 选 1 为 20%）；2013、2014、2017、2021、2025 年冠军总分未找到存档',
             color=c['muted'], fontsize=8.5, va='top')
    fig.subplots_adjust(left=0.06, right=0.98, top=0.8, bottom=0.09)
    out = ROOT / 'docs' / f'human_champion_accuracy_{mode}.png'
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, facecolor=c['surface']); plt.close(fig)
    return out


if __name__ == '__main__':
    for m in THEMES:
        print(draw(m))
