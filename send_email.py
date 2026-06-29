# -*- coding: utf-8 -*-
"""毎朝、今日の20語をメール送信する（GitHub Actionsから実行）。
環境変数:
  GMAIL_USER          送信元Gmailアドレス
  GMAIL_APP_PASSWORD  Gmailアプリパスワード
  TO_EMAIL            送信先（省略時はGMAIL_USER）
  PAGES_URL           学習ページのURL（例: https://<user>.github.io/<repo>/）
  START_DATE          学習開始日 YYYY-MM-DD（今日との差で Day番号 を算出）
"""
import os, io, json, smtplib, datetime, sys
from email.mime.text import MIMEText
from email.header import Header

BASE = os.path.dirname(os.path.abspath(__file__))
sched = json.load(io.open(os.path.join(BASE, 'schedule.json'), encoding='utf-8'))
vocab = json.load(io.open(os.path.join(BASE, 'vocab.json'), encoding='utf-8'))
paras = {}
try:
    paras = json.load(io.open(os.path.join(BASE, 'paragraphs.json'), encoding='utf-8'))
except Exception:
    pass

GMAIL_USER = os.environ['GMAIL_USER']
GMAIL_PW   = os.environ['GMAIL_APP_PASSWORD']
TO_EMAIL   = os.environ.get('TO_EMAIL') or GMAIL_USER
PAGES_URL  = os.environ.get('PAGES_URL', '').rstrip('/')
# 開始日: config.json を最優先（Variable設定に依存しない）→ 環境変数 → 失敗時Day1
START_DATE = os.environ.get('START_DATE', '')
try:
    cfg = json.load(io.open(os.path.join(BASE, 'config.json'), encoding='utf-8'))
    if cfg.get('start_date'):
        START_DATE = cfg['start_date']
except Exception:
    pass

# Day番号を算出（JST基準）
jst = datetime.timezone(datetime.timedelta(hours=9))
today = datetime.datetime.now(jst).date()
try:
    start = datetime.date.fromisoformat(START_DATE)
    day = (today - start).days + 1
except Exception:
    day = 1
day = max(1, min(day, sched['day_count']))

ids = sched['days'][str(day)]
theme = paras.get(str(day), {}).get('theme', '')
link = f"{PAGES_URL}/?day={day}" if PAGES_URL else f"?day={day}"

rows = ''.join(
    f'<tr><td style="padding:4px 10px;font-weight:700">{vocab[str(i)]["en"]}</td>'
    f'<td style="padding:4px 10px;color:#555">{vocab[str(i)]["ja"]}</td>'
    f'<td style="padding:4px 10px;color:#888;font-size:12px">{vocab[str(i)]["pos"]}</td></tr>'
    for i in ids
)
html = f"""<div style="font-family:sans-serif;max-width:560px;margin:auto">
<h2 style="color:#b3502f;margin:0 0 4px">Day {day} / {sched['day_count']} — 今日の20語</h2>
<div style="color:#2f6e62;font-size:13px;margin-bottom:12px">テーマ: {theme}</div>
<a href="{link}" style="display:inline-block;background:#2f6e62;color:#fff;text-decoration:none;
  padding:12px 22px;border-radius:24px;font-weight:700;margin-bottom:16px">📱 スマホで学習する（7言語・音声・クイズ）</a>
<table style="border-collapse:collapse;width:100%">{rows}</table>
<p style="color:#999;font-size:12px;margin-top:16px">物語・全7言語・発音・クイズはリンク先で。苦手な語は⭐でAnkiに書き出せます。</p>
</div>"""

msg = MIMEText(html, 'html', 'utf-8')
msg['Subject'] = Header(f'【今日の20語】Day {day}：{theme}', 'utf-8')
msg['From'] = GMAIL_USER
msg['To'] = TO_EMAIL

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(GMAIL_USER, GMAIL_PW)
    s.sendmail(GMAIL_USER, [TO_EMAIL], msg.as_string())

print(f"Sent Day {day} ({len(ids)} words) to {TO_EMAIL}")
