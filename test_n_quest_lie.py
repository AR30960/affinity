import urllib.request
import urllib.parse
import json
import time
import subprocess
import sys
import os

PORT = 8765
BASE_URL = f"http://localhost:{PORT}"

def run_tests():
    print(">>> 1. Démarrage du serveur de test...")
    proc = subprocess.Popen([sys.executable, "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.5)

    try:
        print(">>> 2. Test GET /api/questions...")
        req = urllib.request.Request(f"{BASE_URL}/api/questions")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        questions = data.get("questions", [])
        print(f"   -> Nombre total de questions : {len(questions)}")
        assert len(questions) > 0, "Aucune question retournée"

        # Recherche de la question parente 22100 ("Boire du vin")
        q22100 = next((q for q in questions if q["id"] == 22100), None)
        assert q22100 is not None, "Question 22100 non trouvée"
        print(f"   -> Question 22100 : '{q22100['texte']}' | subquestions_count = {q22100.get('subquestions_count')}")
        assert q22100.get("subquestions_count") == 3, f"Attendu 3 sous-questions pour 22100, obtenu {q22100.get('subquestions_count')}"

        # Recherche de la sous-question 22110 ("Boire du vin rouge")
        q22110 = next((q for q in questions if q["id"] == 22110), None)
        assert q22110 is not None, "Question 22110 non trouvée"
        print(f"   -> Question 22110 : '{q22110['texte']}' | n_quest_lie = {q22110.get('n_quest_lie')} | parent_texte = '{q22110.get('parent_texte')}'")
        assert q22110.get("n_quest_lie") == 22100, f"Attendu n_quest_lie=22100, obtenu {q22110.get('n_quest_lie')}"
        assert q22110.get("parent_texte") == "Boire du vin", f"Attendu parent_texte='Boire du vin', obtenu {q22110.get('parent_texte')}"

        # Recherche de la question parente 41100 ("Sortir")
        q41100 = next((q for q in questions if q["id"] == 41100), None)
        assert q41100 is not None, "Question 41100 non trouvée"
        print(f"   -> Question 41100 : '{q41100['texte']}' | subquestions_count = {q41100.get('subquestions_count')}")
        assert q41100.get("subquestions_count") == 5, f"Attendu 5 sous-questions pour 41100, obtenu {q41100.get('subquestions_count')}"

        print(">>> 3. Test GET /api/questions/22100/subquestions...")
        req_sub = urllib.request.Request(f"{BASE_URL}/api/questions/22100/subquestions")
        with urllib.request.urlopen(req_sub) as resp_sub:
            data_sub = json.loads(resp_sub.read().decode('utf-8'))
        
        subs = data_sub.get("subquestions", [])
        print(f"   -> Sous-questions retournées pour 22100 : {len(subs)}")
        assert len(subs) == 3, f"Attendu 3 sous-questions, obtenu {len(subs)}"
        sub_texts = [s["texte"] for s in subs]
        print(f"   -> Libellés des sous-questions : {sub_texts}")
        assert any("rouge" in t.lower() for t in sub_texts), "Sous-question vin rouge manquante"

        print(">>> 4. Test Création question liée via POST /api/questions...")
        new_q_payload = {
            "thematique": "Divertissements & Loisirs",
            "sujet": "Sorties",
            "classe": 1,
            "type": "M",
            "cible": 0,
            "texte": "Question Test Sous-Question de Sortir",
            "n_quest_lie": 41100
        }
        post_req = urllib.request.Request(
            f"{BASE_URL}/api/questions",
            data=json.dumps(new_q_payload).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(post_req) as post_resp:
            post_res = json.loads(post_resp.read().decode('utf-8'))
        
        created_id = post_res.get("id")
        assert created_id is not None, "Échec de création de la question"
        print(f"   -> Question test #{created_id} créée avec succès avec n_quest_lie=41100 !")

        # Vérifier que le subquestions_count de 41100 est passé à 6
        req41100 = urllib.request.Request(f"{BASE_URL}/api/questions")
        with urllib.request.urlopen(req41100) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        q41100_updated = next((q for q in data["questions"] if q["id"] == 41100), None)
        print(f"   -> Nouveau count pour 41100 : {q41100_updated.get('subquestions_count')}")
        assert q41100_updated.get("subquestions_count") == 6, "Le compteur de sous-questions n'a pas été incrémenté"

        print(">>> 5. Test Modification via PUT /api/questions/{id}...")
        put_payload = {
            "thematique": "Divertissements & Loisirs",
            "sujet": "Sorties",
            "classe": 1,
            "type": "M",
            "cible": 0,
            "texte": "Question Test Déplacée vers Boire du vin",
            "n_quest_lie": 22100
        }
        put_req = urllib.request.Request(
            f"{BASE_URL}/api/questions/{created_id}",
            data=json.dumps(put_payload).encode('utf-8'),
            headers={"Content-Type": "application/json"},
            method="PUT"
        )
        with urllib.request.urlopen(put_req) as put_resp:
            put_res = json.loads(put_resp.read().decode('utf-8'))
        assert put_res.get("success") is True, "Échec modification question"

        # Vérifier que 22100 a maintenant 4 sous-questions
        req_sub2 = urllib.request.Request(f"{BASE_URL}/api/questions/22100/subquestions")
        with urllib.request.urlopen(req_sub2) as resp_sub2:
            data_sub2 = json.loads(resp_sub2.read().decode('utf-8'))
        print(f"   -> Nouveau count sous-questions 22100 après déplacement : {len(data_sub2.get('subquestions'))}")
        assert len(data_sub2.get("subquestions")) == 4

        print(">>> 6. Nettoyage de la question de test...")
        del_req = urllib.request.Request(f"{BASE_URL}/api/questions/{created_id}", method="DELETE")
        with urllib.request.urlopen(del_req) as del_resp:
            pass
        print("   -> Question de test supprimée.")

        print("\n=======================================================")
        print(">>> SUCCÈS TOTAL : TOUS LES TESTS N_QUEST_LIE SONT VALIDES !")
        print("=======================================================")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    run_tests()
