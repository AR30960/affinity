import sqlite3
import random

def populate():
    conn = sqlite3.connect('affinity.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    print(">>> Mise à jour des profils avec des identifiants clairs...")
    # Profil 1 : Alexandre
    c.execute("""
        UPDATE profiles SET pseudo = 'Alexandre', avatar = 'AL' WHERE id = 1
    """)
    c.execute("""
        UPDATE identity_cards SET
            prenom = 'Alexandre',
            nom = 'Roger',
            sexe = 1,
            date_naissance = '1990-06-15',
            ville = 'Paris',
            statut = 'Célibataire',
            bio = 'Passionné de voyages, de sport et de découvertes culinaires.'
        WHERE profile_id = 1
    """)

    # Profil 2 : Camille
    c.execute("""
        UPDATE profiles SET pseudo = 'Camille', avatar = 'CA' WHERE id = 2
    """)
    c.execute("""
        UPDATE identity_cards SET
            prenom = 'Camille',
            nom = 'Laurent',
            sexe = 2,
            date_naissance = '1992-09-22',
            ville = 'Lyon',
            statut = 'Célibataire',
            bio = 'Adore la lecture, les sorties entre amis et les projets à deux.'
        WHERE profile_id = 2
    """)

    # Profil 3 : Sophie (pour avoir du choix)
    c.execute("INSERT OR IGNORE INTO profiles (id, pseudo, avatar) VALUES (3, 'Sophie', 'SO')")
    c.execute("""
        INSERT OR REPLACE INTO identity_cards (profile_id, nom, prenom, sexe, ville, statut, bio)
        VALUES (3, 'Martin', 'Sophie', 2, 'Bordeaux', 'Célibataire', 'Créative, dynamique, aime la musique et l''art.')
    """)

    # Profil 4 : Maxime
    c.execute("INSERT OR IGNORE INTO profiles (id, pseudo, avatar) VALUES (4, 'Maxime', 'MA')")
    c.execute("""
        INSERT OR REPLACE INTO identity_cards (profile_id, nom, prenom, sexe, ville, statut, bio)
        VALUES (4, 'Dubois', 'Maxime', 1, 'Nantes', 'En recherche', 'Calme, réfléchi, passionné de technologie et de randonnée.')
    """)

    # Récupérer toutes les 108 questions
    c.execute("SELECT id, thematique, sujet, type, texte FROM questions")
    questions = c.fetchall()

    print(f">>> Génération de réponses cohérentes sur les {len(questions)} questions...")
    
    # On vide les réponses pour générer un jeu de données riche et harmonieux
    c.execute("DELETE FROM answers")

    # Réponses thématiques prédéterminées pour Alexandre (P1) et Camille (P2)
    # afin de créer une très belle synergie d'affinité élective (~86%)
    random.seed(42)

    for q in questions:
        qid = q["id"]
        th = q["thematique"]
        qtype = q["type"]

        # 1. Alexandre (P1)
        if qtype == "G":
            # Goûts : 1 à 5
            base_g1 = random.choice([3, 4, 5]) if th in ["Gouts", "Divertissements & Loisirs"] else random.choice([2, 3, 4])
            c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (1, ?, 'G', ?)", (qid, base_g1))
            
            # Camille (P2) : proche avec légères nuances
            base_g2 = max(1, min(5, base_g1 + random.choice([-1, 0, 1])))
            c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (2, ?, 'G', ?)", (qid, base_g2))
            
        else: # MULTI (V, A, D, P)
            # Alexandre (P1)
            v1 = random.choice([2, 3, 4, 5])
            a1 = random.choice([2, 3, 4, 5])
            d1 = random.choice([3, 4, 5]) # envie de découvrir
            p1 = random.choice([3, 4, 5]) # envie de partager

            for ax, val in [("V", v1), ("A", a1), ("D", d1), ("P", p1)]:
                c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (1, ?, ?, ?)", (qid, ax, val))

            # Camille (P2) : harmonie avec P1
            v2 = max(1, min(5, v1 + random.choice([-1, 0, 1])))
            a2 = max(1, min(5, a1 + random.choice([-1, 0, 1])))
            d2 = random.choice([3, 4, 5])
            p2 = random.choice([3, 4, 5])

            for ax, val in [("V", v2), ("A", a2), ("D", d2), ("P", p2)]:
                c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (2, ?, ?, ?)", (qid, ax, val))

    c.execute("SELECT COUNT(*) as count FROM answers")
    total_answers = c.fetchone()["count"]
    print(f"    -> Total réponses enregistrées : {total_answers}")

    conn.commit()
    conn.close()
    print(">>> DONNÉES ENRICHIES AVEC SUCCÈS ! <<<")

if __name__ == '__main__':
    populate()
