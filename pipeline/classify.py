#!/usr/bin/env python3
"""Classifica transcrições com um modelo de linguagem, seguindo pipeline/CLASSIFICACAO.md.

Uso: python3 classify.py <pasta_trabalho> [--provider anthropic|gemini]
Variáveis: ANTHROPIC_API_KEY ou GEMINI_API_KEY. Idempotente: pula chamadas já classificadas.
Saída: <pasta>/analises/<id>.json e <pasta>/analises.json (consolidado).
"""
import json, os, sys, argparse, pathlib, urllib.request

HERE = pathlib.Path(__file__).parent
SCHEMA = (HERE / "CLASSIFICACAO.md").read_text(encoding="utf-8")
SYSTEM = ("Você analisa transcrições de ligações de uma equipe de mobilização/vendas por telefone no Brasil. "
          "Responda SOMENTE com um JSON válido no formato do esquema abaixo, em pt-BR, sem comentários. "
          "Use apenas o que está na transcrição; sem evidência, use null.\n\n" + SCHEMA)

def call_anthropic(prompt, key, model=None):
    model = model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    body = {"model": model, "max_tokens": 2000, "system": SYSTEM,
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=json.dumps(body).encode(),
                                 headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["content"][0]["text"]

def call_gemini(prompt, key, model=None):
    model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    body = {"systemInstruction": {"parts": [{"text": SYSTEM}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["candidates"][0]["content"]["parts"][0]["text"]

def parse_json(s):
    s = s.strip()
    if s.startswith("```"): s = s.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir"); ap.add_argument("--provider", default=None)
    a = ap.parse_args()
    wd = pathlib.Path(a.workdir); out = wd / "analises"; out.mkdir(exist_ok=True)
    prov = a.provider or ("anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "gemini")
    key = os.environ.get("ANTHROPIC_API_KEY" if prov == "anthropic" else "GEMINI_API_KEY") or sys.exit("defina a chave do provedor")
    call = call_anthropic if prov == "anthropic" else call_gemini
    meta = {c["id"]: c for c in json.load(open(wd / "recordings.json"))}
    feitos, erros = 0, 0
    for tp in sorted((wd / "transcripts").glob("*.json")):
        if tp.name.startswith("_") or (out / tp.name).exists(): continue
        t = json.load(open(tp)); c = meta.get(t["id"], {})
        prompt = (f"Chamada id={t['id']} telefone={c.get('to')} vendedor={c.get('first_name')} "
                  f"duracao_s={t['duration']} data={c.get('started_at')}\n\nTRANSCRIÇÃO:\n{t['text'] or '(vazia)'}")
        try:
            res = parse_json(call(prompt, key)); res.setdefault("id", t["id"])
            json.dump(res, open(out / tp.name, "w"), ensure_ascii=False, indent=1); feitos += 1
        except Exception as e:
            erros += 1; print("erro", t["id"], e, file=sys.stderr)
    todos = [json.load(open(p)) for p in sorted(out.glob("*.json"))]
    json.dump(todos, open(wd / "analises.json", "w"), ensure_ascii=False, indent=1)
    print(f"classificadas agora: {feitos} | erros: {erros} | total: {len(todos)}")

if __name__ == "__main__":
    main()
