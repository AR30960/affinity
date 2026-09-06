import unittest
import urllib.request
import json
import re

class TestDernieresDemandes(unittest.TestCase):
    BASE_URL = "http://localhost:8765"

    def test_01_catalog_access_classe8_absente_et_classe1_accordee(self):
        """Vérifie que la classe 8 n'apparaît pas dans catalog-access et que la classe 1 est accordée."""
        url = f"{self.BASE_URL}/api/profiles/1/catalog-access"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
        
        classes = data.get("classes", [])
        class_nums = [c["classe"] for c in classes]
        print(f"\n[TEST] Classes retournées par catalog-access : {class_nums}")
        
        # 1. Classe 8 ne doit pas apparaître
        self.assertNotIn(8, class_nums, "La classe 8 ne doit pas apparaître dans Niveaux & Classes")
        
        # 2. Classe 1 doit être présente et accordée
        cl1 = next((c for c in classes if c["classe"] == 1), None)
        self.assertIsNotNone(cl1, "La Classe 1 doit être présente")
        self.assertTrue(cl1["has_access"], "La Classe 1 doit être accordée")

    def test_02_interdiction_retrait_classe_1_et_classe_8(self):
        """Vérifie que l'API refuse toute demande de révocation de la Classe 1 ou manipulation de la Classe 8."""
        url = f"{self.BASE_URL}/api/access-requests"
        
        # Tentative de révocation de la classe 1
        payload_cl1 = {
            "profile_id": 1,
            "target_type": "classe",
            "target_value": "1",
            "action_type": "revoke"
        }
        req1 = urllib.request.Request(url, data=json.dumps(payload_cl1).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req1) as resp:
                self.fail("La révocation de la classe 1 aurait dû être rejetée (400)")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
            err_data = json.loads(e.read().decode('utf-8'))
            self.assertIn("ne peut pas être retirée", err_data.get("error", ""))
            print(f"[TEST] Rejet révocation Classe 1 validé : {err_data['error']}")

        # Tentative de requête sur la classe 8
        payload_cl8 = {
            "profile_id": 1,
            "target_type": "classe",
            "target_value": "8",
            "action_type": "revoke"
        }
        req8 = urllib.request.Request(url, data=json.dumps(payload_cl8).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req8) as resp:
                self.fail("La requête sur la classe 8 aurait dû être rejetée (400)")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 400)
            err_data = json.loads(e.read().decode('utf-8'))
            self.assertIn("ne peut pas être retirée", err_data.get("error", ""))
            print(f"[TEST] Rejet requête Classe 8 validé : {err_data['error']}")

    def test_03_filtre_questions_non_repondues_html_et_js(self):
        """Vérifie que le sélecteur qFilterStatus est présent dans index.html et géré dans app.js."""
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html = f.read()
        self.assertIn('id="qFilterStatus"', html)
        self.assertIn('value="UNANSWERED"', html)
        self.assertIn('value="ANSWERED"', html)
        print("[TEST] Sélecteur #qFilterStatus validé dans index.html")

        with open("frontend/app.js", "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("qFilterStatus", js)
        self.assertIn("isQuestionAnswered", js)
        self.assertIn("is-standard-locked", js)
        self.assertIn("badge-fixed-standard", js)
        print("[TEST] Logique de filtrage par statut et verrouillage Classe 1 validée dans app.js")

    def test_04_absence_totale_accent_a_caractere_sexuel(self):
        """Vérifie qu'aucune occurrence de 'À caractère sexuel' avec accent sur le A majuscule ne subsiste."""
        files_to_check = [
            "frontend/index.html",
            "frontend/app.js",
            "server.py",
            "Suivi-ARP001.md"
        ]
        for fpath in files_to_check:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn("À caractère sexuel", content, f"Trouvé 'À caractère sexuel' dans {fpath}")
            self.assertIn("A caractère sexuel", content, f"Doit contenir 'A caractère sexuel' dans {fpath}")
            print(f"[TEST] 'A caractère sexuel' sans accent validé dans {fpath}")

if __name__ == "__main__":
    unittest.main()
