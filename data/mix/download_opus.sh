#!/usr/bin/env bash
# Download the D22 OPUS corpora on a machine that can reach object.pouta.csc.fi (D23: it is unreachable
# from the GB10 workstation), then copy them to the GB10 workstation. Run from an empty folder:
#     bash download_opus.sh            # downloads into ./opus-<corpus>-<version>-<pair>/ and writes SHA256SUMS
#     scp -r opus-* SHA256SUMS <user>@<gpu-host>:~/data/raw/incoming-opus/
# On the GB10 workstation, SHA256SUMS, the zip contents and the pair counts are then checked against the OPUS API.
set -euo pipefail
corpora=(
  "CCMatrix v1 en-tl 3113828"
  "OpenSubtitles v2024 en-tl 1072914"
  "WikiMatrix v1 en-tl 75447"
  "bible-uedin v1 en-tl 62195"
  "QED v2.0a en-tl 3092"
  "QED v2.0a en-fil 42864"
  "GlobalVoices v2018q4 en-fil 2742"
)
for spec in "${corpora[@]}"; do
  read -r name ver pair pairs <<<"$spec"
  d="opus-$name-$ver-$pair"
  mkdir -p "$d"
  url="https://object.pouta.csc.fi/OPUS-$name/$ver/moses/$pair.txt.zip"
  echo "downloading $url (expect $pairs pairs)"
  curl -fL --retry 3 -D "$d/headers.txt" -o "$d/$pair.txt.zip" "$url"
  echo "$url" > "$d/SOURCE_URL"
done
sha256sum opus-*/*.zip > SHA256SUMS
cat SHA256SUMS
