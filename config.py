"""能伝書全文検索システム 共通設定。

対象資料・パス・URLパターンはすべてここで一元管理する。
資料を追加する場合は DOCUMENT_IDS に資料ID（アーカイブURLの数字部分）を追記し、
パイプライン（fetch → run_ocr → build_index）を再実行する。
"""

from pathlib import Path

# 検索対象の資料ID（法政大学能楽研究所デジタルアーカイブの documents/{id}）
# 庄田与兵衛手沢笛伝書（鴻山文庫、タイトル検索「庄田与兵衛」全14件）
DOCUMENT_IDS = [
    "3569",  # 森田流『能笛之秘書』
    "3570",  # 万治二年森田光時伝授『聞事』
    "3571",  # 宝暦九年十二月庄田与兵衛奥書「笛頭付百十五番」
    "3572",  # 天明三年山本好手沢「笛頭付百二十九番」
    "3573",  # 森田流『百番笛頭付』
    "3574",  # 森田流『能笛集 仁儀礼智信』
    "3575",  # 森田流『秘事唱歌』
    "3576",  # 森田流「唱歌及び諸流習之次第」
    "3577",  # 灰色表紙折本森田流「笛唱歌付」
    "3578",  # 緑色地小型横本森田流『秘笛集』
    "3579",  # 藍色表紙折本「森田流唱歌付」
    "3580",  # 朽葉色表紙横本「文化八年諸流習事他」
    "3581",  # 朱色地小型横本森田流『狂言アイシライ』
    "4472",  # 赤茶色表紙横本森田流「弐百五十番頭付」
]

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
