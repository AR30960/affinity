import json
import sqlite3
import os

DB_PATH = "affinity.db"
JSON_PATH = "mdb_data.json"

def inspect_and_import():
    with open(JSON_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    
    print("=== TABLES CHARGEES DEPUIS AFFINITY.MDB ===")
    for k in sorted(data.keys()):
        print(f" - {k}: {len(data[k])} enregistrements")
        
    print("\n--- THÉMATIQUES ---")
    themas = {r["N_THEMA"]: r["LB_THEMA"] for r in data.get("T_THEMA", [])}
    for n, lb in sorted(themas.items()):
        print(f" [{n}] {lb}")

    print("\n--- SUJETS ---")
    sujets = {(r["N_THEMA"], r["N_SUJET"]): r["LB_SUJET"] for r in data.get("T_SUJET", [])}
    for (nth, ns), lb in sorted(sujets.items()):
        print(f" Thématique [{nth} - {themas.get(nth, '?')}] / Sujet [{ns}] : {lb}")

    print("\n--- CLASSES ---")
    classes = {r["N_CLASSE"]: r["LB_CLASSE"] for r in data.get("T_CLASSE", [])}
    for n, lb in sorted(classes.items()):
        print(f" Classe [{n}] : {lb}")

    print("\n--- TYPES / CIBLES ---")
    cibles = {r["N_TYPE"]: r["LB_TYPE"] for r in data.get("T_TYPE", [])}
    for n, lb in sorted(cibles.items()):
        print(f" Cible [{n}] : {lb}")

    print(f"\n--- QUESTIONS (TOTAL: {len(data.get('T_QUEST', []))}) ---")
    for q in data.get("T_QUEST", [])[:8]:
        th_name = themas.get(q["N_THEMA"], f"Théma {q['N_THEMA']}")
        suj_name = sujets.get((q["N_THEMA"], q["N_SUJET"]), f"Sujet {q['N_SUJET']}")
        print(f" #{q['N_QUEST']} [{th_name} > {suj_name}] (Classe {q['N_CLASSE']}) : {q['LB_QUEST']}")

    print(f"\n--- PROFILS EXISTANTS (T_PRF) ---")
    for p in data.get("T_PRF", []):
        print(f" Profil ID={p['N_PRF']}, Libellé={p['LB_PRF']}")

    print(f"\n--- RÉPONSES EXISTANTES (M_REP : {len(data.get('M_REP', []))}) ---")
    for r in data.get("M_REP", [])[:6]:
        print(f" Profil {r['N_PRF']} -> Question #{r['N_QUEST']} : V={r['N_REPV']}, A={r['N_REPA']}, D={r['N_REPD']}, P={r['N_REPP']}")

if __name__ == "__main__":
    inspect_and_import()
