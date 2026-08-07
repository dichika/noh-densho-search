"""IIIFマニフェスト・資料メタデータ・全ページ画像を取得する。

使い方:
    python3 pipeline/fetch.py
"""

import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as res:
        return res.read()


def fetch_json(url: str, dest: Path) -> dict:
    if dest.exists():
        return json.loads(dest.read_text(encoding="utf-8"))
    data = http_get(url)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    time.sleep(config.REQUEST_WAIT_SEC)
    return json.loads(data.decode("utf-8"))


def canvas_entries(manifest: dict) -> list[dict]:
    """manifest から (画像名, IIIF service base URL, 幅, 高さ) を順に取り出す。"""
    entries = []
    for canvas in manifest["sequences"][0]["canvases"]:
        resource = canvas["images"][0]["resource"]
        service_base = resource["service"]["@id"]
        if not service_base.endswith("/"):
            service_base += "/"
        # 例: .../iiif/2/1%2fA%2fKZ43-5_001/ → KZ43-5_001
        name = service_base.rstrip("/").split("%2f")[-1].split("/")[-1]
        entries.append(
            {
                "name": name,
                "service_base": service_base,
                "width": resource.get("width"),
                "height": resource.get("height"),
            }
        )
    return entries


def fetch_document(doc_id: str) -> None:
    ddir = config.doc_dir(doc_id)
    manifest = fetch_json(
        config.MANIFEST_URL_TMPL.format(doc_id=doc_id), ddir / "manifest.json"
    )
    fetch_json(
        config.METADATA_API_TMPL.format(doc_id=doc_id), ddir / "metadata.json"
    )

    entries = canvas_entries(manifest)
    img_dir = config.images_dir(doc_id)
    img_dir.mkdir(parents=True, exist_ok=True)
    print(f"[{doc_id}] {manifest.get('label')} : {len(entries)} 画像")

    for i, entry in enumerate(entries, start=1):
        dest = img_dir / f"{entry['name']}.jpg"
        if dest.exists() and dest.stat().st_size > 0:
            continue
        url = config.IIIF_FULL_IMAGE_TMPL.format(base=entry["service_base"])
        dest.write_bytes(http_get(url))
        print(f"  {i}/{len(entries)} {dest.name} ({dest.stat().st_size // 1024} KB)")
        time.sleep(config.REQUEST_WAIT_SEC)


def main() -> None:
    for doc_id in config.DOCUMENT_IDS:
        fetch_document(doc_id)
    print("完了")


if __name__ == "__main__":
    main()
