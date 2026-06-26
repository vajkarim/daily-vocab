# 毎日単語配信システム

毎朝メールで「今日の20語」が届き、スマホで7言語・発音・クイズで学習できる仕組み。

## 構成ファイル
| ファイル | 役割 |
|---|---|
| `vocab_source.json` / `translations.json` | 原データ（1,560語・7言語） |
| `build_schedule.py` → `schedule.json` | 内容語1,339を 級×品詞順に20語/日へ分割（67日） |
| `build_data.py` → `vocab.json` | ページ表示用にデータ統合 |
| `paragraphs.json` | 各日の物語（全7言語・事前生成） |
| `index.html` | スマホ学習ページ（単語・物語・クイズ・苦手→Anki） |
| `send_email.py` | 今日の20語をメール送信 |
| `.github/workflows/daily.yml` | 毎朝6時(JST)に自動実行 |

## データを更新したら
```bash
python build_schedule.py   # schedule.json
python build_data.py       # vocab.json
```

## セットアップ（初回のみ）

### 1. GitHubリポジトリを作成
このフォルダ一式をpush（公開リポジトリ推奨：Pages無料）。

### 2. GitHub Pagesを有効化
Settings → Pages → Source: `main` ブランチ / ルート。
→ 公開URL（例 `https://<ユーザー名>.github.io/<リポジトリ>/`）を控える。

### 3. Gmailアプリパスワードを発行
Googleアカウント → セキュリティ → 2段階認証を有効化 → 「アプリパスワード」を生成（16桁）。

### 4. リポジトリにSecrets / Variablesを登録
Settings → Secrets and variables → Actions

**Secrets**（秘密）:
- `GMAIL_USER` = 送信元Gmailアドレス
- `GMAIL_APP_PASSWORD` = 発行した16桁
- `TO_EMAIL` = 受信したいアドレス（同じでも可）

**Variables**（公開設定）:
- `PAGES_URL` = 手順2のPages URL
- `START_DATE` = 学習開始日（例 `2026-07-01`）。Day番号 = 今日 − START_DATE + 1。

### 5. 動作テスト
Actions → `daily-vocab-mail` → **Run workflow**（手動実行）→ メールが届けばOK。
以降は毎朝6時(JST)に自動送信。

## 運用メモ
- 物語は67日分を順次追加（`paragraphs.json` に dayキーで足すだけ）。未生成の日はページで「準備中」表示。
- 苦手な語はページで⭐ → 「苦手をAnkiへ」でTSVダウンロード → Ankiに取り込み。
- 機能語（I, my, be動詞等）は配信対象外。物語の中で自然に習得する設計。
