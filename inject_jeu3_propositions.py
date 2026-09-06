# -*- coding: utf-8 -*-
import sqlite3
from generate_jeu3_questions import QUESTIONS_CLASSE_5, QUESTIONS_CLASSE_9

def inject_propositions():
    conn = sqlite3.connect('affinity.db')
    c = conn.cursor()

    # 1. Vérifier / Créer le Pack 3
    c.execute("""
        INSERT OR IGNORE INTO question_packs (id, code, nom, description)
        VALUES (3, 'JEU_3', 'Jeu 3', 'Jeu 3 - Intimité, sensualité et explorations avancées')
    """)
    conn.commit()
    print("Pack 3 (JEU_3) vérifié/créé dans question_packs.")

    # 2. Vérifier la colonne status dans questions
    cols = [col[1] for col in c.execute("PRAGMA table_info(questions)").fetchall()]
    if 'status' not in cols:
        print("Ajout de la colonne 'status' dans la table questions...")
        c.execute("ALTER TABLE questions ADD COLUMN status TEXT DEFAULT 'validated'")
        conn.commit()

    # S'assurer que les questions existantes sont bien 'validated'
    c.execute("UPDATE questions SET status = 'validated' WHERE status IS NULL OR status = ''")
    conn.commit()

    # 3. Nettoyer d'éventuelles propositions Jeu 3 précédentes pour idempotence
    c.execute("DELETE FROM questions WHERE pack_id = 3 AND status = 'pending_review'")
    conn.commit()

    # 4. Injection des 100 questions de Classe 5
    # IDs 50001 à 50100
    id_start_5 = 50001
    inserted_5 = 0
    for i, (cible, thematique, sujet, qtype, texte) in enumerate(QUESTIONS_CLASSE_5):
        qid = id_start_5 + i
        # Mapper n_sujet selon le sujet
        sujet_map = {"Pratiques": 1, "Désir": 2, "Communication": 3, "Sensualité": 4, "Rythme": 5}
        n_sujet = sujet_map.get(sujet, 1)
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, status)
            VALUES (?, 3, ?, 5, ?, ?, ?, ?, 9, ?, 'pending_review')
        """, (qid, cible, thematique, sujet, qtype, texte, n_sujet))
        inserted_5 += 1

    # 5. Injection des 50 questions de Classe 9
    # IDs 90001 à 90050
    id_start_9 = 90001
    inserted_9 = 0
    for i, (cible, thematique, sujet, qtype, texte) in enumerate(QUESTIONS_CLASSE_9):
        qid = id_start_9 + i
        sujet_map = {"Fantasmes": 1, "Partenaires": 2, "Limites": 3}
        n_sujet = sujet_map.get(sujet, 1)
        c.execute("""
            INSERT INTO questions (id, pack_id, cible, classe, thematique, sujet, type, texte, n_thema, n_sujet, status)
            VALUES (?, 3, ?, 9, ?, ?, ?, ?, 9, ?, 'pending_review')
        """, (qid, cible, thematique, sujet, qtype, texte, n_sujet))
        inserted_9 += 1

    conn.commit()
    conn.close()

    print(f"Succès : {inserted_5} questions Classe 5 et {inserted_9} questions Classe 9 injectées avec le statut 'pending_review' dans le Pack 3 !")

if __name__ == "__main__":
    inject_propositions()
