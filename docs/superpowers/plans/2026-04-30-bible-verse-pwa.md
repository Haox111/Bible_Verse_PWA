# Bible Verse PWA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a installable PWA hosted on GitHub Pages that shows a daily Bible verse (CUV + RCUV + NIV), supports category browsing, and lets users email themselves the current verse.

**Architecture:** Static site on GitHub Pages with no backend. GitHub Actions runs daily at UTC 17:00 (PST 09:00) to pick a random verse and commit it as `data/today.json`. All interactivity (version tabs, category nav, email) is pure JavaScript on the frontend.

**Tech Stack:** HTML/CSS/JS (no build step), Python 3 + pytest (for pick-verse script), GitHub Actions, GitHub Pages, EmailJS (free tier)

---

## File Map

| File | Responsibility |
|------|---------------|
| `data/verses.json` | Full verse library (~30 starter verses, expandable) |
| `data/today.json` | Today's verse, written daily by GitHub Actions |
| `scripts/pick_verse.py` | Python script: reads verses.json, picks random verse, writes today.json |
| `tests/test_pick_verse.py` | pytest tests for pick_verse.py |
| `config.js` | EmailJS public keys (safe to commit) |
| `index.html` | PWA shell: layout, script/style links |
| `style.css` | Parchment warm color theme |
| `app.js` | All frontend logic: load verse, tabs, nav, email modal |
| `manifest.json` | PWA install config (name, icon, theme color) |
| `service-worker.js` | Cache static assets + verses.json for offline use |
| `.github/workflows/daily.yml` | Cron job: daily verse update |

---

## Task 1: Project Scaffold

**Files:**
- Create: `.gitignore`
- Create: `data/today.json` (placeholder)

- [ ] **Step 1: Create .gitignore**

```
.superpowers/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
.env
node_modules/
```

- [ ] **Step 2: Create placeholder today.json**

```json
{
  "id": "jhn-3-16",
  "book_zh": "约翰福音",
  "book_en": "John",
  "chapter": 3,
  "verse": 16,
  "category": "gospels",
  "cuv": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。",
  "rcuv": "神爱世人，甚至将他的独生子赐给他们，使所有信他的人不致灭亡，反得永生。",
  "niv": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
}
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore data/today.json
git commit -m "chore: project scaffold"
```

---

## Task 2: Verse Database

**Files:**
- Create: `data/verses.json`

- [ ] **Step 1: Create verses.json with 30 starter verses**

```json
[
  {
    "id": "jhn-3-16",
    "book_zh": "约翰福音",
    "book_en": "John",
    "chapter": 3,
    "verse": 16,
    "category": "gospels",
    "cuv": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。",
    "rcuv": "神爱世人，甚至将他的独生子赐给他们，使所有信他的人不致灭亡，反得永生。",
    "niv": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life."
  },
  {
    "id": "jhn-14-6",
    "book_zh": "约翰福音",
    "book_en": "John",
    "chapter": 14,
    "verse": 6,
    "category": "gospels",
    "cuv": "耶稣说，我就是道路、真理、生命；若不藉着我，没有人能到父那里去。",
    "rcuv": "耶稣说：「我就是道路、真理、生命；若不藉着我，没有人能到父那里去。」",
    "niv": "Jesus answered, \"I am the way and the truth and the life. No one comes to the Father except through me.\""
  },
  {
    "id": "jhn-11-25",
    "book_zh": "约翰福音",
    "book_en": "John",
    "chapter": 11,
    "verse": 25,
    "category": "gospels",
    "cuv": "耶稣说，复活在我，生命也在我；信我的人虽然死了，也必复活。",
    "rcuv": "耶稣对她说：「复活在我，生命也在我；信我的人虽然死了，也必复活。」",
    "niv": "Jesus said to her, \"I am the resurrection and the life. The one who believes in me will live, even though they die.\""
  },
  {
    "id": "jhn-8-12",
    "book_zh": "约翰福音",
    "book_en": "John",
    "chapter": 8,
    "verse": 12,
    "category": "gospels",
    "cuv": "耶稣又对众人说，我是世界的光。跟从我的，就不在黑暗里走，必要得着生命的光。",
    "rcuv": "耶稣又对他们说：「我是世界的光，跟从我的就不在黑暗里走，必要得着生命的光。」",
    "niv": "When Jesus spoke again to the people, he said, \"I am the light of the world. Whoever follows me will never walk in darkness, but will have the light of life.\""
  },
  {
    "id": "jhn-1-1",
    "book_zh": "约翰福音",
    "book_en": "John",
    "chapter": 1,
    "verse": 1,
    "category": "gospels",
    "cuv": "太初有道，道与神同在，道就是神。",
    "rcuv": "太初有道，道与神同在，道就是神。",
    "niv": "In the beginning was the Word, and the Word was with God, and the Word was God."
  },
  {
    "id": "mat-6-33",
    "book_zh": "马太福音",
    "book_en": "Matthew",
    "chapter": 6,
    "verse": 33,
    "category": "gospels",
    "cuv": "你们要先求他的国和他的义，这些东西都要加给你们了。",
    "rcuv": "你们要先求他的国和他的义，这些东西都要加给你们了。",
    "niv": "But seek first his kingdom and his righteousness, and all these things will be given to you as well."
  },
  {
    "id": "mat-28-19",
    "book_zh": "马太福音",
    "book_en": "Matthew",
    "chapter": 28,
    "verse": 19,
    "category": "gospels",
    "cuv": "所以，你们要去，使万民作我的门徒，奉父、子、圣灵的名给他们施洗。凡我所吩咐你们的，都教训他们遵守，我就常与你们同在，直到世界的末了。",
    "rcuv": "所以你们要去，使万民作我的门徒，奉父、子、圣灵的名给他们施洗；凡我所吩咐你们的，都教导他们遵守。我就常与你们同在，直到世界的末了。",
    "niv": "Therefore go and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit, and teaching them to obey everything I have commanded you. And surely I am with you always, to the very end of the age."
  },
  {
    "id": "mat-5-3",
    "book_zh": "马太福音",
    "book_en": "Matthew",
    "chapter": 5,
    "verse": 3,
    "category": "gospels",
    "cuv": "虚心的人有福了，因为天国是他们的。哀恸的人有福了，因为他们必得安慰。",
    "rcuv": "虚心的人有福了，因为天国是他们的；哀恸的人有福了，因为他们必得安慰。",
    "niv": "Blessed are the poor in spirit, for theirs is the kingdom of heaven. Blessed are those who mourn, for they will be comforted."
  },
  {
    "id": "luk-2-10",
    "book_zh": "路加福音",
    "book_en": "Luke",
    "chapter": 2,
    "verse": 10,
    "category": "gospels",
    "cuv": "那天使对他们说，不要惧怕！我报给你们大喜的信息，是关乎万民的；因今天在大卫的城里，为你们生了救主，就是主基督。",
    "rcuv": "那天使对他们说：「不要惧怕！看哪，我报给你们大喜的信息，是关乎万民的；因今天在大卫的城里，为你们生了救主，就是主基督。」",
    "niv": "But the angel said to them, \"Do not be afraid. I bring you good news that will cause great joy for all the people. Today in the town of David a Savior has been born to you; he is the Messiah, the Lord.\""
  },
  {
    "id": "mrk-10-45",
    "book_zh": "马可福音",
    "book_en": "Mark",
    "chapter": 10,
    "verse": 45,
    "category": "gospels",
    "cuv": "因为人子来，并不是要受人的服事，乃是要服事人，并且要舍命，作多人的赎价。",
    "rcuv": "因为人子来，并不是要受人的服事，乃是要服事人，并且要舍命作多人的赎价。",
    "niv": "For even the Son of Man did not come to be served, but to serve, and to give his life as a ransom for many."
  },
  {
    "id": "rom-8-28",
    "book_zh": "罗马书",
    "book_en": "Romans",
    "chapter": 8,
    "verse": 28,
    "category": "new_testament",
    "cuv": "我们晓得万事都互相效力，叫爱神的人得益处，就是按他旨意被召的人。",
    "rcuv": "我们知道神使万事互相效力，使爱神的人得益处，就是按他旨意被召的人。",
    "niv": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose."
  },
  {
    "id": "rom-8-38",
    "book_zh": "罗马书",
    "book_en": "Romans",
    "chapter": 8,
    "verse": 38,
    "category": "new_testament",
    "cuv": "因为我深信无论是死，是生，是天使，是掌权的，是有能的，是现在的事，是将来的事，是高处的，是低处的，是别的受造之物，都不能叫我们与神的爱隔绝，这爱是在我们的主基督耶稣里的。",
    "rcuv": "因为我深信，无论是死，是生，是天使，是掌权的，是现在的事，是将来的事，是有能力的，是高处的，是低处的，还是其他受造之物，都不能使我们与神的爱隔绝，就是在我们的主基督耶稣里的爱。",
    "niv": "For I am convinced that neither death nor life, neither angels nor demons, neither the present nor the future, nor any powers, neither height nor depth, nor anything else in all creation, will be able to separate us from the love of God that is in Christ Jesus our Lord."
  },
  {
    "id": "rom-12-2",
    "book_zh": "罗马书",
    "book_en": "Romans",
    "chapter": 12,
    "verse": 2,
    "category": "new_testament",
    "cuv": "不要效法这个世界，只要心意更新而变化，叫你们察验何为神的善良、纯全、可喜悦的旨意。",
    "rcuv": "不要效法这个世界，只要心意更新而变化，使你们能察验何为神的善良、纯全、可喜悦的旨意。",
    "niv": "Do not conform to the pattern of this world, but be transformed by the renewing of your mind. Then you will be able to test and approve what God's will is—his good, pleasing and perfect will."
  },
  {
    "id": "php-4-13",
    "book_zh": "腓立比书",
    "book_en": "Philippians",
    "chapter": 4,
    "verse": 13,
    "category": "new_testament",
    "cuv": "我靠着那加给我力量的，凡事都能做。",
    "rcuv": "我靠着那加给我力量的，凡事都能做。",
    "niv": "I can do all this through him who gives me strength."
  },
  {
    "id": "php-4-6",
    "book_zh": "腓立比书",
    "book_en": "Philippians",
    "chapter": 4,
    "verse": 6,
    "category": "new_testament",
    "cuv": "应当一无挂虑，只要凡事藉着祷告、祈求，和感谢，将你们所要的告诉神。神所赐、出人意外的平安必在基督耶稣里保守你们的心怀意念。",
    "rcuv": "不要为任何事忧虑，要在一切事上以祷告、祈求，和感恩的心将你们的愿望告诉神。那超越一切人所能理解的神的平安，必在基督耶稣里保守你们的心怀意念。",
    "niv": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus."
  },
  {
    "id": "eph-2-8",
    "book_zh": "以弗所书",
    "book_en": "Ephesians",
    "chapter": 2,
    "verse": 8,
    "category": "new_testament",
    "cuv": "你们得救是本乎恩，也因着信；这并不是出于自己，乃是神所赐的；也不是出于行为，免得有人自夸。",
    "rcuv": "你们得救是本乎恩，也因着信；这不是由于你们自己，而是神所赐的礼物；不是由于行为，免得有人夸口。",
    "niv": "For it is by grace you have been saved, through faith—and this is not from yourselves, it is the gift of God— not by works, so that no one can boast."
  },
  {
    "id": "1co-13-13",
    "book_zh": "哥林多前书",
    "book_en": "1 Corinthians",
    "chapter": 13,
    "verse": 13,
    "category": "new_testament",
    "cuv": "如今常存的有信，有望，有爱这三样，其中最大的是爱。",
    "rcuv": "如今长存的有信、有望、有爱这三样，其中最大的是爱。",
    "niv": "And now these three remain: faith, hope and love. But the greatest of these is love."
  },
  {
    "id": "2ti-3-16",
    "book_zh": "提摩太后书",
    "book_en": "2 Timothy",
    "chapter": 3,
    "verse": 16,
    "category": "new_testament",
    "cuv": "圣经都是神所默示的，于教训、督责、使人归正、教导人学义都是有益的，叫属神的人得以完全，预备行各种善事。",
    "rcuv": "圣经都是神所默示的，在教训、督责、矫正和公义的训练上都有益处，使属神的人有所装备，预备行各种善事。",
    "niv": "All Scripture is God-breathed and is useful for teaching, rebuking, correcting and training in righteousness, so that the servant of God may be thoroughly equipped for every good work."
  },
  {
    "id": "heb-11-1",
    "book_zh": "希伯来书",
    "book_en": "Hebrews",
    "chapter": 11,
    "verse": 1,
    "category": "new_testament",
    "cuv": "信就是所望之事的实底，是未见之事的确据。",
    "rcuv": "信心是对所盼望之事的确信，是对未见之事的证明。",
    "niv": "Now faith is confidence in what we hope for and assurance about what we do not see."
  },
  {
    "id": "1jo-4-19",
    "book_zh": "约翰一书",
    "book_en": "1 John",
    "chapter": 4,
    "verse": 19,
    "category": "new_testament",
    "cuv": "我们爱，因为神先爱我们。",
    "rcuv": "我们爱，是因为神先爱了我们。",
    "niv": "We love because he first loved us."
  },
  {
    "id": "psa-23-1",
    "book_zh": "诗篇",
    "book_en": "Psalms",
    "chapter": 23,
    "verse": 1,
    "category": "old_testament",
    "cuv": "耶和华是我的牧者，我必不至缺乏。",
    "rcuv": "耶和华是我的牧者，我必不致缺乏。",
    "niv": "The Lord is my shepherd, I lack nothing."
  },
  {
    "id": "psa-46-1",
    "book_zh": "诗篇",
    "book_en": "Psalms",
    "chapter": 46,
    "verse": 1,
    "category": "old_testament",
    "cuv": "神是我们的避难所，是我们的力量，是我们在患难中随时的帮助。",
    "rcuv": "神是我们的避难所和力量，是我们患难中随时可得的帮助。",
    "niv": "God is our refuge and strength, an ever-present help in trouble."
  },
  {
    "id": "psa-119-105",
    "book_zh": "诗篇",
    "book_en": "Psalms",
    "chapter": 119,
    "verse": 105,
    "category": "old_testament",
    "cuv": "你的话是我脚前的灯，是我路上的光。",
    "rcuv": "你的话是我脚前的灯，是我路上的光。",
    "niv": "Your word is a lamp for my feet, a light on my path."
  },
  {
    "id": "psa-121-1",
    "book_zh": "诗篇",
    "book_en": "Psalms",
    "chapter": 121,
    "verse": 1,
    "category": "old_testament",
    "cuv": "我要向山举目；我的帮助从何而来？我的帮助从造天地的耶和华而来。",
    "rcuv": "我要向山举目，我的帮助从何而来？我的帮助从造天地的耶和华而来。",
    "niv": "I lift up my eyes to the mountains—where does my help come from? My help comes from the Lord, the Maker of heaven and earth."
  },
  {
    "id": "pro-3-5",
    "book_zh": "箴言",
    "book_en": "Proverbs",
    "chapter": 3,
    "verse": 5,
    "category": "old_testament",
    "cuv": "你要专心仰赖耶和华，不可倚靠自己的聪明，在你一切所行的事上都要认定他，他必指引你的路。",
    "rcuv": "你要全心信靠耶和华，不可依靠自己的聪明；在你一切所行的事上，都要认定他，他必指引你的路。",
    "niv": "Trust in the Lord with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight."
  },
  {
    "id": "pro-22-6",
    "book_zh": "箴言",
    "book_en": "Proverbs",
    "chapter": 22,
    "verse": 6,
    "category": "old_testament",
    "cuv": "教养孩童，使他走当行的道，就是到老他也不偏离。",
    "rcuv": "教养孩童走当行的道，就是到老他也不偏离。",
    "niv": "Start children off on the way they should go, and even when they are old they will not turn from it."
  },
  {
    "id": "isa-40-31",
    "book_zh": "以赛亚书",
    "book_en": "Isaiah",
    "chapter": 40,
    "verse": 31,
    "category": "old_testament",
    "cuv": "但那等候耶和华的，必重新得力。他们必如鹰展翅上腾；他们奔跑却不困倦，行走却不疲乏。",
    "rcuv": "但那等候耶和华的，必重新得力；他们必如鹰展翅上腾；他们奔跑却不疲乏，行走却不困倦。",
    "niv": "but those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint."
  },
  {
    "id": "isa-41-10",
    "book_zh": "以赛亚书",
    "book_en": "Isaiah",
    "chapter": 41,
    "verse": 10,
    "category": "old_testament",
    "cuv": "你不要害怕，因为我与你同在；不要惊惶，因为我是你的神。我必坚固你，我必帮助你，我必用我公义的右手扶持你。",
    "rcuv": "你不要害怕，因为我与你同在；不要惊惶，因为我是你的神。我必使你刚强，我必帮助你，我必用我公义的右手扶持你。",
    "niv": "So do not fear, for I am with you; do not be dismayed, for I am your God. I will strengthen you and help you; I will uphold you with my righteous right hand."
  },
  {
    "id": "jer-29-11",
    "book_zh": "耶利米书",
    "book_en": "Jeremiah",
    "chapter": 29,
    "verse": 11,
    "category": "old_testament",
    "cuv": "耶和华说，我知道我向你们所怀的意念，是赐平安的意念，不是降灾祸的意念，要叫你们末后有指望。",
    "rcuv": "耶和华说：我所怀的意念是赐你们平安的意念，不是降祸的意念，要给你们将来和盼望。",
    "niv": "For I know the plans I have for you, declares the Lord, plans to prosper you and not to harm you, plans to give you hope and a future."
  },
  {
    "id": "jos-1-9",
    "book_zh": "约书亚记",
    "book_en": "Joshua",
    "chapter": 1,
    "verse": 9,
    "category": "old_testament",
    "cuv": "我岂没有吩咐你吗？你当刚强壮胆！不要惧怕，也不要惊惶，因为你无论往哪里去，耶和华你的神必与你同在。",
    "rcuv": "我岂没有吩咐你吗？你要刚强壮胆，不要惧怕，也不要惊惶，因为你无论往哪里去，耶和华你的神必与你同在。",
    "niv": "Have I not commanded you? Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go."
  }
]
```

- [ ] **Step 2: Validate JSON is well-formed**

```bash
python -c "import json; data=json.load(open('data/verses.json')); print(f'OK: {len(data)} verses')"
```

Expected output: `OK: 30 verses`

- [ ] **Step 3: Commit**

```bash
git add data/verses.json
git commit -m "feat: add verse database with 30 starter verses"
```

---

## Task 3: Daily Verse Picker Script + Tests

**Files:**
- Create: `scripts/pick_verse.py`
- Create: `tests/test_pick_verse.py`

- [ ] **Step 1: Write failing tests first**

Create `tests/test_pick_verse.py`:

```python
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from pick_verse import pick_verse


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


@pytest.fixture(autouse=True)
def fixtures_dir(tmp_path):
    verses = [
        {"id": "jhn-3-16", "book_zh": "约翰福音", "book_en": "John",
         "chapter": 3, "verse": 16, "category": "gospels",
         "cuv": "CUV text", "rcuv": "RCUV text", "niv": "NIV text"},
        {"id": "psa-23-1", "book_zh": "诗篇", "book_en": "Psalms",
         "chapter": 23, "verse": 1, "category": "old_testament",
         "cuv": "CUV text 2", "rcuv": "RCUV text 2", "niv": "NIV text 2"},
        {"id": "rom-8-28", "book_zh": "罗马书", "book_en": "Romans",
         "chapter": 8, "verse": 28, "category": "new_testament",
         "cuv": "CUV text 3", "rcuv": "RCUV text 3", "niv": "NIV text 3"},
    ]
    verses_path = tmp_path / "verses.json"
    verses_path.write_text(json.dumps(verses, ensure_ascii=False))
    return tmp_path


def test_pick_verse_returns_valid_verse(fixtures_dir):
    output_path = fixtures_dir / "today.json"
    result = pick_verse(str(fixtures_dir / "verses.json"), str(output_path))
    assert result["id"] in ["jhn-3-16", "psa-23-1", "rom-8-28"]
    assert all(k in result for k in ["id", "book_zh", "book_en", "chapter", "verse",
                                      "category", "cuv", "rcuv", "niv"])


def test_pick_verse_writes_output_file(fixtures_dir):
    output_path = fixtures_dir / "today.json"
    pick_verse(str(fixtures_dir / "verses.json"), str(output_path))
    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert "id" in data


def test_pick_verse_filters_by_category(fixtures_dir):
    output_path = fixtures_dir / "today.json"
    for _ in range(20):
        result = pick_verse(str(fixtures_dir / "verses.json"), str(output_path),
                            category="gospels")
        assert result["category"] == "gospels"


def test_pick_verse_raises_on_unknown_category(fixtures_dir):
    output_path = fixtures_dir / "today.json"
    with pytest.raises(ValueError, match="No verses found"):
        pick_verse(str(fixtures_dir / "verses.json"), str(output_path),
                   category="nonexistent")
```

- [ ] **Step 2: Run tests — expect failure (ImportError)**

```bash
python -m pytest tests/test_pick_verse.py -v
```

Expected: `ImportError: No module named 'pick_verse'`

- [ ] **Step 3: Create scripts/pick_verse.py**

```python
import json
import random
import sys
from pathlib import Path


def pick_verse(verses_path: str, output_path: str, category: str = None) -> dict:
    with open(verses_path, encoding="utf-8") as f:
        verses = json.load(f)

    if category:
        verses = [v for v in verses if v["category"] == category]

    if not verses:
        raise ValueError(f"No verses found for category: {category}")

    verse = random.choice(verses)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(verse, f, ensure_ascii=False, indent=2)

    return verse


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    pick_verse(
        str(root / "data" / "verses.json"),
        str(root / "data" / "today.json"),
    )
    print("Today's verse updated.")
```

- [ ] **Step 4: Run tests — expect all pass**

```bash
python -m pytest tests/test_pick_verse.py -v
```

Expected:
```
test_pick_verse_returns_valid_verse PASSED
test_pick_verse_writes_output_file PASSED
test_pick_verse_filters_by_category PASSED
test_pick_verse_raises_on_unknown_category PASSED
4 passed
```

- [ ] **Step 5: Smoke-test the script manually**

```bash
python scripts/pick_verse.py && python -c "import json; print(json.load(open('data/today.json'))['id'])"
```

Expected: prints a verse id like `jhn-3-16`

- [ ] **Step 6: Commit**

```bash
git add scripts/pick_verse.py tests/test_pick_verse.py
git commit -m "feat: add daily verse picker script with tests"
```

---

## Task 4: GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/daily.yml`

- [ ] **Step 1: Create daily.yml**

```yaml
name: Daily Verse Update

on:
  schedule:
    - cron: '0 17 * * *'   # UTC 17:00 = PST 09:00 (UTC-8)
  workflow_dispatch:         # Allow manual trigger for testing

jobs:
  update-verse:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Pick daily verse
        run: python scripts/pick_verse.py

      - name: Commit and push today.json
        run: |
          git config user.name 'github-actions[bot]'
          git config user.email 'github-actions[bot]@users.noreply.github.com'
          git add data/today.json
          git diff --staged --quiet || git commit -m "chore: daily verse update"
          git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/daily.yml
git commit -m "feat: add daily GitHub Actions workflow"
```

---

## Task 5: CSS Styles

**Files:**
- Create: `style.css`

- [ ] **Step 1: Create style.css**

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #f0e6d6;
  --card-bg-start: #fdf8f0;
  --card-bg-end: #f7efe2;
  --accent: #8b5e3c;
  --accent-light: #c4956a;
  --accent-faint: rgba(139, 94, 60, 0.12);
  --text-primary: #3d2b1f;
  --text-secondary: #5a3e28;
  --text-muted: #a07850;
  --border: #d4b896;
}

html, body { height: 100%; }

body {
  font-family: Georgia, 'Times New Roman', serif;
  background: var(--bg);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* ── Header ── */
header {
  text-align: center;
  padding: 20px 16px 8px;
}

.app-label {
  font-size: 11px;
  letter-spacing: 4px;
  color: var(--text-muted);
  text-transform: uppercase;
  margin-bottom: 4px;
}

.date-label {
  font-size: 11px;
  color: var(--accent-light);
}

/* ── Main card area ── */
main {
  flex: 1;
  padding: 12px 16px 8px;
  overflow-y: auto;
}

.card {
  background: linear-gradient(160deg, var(--card-bg-start) 0%, var(--card-bg-end) 100%);
  border-radius: 16px;
  padding: 24px 20px;
  border-left: 5px solid var(--accent);
  box-shadow: 0 4px 20px var(--accent-faint);
}

/* ── Version tabs ── */
.version-tabs {
  display: flex;
  gap: 6px;
  justify-content: center;
  margin-bottom: 18px;
}

.version-tab {
  font-family: Georgia, serif;
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid var(--accent-light);
  background: transparent;
  color: var(--accent);
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: background 0.15s, color 0.15s;
}

.version-tab.active {
  background: var(--accent);
  color: #fdf8f0;
  border-color: var(--accent);
}

/* ── Chinese verse ── */
.verse-zh {
  font-size: 16px;
  line-height: 1.9;
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 4px;
}

/* ── Divider ── */
.verse-divider {
  border: none;
  border-top: 1px dashed var(--border);
  margin: 16px 0;
}

/* ── NIV label + verse ── */
.version-label {
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--text-muted);
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 8px;
}

.verse-niv {
  font-size: 14px;
  line-height: 1.85;
  color: var(--text-secondary);
  text-align: center;
  font-style: italic;
}

/* ── Reference ── */
.verse-ref {
  font-size: 12px;
  color: var(--accent);
  text-align: center;
  letter-spacing: 1.5px;
  margin-top: 14px;
}

/* ── Email button ── */
.solid-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 18px 0 14px;
}

.email-btn {
  display: block;
  width: 100%;
  font-family: Georgia, serif;
  font-size: 13px;
  padding: 10px;
  background: var(--accent);
  color: #fdf8f0;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: opacity 0.15s;
}

.email-btn:hover { opacity: 0.85; }

/* ── Bottom nav ── */
.bottom-nav {
  display: flex;
  background: var(--card-bg-start);
  border-top: 1px solid var(--border);
  padding: 0;
}

.nav-btn {
  flex: 1;
  font-family: Georgia, serif;
  font-size: 12px;
  padding: 12px 4px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.nav-btn.active {
  color: var(--accent);
  background: rgba(139, 94, 60, 0.08);
  font-weight: bold;
}

/* ── Email modal ── */
.modal {
  position: fixed;
  inset: 0;
  background: rgba(61, 43, 31, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 16px;
}

.modal.hidden { display: none; }

.modal-content {
  background: var(--card-bg-start);
  border-radius: 16px;
  padding: 24px 20px;
  width: 100%;
  max-width: 320px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.modal-content h3 {
  font-size: 16px;
  color: var(--text-primary);
  text-align: center;
  margin-bottom: 16px;
}

.modal-content input[type="email"] {
  width: 100%;
  font-family: Georgia, serif;
  font-size: 14px;
  padding: 10px 12px;
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--bg);
  color: var(--text-primary);
  margin-bottom: 12px;
  outline: none;
}

.modal-actions {
  display: flex;
  gap: 8px;
}

.modal-actions button {
  flex: 1;
  font-family: Georgia, serif;
  font-size: 13px;
  padding: 10px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

#send-btn {
  background: var(--accent);
  color: #fdf8f0;
}

#cancel-btn {
  background: var(--border);
  color: var(--text-primary);
}

.send-status {
  font-size: 12px;
  text-align: center;
  margin-top: 10px;
  min-height: 18px;
  color: var(--text-muted);
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: add parchment warm color stylesheet"
```

---

## Task 6: HTML Shell

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create index.html**

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="theme-color" content="#8b5e3c">
  <title>每日灵粮</title>
  <link rel="stylesheet" href="style.css">
  <link rel="manifest" href="manifest.json">
  <link rel="apple-touch-icon" href="icons/icon-192.png">
</head>
<body>
  <div id="app">
    <header>
      <p class="app-label">每日灵粮 · Daily Verse</p>
      <p id="date-display" class="date-label"></p>
    </header>

    <main>
      <div class="card">
        <div class="version-tabs" role="tablist">
          <button class="version-tab active" data-version="cuv" role="tab" aria-selected="true">和合本</button>
          <button class="version-tab" data-version="rcuv" role="tab" aria-selected="false">新译和合本</button>
        </div>

        <div id="verse-zh" class="verse-zh"></div>

        <hr class="verse-divider">

        <p class="version-label">NIV</p>
        <div id="verse-niv" class="verse-niv"></div>

        <p id="verse-ref" class="verse-ref"></p>

        <hr class="solid-divider">
        <button id="email-btn" class="email-btn">发送到我的邮箱</button>
      </div>
    </main>

    <nav class="bottom-nav" role="navigation" aria-label="经文分类">
      <button class="nav-btn active" data-category="today">今日</button>
      <button class="nav-btn" data-category="old_testament">旧约</button>
      <button class="nav-btn" data-category="new_testament">新约</button>
      <button class="nav-btn" data-category="gospels">福音书</button>
      <button class="nav-btn" data-category="random">随机</button>
    </nav>
  </div>

  <div id="email-modal" class="modal hidden" role="dialog" aria-modal="true" aria-label="发送经文到邮箱">
    <div class="modal-content">
      <h3>发送经文</h3>
      <input type="email" id="email-input" placeholder="请输入邮箱地址" autocomplete="email">
      <div class="modal-actions">
        <button id="send-btn">发送</button>
        <button id="cancel-btn">取消</button>
      </div>
      <p id="send-status" class="send-status"></p>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
  <script src="config.js"></script>
  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: add PWA HTML shell"
```

---

## Task 7: EmailJS Config

**Files:**
- Create: `config.js`

- [ ] **Step 1: Create config.js with placeholder values**

```javascript
// EmailJS public configuration — safe to commit (these are public keys)
// Replace these values after setting up your EmailJS account (see README)
const EMAILJS_CONFIG = {
  publicKey:  'YOUR_EMAILJS_PUBLIC_KEY',
  serviceId:  'YOUR_EMAILJS_SERVICE_ID',
  templateId: 'YOUR_EMAILJS_TEMPLATE_ID',
};
```

- [ ] **Step 2: Commit**

```bash
git add config.js
git commit -m "feat: add EmailJS config placeholder"
```

---

## Task 8: App Logic — Core Verse Display

**Files:**
- Create: `app.js` (initial version: load and display today's verse)

- [ ] **Step 1: Create app.js with verse loading and display**

```javascript
// State
let allVerses = [];
let currentVerse = null;
let currentVersion = 'cuv';  // 'cuv' | 'rcuv'

// ── Initialise ──────────────────────────────────────────────────────────────
async function init() {
  setDateDisplay();
  emailjs.init(EMAILJS_CONFIG.publicKey);

  try {
    const [versesRes, todayRes] = await Promise.all([
      fetch('data/verses.json'),
      fetch('data/today.json'),
    ]);
    allVerses = await versesRes.json();
    const todayVerse = await todayRes.json();
    showVerse(todayVerse);
  } catch (err) {
    showError('无法加载经文，请检查网络连接。');
    console.error(err);
  }

  bindEvents();
}

// ── Date display ─────────────────────────────────────────────────────────────
function setDateDisplay() {
  const el = document.getElementById('date-display');
  const now = new Date();
  const formatted = now.toLocaleDateString('zh-CN', {
    year: 'numeric', month: 'long', day: 'numeric', weekday: 'long',
  });
  el.textContent = formatted;
}

// ── Render a verse ───────────────────────────────────────────────────────────
function showVerse(verse) {
  currentVerse = verse;
  document.getElementById('verse-zh').textContent =
    `「${verse[currentVersion]}」`;
  document.getElementById('verse-niv').textContent =
    `"${verse.niv}"`;
  document.getElementById('verse-ref').textContent =
    `— ${verse.book_zh} ${verse.chapter}:${verse.verse} / ${verse.book_en} ${verse.chapter}:${verse.verse}`;
}

function showError(msg) {
  document.getElementById('verse-zh').textContent = msg;
  document.getElementById('verse-niv').textContent = '';
  document.getElementById('verse-ref').textContent = '';
}

// ── Random verse from category ───────────────────────────────────────────────
function pickRandom(verses) {
  return verses[Math.floor(Math.random() * verses.length)];
}

// ── Event binding ─────────────────────────────────────────────────────────────
function bindEvents() {
  // Version tabs
  document.querySelectorAll('.version-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.version-tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      currentVersion = tab.dataset.version;
      if (currentVerse) showVerse(currentVerse);
    });
  });

  // Bottom nav — category switching
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const category = btn.dataset.category;
      let pool;

      if (category === 'today') {
        fetch('data/today.json')
          .then(r => r.json())
          .then(v => showVerse(v))
          .catch(() => showError('无法加载今日经文。'));
        return;
      }

      if (category === 'random') {
        pool = allVerses;
      } else {
        pool = allVerses.filter(v => v.category === category);
      }

      if (pool.length === 0) { showError('该分类暂无经文。'); return; }
      showVerse(pickRandom(pool));
    });
  });

  // Email modal
  document.getElementById('email-btn').addEventListener('click', () => {
    document.getElementById('email-modal').classList.remove('hidden');
    document.getElementById('email-input').focus();
  });

  document.getElementById('cancel-btn').addEventListener('click', closeModal);

  document.getElementById('send-btn').addEventListener('click', sendEmail);

  document.getElementById('email-modal').addEventListener('click', e => {
    if (e.target === e.currentTarget) closeModal();
  });
}

function closeModal() {
  document.getElementById('email-modal').classList.add('hidden');
  document.getElementById('send-status').textContent = '';
  document.getElementById('email-input').value = '';
}

// ── EmailJS send ──────────────────────────────────────────────────────────────
async function sendEmail() {
  const email = document.getElementById('email-input').value.trim();
  const status = document.getElementById('send-status');

  if (!email || !email.includes('@')) {
    status.textContent = '请输入有效的邮箱地址。';
    return;
  }

  if (!currentVerse) { status.textContent = '经文尚未加载，请稍候。'; return; }

  status.textContent = '发送中…';
  document.getElementById('send-btn').disabled = true;

  const verse = currentVerse;
  const zhText = verse[currentVersion];
  const ref = `${verse.book_zh} ${verse.chapter}:${verse.verse} / ${verse.book_en} ${verse.chapter}:${verse.verse}`;

  try {
    await emailjs.send(EMAILJS_CONFIG.serviceId, EMAILJS_CONFIG.templateId, {
      to_email: email,
      verse_zh:  zhText,
      verse_niv: verse.niv,
      verse_ref: ref,
      version_label: currentVersion === 'cuv' ? '和合本' : '新译和合本',
    });
    status.textContent = '✓ 已发送！请查收邮箱。';
    setTimeout(closeModal, 2000);
  } catch (err) {
    status.textContent = '发送失败，请稍后再试。';
    console.error(err);
  } finally {
    document.getElementById('send-btn').disabled = false;
  }
}

// ── Boot ──────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);
```

- [ ] **Step 2: Commit**

```bash
git add app.js
git commit -m "feat: add PWA app logic (verse display, tabs, nav, email)"
```

---

## Task 9: PWA Manifest + Service Worker

**Files:**
- Create: `manifest.json`
- Create: `service-worker.js`
- Create: `icons/icon-192.png` and `icons/icon-512.png` (placeholder PNGs)

- [ ] **Step 1: Create manifest.json**

```json
{
  "name": "每日灵粮",
  "short_name": "灵粮",
  "description": "每日圣经经文 · Daily Bible Verse",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#f0e6d6",
  "theme_color": "#8b5e3c",
  "lang": "zh",
  "icons": [
    {
      "src": "icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

- [ ] **Step 2: Generate simple placeholder icons**

```bash
python - <<'EOF'
import struct, zlib

def make_png(size, r, g, b):
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return struct.pack('>I', len(data)) + name + data + struct.pack('>I', c)
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    raw = b''.join(b'\x00' + bytes([r, g, b] * size) for _ in range(size))
    idat = zlib.compress(raw)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

import os; os.makedirs('icons', exist_ok=True)
open('icons/icon-192.png','wb').write(make_png(192, 139, 94, 60))
open('icons/icon-512.png','wb').write(make_png(512, 139, 94, 60))
print("Icons created.")
EOF
```

Expected: `Icons created.`

- [ ] **Step 3: Create service-worker.js**

```javascript
const CACHE = 'bible-verse-v1';
// Use relative paths so this works under any GitHub Pages base URL
const PRECACHE = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './config.js',
  './manifest.json',
  './data/verses.json',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // Always fetch today.json from network (it changes daily); fall back to cache offline
  if (e.request.url.includes('today.json')) {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
    return;
  }
  // Cache-first for everything else
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
      if (res.ok) {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
      }
      return res;
    }))
  );
});
```

- [ ] **Step 4: Register service worker in app.js**

Add at the bottom of `app.js`, after the `DOMContentLoaded` listener:

```javascript
if ('serviceWorker' in navigator) {
  // Relative path works under any GitHub Pages base URL
  navigator.serviceWorker.register('service-worker.js').catch(console.error);
}
```

- [ ] **Step 5: Commit**

```bash
git add manifest.json service-worker.js icons/ app.js
git commit -m "feat: add PWA manifest, service worker, and icons"
```

---

## Task 10: Deploy to GitHub Pages

- [ ] **Step 1: Push code to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/bible-verse-pwa.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

- [ ] **Step 2: Enable GitHub Pages**

Go to your GitHub repo → **Settings** → **Pages** → Source: **Deploy from a branch** → Branch: `main` / `/ (root)` → Save.

Wait ~1 minute, then visit `https://YOUR_USERNAME.github.io/bible-verse-pwa/`.

- [ ] **Step 3: Set up EmailJS (one-time)**

1. Go to [emailjs.com](https://emailjs.com) → Sign Up (free)
2. **Email Services** → Add Service → Gmail → connect your Gmail account → copy **Service ID**
3. **Email Templates** → Create Template with these variables:

```
Subject: 每日灵粮 · {{verse_ref}}

{{version_label}}
{{verse_zh}}

NIV
{{verse_niv}}

— {{verse_ref}}
```

Copy **Template ID**.

4. **Account** → **Public Key** → copy it.

- [ ] **Step 4: Fill in config.js with real values**

Edit `config.js`:

```javascript
const EMAILJS_CONFIG = {
  publicKey:  'abc123XYZ',          // ← your real public key
  serviceId:  'service_xxxxxxx',    // ← your real service ID
  templateId: 'template_xxxxxxx',   // ← your real template ID
};
```

- [ ] **Step 5: Commit and push config**

```bash
git add config.js
git commit -m "config: add EmailJS keys"
git push
```

- [ ] **Step 6: Test manual Actions trigger**

GitHub repo → **Actions** → **Daily Verse Update** → **Run workflow** → Run.

After it completes, refresh the site — today.json should be updated.

- [ ] **Step 7: Test email send**

Open the live site, click "发送到我的邮箱", enter your email, click 发送. Check your inbox.

- [ ] **Step 8: Test PWA install**

Open the site on your phone in Chrome → tap browser menu → "Add to Home Screen". The app should open in standalone mode (no browser chrome).

---

## Done ✓

The PWA is live. Share `https://YOUR_USERNAME.github.io/bible-verse-pwa/` with your small circle — they can open it in their phone browser and add it to their home screen.

To add more verses later, edit `data/verses.json` and commit. The format is the same as the starter entries.
