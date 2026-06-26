# -*- coding: utf-8 -*-
"""配信ページ用データ vocab.json を生成（id -> 全7言語フィールド）。schedule.json は build_schedule.py が生成。"""
import json, io, os, sys
sys.stdout.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))
vocab = json.load(io.open(os.path.join(BASE, 'vocab_source.json'), encoding='utf-8'))
tr = json.load(io.open(os.path.join(BASE, 'translations.json'), encoding='utf-8'))

out = {}
for v in vocab:
    t = tr.get(str(v['id']), {})
    out[str(v['id'])] = {
        'en': v['en'], 'ja': v['ja'], 'level': v['level'], 'pos': v['pos'],
        'hi': v.get('hi', ''),
        'zh': t.get('zh', ''), 'zh_r': t.get('zh_r', ''),
        'ne': t.get('ne', ''), 'ne_r': t.get('ne_r', ''),
        'idn': t.get('idn', ''), 'vi': t.get('vi', ''),
    }
json.dump(out, io.open(os.path.join(BASE, 'vocab.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(f"vocab.json 出力: {len(out)}語")

sched = json.load(io.open(os.path.join(BASE, 'schedule.json'), encoding='utf-8'))
for d in range(1, 4):
    ids = sched['days'][str(d)]
    print(f"\nDay{d}: " + ', '.join(out[str(i)]['en'] for i in ids))
