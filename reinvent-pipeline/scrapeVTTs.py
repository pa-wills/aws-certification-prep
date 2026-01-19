#!/bin/bash

PLAYLIST_URL="PASTE_YOUR_PLAYLIST_URL_HERE"
OUTPUT_DIR="vtts"
mkdir -p "$OUTPUT_DIR"

yt-dlp \
  --skip-download \
  --write-auto-sub \
  --sub-format vtt \
  -o "$OUTPUT_DIR/%(id)s.%(ext)s" \
  "$PLAYLIST_URL"
