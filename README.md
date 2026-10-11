# willskills

A personal collection of agent **skills** — each one is a `SKILL.md` (plus
optional scripts) that teaches an agent how to handle a recurring task well,
instead of improvising every time.

## Skills

| Skill | What it does |
|---|---|
| [`ai-podcast-generation`](skills/ai-podcast-generation) | Turns a topic into a two-host AI podcast **locally** (bilingual CN/EN): an LLM writes the dialogue, edge-tts voices it, ffmpeg joins it — no paid TTS service or proxy needed. |
| [`metacode`](skills/metacode) | A meta-programming skill that configures and manages agent software (OpenCode, etc.) purely by conversation — initial config, skill/plugin/MCP creation, update diagnostics, and self-evolution. |
| [`optimization-algorithm`](skills/optimization-algorithm) | Designs and improves optimization algorithms from operations research and machine learning (LP/IP/NLP, convex optimization, SGD/Adam/EM/MCMC), and implements new methods from arXiv papers with rigorous benchmarking. |
| [`reading-books`](skills/reading-books) | Reads and interprets works in philosophy, religion, and other humanities — core-idea summaries, key passages, chapter abstracts, historical appraisal, and AI-era reflection. |

## Install

```bash
# all skills
npx skills add Freakwill/willskills -g -y

# one skill
npx skills add Freakwill/willskills --skill metacode -g -y
```
