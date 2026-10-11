---
name: ai-podcast-generation
description: Use when generating an AI podcast from a topic or text. Builds local two-host dialogue audio (bilingual CN/EN) as LLM script + edge-tts voices + ffmpeg, with no paid TTS service or proxy required.
category: media
author: William
tags: [podcast, tts, edge-tts, audio, llm, bilingual]
version: 0.1.0
---

# AI Podcast / Spoken-Audio Generation

Generate podcast-style audio **locally** instead of relying on packaged tools
(Doubao / NotebookLM — often no public API, feature-limited, or blocked in some
regions). An "AI podcast" is just three decoupled steps:

1. **LLM writes a dialogue script** from a topic + bullet points.
2. **TTS synthesizes** each line with a per-speaker voice.
3. **ffmpeg concatenates** the segments into one MP3.

Keeping the steps separate gives full control — hand-edit the script, pick
voices, and dial the exact length — that packaged tools deny.

## Pipeline

`scripts/aipod.py` is a complete, tested generator:

```
topic + bullet points → LLM writes a two-host CN/EN dialogue
                      → edge-tts synthesizes per-speaker voices (free, no proxy)
                      → ffmpeg concat → one MP3
```

```bash
pip install edge-tts openai          # plus ffmpeg on PATH
export DEEPSEEK_API_KEY=...          # or pass --api-key for any OpenAI-compatible API

python3 scripts/aipod.py \
  --topic "Why diffusion models can generate images" \
  --points "start from denoising intuition;why training is stabler than GANs;how it differs from autoregressive generation" \
  --lang bilingual --minutes 6 --out ~/podcasts/diffusion
```

Key flags:

| Flag | Meaning |
|---|---|
| `--lang bilingual\|zh\|en` | Bilingual CN/EN, pure Chinese, or pure English |
| `--points "a;b;c"` | Bullet points the script must cover (split on `;`) |
| `--minutes N` | Target duration (see length caveat below) |
| `--voice-set multi\|zh` | `multi` = Multilingual voices; `zh` = native Chinese voices |
| `--rate +10%` / `--pitch +5Hz` | Speech rate / pitch |
| `--script-only` | Write the script (JSON + TXT), skip audio |
| `--from-script x.json` | Skip the LLM; synthesize an already-edited script |
| `--api-key/--base-url/--model` | Point at any OpenAI-compatible provider |

**Recommended workflow**: `--script-only` → hand-edit the `.script.json` →
`--from-script` to synthesize. The script is the expensive-to-review part; TTS
is the cheap step to re-run.

## Voice choice

- **Bilingual episodes**: use edge-tts *Multilingual* voices
  (`en-US-AvaMultilingualNeural`, `en-US-AndrewMultilingualNeural`) — one timbre
  reads both Chinese and English, so a host never switches voice mid-sentence.
- **Pure Chinese**: native voices `zh-CN-XiaoxiaoNeural` (F),
  `zh-CN-YunxiNeural` (M).
- List everything: `python3 -m edge_tts --list-voices | grep -E '^(zh-CN|en-US)-'`

## Hitting a target length

**`--minutes` does NOT reliably set the final length.** In testing, DeepSeek
caps the script at ~1000–1100 English words (~150 spoken words/min ⇒ ~7 min)
no matter how large `--minutes` is — runs at 8 / 10 / 12 min all landed at
~6.5–7.0 min of audio. So do **not** re-roll hoping for a longer script.

Instead, extend the best script **deterministically** with
`scripts/extend_script.py`, which asks the model to insert a few extra
exchanges (~200–250 words ≈ +1 min) just before the conclusion:

```bash
python3 scripts/extend_script.py \
  --src grief.script.json --out grief-ext.script.json \
  --topic "Grief" --add "theme one;theme two;theme three" --n 3
python3 scripts/aipod.py --topic "Grief" \
  --from-script grief-ext.script.json --out grief-final
```

Verified: 7.1 min → 8.7 min. (Sometimes one generation already lands near the
target — always measure the MP3 with `ffprobe` before deciding to extend.)

## Pitfalls

- **LLM JSON wrapping.** Models sometimes wrap the script in ```json fences or
  add prose. Strip fences and regex-extract the outermost `[...]` array before
  parsing (aipod.py already does this).
- **Speaker names leak into text.** The dialogue prompt must forbid
  speaker-name prefixes inside each line's text — names come from the voice
  mapping, not the spoken content.
- **Use the language-appropriate host names.** For `--lang en`, give the model
  English names (Ava/Andrew); passing Chinese names leaks them into an
  otherwise-English script. aipod.py selects the name set from `--lang`.
- **edge-tts `Connection reset by peer` on `speech.platform.bing.com:443`.**
  The Microsoft endpoint intermittently resets connections when many WebSockets
  open quickly. Fix: exponential-backoff retry per line + a ~0.4 s gap between
  requests (built into aipod.py `synth_line`). Do not conclude edge-tts is
  broken — retry makes it reliable.
- **edge-tts can still exhaust retries** on a bad network moment ("Cannot write
  to closing transport"). The run aborts with no partial output; just re-run —
  synthesis is deterministic, so re-running is safe.
- **API key variable.** DeepSeek's key is conventionally `DEEPSEEK_API_KEY`.
  Do not assume a custom name like `DEEPSEEK2_API_KEY`.

## Upgrading TTS quality

If edge-tts sounds too flat, swap only `synth_line` to call **MiniMax** (海螺,
direct-connect from China, top-tier Chinese TTS, has an API) or **ElevenLabs**
(best timbre, may need a proxy). The script-generation and concat stages stay
unchanged.

## Building blocks (reuse without the full script)

- **LLM step**: any OpenAI-compatible API. Default DeepSeek
  (`DEEPSEEK_API_KEY`, base_url `https://api.deepseek.com`, model `deepseek-chat`).
- **TTS step**: `edge_tts.Communicate(text, voice, rate, pitch).save(path)`.
- **Concat**: `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp3`.

## Requirements

- Python 3, `edge-tts`, `openai`, and `ffmpeg` on `PATH`.
- Any OpenAI-compatible LLM endpoint (DeepSeek by default).
