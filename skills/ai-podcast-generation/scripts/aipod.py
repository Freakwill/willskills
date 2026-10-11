#!/usr/bin/env python3
"""
aipod — Local AI podcast generator (bilingual CN/EN two-host dialogue).

Pipeline:
  1) An LLM (DeepSeek by default) writes a two-host dialogue script from a
     topic + optional bullet points.
  2) edge-tts synthesizes each line with a per-speaker voice (free, no proxy).
  3) ffmpeg concatenates the segments into one MP3.

Everything runs locally and free. Multilingual voices read CN and EN with the
same voice, which is ideal for bilingual episodes.

Usage:
  python3 aipod.py --topic "扩散模型为什么能生成图像" \
      --points "从去噪讲起;类比;为什么比GAN稳定" \
      --lang bilingual --minutes 6 --out ~/podcasts/diffusion

Env:
  DEEPSEEK_API_KEY    DeepSeek API key (canonical name, used by default).
  Or pass --api-key / --base-url / --model to use any OpenAI-compatible API.
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import edge_tts
except ImportError:
    sys.exit("edge-tts not installed. Run: pip3 install edge-tts")

try:
    from openai import OpenAI
except ImportError:
    sys.exit("openai SDK not installed. Run: pip3 install openai")


# --- Speaker -> voice mapping ------------------------------------------------
# Multilingual voices handle both Chinese and English with one timbre.
VOICES = {
    "A": "en-US-AvaMultilingualNeural",     # host A (female)
    "B": "en-US-AndrewMultilingualNeural",  # host B (male)
}
# Pure-Chinese alternatives if you prefer native zh timbres:
VOICES_ZH = {
    "A": "zh-CN-XiaoxiaoNeural",
    "B": "zh-CN-YunxiNeural",
}

HOST_NAMES = {"A": "小艾", "B": "老德"}
HOST_NAMES_EN = {"A": "Ava", "B": "Andrew"}


def host_names(lang):
    return HOST_NAMES_EN if lang == "en" else HOST_NAMES


def build_prompt(topic, points, lang, minutes):
    lang_rule = {
        "bilingual": (
            "对话用中文为主，但在解释专业术语时自然地夹带英文原词与一两句英文补充，"
            "像双语播客那样流畅切换，不要生硬翻译。"
        ),
        "zh": "全程中文。",
        "en": "Entirely in English.",
    }[lang]

    names = host_names(lang)
    if lang == "en":
        intro = (f"You are the writer of a knowledge podcast. Write a dialogue "
                 f"between two hosts, {names['A']} (A) and {names['B']} (B).")
    else:
        intro = (f"你是一档知识播客的编剧。写一段两位主持人 "
                 f"{names['A']}(A) 和 {names['B']}(B) 的对话。")

    pts = ""
    if points:
        pts = "必须覆盖以下要点：\n" + "\n".join(f"- {p}" for p in points) + "\n"

    words = int(minutes * 160)  # ~160 spoken words per minute
    return f"""{intro}
主题：{topic}
{pts}
要求：
- {lang_rule}
- 目标时长约 {minutes} 分钟（约 {words} 字），自然口语，有互相追问、举例、偶尔幽默，不要念稿感。
- 开头有简短欢迎语，结尾有简短总结与告别。
- 深入浅出：先给直觉/类比，再给准确表述。避免空话套话。
- 严格按下面 JSON 数组格式输出，不要任何额外文字、不要 markdown 代码块：
[{{"speaker":"A","text":"..."}},{{"speaker":"B","text":"..."}}, ...]
每条 text 是一句或几句完整的话，不要包含说话人名字前缀。"""


def gen_script(client, model, topic, points, lang, minutes):
    prompt = build_prompt(topic, points, lang, minutes)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )
    raw = resp.choices[0].message.content.strip()
    # Strip accidental code fences.
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    # Grab the outermost JSON array.
    m = re.search(r"\[.*\]", raw, flags=re.DOTALL)
    if not m:
        sys.exit("LLM did not return a JSON array. Raw output:\n" + raw[:500])
    lines = json.loads(m.group(0))
    lines = [d for d in lines if d.get("speaker") in ("A", "B") and d.get("text")]
    if not lines:
        sys.exit("Parsed script is empty.")
    return lines


async def synth_line(text, voice, out_path, rate, pitch, retries=6):
    # Microsoft's TTS endpoint intermittently resets connections (common on
    # direct connections from CN). Retry with exponential backoff.
    last_err = None
    for attempt in range(retries):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await comm.save(str(out_path))
            if out_path.exists() and out_path.stat().st_size > 0:
                return
            raise RuntimeError("empty audio")
        except Exception as e:  # noqa: BLE001 - network layer raises many types
            last_err = e
            wait = min(2 ** attempt, 20)
            await asyncio.sleep(wait)
    raise RuntimeError(f"TTS failed after {retries} tries: {last_err}")


async def synth_all(lines, voices, tmpdir, rate, pitch):
    seg_paths = []
    for i, d in enumerate(lines):
        voice = voices[d["speaker"]]
        p = tmpdir / f"seg_{i:04d}.mp3"
        await synth_line(d["text"], voice, p, rate, pitch)
        seg_paths.append(p)
        print(f"  [{i+1}/{len(lines)}] {d['speaker']} ({voice.split('-')[-1]}): "
              f"{d['text'][:40]}...")
        # Small gap between requests eases the endpoint's rate limiting.
        await asyncio.sleep(0.4)
    return seg_paths


def concat_mp3(seg_paths, out_mp3):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in seg_paths:
            f.write(f"file '{p}'\n")
        listfile = f.name
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
         "-c", "copy", str(out_mp3)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    os.unlink(listfile)


def main():
    ap = argparse.ArgumentParser(description="Local bilingual AI podcast generator")
    ap.add_argument("--topic", required=True, help="Episode topic")
    ap.add_argument("--points", default="", help="Bullet points separated by ;")
    ap.add_argument("--lang", default="bilingual",
                    choices=["bilingual", "zh", "en"])
    ap.add_argument("--minutes", type=float, default=6)
    ap.add_argument("--out", default="~/podcasts/episode",
                    help="Output path prefix (no extension)")
    ap.add_argument("--voice-set", default="multi", choices=["multi", "zh"],
                    help="multi=Multilingual voices; zh=native Chinese voices")
    ap.add_argument("--rate", default="+0%", help="Speech rate, e.g. +10%%")
    ap.add_argument("--pitch", default="+0Hz", help="Pitch, e.g. +5Hz")
    ap.add_argument("--script-only", action="store_true",
                    help="Only write the script JSON/TXT, skip TTS")
    ap.add_argument("--from-script", default="",
                    help="Skip LLM; synthesize from an existing script JSON")
    ap.add_argument("--api-key",
                    default=os.environ.get("DEEPSEEK_API_KEY", ""),
                    help="API key (default: $DEEPSEEK_API_KEY)")
    ap.add_argument("--base-url", default="https://api.deepseek.com")
    ap.add_argument("--model", default="deepseek-chat")
    args = ap.parse_args()

    out = Path(os.path.expanduser(args.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    points = [p.strip() for p in args.points.split(";") if p.strip()]
    voices = VOICES if args.voice_set == "multi" else VOICES_ZH

    # 1) script
    if args.from_script:
        lines = json.loads(Path(os.path.expanduser(args.from_script)).read_text())
    else:
        if not args.api_key:
            sys.exit("No API key. Set DEEPSEEK_API_KEY or pass --api-key.")
        print(f"Generating script via {args.model} ...")
        client = OpenAI(api_key=args.api_key, base_url=args.base_url)
        lines = gen_script(client, args.model, args.topic, points,
                           args.lang, args.minutes)
        script_json = out.with_suffix(".script.json")
        script_txt = out.with_suffix(".script.txt")
        script_json.write_text(json.dumps(lines, ensure_ascii=False, indent=2))
        script_txt.write_text(
            "\n\n".join(f"{host_names(args.lang)[d['speaker']]}：{d['text']}"
                        for d in lines)
        )
        print(f"Script saved: {script_json}")
        print(f"Readable:     {script_txt}")

    if args.script_only:
        return

    # 2) TTS
    print(f"Synthesizing {len(lines)} lines with edge-tts ...")
    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        seg_paths = asyncio.run(
            synth_all(lines, voices, tmpdir, args.rate, args.pitch)
        )
        # 3) concat
        out_mp3 = out.with_suffix(".mp3")
        print("Concatenating -> " + str(out_mp3))
        concat_mp3(seg_paths, out_mp3)

    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)],
        capture_output=True, text=True,
    ).stdout.strip()
    print(f"\nDone. {out_mp3}  (~{float(dur)/60:.1f} min)")


if __name__ == "__main__":
    main()
