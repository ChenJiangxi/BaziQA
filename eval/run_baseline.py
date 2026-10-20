"""A multi-turn baseline for any OpenAI-compatible chat API.

One conversation per chart: the model first reads the chart and writes a general analysis, then
answers that chart's questions one by one, ending each reply with 「答案：X」. This follows the flow of
the paper's Multi-turn setting, but it is not the paper's exact setup: the prompts below are a
shortened rewrite, and the charts come from paipan/ (no 神煞; Zi Wei added for Zi Wei setters)
instead of xuan-utils-pro. Scores from this script are therefore not directly comparable with the
paper's table. The prompts were not tuned on the answer key.

Birth time convention: always ``stated`` (see paipan/README.md). API errors are retried with
backoff; a chart that still fails is skipped and reported, and ``--resume`` fills such gaps later.

usage:
  export OPENAI_API_KEY=...                       # or --api-key-env NAME
  python eval/run_baseline.py --files contest8_2025 --model deepseek-chat \
      --base-url https://api.deepseek.com/v1 --runs 5 --out preds/deepseek-chat.jsonl
  python eval/run_baseline.py ... --resume                       # same command again: only missing charts
  python eval/run_baseline.py --files contest8_2025 --dry-run   # print the first prompt, no API call
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prompt import chart_text, load_year, wants_ziwei  # noqa: E402

SYSTEM = """你是专业的命理分析师（八字为主，题目附紫微斗数盘时也参考紫微）。当前年份：{year}年。

重要规则：
1. 必须以提供的排盘数据为准，包括大运、流年干支表等
2. 如果题目中提到的大运干支与排盘数据中该年龄段的大运不符，以排盘数据为准
3. 分析流年事件时，结合「原局 + 大运 + 流年」综合判断
4. 每道题回答的最后一行必须是「答案：X」（X 为选项字母）"""

ANALYSIS = """{chart}

请根据以上排盘信息进行系统分析：
1. 格局判定：日主强弱（月令得失、地支根气、天干生克），喜用神、忌神
2. 六亲：父母、配偶、子女的宫位与十神
3. 大运：逐步分析每步大运与原局的生克关系及吉凶走势
4. 特殊组合：合、冲、刑、害、穿等
（若附有紫微斗数盘，另看命宫、身宫、四化与大限。）
注意：大运起止年龄和干支以排盘数据为准，不要自行计算。"""

QUESTION = """问题：{question}

{options}

分析时先把题目中的年龄或年份换算成公历年份，查出对应的大运和流年干支，再结合原局判断。
最后一行输出：答案：X"""

RETRY = '请明确给出你的答案，最后一行严格输出：答案：X（X 必须是 {letters} 之一）'


def parse_answer(text: str, letters: str) -> str:
    for line in reversed(text.strip().splitlines()):
        m = re.search(rf'答案\s*[:：]\s*\**\s*([{letters}])', line, re.I)
        if m:
            return m.group(1).upper()
    return ''


class Chat:
    def __init__(self, client, model: str, system: str, max_tokens: int, temperature: float | None):
        self.client, self.model, self.max_tokens, self.temperature = client, model, max_tokens, temperature
        self.messages = [{'role': 'system', 'content': system}]

    def ask(self, text: str, tries: int = 5) -> tuple[str, bool]:
        """Send one user turn; return (reply, truncated). Transient API errors are retried."""
        self.messages.append({'role': 'user', 'content': text})
        kw = {'model': self.model, 'messages': self.messages, 'max_tokens': self.max_tokens}
        if self.temperature is not None:
            kw['temperature'] = self.temperature
        for attempt in range(tries):
            try:
                choice = self.client.chat.completions.create(**kw).choices[0]
                break
            except Exception as e:                      # noqa: BLE001 — any client or network error
                # bad request / auth / unknown model will not get better by waiting
                if getattr(e, 'status_code', None) in (400, 401, 403, 404) or attempt == tries - 1:
                    raise
                time.sleep(5 * 2 ** attempt)
        reply = choice.message.content or ''
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply, choice.finish_reason == 'length'


def run_chart(client, args, meta, person, bazi, ziwei, run: int) -> list[dict]:
    chat = Chat(client, args.model, SYSTEM.format(year=meta['current_year']), args.max_tokens, args.temperature)
    chat.ask(ANALYSIS.format(chart=chart_text(meta, person, bazi, ziwei, args.ziwei)))
    with_ziwei = person['person_id'] in ziwei and wants_ziwei(person, args.ziwei)
    rows = []
    for q in person['questions']:
        letters = ''.join(o[0] for o in q['options'])
        reply, truncated = chat.ask(QUESTION.format(question=q['question'], options='\n'.join(q['options'])))
        ans = parse_answer(reply, letters)
        if not ans:
            extra, t2 = chat.ask(RETRY.format(letters='、'.join(letters)))
            reply += '\n[追问]\n' + extra
            truncated = truncated or t2
            ans = parse_answer(reply, letters)
        row = {'question_id': q['question_id'], 'year': int(meta['current_year']), 'run': run,
               'answer': ans, 'model': args.model, 'time_convention': 'stated', 'ziwei_shown': with_ziwei}
        if truncated:
            row['truncated'] = True                     # hit --max-tokens at least once
        if args.save_text:
            row['response'] = reply
        rows.append(row)
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--files', nargs='+', required=True, help='data file stems, e.g. contest8_2025 hkjfma_2018')
    ap.add_argument('--model', default='')
    ap.add_argument('--base-url', default=None)
    ap.add_argument('--api-key-env', default='OPENAI_API_KEY')
    ap.add_argument('--runs', type=int, default=1)
    ap.add_argument('--first-run', type=int, default=1, help='run number of the first run (to append more runs later)')
    ap.add_argument('--ziwei', choices=['auto', 'always', 'never'], default='auto',
                    help='include the Zi Wei chart: auto = only for charts whose setter used Zi Wei')
    ap.add_argument('--max-tokens', type=int, default=4000)
    ap.add_argument('--temperature', type=float, default=None)
    ap.add_argument('--workers', type=int, default=4, help='charts processed in parallel')
    ap.add_argument('--save-text', action='store_true', help='keep the model replies in the output')
    ap.add_argument('--out', default='predictions.jsonl', help='appended to, never overwritten')
    ap.add_argument('--resume', action='store_true',
                    help='skip (run, chart) pairs already complete in --out, e.g. after API failures')
    ap.add_argument('--dry-run', action='store_true', help='print the first chart prompt and exit')
    args = ap.parse_args()

    years = [(stem, *load_year(stem)) for stem in args.files]
    if args.dry_run:
        stem, meta, persons, bazi, ziwei = years[0]
        print(SYSTEM.format(year=meta['current_year']))
        print('\n=== 第 1 轮 ===\n' + ANALYSIS.format(chart=chart_text(meta, persons[0], bazi, ziwei, args.ziwei)))
        q = persons[0]['questions'][0]
        print('\n=== 第 2 轮 ===\n' + QUESTION.format(question=q['question'], options='\n'.join(q['options'])))
        return

    from openai import OpenAI
    key = os.environ.get(args.api_key_env)
    if not key or not args.model:
        sys.exit(f'set --model and the API key in ${args.api_key_env}')
    client = OpenAI(api_key=key, base_url=args.base_url)
    done = set()
    if args.resume and os.path.exists(args.out):
        for line in open(args.out, encoding='utf-8'):
            if line.strip():
                r = json.loads(line)
                done.add((r.get('run'), r['question_id']))
    jobs = [(meta, p, bazi, ziwei, r) for r in range(args.first_run, args.first_run + args.runs)
            for _, meta, persons, bazi, ziwei in years for p in persons
            if not all((r, q['question_id']) in done for q in p['questions'])]
    if args.resume:
        print(f'resume: {len(jobs)} (run, chart) pairs left to do')
    lock = threading.Lock()
    failed = []
    out = open(args.out, 'a', encoding='utf-8')

    def work(job):
        try:
            rows = run_chart(client, args, *job)
        except Exception as e:                          # noqa: BLE001 — keep the other charts going
            with lock:
                failed.append(job)
                print(f"FAILED {job[0]['current_year']} {job[1]['person_id']} run {job[4]}: {e!r}",
                      file=sys.stderr, flush=True)
            return
        with lock:
            for row in rows:
                out.write(json.dumps(row, ensure_ascii=False) + '\n')
            out.flush()
            print(f"{job[0]['current_year']} {job[1]['person_id']} run {job[4]}: "
                  + ' '.join(r['answer'] or '?' for r in rows), flush=True)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(work, jobs))
    out.close()
    if failed:
        print(f'{len(failed)} (run, chart) pairs failed and were not written; '
              f'run the same command again with --resume to fill them in', file=sys.stderr)
    print(f'written to {args.out}; score with: python eval/score.py {args.out}')


if __name__ == '__main__':
    main()
