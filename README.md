# 能伝書全文検索システム

法政大学能楽研究所デジタルアーカイブ（https://nohken-digitalarchives.hosei.ac.jp/）の能伝書画像を、
くずし字OCRでテキスト化してスマホから全文検索できるようにする個人研究用ツールである。

- 画像は再配布せず、アーカイブのIIIF Image APIから直接表示する。
- 本文テキストは NDL古典籍OCR-Lite（国立国会図書館, CC BY 4.0）による機械翻刻であり、誤読を多く含む。
- 検索UI（docs/）には noindex を設定し、検索エンジンのインデックスを拒否している。

## 構成

| パス | 役割 |
|------|------|
| `config.py` | 対象資料ID・パス・URLパターンの一元管理 |
| `pipeline/fetch.py` | IIIFマニフェスト・メタデータ・ページ画像の取得 |
| `pipeline/run_ocr.py` | NDL古典籍OCR-Lite による一括OCR |
| `pipeline/build_index.py` | 検索インデックス `docs/data/index.json` の生成 |
| `docs/` | GitHub Pages 公開ディレクトリ（検索UI） |

## 資料の追加手順

1. `config.py` の `DOCUMENT_IDS` にアーカイブの資料ID（`documents/{id}` の数字）を追記する。
2. 以下を順に実行する。

```bash
python3 pipeline/fetch.py
.venv/bin/python pipeline/run_ocr.py
python3 pipeline/build_index.py
```

## 初回セットアップ

```bash
git clone https://github.com/ndl-lab/ndlkotenocr-lite tools/ndlkotenocr-lite
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r tools/ndlkotenocr-lite/requirements.txt
```

## クレジット

- 画像・資料: 野上記念法政大学能楽研究所 能楽資料総合デジタルアーカイブ
- OCR: [NDL古典籍OCR-Lite](https://github.com/ndl-lab/ndlkotenocr-lite)（国立国会図書館, CC BY 4.0）
