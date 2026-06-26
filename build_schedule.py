# -*- coding: utf-8 -*-
"""内容語のみ(機能語=その他を除外)を 級×品詞順 に並べ、20語/日に分割して schedule.json を出力。
品詞順: 動詞 → 形容詞 → イディオム → 名詞 / 級順: 5級 → 4級
"""
import json, io, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
vocab = json.load(io.open(os.path.join(BASE, 'vocab_source.json'), encoding='utf-8'))

POS_ORDER = ['動詞', '形容詞', 'イディオム', '名詞']   # その他(機能語)は除外
LEVEL_ORDER = ['5級', '4級']
PER_DAY = 20

content = [v for v in vocab if v['pos'] in POS_ORDER]
content.sort(key=lambda v: (LEVEL_ORDER.index(v['level']), POS_ORDER.index(v['pos']), v['id']))
ids = [v['id'] for v in content]

days = [ids[i:i + PER_DAY] for i in range(0, len(ids), PER_DAY)]
schedule = {
    'per_day': PER_DAY,
    'day_count': len(days),
    'total_words': len(ids),
    'order': {'level': LEVEL_ORDER, 'pos': POS_ORDER},
    'days': {str(n + 1): chunk for n, chunk in enumerate(days)},
}
json.dump(schedule, io.open(os.path.join(BASE, 'schedule.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)

# ---- 検証レポート ----
import sys
sys.stdout.reconfigure(encoding='utf-8')
excluded = sum(1 for v in vocab if v['pos'] == 'その他')
print(f"内容語: {len(ids)}  / 除外(その他): {excluded}  / 合計: {len(vocab)}")
print(f"日数: {len(days)}  最終日の語数: {len(days[-1])}")
print("品詞内訳:", dict(Counter(v['pos'] for v in content)))
# 順序が崩れていないか（最初の数件と境界）
byid = {v['id']: v for v in vocab}
print("--- day1 (先頭) ---")
for i in schedule['days']['1']:
    print(' ', i, byid[i]['en'], byid[i]['level'], byid[i]['pos'])
