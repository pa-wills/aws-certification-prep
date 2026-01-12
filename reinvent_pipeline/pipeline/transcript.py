def vtt_to_text(vtt_file):
    text_lines = []
    with open(vtt_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "" or "-->" in line or line.startswith("WEBVTT"):
                continue
            text_lines.append(line.strip())
    text = " ".join(text_lines)
    output_file = vtt_file.replace(".vtt", ".txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    return output_file
