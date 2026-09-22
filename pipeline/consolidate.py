#!/usr/bin/env python3
"""Consolida análises por telefone e por vendedor e gera relatório em Markdown e CSV.

Uso: python3 consolidate.py <pasta_trabalho>
Lê <pasta>/calls.json (todas as chamadas, inclusive sem gravação), <pasta>/recordings.json e
<pasta>/analises/*.json. Escreve <pasta>/leads_classificados.csv, <pasta>/vendedores.csv e
<pasta>/RELATORIO.md.
"""
import json, csv, sys, pathlib, collections, statistics

ORDEM = ["apoiador_ativo", "engajado", "recebeu_material", "retornar_depois", "neutro",
         "pede_ajuda_ou_beneficio", "nao_e_o_contato", "recusou", "invalido"]
CRIT = ["abertura", "escuta", "objecoes", "clareza", "fechamento", "proximo_passo"]

def norm_tel(t):
    t = "".join(ch for ch in str(t or "") if ch.isdigit())
    return t[-11:] if len(t) >= 11 else t

def main():
    wd = pathlib.Path(sys.argv[1])
    calls = json.load(open(wd / "calls.json")) if (wd / "calls.json").exists() else []
    recs = {r["id"]: r for r in json.load(open(wd / "recordings.json"))}
    analises = {}
    for p in (wd / "analises").glob("*.json"):
        try: a = json.load(open(p)); analises[a["id"]] = a
        except Exception: pass
    por_tel = collections.defaultdict(lambda: {"tentativas": 0, "conversas": 0, "chamadas": []})
    for c in calls:
        k = norm_tel(c.get("to")); por_tel[k]["tentativas"] += 1
        por_tel[k]["chamadas"].append(c)
    leads = []
    for tel, d in por_tel.items():
        an = [analises[c["id"]] for c in sorted(d["chamadas"], key=lambda x: x["started_at"]) if c["id"] in analises]
        conv = [a for a in an if a.get("falou_com_lead")]
        ult = conv[-1] if conv else (an[-1] if an else None)
        leads.append({
            "telefone": tel, "tentativas": d["tentativas"], "conversas": len(conv),
            "classificacao": (ult or {}).get("classificacao_lead") or ("sem_conversa" if not conv else None),
            "interesse": (ult or {}).get("interesse"), "sentimento": (ult or {}).get("sentimento_lead"),
            "aceitou_grupo": (ult or {}).get("aceitou_grupo"), "recebeu_material": (ult or {}).get("recebeu_material"),
            "vai_divulgar": (ult or {}).get("vai_divulgar"), "cidade": (ult or {}).get("cidade_mencionada"),
            "votos_familia": (ult or {}).get("familia_votos_estimados"),
            "proximo_passo": (ult or {}).get("proximo_passo"), "vendedor": (ult or {}).get("vendedor") or (d["chamadas"][-1].get("first_name")),
            "resumo": (ult or {}).get("resumo"), "alertas": "; ".join((ult or {}).get("alertas") or []),
            "ultima_chamada": max(c["started_at"] for c in d["chamadas"]),
        })
    leads.sort(key=lambda l: (ORDEM.index(l["classificacao"]) if l["classificacao"] in ORDEM else 99, -(l["interesse"] or 0)))
    with open(wd / "leads_classificados.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(leads[0].keys()) if leads else ["telefone"]); w.writeheader(); w.writerows(leads)
    # vendedores
    vend = collections.defaultdict(lambda: {"chamadas": 0, "conversas": 0, "notas": collections.defaultdict(list), "engajados": 0, "fortes": collections.Counter(), "melhorar": collections.Counter()})
    for c in calls: vend[c.get("first_name")]["chamadas"] += 1
    for a in analises.values():
        v = vend[a.get("vendedor")]
        if a.get("falou_com_lead"): v["conversas"] += 1
        if a.get("classificacao_lead") in ("apoiador_ativo", "engajado", "recebeu_material"): v["engajados"] += 1
        r = a.get("rubrica_vendedor") or {}
        for k in CRIT:
            n = (r.get(k) or {}).get("nota")
            if isinstance(n, (int, float)): v["notas"][k].append(n)
        for s in a.get("pontos_fortes") or []: v["fortes"][s[:60]] += 1
        for s in a.get("pontos_a_melhorar") or []: v["melhorar"][s[:60]] += 1
    rows = []
    for nome, v in vend.items():
        med = {k: (round(statistics.mean(v["notas"][k]), 2) if v["notas"][k] else None) for k in CRIT}
        geral = [x for x in med.values() if x is not None]
        rows.append({"vendedor": nome, "chamadas": v["chamadas"], "conversas": v["conversas"], "engajados": v["engajados"],
                     "taxa_engajamento": round(v["engajados"] / v["conversas"], 2) if v["conversas"] else None,
                     **{f"nota_{k}": med[k] for k in CRIT}, "nota_geral": round(statistics.mean(geral), 2) if geral else None,
                     "forte_mais_comum": (v["fortes"].most_common(1) or [("", 0)])[0][0],
                     "melhorar_mais_comum": (v["melhorar"].most_common(1) or [("", 0)])[0][0]})
    rows.sort(key=lambda r: -(r["nota_geral"] or 0))
    with open(wd / "vendedores.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["vendedor"]); w.writeheader(); w.writerows(rows)
    # relatório
    cls = collections.Counter(l["classificacao"] for l in leads)
    obj = collections.Counter((o.get("tipo") or "?") for a in analises.values() for o in (a.get("objecoes") or []))
    ped = collections.Counter(p for a in analises.values() for p in (a.get("pedidos") or a.get("pediu") or []))
    px = collections.Counter(l["proximo_passo"] for l in leads if l["proximo_passo"])
    alertas = [(a["id"], a.get("vendedor"), al) for a in analises.values() for al in (a.get("alertas") or [])]
    L = [f"# Relatório da força-tarefa de chamadas\n",
         f"- Chamadas: {len(calls)} · telefones únicos: {len(leads)} · gravações analisadas: {len(analises)}",
         f"- Conversas reais (falou com o lead): {sum(1 for a in analises.values() if a.get('falou_com_lead'))}\n",
         "## Classificação dos telefones\n", "| Classificação | Telefones |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in sorted(cls.items(), key=lambda kv: -kv[1])]
    L += ["\n## Próximo passo sugerido\n", "| Ação | Telefones |", "|---|---|"] + [f"| {k} | {v} |" for k, v in px.most_common()]
    L += ["\n## Objeções mais frequentes\n"] + [f"- {k}: {v}" for k, v in obj.most_common(8)]
    L += ["\n## Pedidos dos leads\n"] + [f"- {k}: {v}" for k, v in ped.most_common(8)]
    L += ["\n## Vendedores (rubrica 1–5)\n", "| Vendedor | Chamadas | Conversas | Engajados | Taxa | Nota geral | Melhor critério | Pior critério |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        notas = {k: r[f"nota_{k}"] for k in CRIT if r[f"nota_{k}"] is not None}
        mb = max(notas, key=notas.get) if notas else "—"; pi = min(notas, key=notas.get) if notas else "—"
        L.append(f"| {r['vendedor']} | {r['chamadas']} | {r['conversas']} | {r['engajados']} | {r['taxa_engajamento'] or '—'} | {r['nota_geral'] or '—'} | {mb} | {pi} |")
    L += ["\n## Alertas para o coordenador\n"] + ([f"- {v}: {al} (chamada {i})" for i, v, al in alertas] or ["- nenhum"])
    L += ["\n## Top 15 leads por interesse\n", "| Telefone | Classificação | Interesse | Cidade | Votos família | Próximo passo | Resumo |", "|---|---|---|---|---|---|---|"]
    for l in [x for x in leads if x["interesse"] is not None][:15]:
        L.append(f"| {l['telefone']} | {l['classificacao']} | {l['interesse']} | {l['cidade'] or '—'} | {l['votos_familia'] or '—'} | {l['proximo_passo'] or '—'} | {(l['resumo'] or '')[:120]} |")
    (wd / "RELATORIO.md").write_text("\n".join(L), encoding="utf-8")
    print(f"leads: {len(leads)} | analises: {len(analises)} | vendedores: {len(rows)} → RELATORIO.md, leads_classificados.csv, vendedores.csv")

if __name__ == "__main__":
    main()
