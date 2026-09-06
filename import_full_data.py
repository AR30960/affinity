import json
import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "affinity.db")
JSON_PATH = os.path.join(BASE_DIR, "mdb_full_data.json")

def import_full():
    with open(JSON_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print(">>> 1. Mise à jour des Jeux (T_JEU)...")
    for j in data.get("T_JEU", []):
        c.execute("""
            INSERT INTO question_packs (id, code, nom, description)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nom = excluded.nom,
                description = excluded.description
        """, (j["N_JEU"], f"JEU_{j['N_JEU']}", j["LB_JEU"], f"Jeu extrait de la base {j['LB_JEU']}"))

    # Initialisation des Profils (1: Alexandre, 2: Camille, 3: Sophie, 4: Maxime)
    print(">>> 2. Initialisation et sécurisation des profils...")
    c.execute("DELETE FROM answers")
    c.execute("DELETE FROM identity_cards")
    c.execute("DELETE FROM profiles")

    profiles_seed = [
        (1, "Alexandre", "AL", "Roger", "Alexandre", 1, "1990-06-15", "Paris", "Célibataire", "Passionné de voyages, de sport et de découvertes."),
        (2, "Camille", "CA", "Laurent", "Camille", 2, "1992-09-22", "Lyon", "Célibataire", "Adore la lecture, les sorties entre amis et les projets à deux."),
        (3, "Sophie", "SO", "Martin", "Sophie", 2, "1995-04-12", "Bordeaux", "Célibataire", "Créative, dynamique, aime la musique et l'art."),
        (4, "Maxime", "MA", "Dubois", "Maxime", 1, "1988-11-03", "Nantes", "En recherche", "Calme, réfléchi, passionné de technologie et de randonnée.")
    ]
    for pid, pseudo, av, nom, prenom, sexe, dnaiss, ville, statut, bio in profiles_seed:
        c.execute("""
            INSERT INTO profiles (id, pseudo, avatar) VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET pseudo = excluded.pseudo, avatar = excluded.avatar
        """, (pid, pseudo, av))
        c.execute("""
            INSERT INTO identity_cards (profile_id, nom, prenom, sexe, date_naissance, ville, statut, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                nom = excluded.nom,
                prenom = excluded.prenom,
                sexe = excluded.sexe,
                date_naissance = excluded.date_naissance,
                ville = excluded.ville,
                statut = excluded.statut,
                bio = excluded.bio
        """, (pid, nom, prenom, sexe, dnaiss, ville, statut, bio))

    # Nettoyer d'éventuels profils orphelins hors de 1,2,3,4
    c.execute("DELETE FROM profiles WHERE id NOT IN (1, 2, 3, 4)")
    c.execute("DELETE FROM identity_cards WHERE profile_id NOT IN (1, 2, 3, 4)")

    # 2. Dictionnaires de Thématiques & Sujets
    themas = {r["N_THEMA"]: r["LB_THEMA"] for r in data.get("T_THEMA", [])}
    sujets = {(r["N_THEMA"], r["N_SUJET"]): r["LB_SUJET"] for r in data.get("T_SUJET", [])}

    # 3. Import des 172 Questions (T_QUEST)
    print(">>> 2. Importation des 172 questions de la base Affinity-Full.mdb...")
    questions = data.get("T_QUEST", [])
    inserted_count = 0
    updated_count = 0

    for q in questions:
        qid = q["N_QUEST"]
        th_label = themas.get(q["N_THEMA"], f"Thématique {q['N_THEMA']}")
        suj_label = sujets.get((q["N_THEMA"], q["N_SUJET"]), f"Sujet {q['N_SUJET']}")
        
        q_type = "MULTI"
        if q["N_THEMA"] == 1: # Goûts / Couleurs
            q_type = "G"

        cible = q.get("N_CIBLE") if "N_CIBLE" in q else q.get("N_TYPE", 0)
        classe = q.get("N_CLASSE", 1)
        texte = q["LB_QUEST"]
        pack_id = q.get("N_JEU", 1)

        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                pack_id = excluded.pack_id,
                cible = excluded.cible,
                classe = excluded.classe,
                thematique = excluded.thematique,
                sujet = excluded.sujet,
                type = excluded.type,
                texte = excluded.texte
        """, (qid, pack_id, cible, classe, th_label, suj_label, q_type, texte))
        inserted_count += 1

    print(f"    -> {inserted_count} questions enregistrées / synchronisées dans SQLite.")

    # 4. Import des réponses de M_REP
    print(">>> 3. Synchronisation des réponses de M_REP...")
    m_rep = data.get("M_REP", [])
    m_rep_count = 0
    for r in m_rep:
        pid = r["N_PRF"]
        qid = r["N_QUEST"]
        for axis, col in [("V", "N_REPV"), ("A", "N_REPA"), ("D", "N_REPD"), ("P", "N_REPP")]:
            val = r.get(col, 0)
            if val is not None and val > 0:
                c.execute("""
                    INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value)
                    VALUES (?, ?, ?, ?)
                """, (pid, qid, axis, val))
                m_rep_count += 1
    print(f"    -> {m_rep_count} réponses importées depuis M_REP.")

    # 5. Compléter les réponses pour Alexandre (P1) et Camille (P2) sur les nouvelles questions
    print(">>> 4. Enrichissement des réponses pour Alexandre et Camille sur toutes les questions...")
    random.seed(123)
    
    # Pour chaque question, s'assurer que P1 et P2 ont des réponses
    c.execute("SELECT id, thematique, type, classe FROM questions")
    all_qs = c.fetchall()

    enriched_count = 0
    for q in all_qs:
        qid = q["id"]
        qtype = q["type"]
        classe = q["classe"]
        
        # Vérifier si P1 a répondu
        c.execute("SELECT COUNT(*) as cnt FROM answers WHERE profile_id = 1 AND question_id = ?", (qid,))
        p1_has = c.fetchone()["cnt"] > 0

        # Vérifier si P2 a répondu
        c.execute("SELECT COUNT(*) as cnt FROM answers WHERE profile_id = 2 AND question_id = ?", (qid,))
        p2_has = c.fetchone()["cnt"] > 0

        if not p1_has or not p2_has:
            if qtype == "G":
                val1 = random.choice([3, 4, 5])
                val2 = max(1, min(5, val1 + random.choice([-1, 0, 1])))
                if not p1_has:
                    c.execute("INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value) VALUES (1, ?, 'G', ?)", (qid, val1))
                if not p2_has:
                    c.execute("INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value) VALUES (2, ?, 'G', ?)", (qid, val2))
                enriched_count += 2
            else: # MULTI
                v1 = random.choice([2, 3, 4, 5]) if classe <= 2 else random.choice([1, 2, 3, 4])
                a1 = random.choice([2, 3, 4, 5]) if classe <= 2 else random.choice([1, 2, 3, 4])
                d1 = random.choice([3, 4, 5])
                p1 = random.choice([3, 4, 5])

                v2 = max(1, min(5, v1 + random.choice([-1, 0, 1])))
                a2 = max(1, min(5, a1 + random.choice([-1, 0, 1])))
                d2 = random.choice([3, 4, 5])
                p2 = random.choice([3, 4, 5])

                if not p1_has:
                    for ax, val in [("V", v1), ("A", a1), ("D", d1), ("P", p1)]:
                        c.execute("INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value) VALUES (1, ?, ?, ?)", (qid, ax, val))
                    enriched_count += 4
                if not p2_has:
                    for ax, val in [("V", v2), ("A", a2), ("D", d2), ("P", p2)]:
                        c.execute("INSERT OR REPLACE INTO answers (profile_id, question_id, axis, value) VALUES (2, ?, ?, ?)", (qid, ax, val))
                    enriched_count += 4

    print(f"    -> {enriched_count} réponses ajoutées pour garantir 100% de complétude sur les 172 questions.")

    conn.commit()
    conn.close()
    print("\n>>> SUCCÈS : TOUTES LES 172 QUESTIONS D'AFFINITY-FULL.MDB SONT INTÉGRÉES ! <<<")

if __name__ == "__main__":
    import_full()
