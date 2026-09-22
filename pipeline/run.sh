#!/usr/bin/env bash
# Executa o pipeline completo com lock. Uso: run.sh <pasta_trabalho>
set -euo pipefail
WD="${1:?pasta de trabalho}"; HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$WD"; exec 9>"$WD/.lock"; flock -n 9 || { echo "já em execução"; exit 0; }
echo "[$(date -Is)] fetch";       python3 "$HERE/fetch_calls.py" "$WD"
echo "[$(date -Is)] transcribe";  python3 "$HERE/transcribe.py" "$WD/audio" "$WD/transcripts"
echo "[$(date -Is)] classify";    python3 "$HERE/classify.py" "$WD"
echo "[$(date -Is)] consolidate"; python3 "$HERE/consolidate.py" "$WD"
echo "[$(date -Is)] ok"
