# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **Python**: 3.14 (via `.venv/`)
- **Run any script**: `python "<filename>.py"` — note that many filenames contain spaces and require quotes.
- **Activate venv**: `source .venv/bin/activate`

Key installed packages: `tkinter` (stdlib), `Pillow`, `pandas`, `numpy`, `matplotlib`, `requests`, `openpyxl`.

## Repository Structure

This is a **university coursework repository** (FP016 Computer Science). Files fall into two categories:

**Classwork / exercises** — standalone scripts named by date:
`9 dec.py`, `12 jan class.py`, `6feb.py`, `16feb.py`, `9 feb.py`, `2 march.py`, `3 maer.py`, `6 march.py`, `18 march.py`, `worsheet 1.py`, `classwork 8dec.py`, `first.py`, `second.py`, `welcome.py`, `f.py`, `dd.py`, `aa.py`, `kk].py`

**Projects (Summative Assessments)**:
- `12.py` — main project: *Whispers at Victor's Manor* (narrative mystery game)
- `weather forecast application.py` — weather app using OpenWeatherMap API
- `social network project.py` — graph-based social network simulation
- `irs.py` / `IRS PREFINAL STATS.py` — statistical analysis with pandas/matplotlib
- `implementation python.py`, `project cs.py`, `job done.py` — other assessment work

**Data files**: `medata.xlsx`, `mydata.xls`, `myprjct.xlsx`, `.csv` files (UK mobile coverage data) — used by the stats/IRS scripts.

## Main Project: `12.py` — Whispers at Victor's Manor

Architecture is a clean 6-section single-file application:

| Section | Contents |
|---------|----------|
| 1 — Data Structures | `StoryNode`, `Stack` (LIFO for rewind), `ClueHeap` (max-heap via negated `heapq`) |
| 2 — Story Graph | `build_story_graph()` — builds `Dict[str, StoryNode]`; rooted at `"S1"`, two branches (Security / Sophia), four endings |
| 3 — Algorithms | `dfs_reachability`, `bfs_shortest_path`, `insertion_sort_clues`, `topological_sort`, `get_clue_dependencies` |
| 4 — Game Engine | `GameEngine` — owns all state; exposes `make_choice()`, `rewind()`, `restart()`; no UI code |
| 5 — GUI | `StartWindow`/`StartScreen`, `GameApp` (main window), `EvidencePanel` (Toplevel), `AnalysisWindow` (tabbed Toplevel) |
| 6 — Entry point | `main()` — creates start-screen root, then main-game root if confirmed |

**Story graph shape**: `S1 → S2 → {Q1_SECURITY, Q1_SOPHIA}` — each branch leads to 2 sub-paths → 4 endings (`ENDING_1`, `ENDING_2A`, `ENDING_2B`, `ENDING_3`). Nodes with `allow_rewind=False` block the rewind feature.

**Clue system**: clues are stored in both a `ClueHeap` (priority by importance) and a flat `discovered_clues` list (chronological). The Evidence Panel can display either view.
