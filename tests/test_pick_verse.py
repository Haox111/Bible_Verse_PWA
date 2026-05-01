import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from pick_verse import pick_verse, load_bible, filter_books_by_testament


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_bible():
    """Minimal bible structure matching ChiUn.json format."""
    return {
        "translation": "ChiUn",
        "books": [
            {
                "name": "Genesis",
                "chapters": [
                    {"chapter": 1, "verses": [
                        {"verse": 1, "text": "起初神創造天地。"},
                        {"verse": 2, "text": "地是空虛混沌。"},
                    ]},
                ]
            },
            {
                "name": "John",
                "chapters": [
                    {"chapter": 3, "verses": [
                        {"verse": 16, "text": "神愛世人，甚至將他的獨生子賜給他們。"},
                    ]},
                ]
            },
            {
                "name": "Matthew",
                "chapters": [
                    {"chapter": 6, "verses": [
                        {"verse": 33, "text": "你們要先求他的國和他的義。"},
                    ]},
                ]
            },
        ]
    }


@pytest.fixture
def sample_meta():
    return [
        {"index": 0, "name_en": "Genesis",  "name_zh": "創世記",  "testament": "old_testament"},
        {"index": 1, "name_en": "John",     "name_zh": "約翰福音","testament": "gospels"},
        {"index": 2, "name_en": "Matthew",  "name_zh": "馬太福音","testament": "gospels"},
    ]


@pytest.fixture
def bible_files(tmp_path, sample_bible, sample_meta):
    bible_path = tmp_path / "chiun.json"
    meta_path  = tmp_path / "book_meta.json"
    out_path   = tmp_path / "today.json"
    bible_path.write_text(json.dumps(sample_bible), encoding="utf-8")
    meta_path.write_text(json.dumps(sample_meta),   encoding="utf-8")
    return str(bible_path), str(meta_path), str(out_path)


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_pick_verse_returns_required_fields(bible_files):
    bible_path, meta_path, out_path = bible_files
    result = pick_verse(bible_path, meta_path, out_path)
    for field in ("text", "book_zh", "book_en", "chapter", "verse", "testament"):
        assert field in result, f"Missing field: {field}"


def test_pick_verse_writes_output_file(bible_files):
    bible_path, meta_path, out_path = bible_files
    pick_verse(bible_path, meta_path, out_path)
    assert os.path.exists(out_path)
    data = json.loads(open(out_path, encoding="utf-8").read())
    assert "text" in data


def test_pick_verse_filters_old_testament(bible_files):
    bible_path, meta_path, out_path = bible_files
    for _ in range(20):
        result = pick_verse(bible_path, meta_path, out_path, testament="old_testament")
        assert result["testament"] == "old_testament"
        assert result["book_en"] == "Genesis"


def test_pick_verse_filters_gospels(bible_files):
    bible_path, meta_path, out_path = bible_files
    for _ in range(20):
        result = pick_verse(bible_path, meta_path, out_path, testament="gospels")
        assert result["testament"] == "gospels"
        assert result["book_en"] in ("John", "Matthew")


def test_pick_verse_raises_on_empty_filter(bible_files):
    bible_path, meta_path, out_path = bible_files
    with pytest.raises(ValueError, match="No verses found"):
        pick_verse(bible_path, meta_path, out_path, testament="new_testament")


def test_text_stripped_of_extra_spaces(bible_files):
    bible_path, meta_path, out_path = bible_files
    result = pick_verse(bible_path, meta_path, out_path)
    assert "  " not in result["text"]   # no double spaces
    assert result["text"] == result["text"].strip()
