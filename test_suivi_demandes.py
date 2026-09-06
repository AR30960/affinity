# -*- coding: utf-8 -*-
"""
Tests automatisés des fonctionnalités demandées dans Suivi-ARP001 :
1. Calcul automatique de l'âge et vérification de cohérence (<18 ans, futur)
2. Contrôle d'existence du pays de naissance et pays de résidence/travail
3. Sauvegarde et cohérence des blocs 'J'habite ici' et 'Je travaille là'
4. Présence des questions de Classe 0 (Identité) et calcul du taux de complétude
5. Référentiel des pays /api/countries
"""

import urllib.request
import json
import sqlite3
import server

BASE_URL = "http://localhost:8765"

def run_all_tests():
    print("=== DÉBUT DES TESTS SUIVI-ARP001 ===")
    
    # 1. Test GET /api/countries
    req = urllib.request.urlopen(f"{BASE_URL}/api/countries")
    assert req.status == 200, f"Erreur GET /api/countries : {req.status}"
    countries_data = json.loads(req.read().decode('utf-8'))
    assert "countries" in countries_data
    assert "France" in countries_data["countries"]
    assert "Canada" in countries_data["countries"]
    print(f"Test 1 Réussi : Référentiel pays disponible ({len(countries_data['countries'])} pays reconnus).")

    # 2. Test existence des questions de Classe 0 (Identité)
    conn = server.get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as cnt FROM questions WHERE classe = 0")
    cnt_c0 = c.fetchone()["cnt"]
    assert cnt_c0 >= 5, f"Expected >= 5 questions classe 0, got {cnt_c0}"
    print(f"Test 2 Réussi : {cnt_c0} questions de Classe 0 - Identité amorcées avec succès.")

    # 3. Test validation de date de naissance dans le futur (doit échouer avec code 400)
    test_body_futur = {
        "prenom": "TestFutur",
        "date_naissance": "2035-06-12",
        "pays_naissance": "France"
    }
    req_futur = urllib.request.Request(
        f"{BASE_URL}/api/profiles/2/identity",
        data=json.dumps(test_body_futur).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req_futur)
        assert False, "La date dans le futur aurait dû être rejetée avec HTTP 400"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        err_msg = json.loads(e.read().decode('utf-8'))["error"]
        assert "futur" in err_msg.lower(), f"Expected 'futur' in error, got {err_msg}"
        print(f"Test 3 Réussi : Date dans le futur correctement rejetée ({err_msg}).")

    # 4. Test validation d'âge mineur < 18 ans (doit échouer avec code 400)
    test_body_mineur = {
        "prenom": "TestMineur",
        "date_naissance": "2015-01-01",
        "pays_naissance": "France"
    }
    req_mineur = urllib.request.Request(
        f"{BASE_URL}/api/profiles/2/identity",
        data=json.dumps(test_body_mineur).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req_mineur)
        assert False, "L'âge mineur < 18 ans aurait dû être rejeté avec HTTP 400"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        err_msg = json.loads(e.read().decode('utf-8'))["error"]
        assert "18 ans" in err_msg, f"Expected '18 ans' in error, got {err_msg}"
        print(f"Test 4 Réussi : Âge < 18 ans correctement rejeté ({err_msg}).")

    # 5. Test validation pays inconnu (doit échouer avec code 400)
    test_body_bad_country = {
        "prenom": "TestPays",
        "date_naissance": "1992-04-10",
        "pays_naissance": "AtlantideImaginaire"
    }
    req_bad_country = urllib.request.Request(
        f"{BASE_URL}/api/profiles/2/identity",
        data=json.dumps(test_body_bad_country).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        urllib.request.urlopen(req_bad_country)
        assert False, "Le pays inconnu aurait dû être rejeté avec HTTP 400"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        err_msg = json.loads(e.read().decode('utf-8'))["error"]
        assert "pas reconnu" in err_msg, f"Expected 'pas reconnu' in error, got {err_msg}"
        print(f"Test 5 Réussi : Pays non reconnu correctement rejeté ({err_msg}).")

    # 6. Test enregistrement valide avec sections 'J'habite ici' et 'Je travaille là'
    test_body_valid = {
        "prenom": "Camille",
        "nom": "Dupont",
        "sexe": 2,
        "date_naissance": "1994-08-20",
        "pays_naissance": "France",
        "habite_pays": "France",
        "habite_region_dept": "Île-de-France (75)",
        "habite_commune": "Paris",
        "travail_pays": "France",
        "travail_region_dept": "Île-de-France (92)",
        "travail_commune": "Courbevoie",
        "style": "Élégant / Soigné",
        "statut": "Célibataire"
    }
    req_valid = urllib.request.Request(
        f"{BASE_URL}/api/profiles/2/identity",
        data=json.dumps(test_body_valid).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    res_valid = urllib.request.urlopen(req_valid)
    assert res_valid.status == 200
    print("Test 6 Réussi : Enregistrement complet avec J'habite ici et Je travaille là validé.")

    # 7. Vérification de la lecture de la fiche et du calcul d'âge
    req_get = urllib.request.urlopen(f"{BASE_URL}/api/profiles/2/identity")
    card = json.loads(req_get.read().decode('utf-8'))
    assert card["pays_naissance"] == "France"
    assert card["habite_commune"] == "Paris"
    assert card["travail_commune"] == "Courbevoie"
    assert card["style"] == "Élégant / Soigné"
    assert card["age"] is not None and card["age"] >= 30, f"Age calculé invalide : {card.get('age')}"
    print(f"Test 7 Réussi : Données persistées et âge calculé avec exactitude ({card['age']} ans).")

    # 8. Test de l'API /api/profiles avec retour des données enrichies
    req_profs = urllib.request.urlopen(f"{BASE_URL}/api/profiles")
    profs = json.loads(req_profs.read().decode('utf-8'))["profiles"]
    p2 = next(p for p in profs if p["id"] == 2)
    assert "identity_answers_count" in p2
    assert "identity_questions_total" in p2
    assert p2["identity_questions_total"] >= 5
    print(f"Test 8 Réussi : /api/profiles expose les métriques de complétude de classe 0 ({p2['identity_answers_count']}/{p2['identity_questions_total']}).")

    conn.close()
    print("\n>>> TOUS LES TESTS SUIVI-ARP001 SONT PASSES AVEC SUCCES ! <<<")

if __name__ == '__main__':
    run_all_tests()
