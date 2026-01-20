# pipeline/runVideoPipeline.py
import argparse
import os
import sys
import re
import html
import os

def recurse_and_clean(base_input_dir, base_output_dir):
    for root, _, files in os.walk(base_input_dir):
        for file in files:
            if file.endswith(".vtt"):
                input_path = os.path.join(root, file)

                # Preserve directory structure in output
                rel_path = os.path.relpath(input_path, base_input_dir)
                output_path = os.path.join(base_output_dir, rel_path).replace(".vtt", ".txt")

                process_vtt_file(input_path, output_path)

def vtt_to_text(body_bytes):
    lines = []
    seen = set()

    for raw_line in body_bytes.splitlines():
        line = raw_line.decode("utf-8").strip()

        # Remove header lines
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue

        # Remove timestamps
        if "-->" in line:
            continue

        # Remove all <...> including time fragments like <00:00:00.800>
        line = re.sub(r"<[^>]*>", " ", line)

        # Unescape HTML entities
        line = html.unescape(line)

        # Normalize whitespace
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue

        # Remove duplicates (exact match)
        if line in seen:
            continue

        # Remove near duplicates by using a simple normalization
        norm = re.sub(r"[^a-z0-9 ]", "", line.lower())
        if norm in seen:
            continue

        seen.add(line)
        seen.add(norm)

        lines.append(line)

    return " ".join(lines)


def process_vtt_file(input_path, output_path):
    with open(input_path, "rb") as f:
        raw = f.read()

    cleaned = vtt_to_text(raw)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)


if __name__ == "__main__":
    base_input_dir  = "/Users/pwills/Desktop/reinvent 2025/_1_ VTTs as downloaded/"
    base_output_dir = "/Users/pwills/Desktop/reinvent 2025/_2_ Cleaned summaries/"

    recurse_and_clean(base_input_dir, base_output_dir)
