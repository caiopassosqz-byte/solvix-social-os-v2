#!/bin/bash
# Gera um Reels completo: vídeo mudo, trilha, vídeo com som, prévia da trilha e capa.
#   reels/gerar.sh d04 d04-redesign-clinica
# Requer Node com Playwright (PLAYWRIGHT=/caminho/do/playwright se não estiver no projeto), Python 3 com numpy e ffmpeg.
set -e
R=$(cd "$(dirname "$0")/.." && pwd)
id=$1; slug=$2; ID=$(echo "$id" | tr a-z A-Z)
TMP=$(mktemp -d); D=$R/posts/$slug; mkdir -p "$D"
node "$R/reels/render.js" "$id" video "$TMP/$id.mp4"
python3 "$R/reels/trilha.py" "$ID" "$TMP/$id.json" "$TMP/$id.wav"
ffmpeg -y -loglevel error -i "$TMP/$id.mp4" -i "$TMP/$id.wav" -c:v copy -c:a aac -b:a 192k -shortest "$D/reels-$id.mp4"
cp "$TMP/$id.mp4" "$D/reels-$id-mudo.mp4"
ffmpeg -y -loglevel error -i "$TMP/$id.wav" -c:a libmp3lame -b:a 160k "$R/trilhas/demos/$id.mp3"
T=$(node -e "const m=require('$TMP/$id.json');const e=m.estrutura[0];console.log((e.compassos*4*60/m.bpm*0.93).toFixed(2))")
node "$R/reels/render.js" "$id" capa "$D/capa.png" "$T"
rm -rf "$TMP"; echo "$id pronto em posts/$slug"
