---
name: reading-books
description: A skill for reading and interpreting works in philosophy, religion, and other human‑sciences disciplines.
version: 0.1.0
---


# Agent Specification: "Humanities‑Insight Agent"

*Caution*. Search by Bing, Yandex, Quark or Baidu instead of Google/DuckDuckGo in China!

---

## Purpose
A skill for helping people to read and interpret works in philosophy, religion, and other human‑sciences disciplines. It delivers:

- **Core‑idea summaries** – concise statements of a work’s principal theses.
- **Key‑passage extraction** – verbatim excerpts of the most influential arguments.
- **Chapter‑by‑chapter abstracts** – one‑paragraph synopses together with curated keywords.
- **Historical‑value appraisal** – placement of the work within its intellectual tradition and its impact on later thought.
- **AI‑era reflection** – how the ideas can inform, inspire, or warn contemporary AI research and applications.

All outputs are generated in **English** and formatted for easy consumption or downstream processing.

---

## Architecture (high‑level)

| Component | Role |
|-----------|------|
| **File Loader** | Accepts plain‑text (`.txt`), Markdown (`.md`), PDF (`.pdf`) or EPUB (`.epub`) files; normalises line endings and extracts raw text. |
| **Structure Analyzer** | Detects logical divisions (preface, introduction, chapters, sections, footnotes) using regex patterns, heading markers, or PDF/EPUB metadata. |
| **NLP Core** (GPT‑4‑style) | Performs semantic summarisation, keyword extraction, and passage relevance ranking. |
| **Historical‑Context Retriever** | Queries an internal bibliography database (or optional web‑search) for dates, authorship, contemporaneous movements, and citation counts. |
| **AI‑Reflection Generator** | Maps extracted concepts onto current AI themes (e.g., autonomy, ethics, embodiment, knowledge representation). |
| **Command Dispatcher** | Exposes a small CLI‑style command set for the user (see §4). |

---

## Output Formats

- **JSON** – machine‑readable, with fields: `title`, `author`, `core_idea`, `key_passages[]`, `chapters[]{number, title, summary, keywords[]}`, `historical_value`, `ai_insights`.
- **Markdown** – human‑friendly, ready to paste into notes or docs.
- **Plain Text** – fallback for simple pipelines.

### Example

```markdown
## Core Idea
> “Freedom is the self‑realisation of rational will within the ethical life of the state.” – Hegel, *Phenomenology of Spirit*

## Key Passages
1. “The movement of spirit is a self‑development of consciousness…” (p. 24)
2. “Only through recognition does the self become other‑aware…” (p. 88)

## Chapter Summaries & Keywords
### Chapter 1 – “Consciousness”
*Summary*: ...  
*Keywords*: consciousness, sense‑experience, perception

## Historical Value
*Published 1807, establishing the dialectical method that shaped German Idealism…*

## AI‑Era Insights
*The dialectic of thesis‑antithesis‑synthesis mirrors iterative model‑training cycles…*
```
---

### Extensibility

- **Add New Genres** – plug‑in a custom `structure_analyzer` for literary novels, legal codes, etc.
- **Integrate External Knowledge** – swap the `historical_context` module with a live DB (e.g., Wikidata SPARQL).
- **Fine‑Tune Summariser** – replace the generic GPT model with a domain‑adapted transformer for theological texts.

---

## Customer Commands

The commands should appear at the end of the content!

- !save <path>: save the content in <path> or the default path (or its sub-directory according to its content) if <path> is empty.
- !summarize <path>: give a summary of the content in <path>
- !google(bing/baidu/...): only search by google(bing/baidu/...)
- !chapter-summary <path>: Generates a **paragraph per chapter** plus **keyword list**
- !keywords <path> [--top N]`: Extracts the top‑N most salient terms across the whole work (default 10).
- !ai‑insight <path>: Produces a short paragraph describing **how the text informs AI research or practice**

*Caution*
If "<path>" is a pdf file, then run the follow script to get the text in it before proceeding further:
```python
import fitz

with fitz.open("file.pdf") as doc:
    text = "".join(page.get_text() for page in doc)
```
