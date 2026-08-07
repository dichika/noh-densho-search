"""NDL古典籍OCR-Lite で全資料の画像をOCRする。

使い方:
    .venv/bin/python pipeline/run_ocr.py

tools/ndlkotenocr-lite の CLI (src/ocr.py) をディレクトリ一括モードで呼び出し、
結果（json/txt/xml）を data/{doc_id}/ocr/ に保存する。
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config


def run_ocr(doc_id: str) -> None:
    src_dir = config.OCR_TOOL_DIR / "src"
    images = config.images_dir(doc_id)
    out = config.ocr_dir(doc_id)
    out.mkdir(parents=True, exist_ok=True)

    n_images = len(list(images.glob("*.jpg")))
    done = {p.stem for p in out.glob("*.json")}
    if len(done) >= n_images and n_images > 0:
        print(f"[{doc_id}] OCR済み ({len(done)}/{n_images}) スキップ")
        return

    print(f"[{doc_id}] OCR開始: {n_images} 画像")
    subprocess.run(
        [
            sys.executable,
            "ocr.py",
            "--sourcedir",
            str(images),
            "--output",
            str(out),
        ],
        cwd=src_dir,
        check=True,
    )
    n_out = len(list(out.glob("*.json")))
    print(f"[{doc_id}] OCR完了: {n_out}/{n_images} 件のJSONを出力")


def main() -> None:
    for doc_id in config.DOCUMENT_IDS:
        run_ocr(doc_id)


if __name__ == "__main__":
    main()
