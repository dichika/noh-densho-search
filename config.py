"""能伝書全文検索システム 共通設定。

対象資料・パス・URLパターンはすべてここで一元管理する。
資料を追加する場合は DOCUMENT_IDS に資料ID（アーカイブURLの数字部分）を追記し、
パイプライン（fetch → run_ocr → build_index）を再実行する。
"""

from pathlib import Path

# 検索対象の資料ID（法政大学能楽研究所デジタルアーカイブの documents/{id}）
DOCUMENT_IDS = ["3569"]

# ディレクトリ構成
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"
TOOLS_DIR = BASE_DIR / "tools"
OCR_TOOL_DIR = TOOLS_DIR / "ndlkotenocr-lite"
INDEX_JSON = DOCS_DIR / "data" / "index.json"

# アーカイブ側URLパターン
MANIFEST_URL_TMPL = "https://d2pw8r4okaxs06.cloudfront.net/manifests/{doc_id}.json"
METADATA_API_TMPL = "https://nohken-digitalarchives.hosei.ac.jp/api/documents/{doc_id}"
VIEWER_URL_TMPL = "https://nohken-digitalarchives.hosei.ac.jp/documents/{doc_id}/viewer"
DETAIL_URL_TMPL = "https://nohken-digitalarchives.hosei.ac.jp/documents/{doc_id}"

# IIIF Image API のパスパターン（{base} は manifest 中の service @id）
IIIF_FULL_IMAGE_TMPL = "{base}full/full/0/default.jpg"
IIIF_THUMB_TMPL = "{base}full/400,/0/default.jpg"

# サーバーへの配慮
REQUEST_WAIT_SEC = 1.0
USER_AGENT = "noh-densho-search/0.1 (personal research tool)"


def doc_dir(doc_id: str) -> Path:
    return DATA_DIR / doc_id


def images_dir(doc_id: str) -> Path:
    return doc_dir(doc_id) / "images"


def ocr_dir(doc_id: str) -> Path:
    return doc_dir(doc_id) / "ocr"
