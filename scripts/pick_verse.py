"""
pick_verse.py — randomly select a verse from ChiUn.json and write today.json.

Usage:
    python scripts/pick_verse.py [testament]

    testament: old_testament | new_testament | gospels  (optional, default: any)
"""
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_bible(bible_path: str) -> dict:
    with open(bible_path, encoding="utf-8") as f:
        return json.load(f)


def load_meta(meta_path: str) -> list:
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def clean_text(text: str) -> str:
    """Remove inter-character spaces that ChiUn.json adds, keep punctuation."""
    text = text.strip()
    # Collapse multiple spaces to one, then remove spaces between CJK characters
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'(?<=[一-鿿＀-￯，。！？；：「」『』、]) (?=[一-鿿＀-￯，。！？；：「」『』、])', '', text)
    return text.strip()


def filter_books_by_testament(bible: dict, meta: list, testament: str) -> list:
    """Return list of (book_index, book_data, meta_entry) for the given testament."""
    meta_by_index = {m["index"]: m for m in meta}
    result = []
    for i, book in enumerate(bible["books"]):
        m = meta_by_index.get(i)
        if m and m["testament"] == testament:
            result.append((i, book, m))
    return result


def pick_verse(bible_path: str, meta_path: str, output_path: str,
               testament: str = None) -> dict:
    """
    Pick a random verse, write it to output_path as JSON, and return it.

    Args:
        bible_path:  path to chiun.json
        meta_path:   path to book_meta.json
        output_path: where to write today.json
        testament:   'old_testament' | 'new_testament' | 'gospels' | None (any)

    Returns:
        dict with keys: text, book_zh, book_en, chapter, verse, testament
    """
    bible = load_bible(bible_path)
    meta  = load_meta(meta_path)

    if testament:
        book_pool = filter_books_by_testament(bible, meta, testament)
    else:
        meta_by_index = {m["index"]: m for m in meta}
        book_pool = [
            (i, book, meta_by_index[i])
            for i, book in enumerate(bible["books"])
            if i in meta_by_index
        ]

    if not book_pool:
        raise ValueError(f"No verses found for testament: {testament!r}")

    # Weighted random: pick book proportional to its verse count
    weights = [
        sum(len(ch["verses"]) for ch in book["chapters"])
        for _, book, _ in book_pool
    ]
    _, chosen_book, chosen_meta = random.choices(book_pool, weights=weights, k=1)[0]

    # Pick a random chapter, then a random verse
    chapter_data = random.choice(chosen_book["chapters"])
    verse_data   = random.choice(chapter_data["verses"])

    result = {
        "text":      clean_text(verse_data["text"]),
        "book_zh":   chosen_meta["name_zh"],
        "book_en":   chosen_meta["name_en"],
        "chapter":   chapter_data["chapter"],
        "verse":     verse_data["verse"],
        "testament": chosen_meta["testament"],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result


if __name__ == "__main__":
    testament_arg = sys.argv[1] if len(sys.argv) > 1 else None
    verse = pick_verse(
        str(ROOT / "data" / "chiun.json"),
        str(ROOT / "data" / "book_meta.json"),
        str(ROOT / "data" / "today.json"),
        testament=testament_arg,
    )
    ref = f"{verse['book_zh']} {verse['chapter']}:{verse['verse']}"
    print(f"[{verse['testament']}] {ref}")
    print(verse["text"])
