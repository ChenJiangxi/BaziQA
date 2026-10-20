// Zi Wei Dou Shu charts with iztro (https://github.com/SylarLong/iztro, MIT).
// usage: node ziwei.mjs requests.json > charts.json
// requests.json: [{"id": "...", "date": "YYYY-M-D", "timeIndex": 0-12, "gender": "男"|"女"}]
// timeIndex: 0 早子 00:00–00:59, 1 丑 … 11 亥, 12 晚子 23:00–23:59 (iztro convention)
import { readFileSync } from 'node:fs';
import { astro } from 'iztro';

const star = (s) => {
  const o = { name: s.name };
  if (s.brightness) o.brightness = s.brightness;   // 庙旺利陷
  if (s.mutagen) o.mutagen = s.mutagen;            // 四化：禄权科忌
  return o;
};

const palace = (p) => ({
  name: p.name,
  stem: p.heavenlyStem,
  branch: p.earthlyBranch,
  is_body_palace: Boolean(p.isBodyPalace),
  major_stars: (p.majorStars || []).map(star),
  minor_stars: (p.minorStars || []).map(star),
  adjective_stars: (p.adjectiveStars || []).map((s) => s.name),
  changsheng12: p.changsheng12,
  decadal: p.decadal ? { range: p.decadal.range, stem: p.decadal.heavenlyStem, branch: p.decadal.earthlyBranch } : null,
  ages: p.ages,                                     // 小限所临年龄
});

const requests = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const out = requests.map((r) => {
  const a = astro.bySolar(r.date, r.timeIndex, r.gender, true, 'zh-CN');
  return {
    id: r.id,
    input: { date: r.date, timeIndex: r.timeIndex, gender: r.gender },
    lunar_date: a.lunarDate,
    chinese_date: a.chineseDate,                    // iztro 的四柱（年按农历正月初一换）
    time: a.time,
    time_range: a.timeRange,
    five_elements_class: a.fiveElementsClass,       // 五行局
    soul: a.soul,                                   // 命主
    body: a.body,                                   // 身主
    soul_palace_branch: a.earthlyBranchOfSoulPalace,
    body_palace_branch: a.earthlyBranchOfBodyPalace,
    palaces: a.palaces.map(palace),
  };
});
process.stdout.write(JSON.stringify(out));
