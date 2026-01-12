def chunk_text(text_file, chunk_size=500):
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks
