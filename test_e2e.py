import urllib.request
import json

def test_api_e2e():
    base_url = "http://localhost:8765"
    print(">>> Test E2E API Affinity...")
    
    # 1. Création d'un 3ème profil (Sophie)
    req = urllib.request.Request(
        f"{base_url}/api/profiles",
        data=json.dumps({"pseudo": "Sophie"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        id_sophie = res['id']
        print(f"    [1/4] Profil créé : ID {id_sophie} (Sophie)")

    # 2. Compléter la fiche d'identité
    id_card_data = {
        "prenom": "Sophie",
        "nom": "Martin",
        "sexe": 2,
        "date_naissance": "1995-04-12",
        "ville": "Bordeaux",
        "statut": "Célibataire",
        "bio": "Passionnée d'art et de voyages."
    }
    req_id = urllib.request.Request(
        f"{base_url}/api/profiles/{id_sophie}/identity",
        data=json.dumps(id_card_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_id) as resp:
        print("    [2/4] Fiche d'identité de Sophie enregistrée.")

    # 3. Enregistrer des réponses
    answers_data = {
        "profile_id": id_sophie,
        "answers": [
            {"question_id": 1, "axis": "V", "value": 4},
            {"question_id": 1, "axis": "A", "value": 5},
            {"question_id": 1, "axis": "D", "value": 5},
            {"question_id": 1, "axis": "P", "value": 5},
            {"question_id": 4, "axis": "G", "value": 5}
        ]
    }
    req_ans = urllib.request.Request(
        f"{base_url}/api/answers",
        data=json.dumps(answers_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req_ans) as resp:
        print("    [3/4] Réponses au questionnaire enregistrées.")

    # 4. Calculer l'affinité entre Alex (ID 1) et Sophie (ID 3)
    calc_req = urllib.request.Request(
        f"{base_url}/api/affinity/calculate",
        data=json.dumps({"profile1_id": 1, "profile2_id": id_sophie}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(calc_req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print(f"    [4/4] Affinité Alex & Sophie : {result['score_global']}%")
        print(f"          Concordances : {[p['sujet'] for p in result['points_de_fusion']]}")
        assert result['score_global'] > 80

    print("\n>>> SIMULATION END-TO-END REUSSIE A 100% ! <<<")

if __name__ == "__main__":
    test_api_e2e()
