import sqlite3
import os
import sys
from server import init_db, get_db, calculate_affinity

def run_tests():
    print(">>> 1. Initialisation d'une base de test temporaire dédiée...")
    test_db_path = "test_affinity_temp.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
        
    conn = sqlite3.connect(test_db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Copie du schéma de base
    main_conn = get_db()
    schema = "\n".join(line for line in main_conn.iterdump() if "CREATE TABLE" in line or "CREATE INDEX" in line or "INSERT INTO" in line)
    main_conn.close()
    conn.executescript(schema)
    
    c.execute("SELECT COUNT(*) as cnt FROM questions")
    nb_q = c.fetchone()["cnt"]
    print(f"    Questions initiales en base : {nb_q}")
    assert nb_q > 0, "Aucune question créée"
    
    print("\n>>> 2. Création de deux profils tests (Alex et Camille)...")
    c.execute("DELETE FROM answers")
    c.execute("DELETE FROM identity_cards")
    c.execute("DELETE FROM profiles")
    conn.commit()
    
    c.execute("INSERT INTO profiles (pseudo, avatar) VALUES ('Alex', 'alex')")
    id_alex = c.lastrowid
    c.execute("INSERT INTO identity_cards (profile_id) VALUES (?)", (id_alex,))
    
    c.execute("INSERT INTO profiles (pseudo, avatar) VALUES ('Camille', 'camille')")
    id_camille = c.lastrowid
    c.execute("INSERT INTO identity_cards (profile_id) VALUES (?)", (id_camille,))
    conn.commit()
    
    print(f"    Alex ID = {id_alex}, Camille ID = {id_camille}")
    
    print("\n>>> 3. Test de la règle d'or : Fiche d'identité obligatoire pour calculer...")
    res = calculate_affinity(id_alex, id_camille)
    assert res.get("error") == "FICHE_MANQUANTE", f"Devrait bloquer si fiches vides : {res}"
    print("    [OK] Le calcul a bien été bloqué car les fiches d'identité sont incomplètes.")
    
    print("\n>>> 4. Renseignement des fiches d'identité...")
    c.execute("""
        UPDATE identity_cards 
        SET prenom = 'Alexandre', nom = 'Dubois', sexe = 1, ville = 'Paris', statut = 'Célibataire'
        WHERE profile_id = ?
    """, (id_alex,))
    c.execute("""
        UPDATE identity_cards 
        SET prenom = 'Camille', nom = 'Laurent', sexe = 2, ville = 'Lyon', statut = 'Célibataire'
        WHERE profile_id = ?
    """, (id_camille,))
    conn.commit()
    print("    [OK] Fiches d'Alex et Camille complétées.")
    
    print("\n>>> 5. Saisie de réponses concordantes et complémentaires...")
    # Question 1: Sport (MULTI)
    # Alex: V=4, A=5, D=4, P=5 (très sportif, veut continuer et veut partager)
    # Camille: V=3, A=4, D=5, P=4 (sportive, veut découvrir plus et aime partager) -> Super synergie !
    c.execute("SELECT id FROM questions WHERE sujet = 'Sport'")
    q_sport = c.fetchone()["id"]
    for axis, val in [("V", 4), ("A", 5), ("D", 4), ("P", 5)]:
        c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, ?, ?)", (id_alex, q_sport, axis, val))
    for axis, val in [("V", 3), ("A", 4), ("D", 5), ("P", 4)]:
        c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, ?, ?)", (id_camille, q_sport, axis, val))
        
    # Question 2: Gastronomie (G)
    # Alex: 4 (Passionnément), Camille: 5 (À la folie) -> Forte concordance
    c.execute("SELECT id FROM questions WHERE sujet = 'Gastronomie'")
    q_gastro = c.fetchone()["id"]
    c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, 'G', 4)", (id_alex, q_gastro))
    c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, 'G', 5)", (id_camille, q_gastro))

    # Question 3: Fêtes & Sorties (G)
    # Alex: 2 (Moyennement), Camille: 2 (Moyennement) -> Parfaite égalité
    c.execute("SELECT id FROM questions WHERE sujet = 'Fêtes & Sorties'")
    q_fete = c.fetchone()["id"]
    c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, 'G', 2)", (id_alex, q_fete))
    c.execute("INSERT INTO answers (profile_id, question_id, axis, value) VALUES (?, ?, 'G', 2)", (id_camille, q_fete))

    conn.commit()
    conn.close()
    
    print("\n>>> 6. Calcul de l'affinité entre Alex et Camille...")
    result = calculate_affinity(id_alex, id_camille)
    print(f"    Score Global : {result['score_global']}%")
    print(f"    Détail Thématiques : {result['thematiques']}")
    print(f"    Détail Axes : {result['axes']}")
    print(f"    Points de fusion : {[p['sujet'] for p in result['points_de_fusion']]}")
    
    assert result["score_global"] >= 80, f"Le score devrait être élevé (>80%), obtenu : {result['score_global']}"
    assert "Activités" in result["thematiques"]
    assert "Goûts" in result["thematiques"]
    print("\n>>> TOUS LES TESTS SONT VALIDES AVEC SUCCÈS ! <<<")

if __name__ == "__main__":
    run_tests()
