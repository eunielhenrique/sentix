#!/usr/bin/env python3
"""Transcreve gravações de chamadas (MP3) com faster-whisper, uma saída JSON por gravação.

Uso: python3 transcribe.py <pasta_audio> <pasta_saida> [--model large-v3-turbo]
Idempotente: pula arquivos já transcritos. Escreve progresso em <pasta_saida>/_progress.log.
"""
import json, sys, time, argparse, pathlib

VOCAB = ("Wesley Cezar, Ratinho, Santana de Parnaíba, deputado estadual, deputado federal, "
         "cabo eleitoral, material digital, grupo de WhatsApp, apoio, campanha, candidato, "
         "Barueri, Cajamar, Osasco, Carapicuíba, Campinas, Bauru, Sorocaba, Ribeirão Preto.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio_dir"); ap.add_argument("out_dir")
    ap.add_argument("--model", default="large-v3-turbo")
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args()
    from faster_whisper import WhisperModel
    audio = pathlib.Path(a.audio_dir); out = pathlib.Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    log = open(out / "_progress.log", "a")
    files = sorted(p for p in audio.glob("*.mp3") if p.stem not in ("teste", "amostra"))
    todo = [p for p in files if not (out / f"{p.stem}.json").exists()]
    print(f"{len(files)} áudios, {len(todo)} a transcrever", file=log, flush=True)
    model = WhisperModel(a.model, device="cpu", compute_type="int8", cpu_threads=a.threads)
    t0 = time.time(); done_sec = 0
    for i, p in enumerate(todo, 1):
        t = time.time()
        segs, info = model.transcribe(str(p), language="pt", beam_size=1, vad_filter=True,
                                      initial_prompt=VOCAB, condition_on_previous_text=False)
        segments = [{"start": round(s.start, 1), "end": round(s.end, 1), "text": s.text.strip()} for s in segs]
        text = " ".join(s["text"] for s in segments)
        json.dump({"id": p.stem, "model": a.model, "duration": round(info.duration, 1),
                   "text": text, "segments": segments}, open(out / f"{p.stem}.json", "w"),
                  ensure_ascii=False, indent=1)
        done_sec += info.duration
        print(f"{i}/{len(todo)} {p.stem} {info.duration:.0f}s em {time.time()-t:.0f}s | "
              f"acumulado {done_sec/60:.0f} min de áudio em {(time.time()-t0)/60:.0f} min", file=log, flush=True)
    print("CONCLUIDO", file=log, flush=True)

if __name__ == "__main__":
    main()
