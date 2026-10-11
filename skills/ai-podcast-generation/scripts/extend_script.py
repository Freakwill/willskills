#!/usr/bin/env python3
"""Extend an existing podcast script with extra exchanges, keeping hosts/tone.

DeepSeek caps script length (~1000-1100 words) regardless of --minutes, so to
hit a longer target duration we extend a good script deterministically instead
of re-rolling.

Usage:
  python3 extend_script.py --src a.script.json --out b.script.json \
      --topic "..." --add "theme one;theme two;theme three" --n 3
Then synth with:  python3 aipod.py --topic "..." --from-script b.script.json \
      --out final
"""
import argparse, json, os, re, sys
from openai import OpenAI


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--topic", required=True)
    ap.add_argument("--add", required=True,
                    help="New themes to cover, separated by ;")
    ap.add_argument("--n", type=int, default=3, help="Exchanges to insert")
    ap.add_argument("--words", type=int, default=230, help="Approx words to add")
    ap.add_argument("--lang", default="en")
    args = ap.parse_args()

    lines = json.loads(open(os.path.expanduser(args.src)).read())
    themes = [t.strip() for t in args.add.split(";") if t.strip()]
    themed = "\n".join(f"  {i+1}) {t}" for i, t in enumerate(themes))

    prompt = f"""Here is a two-host podcast script as a JSON array (A = Ava, B = Andrew).
Topic: {args.topic}

TASK: Extend it. Insert {args.n} additional exchanges between the two hosts,
placed just BEFORE the final two exchanges (the summary/outro). Add roughly
{args.words} words total. The new exchanges must deepen the discussion without
repeating earlier points, covering:
{themed}

Rules: same tone, natural spoken {args.lang}, no stage directions, no host names
inside the text. Return the COMPLETE new JSON array only (all original lines,
with the new ones inserted), nothing else.

Current script:
{json.dumps(lines, ensure_ascii=False)}"""

    client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
                    base_url="https://api.deepseek.com")
    raw = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    ).choices[0].message.content.strip()
    raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
    m = re.search(r"\[.*\]", raw, flags=re.DOTALL)
    if not m:
        sys.exit("No JSON array in model output:\n" + raw[:500])
    new = [d for d in json.loads(m.group(0))
           if d.get("speaker") in ("A", "B") and d.get("text")]
    out = os.path.expanduser(args.out)
    json.dump(new, open(out, "w"), ensure_ascii=False, indent=2)
    words = sum(len(d["text"].split()) for d in new)
    print(f"{len(lines)} -> {len(new)} lines ; ~{words} words ; saved {out}")


if __name__ == "__main__":
    main()
