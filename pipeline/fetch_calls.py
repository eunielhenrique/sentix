#!/usr/bin/env python3
"""Busca chamadas na API4COM, baixa gravações novas e mantém um índice local.

Uso: API4COM_TOKEN=... python3 fetch_calls.py <pasta_trabalho> [--since 2026-09-21] [--all]
- Sem --all, busca só as páginas mais recentes até encontrar chamadas já conhecidas (modo cron).
- Escreve <pasta>/calls.json (índice), <pasta>/audio/<id>.mp3 e <pasta>/recordings.json.
Token: gere em https://app.api4com.com/user/tokens (ou POST /users/login) e passe por variável de ambiente.
"""
import json, os, sys, argparse, pathlib, urllib.parse, urllib.request

API = "https://api.api4com.com/api/v1"

def get(path, token):
    req = urllib.request.Request(f"{API}/{path}", headers={"Authorization": token})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("--since"); ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    token = os.environ.get("API4COM_TOKEN") or sys.exit("defina API4COM_TOKEN")
    wd = pathlib.Path(a.workdir); (wd / "audio").mkdir(parents=True, exist_ok=True)
    idx_path = wd / "calls.json"
    known = {c["id"]: c for c in json.load(open(idx_path))} if idx_path.exists() else {}
    where = {"started_at": {"gte": a.since}} if a.since else {}
    page, novos = 1, 0
    while True:
        f = urllib.parse.quote(json.dumps({"where": where, "limit": 100, "order": "started_at desc"}))
        d = get(f"calls?page={page}&filter={f}", token)
        rows = d.get("data", []); meta = d.get("meta", {})
        hit_known = False
        for c in rows:
            if c["id"] in known: hit_known = True; continue
            known[c["id"]] = c; novos += 1
        if not rows or page >= meta.get("totalPageCount", 1) or (hit_known and not a.all): break
        page += 1
    json.dump(list(known.values()), open(idx_path, "w"), ensure_ascii=False, indent=1)
    recs = [c for c in known.values() if c.get("record_url")]
    baixados = 0
    for c in recs:
        dest = wd / "audio" / f"{c['id']}.mp3"
        if dest.exists(): continue
        urllib.request.urlretrieve(c["record_url"], dest); baixados += 1
    json.dump(recs, open(wd / "recordings.json", "w"), ensure_ascii=False, indent=1)
    print(f"chamadas conhecidas: {len(known)} | novas: {novos} | gravações: {len(recs)} | áudios baixados agora: {baixados}")

if __name__ == "__main__":
    main()
