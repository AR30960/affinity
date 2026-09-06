import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "affinity.db")
JSON_PATH = os.path.join(BASE_DIR, "mdb_data.json")

def import_data():
    with open(JSON_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print(">>> Nettoyage et préparation de la base SQLite...")
    # On vide les anciennes données pour injecter la vraie base Access
    c.execute("DELETE FROM answers")
    c.execute("DELETE FROM questions")
    c.execute("DELETE FROM question_packs")
    c.execute("DELETE FROM identity_cards")
    c.execute("DELETE FROM profiles")

    # 1. Import des Packs (T_JEU)
    print(">>> Import des jeux (T_JEU)...")
    for j in data.get("T_JEU", []):
        c.execute("""
            INSERT INTO question_packs (id, code, nom, description)
            VALUES (?, ?, ?, ?)
        """, (j["N_JEU"], f"JEU_{j['N_JEU']}", j["LB_JEU"], "Jeu extrait de la base Microsoft Access Affinity.mdb"))

    # 2. Dictionnaire Thématiques & Sujets
    themas = {r["N_THEMA"]: r["LB_THEMA"] for r in data.get("T_THEMA", [])}
    sujets = {(r["N_THEMA"], r["N_SUJET"]): r["LB_SUJET"] for r in data.get("T_SUJET", [])}

    # 3. Import des 108 Questions (T_QUEST)
    print(">>> Import des 108 questions officielles (T_QUEST)...")
    questions_list = data.get("T_QUEST", [])
    for q in questions_list:
        th_label = themas.get(q["N_THEMA"], f"Thématique {q['N_THEMA']}")
        suj_label = sujets.get((q["N_THEMA"], q["N_SUJET"]), f"Sujet {q['N_SUJET']}")
        
        # Déterminer le type: si la thématique est 'Gouts' ou Sujet 'Couleurs', ou MULTI V-A-D-P
        q_type = "MULTI"
        if q["N_THEMA"] == 1: # Gouts / Couleurs
            q_type = "G"

        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["N_QUEST"],
            q["N_JEU"],
            q.get("N_TYPE", 0),
            q.get("N_CLASSE", 1),
            th_label,
            suj_label,
            q_type,
            q["LB_QUEST"]
        ))
    print(f"    -> {len(questions_list)} questions insérées.")

    # 4. Import des Profils (T_PRF)
    print(">>> Import des profils (T_PRF)...")
    prfs = data.get("T_PRF", [])
    for p in prfs:
        pid = p["N_PRF"]
        pseudo = p["LB_PRF"]
        c.execute("INSERT INTO profiles (id, pseudo, avatar) VALUES (?, ?, ?)", (pid, pseudo, pseudo[:2].upper()))
        
        # Fiche d'identité pré-remplie pour que le calcul soit immédiatement disponible
        prenom = "Alexandre" if pid == 1 else "Camille"
        nom = "Testeur 1" if pid == 1 else "Testeuse 2"
        sexe = 1 if pid == 1 else 2
        ville = "Paris" if pid == 1 else "Lyon"
        c.execute("""
            INSERT INTO identity_cards (profile_id, nom, prenom, sexe, ville, statut, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pid, nom, prenom, sexe, ville, "Profil Access", "Données importées depuis Affinity.mdb"))
    print(f"    -> {len(prfs)} profils créés avec leurs fiches d'identité.")

    # 5. Import des Réponses (M_REP)
    print(">>> Import des réponses (M_REP)...")
    m_rep = data.get("M_REP", [])
    count_ans = 0
    for r in m_rep:
        pid = r["N_PRF"]
        qid = r["N_QUEST"]
        
        # Axes V, A, D, P
        for axis, col in [("V", "N_REPV"), ("A", "N_REPA"), ("D", "N_REPD"), ("P", "N_REPP")]:
            val = r.get(col, 0)
            if val is not None and val > 0:
                c.execute("""
                    INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value)
                    VALUES (?, ?, ?, ?)
                """, (pid, qid, axis, val))
                count_ans += 1
                
        # Pour les questions de type 'G', mapper la valeur si présente (ex: A ou D)
        if qid in [q["N_QUEST"] for q in questions_list if q["N_THEMA"] == 1]:
            val_g = r.get("N_REPA") or r.get("N_REPV") or 3
            c.execute("""
                INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value)
                VALUES (?, ?, 'G', ?)
            """, (pid, qid, val_g))
            count_ans += 1

    print(f"    -> {count_ans} points de réponses enregistrés.")

    conn.commit()
    conn.close()
    print("\n>>> SUCCÈS : TOUTES LES QUESTIONS ET DONNÉES D'AFFINITY.MDB SONT DANS L'APPLICATION ! <<<")

if __name__ == "__main__":
    import_data()
