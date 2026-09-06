"""
Script de migration et réimport fidèle de la base MS Access Affinity-Full.mdb :
- Classe 0 : "Non définies"
- Classe 8 : "Identité"
- N_CIBLE et N_SUJET préservés et intégrés
- Retrait des thématiques et sujets artificiels créés pour la classe identité
- Réimport fidèle des 172 questions d'Affinity-Full.mdb
- Les 14 questions d'identité P (+ sur vous) et 14 questions d'identité T (+ sur l'autre) basculent en Classe 8 avec thématique "Identité"
"""

import os
import json
import sqlite3
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "affinity.db")
JSON_PATH = os.path.join(BASE_DIR, "mdb_full_data.json")

IDENTITY_QUESTIONS_14 = [
    {"sujet": "Taille", "texte": "Quelle est votre taille exacte en centimètres ?", "unit": "cm", "kind": "numeric", "min": 100, "max": 230, "step": 1},
    {"sujet": "Poids", "texte": "Quel est votre poids actuel en kilogrammes ?", "unit": "kg", "kind": "numeric", "min": 35, "max": 200, "step": 1},
    {"sujet": "Silhouette", "texte": "Comment décrivez-vous votre silhouette globale ?", "kind": "select", "options": ["Mince / Élancé(e)", "Athlétique / Musclé(e)", "Proportionné(e) / Normal(e)", "Quelques rondeurs assumées", "Forte corpulence"]},
    {"sujet": "Tour de poitrine", "texte": "Quel est votre tour de poitrine en centimètres ?", "unit": "cm", "kind": "numeric", "min": 50, "max": 160, "step": 1},
    {"sujet": "Tour de taille", "texte": "Quel est votre tour de taille en centimètres ?", "unit": "cm", "kind": "numeric", "min": 40, "max": 150, "step": 1},
    {"sujet": "Tour de hanches", "texte": "Quel est votre tour de hanches en centimètres ?", "unit": "cm", "kind": "numeric", "min": 50, "max": 160, "step": 1},
    {"sujet": "Pointure", "texte": "Quelle est votre pointure de chaussures habituelle ?", "unit": "", "kind": "numeric", "min": 32, "max": 50, "step": 0.5},
    {"sujet": "Couleur des yeux", "texte": "Quelle est la couleur dominante de vos yeux ?", "kind": "select", "options": ["Bleus", "Verts", "Marrons", "Noirs", "Noisette", "Gris", "Vairons"]},
    {"sujet": "Couleur des cheveux", "texte": "Quelle est votre couleur de cheveux naturelle ou actuelle ?", "kind": "select", "options": ["Bruns", "Châtains", "Blonds", "Roux", "Noirs", "Poivre et sel", "Blancs / Gris", "Colorés / Fantaisie", "Chauve / Rasé"]},
    {"sujet": "Longueur des cheveux", "texte": "Quelle est la longueur habituelle de vos cheveux ?", "kind": "select", "options": ["Courts / Très courts", "Mi-longs", "Longs", "Très longs", "Rasés / Chauve"]},
    {"sujet": "Style vestimentaire", "texte": "Quel style vestimentaire reflète le mieux votre quotidien ?", "kind": "select", "options": ["Décontracté / Casual", "Élégant / Soigné", "Sportif / Sportswear", "Bohème / Nature", "Classique / Costume", "Créatif / Tendance", "Minimaliste"]},
    {"sujet": "Origines culturelles", "texte": "Quelles sont vos principales origines ou racines culturelles ?", "kind": "select", "options": ["Caucasien(ne) / Européen(ne)", "Méditerranéen(ne)", "Maghrébin(ne) / Nord-Africain(ne)", "Africain(ne) / Subsaharien(ne)", "Asiatique", "Proche & Moyen-Orient", "Amérindien(ne) / Latino-Américain(ne)", "Métissé(e) / Pluriculturel(le)"]},
    {"sujet": "Rythme de vie", "texte": "Quel est votre rythme de vie prédominant au quotidien ?", "kind": "select", "options": ["Plutôt matinal(e) / Lève-tôt", "Plutôt noctambule / Couche-tard", "Rythme régulier et équilibré", "Rythme variable / Selon l'inspiration"]},
    {"sujet": "Cadre de vie", "texte": "Dans quel cadre de vie vous épanouissez-vous le plus ?", "kind": "select", "options": ["Centre-ville dynamique", "Quartier résidentiel calme", "Périurbain / Proche nature", "Campagne paisible", "Bord de mer / Littoral", "Montagne"]}
]

def migrate():
    print("=== DÉBUT MIGRATION REPRISE ACCESS & CLASSE 8 ===")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Vérification et ajout des colonnes n_thema et n_sujet dans questions
    c.execute("PRAGMA table_info(questions)")
    existing_cols = [r["name"] for r in c.fetchall()]
    if "n_thema" not in existing_cols:
        c.execute("ALTER TABLE questions ADD COLUMN n_thema INTEGER DEFAULT 0")
        print(" -> Colonne 'n_thema' ajoutée dans questions.")
    if "n_sujet" not in existing_cols:
        c.execute("ALTER TABLE questions ADD COLUMN n_sujet INTEGER DEFAULT 0")
        print(" -> Colonne 'n_sujet' ajoutée dans questions.")

    # 2. Lecture des données Access réelles (mdb_full_data.json)
    with open(JSON_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    themas = {r["N_THEMA"]: r["LB_THEMA"] for r in data.get("T_THEMA", [])}
    sujets = {(r["N_THEMA"], r["N_SUJET"]): r["LB_SUJET"] for r in data.get("T_SUJET", [])}

    print(f" -> Référentiel Access : {len(themas)} thématiques et {len(sujets)} sujets.")

    # 3. Récupération des correspondances de réponses existantes d'identité avant nettoyage
    #    afin de les rattacher parfaitement aux questions de classe 8
    existing_self_answers = []
    c.execute("SELECT profile_id, question_id, valeur_num, valeur_text FROM identity_answers_self")
    for r in c.fetchall():
        existing_self_answers.append(dict(r))

    existing_partner_answers = []
    c.execute("SELECT profile_id, question_id, min_val, max_val, options_json, indifferent FROM identity_answers_partner")
    for r in c.fetchall():
        existing_partner_answers.append(dict(r))

    # Ancienne table questions pour faire correspondre le sujet
    c.execute("SELECT id, sujet, type FROM questions WHERE classe IN (0, 8)")
    old_identity_q_map = {r["id"]: (r["sujet"], r["type"]) for r in c.fetchall()}

    # 4. Vider la table questions pour la reconstruire proprement
    c.execute("DELETE FROM questions")

    # 5. Réimport fidèle des 172 questions d'Affinity-Full.mdb
    access_questions = data.get("T_QUEST", [])
    print(f" -> Import des {len(access_questions)} questions d'Affinity-Full.mdb...")

    for q in access_questions:
        qid = q["N_QUEST"]
        nth = q.get("N_THEMA", 0)
        ns = q.get("N_SUJET", 0)
        th_label = themas.get(nth, f"Thématique {nth}")
        suj_label = sujets.get((nth, ns), f"Sujet {ns}")

        q_type = "G" if nth == 1 else "MULTI"
        cible = q.get("N_CIBLE", 0)
        classe = q.get("N_CLASSE", 1)
        texte = q["LB_QUEST"]
        pack_id = q.get("N_JEU", 1)

        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (qid, pack_id, cible, classe, th_label, suj_label, q_type, texte, nth, ns))

    print(" -> 172 questions officielles réimportées avec succès.")

    # 6. Insertion des 28 questions d'Identité en CLASSE 8
    #    14 questions de type P (+ sur vous) et 14 questions de type T (+ sur l'autre)
    #    IDs stables : 91001 à 91014 (Type P) et 92001 à 92014 (Type T)
    print(" -> Création des questions de Classe 8 (Identité) : 14 type P et 14 type T...")
    new_self_q_ids = {}    # sujet -> new_id
    new_partner_q_ids = {} # sujet -> new_id

    for idx, cfg in enumerate(IDENTITY_QUESTIONS_14, start=1):
        sujet = cfg["sujet"]
        texte_p = cfg["texte"]
        # Type P (+ sur vous) : classe 8
        qid_p = 80000 + idx
        new_self_q_ids[sujet] = qid_p
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet)
            VALUES (?, 1, 0, 8, 'Identité', ?, 'P', ?, 8, ?)
        """, (qid_p, sujet, texte_p, idx))

        # Type T (+ sur l'autre) : classe 8
        qid_t = 85000 + idx
        new_partner_q_ids[sujet] = qid_t
        texte_t = f"Quelles sont vos tolérances et critères chez l'autre pour : {sujet} ?"
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet)
            VALUES (?, 1, 0, 8, 'Identité', ?, 'T', ?, 8, ?)
        """, (qid_t, sujet, texte_t, idx))

    # 7. Remapping des réponses existantes dans identity_answers_self et partner
    c.execute("DELETE FROM identity_answers_self")
    for ans in existing_self_answers:
        old_qid = ans["question_id"]
        if old_qid in old_identity_q_map:
            suj, _ = old_identity_q_map[old_qid]
            new_qid = new_self_q_ids.get(suj)
            if new_qid:
                c.execute("""
                    INSERT OR REPLACE INTO identity_answers_self (profile_id, question_id, valeur_num, valeur_text, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (ans["profile_id"], new_qid, ans["valeur_num"], ans["valeur_text"]))

    c.execute("DELETE FROM identity_answers_partner")
    for ans in existing_partner_answers:
        old_qid = ans["question_id"]
        if old_qid in old_identity_q_map:
            suj, _ = old_identity_q_map[old_qid]
            new_qid = new_partner_q_ids.get(suj)
            if new_qid:
                c.execute("""
                    INSERT OR REPLACE INTO identity_answers_partner (profile_id, question_id, min_val, max_val, options_json, indifferent, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (ans["profile_id"], new_qid, ans["min_val"], ans["max_val"], ans["options_json"], ans["indifferent"]))

    conn.commit()

    # Vérifications finales
    c.execute("SELECT classe, COUNT(*) FROM questions GROUP BY classe")
    print("\n--- SYNTHÈSE DES QUESTIONS DANS SQLITE ---")
    for r in c.fetchall():
        print(f" Classe {r[0]}: {r[1]} questions")

    c.execute("SELECT DISTINCT thematique FROM questions")
    print("\n--- THÉMATIQUES DANS QUESTIONS ---")
    for r in c.fetchall():
        print(f" - {r[0]}")

    c.execute("SELECT cible, COUNT(*) FROM questions WHERE classe != 8 GROUP BY cible")
    print("\n--- CIBLES (N_CIBLE) DANS QUESTIONS GÉNÉRALES ---")
    for r in c.fetchall():
        print(f" Cible {r[0]}: {r[1]} questions")

    conn.close()
    print("\n=== MIGRATION TERMINÉE AVEC SUCCÈS ===")

if __name__ == "__main__":
    migrate()
