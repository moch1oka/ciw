import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_VERSION = "v5.2.55"

EXPECTED_CHAPTERS = [
    "chapter-0-prologue",
    "chapter-1-xiyang",
    "chapter-2-cloud-dwellers-1",
    "chapter-2-cloud-dwellers-2",
    "chapter-2-cloud-dwellers-3",
    "chapter-3-beyond-light-cone-1",
    "chapter-3-beyond-light-cone-2",
    "chapter-4-fate-1",
    "chapter-4-fate-2",
    "chapter-5-wuzhui-1",
    "chapter-5-wuzhui-2"
]

def main():
    print(f"=== CLOUDINSECT SITE VERIFICATION ({EXPECTED_VERSION}) ===")
    errors = []
    
    # 1. Verify root index.html
    root_html_path = os.path.join(ROOT_DIR, "index.html")
    if not os.path.exists(root_html_path):
        errors.append("Missing root index.html")
    else:
        with open(root_html_path, "r", encoding="utf-8") as f:
            root_html = f.read()
        if EXPECTED_VERSION not in root_html:
            errors.append(f"Root index.html missing {EXPECTED_VERSION}")
        if "darkreader-lock" not in root_html:
            errors.append("Root index.html missing darkreader-lock")
        if ".cover-bg video" not in root_html:
            errors.append("Root index.html missing cover-bg video styling")
        for ch in EXPECTED_CHAPTERS:
            if f"chapters/{ch}/index.html" not in root_html:
                errors.append(f"Root index.html missing link to {ch}")
        print("  [OK] Root index.html verified.")

    # 2. Verify data/all_chapters.json
    all_ch_path = os.path.join(ROOT_DIR, "data", "all_chapters.json")
    if not os.path.exists(all_ch_path):
        errors.append("Missing data/all_chapters.json")
    else:
        try:
            with open(all_ch_path, "r", encoding="utf-8") as f:
                all_data = json.load(f)
            if len(all_data) != len(EXPECTED_CHAPTERS):
                errors.append(f"all_chapters.json count mismatch: {len(all_data)} != {len(EXPECTED_CHAPTERS)}")
            else:
                print(f"  [OK] data/all_chapters.json verified ({len(all_data)} chapters).")
        except Exception as e:
            errors.append(f"Invalid all_chapters.json: {e}")

    # 3. Verify each chapter
    for ch in EXPECTED_CHAPTERS:
        ch_path = os.path.join(ROOT_DIR, "chapters", ch)
        if not os.path.isdir(ch_path):
            errors.append(f"Chapter directory missing: {ch}")
            continue
            
        # Files required
        req_files = [
            "index.html",
            "chapter_data.json",
            "chapter_vi.md",
            "chapter_vi_bilingual.md",
            "chapter_zh.md"
        ]
        for rf in req_files:
            fp = os.path.join(ch_path, rf)
            if not os.path.exists(fp):
                errors.append(f"[{ch}] Missing {rf}")
                
        # Check chapter_data.json
        cd_path = os.path.join(ch_path, "chapter_data.json")
        if os.path.exists(cd_path):
            try:
                with open(cd_path, "r", encoding="utf-8") as f:
                    cd = json.load(f)
                langs = cd.get("available_languages", [])
                if "vi" not in langs or "zh" not in langs:
                    errors.append(f"[{ch}] chapter_data.json missing vi or zh in available_languages: {langs}")
                for lang in ["en", "es", "fr", "ru", "ar", "ja", "ko", "ptBR"]:
                    if lang in langs:
                        errors.append(f"[{ch}] Obsolete language '{lang}' still in chapter_data.json")
            except Exception as e:
                errors.append(f"[{ch}] Invalid chapter_data.json: {e}")
                
        # Check chapter index.html
        ci_path = os.path.join(ch_path, "index.html")
        if os.path.exists(ci_path):
            with open(ci_path, "r", encoding="utf-8") as f:
                ci_html = f.read()
            if EXPECTED_VERSION not in ci_html:
                errors.append(f"[{ch}] index.html missing {EXPECTED_VERSION}")
            if "darkreader-lock" not in ci_html:
                errors.append(f"[{ch}] index.html missing darkreader-lock")
            if "Be Vietnam Pro" not in ci_html:
                errors.append(f"[{ch}] index.html missing Be Vietnam Pro font")
                
    # 4. Summary
    if errors:
        print("\n=== VERIFICATION FAILED ===")
        for err in errors:
            print(f"  [ERROR] {err}")
        sys.exit(1)
    else:
        print(f"\n=== ALL {len(EXPECTED_CHAPTERS)} CHAPTERS & ASSETS VERIFIED SUCCESSFULLY! ===")
        sys.exit(0)

if __name__ == "__main__":
    main()
