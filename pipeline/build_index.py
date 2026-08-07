"""OCR結果とメタデータから検索インデックス docs/data/index.json を生成する。

使い方:
    python3 pipeline/build_index.py

インデックス構造:
{
  "documents": [
    {
      "id": "3569",
      "title": "...", "collection": "...", "repository": "...", "code": "...",
      "commentary": "...",       # 解題（資料単位の検索対象）
      "viewerUrl": "...", "detailUrl": "...",
      "pages": [
        {
          "n": 1,                # ページ番号（ビューア上のコマ番号）
          "name": "KZ43-5_001",
          "iiif": "https://.../iiif/2/1%2fA%2fKZ43-5_001/",  # IIIF service base
          "w": 2069, "h": 1379,
          "lines": [ {"t": "行テキスト", "b": [x, y, w, h], "c": 0.51}, ... ]
        }, ...
      ]
    }
  ]
}
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
from fetch import canvas_entries


def bbox_to_xywh(bounding_box: list) -> list:
    xs = [p[0] for p in bounding_box]
    ys = [p[1] for p in bounding_box]
    x0, y0 = max(0, min(xs)), max(0, min(ys))
    return [x0, y0, max(xs) - x0, max(ys) - y0]


# 認識崩壊行（同一文字の長い繰り返し）。実際は唱歌などの文字列だが
# OCRが読めておらず、検索ノイズになるためインデックスから除外する。
DEGENERATE_RE = re.compile(r"(.)\1{4,}")


def is_degenerate(text: str) -> bool:
    return bool(DEGENERATE_RE.search(text))


def load_page_lines(ocr_json_path: Path) -> list[dict]:
    data = json.loads(ocr_json_path.read_text(encoding="utf-8"))
    lines = []
    for block in data.get("contents", []):
        for line in block:
            text = (line.get("text") or "").strip()
            if not text or is_degenerate(text):
                continue
            lines.append(
                {
                    "t": text,
                    "b": bbox_to_xywh(line["boundingBox"]),
                    "c": round(float(line.get("confidence", 0)), 3),
                }
            )
    return lines


def build_document(doc_id: str) -> dict:
    ddir = config.doc_dir(doc_id)
    manifest = json.loads((ddir / "manifest.json").read_text(encoding="utf-8"))
    metadata = json.loads((ddir / "metadata.json").read_text(encoding="utf-8"))

    pages = []
    for n, entry in enumerate(canvas_entries(manifest), start=1):
        ocr_path = config.ocr_dir(doc_id) / f"{entry['name']}.json"
        lines = load_page_lines(ocr_path) if ocr_path.exists() else []
        if not ocr_path.exists():
            print(f"  警告: OCR結果なし {ocr_path.name}", file=sys.stderr)
        pages.append(
            {
                "n": n,
                "name": entry["name"],
                "iiif": entry["service_base"],
                "w": entry["width"],
                "h": entry["height"],
                "lines": lines,
            }
        )

    return {
        "id": doc_id,
        "title": metadata.get("title") or manifest.get("label") or doc_id,
        "collection": metadata.get("collection"),
        "repository": metadata.get("repository"),
        "code": metadata.get("code"),
        "commentary": metadata.get("commentary"),
        "viewerUrl": config.VIEWER_URL_TMPL.format(doc_id=doc_id),
        "detailUrl": config.DETAIL_URL_TMPL.format(doc_id=doc_id),
        "pages": pages,
    }


def main() -> None:
    documents = [build_document(doc_id) for doc_id in config.DOCUMENT_IDS]
    config.INDEX_JSON.parent.mkdir(parents=True, exist_ok=True)
    config.INDEX_JSON.write_text(
        json.dumps({"documents": documents}, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    n_pages = sum(len(d["pages"]) for d in documents)
    n_lines = sum(len(p["lines"]) for d in documents for p in d["pages"])
    size_kb = config.INDEX_JSON.stat().st_size // 1024
    print(f"index.json 生成: 資料{len(documents)}点 / {n_pages}ページ / {n_lines}行 / {size_kb} KB")


if __name__ == "__main__":
    main()
